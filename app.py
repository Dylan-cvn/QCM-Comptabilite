import streamlit as st
import random
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd

# Configuration de la page Streamlit
st.set_page_config(page_title="QCM Comptabilité financière", page_icon="🧠", layout="centered")

# Données du Quiz
QUESTIONS = [

    {
        "q": "Lequel de ces comptes ne figure pas à l’actif ?",
        "choices": [
            "Charge à payer.",
            "Impôt anticipé à récupérer.",
            "Créances résultant des ventes.",
            "Titre de placement.",
        ],
        "answer": 0,
        "explain": (
            "Charge à payer n'est pas un actif mais un passif(dette à court terme)."),
        "highlight_color": "#ffc107",
    },
    {
        "q": "Lequel de ces comptes ne figure pas à l'actif ?",
        "choices": [
            "Trésorerie.",
            "Pertes sur créances.",
            "Correction de valeur sur créances.",
            "Stock de marchandises.",
        ],
        "answer": 1,
        "explain": (
            "Perte sur créance n'est pas un actif mais un passif(dette à court terme)."),
    },
    {
        "q": "Lequel de ces comptes ne figure pas au passif ?",
        "choices": [
            "Produit reçus d'avance.",
            "Dette hypothécaire.",
            "Intérêts hypothécaires.",
            "Dividendes nets.",
        ],
        "answer": 2,
        "explain": (
            "Intérêts hypothécaires n'est pas un passif mais une charge."),
    },
    {
        "q": "Lequel de ces comptes ne figure pas au passif ?",
        "choices": [
            "Pertes sur créances.",
            "Emprunt obligataire.",
            "Capital-actions.",
            "Correction de valeur s/actif",
        ],
        "answer": 3,
        "explain": (
            "Correction de valeur s/actif n'est pas un passif mais un actif correcteur."),
    },
    {
        "q": "Quel est l’EBITDA de l’année N ?",
        "choices": [
            "1'357.",
            "2'167.",
            "3'524.",
            "5'691",
        ],
        "answer": 2,
        "explain": (
            "EBITDA N = EBIT N + Amortissements = (88'886 - 33'351 - 10'660 - 30'992 - 12'526) + 2'167 = 3'524"),
    }
    ]

#-------------------------------------------------------------------------------------------------------------------------------------------
# CONFIGURATION ET VARIABLES GLOBALES
#-------------------------------------------------------------------------------------------------------------------------------------------

RESULTS_FILE = "results.csv" # Fichier de résultats

#-------------------------------------------------------------------------------------------------------------------------------------------
# FONCTIONS DE GESTION DES RÉSULTATS
#-------------------------------------------------------------------------------------------------------------------------------------------

def log_answer(user_name: str, q_index: int, correct: bool, selected: int) -> None:
    """Enregistre une réponse dans un fichier CSV."""
    name = user_name.strip() or "Anonyme"
    q = QUESTIONS[q_index]

    row = {
        "timestamp": datetime.now().isoformat(),  # Format ISO8601
        "user": name,
        "question_index": q_index,
        "question": q["q"].replace("\n", " "),
        "selected_index": selected,
        "selected_choice": q["choices"][selected],
        "correct_index": q["answer"],
        "correct_choice": q["choices"][q["answer"]],
        "is_correct": int(bool(correct)),
    }

    df = pd.DataFrame([row])
    file_exists = Path(RESULTS_FILE).exists()
    df.to_csv(RESULTS_FILE, mode="a", header=not file_exists, index=False)


# Sidebar
with st.sidebar:
    st.header("⚙️ Paramètres")
    user_name = st.text_input("Votre nom (optionnel)", "")
    shuffle_q = st.checkbox("Mélanger les questions (au démarrage)", value=True)
    show_explain = st.checkbox("Afficher l'explication après validation", value=True)
    st.caption("Partagez simplement l'URL publique de cette page.")

    admin_password = st.text_input("Mdp", type="password")
    ADMIN_PASSWORD = st.secrets.get("ADMIN_PASSWORD", "Testz")
    is_admin = admin_password == ADMIN_PASSWORD

TARGET_MASTERY = 1

#-------------------------------------------------------------------------------------------------------------------------------------------
# FONCTIONS DE GESTION DU QUIZ
#-------------------------------------------------------------------------------------------------------------------------------------------

def full_init():
    st.session_state.init = True
    st.session_state.n_questions = len(QUESTIONS)
    st.session_state.order = list(range(len(QUESTIONS)))
    if shuffle_q:
        random.shuffle(st.session_state.order)
    st.session_state.mastery = {i: 0 for i in range(len(QUESTIONS))}
    st.session_state.current = st.session_state.order[0]
    st.session_state.answers = {}
    st.session_state.just_validated = False
    st.session_state.last_result = None


def reset_all():
    full_init()


if ("init" not in st.session_state) or (st.session_state.get("n_questions") != len(QUESTIONS)):
    full_init()

st.title("🎈Révision examen : Comptabilité financière I")
st.caption("Mode **apprentissage** : répéter les erreurs jusqu'à maîtriser le sujet.")


def _choose_next(exclude_idx=None):
    remaining = [i for i in st.session_state.order if st.session_state.mastery[i] < TARGET_MASTERY]
    if not remaining:
        return None

    remaining.sort(key=lambda i: st.session_state.mastery[i])
    min_level = st.session_state.mastery[remaining[0]]
    candidates = [i for i in remaining if st.session_state.mastery[i] == min_level]

    if exclude_idx in candidates and len(candidates) > 1:
        candidates = [i for i in candidates if i != exclude_idx]

    return random.choice(candidates)
# --------------------------------
def _advance_to_next():
    next_idx = _choose_next(exclude_idx=st.session_state.current)

    if next_idx is None:
        # Toutes les questions sont maîtrisées
        st.balloons()
        st.toast("👏 Bravo ! C'est Maîtrisé", icon="🎉")
        stamped = datetime.now().strftime("%Y-%m-%d %H:%M")
        name_line = f" par {user_name}" if user_name.strip() else ""
        total_success = sum(st.session_state.mastery.values())
        
        # Afficher le message de succès
        st.success(
            f"🎉 Maîtrise atteinte{name_line} — toutes les questions réussies "
            f"{TARGET_MASTERY} fois. ({total_success} réussites comptées) — {stamped}"
        )
        
        # Afficher le bouton "Recommencer"
        if st.button("🔁 Recommencer", key="restart_final"):
            reset_all()
            st.rerun()
    else:
        # Continuer vers la prochaine question
        st.session_state.current = next_idx
        st.session_state.just_validated = False
        st.session_state.last_result = None
        st.rerun()


def render_single(q_index):
    """Affiche une question."""
    q = QUESTIONS[q_index]
    highlight_color = q.get("highlight_color")

    # Afficher l'énoncé
    lines = [s for s in q["q"].split("\n") if s.strip()]
    if lines:
        if highlight_color:
            st.markdown(
                f"<h3 style='color:{highlight_color};margin-bottom:0.3rem;'>{lines[0]}</h3>",
                unsafe_allow_html=True,
            )
        else:
            st.subheader(lines[0])

        for line in lines[1:]:
            has_math = any(token in line for token in ("=", "^", "\\frac", "\\cdot", "\\times"))
            if highlight_color and has_math:
                st.markdown(
                    f"$$\\color{{{highlight_color}}}{{{line}}}$$",
                    unsafe_allow_html=True,
                )
            elif highlight_color:
                st.markdown(
                    f"<span style='color:{highlight_color};'>{line}</span>",
                    unsafe_allow_html=True,
                )
            elif has_math:
                try:
                    st.latex(line)
                except Exception:
                    st.markdown(line)
            else:
                st.markdown(line)

    # Afficher l'image si elle existe
    if q.get("image"):
        try:
            st.image(q["image"], use_container_width=True, caption="Graphique de référence")
        except Exception as e:
            st.warning(f"⚠️ Impossible de charger l'image : {e}")
    
    # Choix
    key_radio = f"choice_{q_index}"
    if key_radio not in st.session_state:
        st.session_state[key_radio] = st.session_state.answers.get(q_index, None)

    selected = st.radio(
        "Choisissez une réponse :",
        options=list(range(4)),
        format_func=lambda i: q["choices"][i],
        key=key_radio,
    )
    st.session_state.answers[q_index] = selected

    # Bouton de validation
    validate = st.button("✅ Valider", key=f"validate_{q_index}")
    if validate:
        # ✅ Vérifier que l'utilisateur a sélectionné une réponse
        if selected is None:
            st.warning("⚠️ Veuillez sélectionner une réponse avant de valider.")
            return None

        
#-------------------------------------------------------------------------------------------------------------------------------------------
# FONCTIONS DE GESTION DU QUIZ
#-------------------------------------------------------------------------------------------------------------------------------------------
    
        correct = selected == q["answer"]
        st.session_state.just_validated = True
        st.session_state.last_result = correct

        # Enregistrer la réponse
        log_answer(user_name, q_index, correct, selected)

        # Mise à jour de la maîtrise
        if correct and st.session_state.mastery[q_index] < TARGET_MASTERY:
            st.session_state.mastery[q_index] += 1

        if correct:
            st.success("✔️ Bonne réponse !")
        else:
            st.error(f"❌ Mauvaise réponse. Réponse attendue : {q['choices'][q['answer']]}")
        if show_explain and q.get("explain"):
            st.info(f"💡 Explication : {q['explain']}")
        return correct

    # Réaffichage après validation
    if st.session_state.just_validated:
        correct = st.session_state.last_result
        if correct:
            st.success("✔️ Bonne réponse !")
        else:
            st.error(f"❌ Mauvaise réponse. Réponse attendue : {q['choices'][q['answer']]}")
        if show_explain and q.get("explain"):
            st.info(f"💡 Explication : {q['explain']}")

    return None


# MODE APPRENTISSAGE
progress_bar_slot = st.empty()
progress_text_slot = st.empty()

q_idx = st.session_state.current
_ = render_single(q_idx)

mastered_count = sum(1 for v in st.session_state.mastery.values() if v >= TARGET_MASTERY)
progress_bar_slot.progress(mastered_count / len(QUESTIONS))
progress_text_slot.write(f"Maîtrise : **{mastered_count}/{len(QUESTIONS)}** questions ")

if st.session_state.just_validated:
    # Vérifier s'il reste des questions à maîtriser
    remaining = [i for i in st.session_state.order if st.session_state.mastery[i] < TARGET_MASTERY]
    
    if remaining:
        if st.button("➡️ Continuer", key=f"next_{q_idx}"):
            _advance_to_next()
    else:
        # Si toutes les questions sont maîtrisées, afficher directement l'écran de fin
        _advance_to_next()

# -----------------------
# 🧠 Section analyse (version avec nettoyage automatique)
# -----------------------

st.markdown("---")
st.markdown("### Mode analyse")

# 🔒 Section réservée au développeur
if not is_admin:
    st.info("🔒 Section dev.")
else:
    results_path = Path(RESULTS_FILE)

    if not results_path.exists():
        st.info("Aucune réponse enregistrée pour l'instant.")
    else:
        try:
            # Vérifier si le fichier n'est pas vide
            if results_path.stat().st_size == 0:
                st.warning("Le fichier de résultats existe mais est vide.")
                df = pd.DataFrame()
            else:
                # 📥 Chargement des données
                df = pd.read_csv(results_path)
                
                # Nettoyage automatique des données de plus de 24h
                if not df.empty and 'timestamp' in df.columns:
                    # Conversion sécurisée des dates
                    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
                    
                    # Filtrer pour garder seulement les dernières 24h
                    cutoff_time = datetime.now() - timedelta(hours=24)
                    df_clean = df[df['timestamp'] >= cutoff_time].copy()
                    
                    # Si des données ont été supprimées, mettre à jour le fichier
                    if len(df_clean) < len(df):
                        deleted_count = len(df) - len(df_clean)
                        st.info(f"🔧 {deleted_count} entrées de plus de 24h ont été automatiquement supprimées.")
                        
                        # Sauvegarder les données nettoyées
                        df_clean.to_csv(results_path, index=False)
                        df = df_clean
                    
                    # Réinitialiser l'index après nettoyage
                    df = df.reset_index(drop=True)
                
        except Exception as e:
            st.error(f"Erreur lors du chargement : {e}")
            # Option pour réinitialiser le fichier
            if st.button("🔄 Réinitialiser le fichier de résultats"):
                try:
                    results_path.unlink()
                    st.success("Fichier réinitialisé. Les nouvelles données seront enregistrées normalement.")
                    st.rerun()
                except Exception as delete_error:
                    st.error(f"Erreur lors de la réinitialisation : {delete_error}")
            df = pd.DataFrame()

        if df.empty:
            st.info("Aucune donnée à afficher (ou toutes les données étaient de plus de 24h).")
        else:
            # Afficher les statistiques de base
            st.subheader("📊 Statistiques générales")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                total_reponses = len(df)
                st.metric("Total réponses", total_reponses)
            
            with col2:
                if 'is_correct' in df.columns:
                    taux_reussite = (df['is_correct'].sum() / len(df)) * 100
                    st.metric("Taux de réussite", f"{taux_reussite:.1f}%")
            
            with col3:
                if 'timestamp' in df.columns and not df.empty:
                    # Convertir le timestamp en format lisible
                    derniere_activite = df['timestamp'].max()
                    if pd.notna(derniere_activite):
                        # Formater la date pour l'affichage
                        derniere_activite_str = derniere_activite.strftime("%d/%m/%Y %H:%M")
                        st.metric("Dernière activité", derniere_activite_str)
                    else:
                        st.metric("Dernière activité", "N/A")
                else:
                    st.metric("Dernière activité", "N/A")

            # 📋 Tableau des réponses
            st.subheader("📋 Toutes les réponses (24h max)")
            st.dataframe(df)

            # 📥 Téléchargement
            csv_all = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Télécharger toutes les réponses (CSV)",
                data=csv_all,
                file_name="results_qcm_microeconomie.csv",
                mime="text/csv",
            )

            # 🗑️ Option de nettoyage manuel
            st.subheader("🔧 Maintenance")
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🗑️ Nettoyer maintenant", help="Supprime toutes les données de plus de 24h"):
                    try:
                        if not df.empty and 'timestamp' in df.columns:
                            cutoff_time = datetime.now() - timedelta(hours=24)
                            df_clean = df[df['timestamp'] >= cutoff_time].copy()
                            deleted_count = len(df) - len(df_clean)
                            
                            if deleted_count > 0:
                                df_clean.to_csv(results_path, index=False)
                                st.success(f"{deleted_count} entrées supprimées !")
                                st.rerun()
                            else:
                                st.info("Aucune donnée à nettoyer (toutes sont récentes).")
                    except Exception as clean_error:
                        st.error(f"Erreur lors du nettoyage : {clean_error}")
            
            with col2:
                if st.button("⚠️ Tout supprimer", help="Supprime TOUTES les données (irréversible)"):
                    try:
                        results_path.unlink()
                        st.success("Toutes les données ont été supprimées !")
                        st.rerun()
                    except Exception as delete_error:
                        st.error(f"Erreur lors de la suppression : {delete_error}")
