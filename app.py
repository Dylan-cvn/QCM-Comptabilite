import streamlit as st
import pandas as pd

st.set_page_config(page_title="QCM Comptabilité Financière", page_icon="📊")

st.title("📊 QCM Comptabilité Financière")
st.markdown("**25_26_HES-SO-GE-Comptabilité financière S1**")

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Aller à", ["Accueil", "QCM", "Résultats"])
    
    if page == "Accueil":
        show_home()
    elif page == "QCM":
        show_quiz()
    elif page == "Résultats":
        show_results()

def show_home():
    st.write("Bienvenue au QCM de Comptabilité Financière")
    st.write("Sélectionnez 'QCM' dans la navigation pour commencer le quiz.")

def show_quiz():
    st.subheader("Questionnaire QCM")
    # Pour l'instant un placeholder
    st.info("Les questions seront ajoutées prochainement!")

def show_results():
    st.subheader("Résultats")
    st.write("Aucun résultat pour le moment.")

if __name__ == "__main__":
    main()
