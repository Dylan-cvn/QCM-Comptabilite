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
            "Charge à payer n'est pas un actif mais un passif (dette c-t car régularisation)."),
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
            "Perte sur créance n'est pas un actif mais une charge (cha. d'expl.)."),
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
            "1'357",
            "2'167",
            "3'524",
            "5'691",
        ],
        "answer": 2,
        "explain": (
            "EBITDA N = EBIT N + amortissements = (88'886 - 33'351 - 10'660 - 30'992 - 12'526) + 2'167 = 3'524"),
        "image": "série_1_compte_resultat.png"
    },
    {
            "q": "Quel est l’EBIT de l’année N-1 ?",
        "choices": [
            "-140",
            "75",
            "931",
            "2'126",
        ],
        "answer": 1,
        "explain": (
            "EBIT N-1 = EBITDA N-1 - amortissements = (prod. d'expl. - cha. d'expl) - amortissements = "
            "[(89'878 + 51) - (36’494 + 16’206 + 30’219 + 4’884)] - 2’051 = 75"),
        "image": "série_1_compte_resultat.png"
},
{
  "q": "Quel est le résultat avant impôt de l’année N ?",
        "choices": [
            "–98",
            "1'259",
            "1'357",
            "3'524",
        ],
        "answer": 1,
        "explain": (
            "EBT N = EBIT N + prod. fin. - cha. fin. = (EBITDA N - amortissements) + (230 - 328) = "
            "[(88'886 - 33'351 - 10'660 - 30'992 - 12'526 + 2'167) - 2'167] - 98 = 1'259"),
        "image": "série_1_compte_resultat.png"  
},
{
  "q": "Quel est le résultat de l'exercice de l’année N-1 ?",
        "choices": [
            "75",
            "571",
            "636",
            "1'299",
        ],
        "answer": 1,
        "explain": (
            "Res. de l'exercice N-1 = EBT N-1 - impôts = (EBIT N-1 + prod. fin. - cha. fin.) - 140 = (EBITDA N-1 - amortissements) + (931 - 295) - 140 = "
            "[(89'878 - 36'494 - 16'206 - 30'219 - 4'884 + 2'051) - 2'051] + 636 - 140 = 571"),
        "image": "série_1_compte_resultat.png" 
},
{
      "q": "Quel est le résultat EBITDA de l’exercice au 31.12.20xx ?",
        "choices": [
            "150'500",
            "171'000",
            "271'000",
            "288'500",
        ],
        "answer": 2,
        "explain": (
            "EBITDA = EBIT + amortissements = [(prod. d'expl - cha. d'expl) - amortissements] + 100'000 = "
            "[3'000'000 - (charges liées à l’activité courante) - 100'000] + 100'000 = "
            "[3'000'000 - (1'550'000 + 350'000 + 700'000 + 96'000 + 15'500 + 17'500)] = 271'000"),
        "image": "serie_1_balance_verification.png"   
},
{
      "q": "Si le résultat de l’exercice s’élève à CHF 25'500, quel est le montant du résultat EBIT ?",
        "choices": [
            "50'500",
            "171'000",
            "271'000",
            "Aucune des réponses",
        ],
        "answer": 1,
        "explain": (
            "EBIT = Res. de l'exercice + impôts + (Cha. fin - prod. fin) + (Cha. hors expl. - prod. hors expl.) + (Cha. exc. - prod. exc) = "
            " 25'500 + 25'000 + 0 + (120'500 - 0) + 0 = 171'000"),
        "image": "serie_1_balance_verification.png"
},
{
    "q": "Sachant que l’entreprise présente ses comptes selon le plan comptable PME, quel est le montant des actifs circulants du bilan ?",
        "choices": [
            "875'500",
            "1'118'000",
            "1'125'500",
            "1'140'500",
        ],
        "answer": 2,
        "explain": (
            "actifs circulants = trésorerie + créances + stocks + régularisation = "
            "(banques) + (cr. clients - correction s/cr. clients + cr. envers personnes proches) + (stock de marchandises) + (actifs de régularisations) = "
            "543'000 + (300'000 - 15'000 + 250'000) + 40'000 + 7'500 = 1'125'500"),
        "image": "serie_1_balance_verification.png"
},
{
    "q": "Sachant que l’entreprise présente ses comptes selon le plan comptable PME, quel est le montant des capitaux étrangers du bilan ?",
        "choices": [
            "410'000",
            "2'660'000",
            "2'800'000",
            "2'910'000",
        ],
        "answer": 3,
        "explain": (
            "capitaux étrangers = Capitaux étrangers à c-t + Capitaux étrangers à l-t = "
            "(dettes c-t + régularisations) + (dettes l-t) = "
            "(dettes résultant d’achats + dettes c-t envers personnes proches + passifs de régularisation) + dettes l-t intérêts = "
            "(50'000 + 250'000 + 110'000) + 2'500'000 = 2'910'000"),
        "image": "serie_1_balance_verification.png"
},
{
    "q": "L’entreprise « JARDINS SA » est une société anonyme active depuis une dizaine d’années dans le domaine de l’aménagement des espaces extérieurs. \n" 
         "Elle a été fondée par trois frères actifs dans le secteur d’activité depuis de nombreuses années. \n"
         "La jeune société n’est pas cotée en bourse. Durant N-1, la société a généré un chiffre d’affaires de 38M et employé 252 personnes travaillant plein temps pendant 2 ans consécutifs. \n"
         "le résultat de son bilan le 31.12.N-1 est de 22'295 KCHF. \n"
         "A quel type de contrôle la société est-elle soumise selon le CO ?",
        "choices": [
            "Contrôle restreint.",
            "Contrôle ordinaire.",
            "Contrôle ordinaire avec respect des normes comptables Swiss Gaap.",
            "Contrôle standard.",
        ],
        "answer": 1,
        "explain": (
            "On peut conclure à un contrôle ordinaire, car l’entreprise dépasse 2 des 3 seuils : "
            "bilan ≥ 20M (oui), CAN ≥ 40M (non), EPT ≥ 250 (oui) donc la société est soumise au contrôle ordinaire."),
},
{
    "q": "Quels états financiers doit présenter une société sous contrôle ordinaire ? ",
        "choices": [
            "Bilan & compte de résultat.",
            "Bilan, compte de résultat, tableau de flux de trésorerie & annexe.",
            "Bilan, compte de résultat & annexe étendue.",
            "Bilan, compte de résultat, annexe étendue, tableau de flux de trésorerie & rapport de gestion.",
        ],
        "answer": 3,
        "explain": (
            "Une société soumise au contrôle ordinaire doit présenter des états financiers complets, incluant le bilan, le compte de résultat, l’annexe étendue, "
            "le tableau des flux de trésorerie ainsi que le rapport de gestion, conformément au Code des Obligations."),
},
{
     "q": "Les actionnaires d'une société soumise au contrôle ordinaire souhaite faire un opting out. "
          " Quelles seraient les conditions à réunir pour pouvoir le réaliser ?",
        "choices": [
            "L’opting out est possible avec l’accord de la majorité des actionnaires.",
            "L’opting out est possible avec l’accord de l’unanimité des actionnaires.",
            "L’opting out est possible avec l’accord de l’unanimité des administrateurs.",
            "L’opting out n’est pas possible.",
        ],
        "answer": 3,
        "explain": (
            "Une société soumise au contrôle ordinaire ne peut pas renoncer au contrôle, même avec l’accord unanime des actionnaires. "
            "Elle peut renoncer au contrôle seulement si elle repasse sous les seuils légaux pendant deux exercices consécutifs."),
},
{
     "q": "Qu’est-ce que l’EBITDA ?",
        "choices": [
            "Il s’agit du résultat de l’exercice avant produits/charges financiers & avant impôts, mais après amortissements.",
            "Il s’agit du résultat de l’exercice après produits/charges financiers mais avant impôts.",
            "Il s’agit du résultat de l’exercice avant amortissements, avant produits/charges financiers & avant impôts.",
            "Il s’agit du résultat de l’exercice après produits/charges financiers & après impôts.",
        ],
        "answer": 2,
        "explain": (
            "Le résultat de l'exercice avant produits/charges financiers & avant impôts, mais après amortissements ⇒ EBIT "
            "Le résultat de l’exercice après produits/charges financiers mais avant impôts ⇒ EBT "
            "Le résultat de l’exercice après produits/charges financiers & après impôts ⇒ Res. de l'exercice"),
},
{
     "q": "Un administrateur vous demande quels sont les critères de définition de la taille des entreprises selon le CO. ",
        "choices": [
            "Le nombre d’emplois à plein temps, le montant du résultat d’exploitation et le chiffre d’affaires. ",
            "Le total du bilan, le chiffre d’affaires et le nombre d’emplois à plein temps.",
            "le total du bilan, le nombre d’administrateurs à plein temps et le chiffre d’affaires.",
            "Aucunes réponses.",
        ],
        "answer": 1,
        "explain": (
            "Le CO définit la taille des entreprises (et donc l’obligation de contrôle ordinaire) sur la base de ces trois critères uniquement."),
},
{
     "q": "Une administratrice vous demande quelles sont les sociétés qui doivent présenter les comptes selon une norme comptable reconnue ? ",
        "choices": [
            "Les grandes entreprises selon le CO. ",
            "Les petites entreprises selon le CO.",
            "Les sociétés cotées en bourse.",
            "Aucune société en Suisse.",
        ],
        "answer": 2,
        "explain": (
            "Le CO impose une norme comptable reconnue à toutes les sociétés cotées en bourse. "),
},
{
     "q": "Afin d’économiser des frais, les administrateurs envisagent de ne pas soumettre les comptes présentés à une révision (opting out). "
          "Quelles sont les conditions à réunir pour avoir le droit de renoncer à la révision des comptes ?",
        "choices": [
            "Moins de 10 collaborateurs à plein temps et acceptation à l’unanimité des actionnaires. ",
            "Moins de 20 emplois à plein temps et acceptation à l’unanimité des actionnaires.",
            "Moins de 10 collaborateurs à plein temps et acceptation à l’unanimité des administrateurs.",
            "Moins de 20 collaborateurs à plein temps et acceptation à la majorité des actionnaires.",
        ],
        "answer": 0,
        "explain": (
            "Selon le CO, l’opting-out n’est possible que si l’entreprise compte moins de 10 employés en moyenne "
            "et que tous les actionnaires renoncent unanimement à la révision."),
},
{
     "q": "La présidente du conseil d’administration vous fait remarquer qu’aucune charge financière n’apparaît dans les états financiers. " 
          "Or un prêt bancaire à long terme au taux de 2.25% a été conclu le 31 mai pour CHF 2'500'000. "
          "Quelle serait l’incidence de ces charges financières sur l’EBIT ? ",
        "choices": [
            "L’EBIT aurait augmenté du montant des charges financières.",
            "L’EBIT aurait diminué du  montant des charges financières.",
            "L’EBIT aurait augmenté de la variation des charges financières entre l’année N et N-1.",
            "L’EBIT n’aurait pas été modifié.",
        ],
        "answer": 3,
        "explain": (
            "Cha. fin = 2'500'000 × 2.25% = 56'250 "
            "EBIT = Res. avant intérêts & impôts ∴ avant cha. fin ⇒ l'incidence sur l'EBIT est 0"),
},
{ 
     "q": "Alpina SA présentait pour l’année N un total du bilan 21M, un chiffre d’affaires de 46M et un effectif moyen de 255 employés à plein temps. "
          "Pour l’année N+1, le total du bilan atteint 23M, le chiffre d’affaires 48M et l’effectif moyen 270 employés. "
          "Selon le CO, quels éléments Alpina SA doit-elle fournir en plus du bilan et du compte de résultat pour ses états financiers N+1 ?",
        "choices": [
            "Une simple annexe et un rapport de durabilité.",
            "Une annexe étendue et un tableau de flux de trésorerie.",
            "Un tableau de financement et un rapport spécial sur la gouvernance.",
            "Un rapport de rémunération obligatoire et une norme IFRS complète.",
        ],
        "answer": 1,
        "explain": (
            "Alpina dépasse deux des trois seuils CO : bilan > 20 Mio, CA > 40 Mio, EMP > 250 ⇒ grande entreprise ⇒ annexe étendue + tableau des flux de trésorerie."),
},
{
     "q": "Alpimage SA a pour l’année N+1 : Total du bilan à CHF 12 millions / Chiffre d’affaires à CHF 25 millions / Effectif moyen à 80 employés plein temps. "
          "Alpimage ne dépasse donc aucun des seuils du contrôle ordinaire mais emploi nettement plus que 10 personnes. "
          "A quel type de contrôle Alpimage SA est-elle soumise et que pourraient demander les actionnaires ?",
        "choices": [
            "Contrôle restreint et les actionnaires pourraient demander un contrôle ordinaire.",
            "Contrôle ordinaire et les actionnaires pourraient demander l’opting out.",
            "Aucun contrôle légal et les actionnaires ne peuvent pas exiger de contrôle tant que les statuts ne sont pas modifiés.",
            "Contrôle restreint mais les actionnaires ne peuvent pas exiger de contrôle ordinaire.",
        ],
        "answer": 0,
        "explain": (
            "Pour Alpimage SA, le contrôle restreint obligatoire & les actionnaires représentant au moins 10 % du capital peuvent exiger un contrôle ordinaire."),
},
{
     "q": "EBITDA = 351'000 / Cha. fin = 15'600 / Prod. fin = 2'400 / impôts = 66'200 / Prod. exc = 24'900 / Res. de l'exercice = 233'800 " 
          "Calculer l'EBIT N+1.",
        "choices": [
            "288'300",
            "318'000",
            "338'100",
            "342'900",
        ],
        "answer": 0,
        "explain": (
            "EBIT = Res. de l'exercice + impôts + (Cha. fin - prod. fin) + (Cha. hors expl. - prod. hors expl.) + (Cha. exc. - prod. exc) ∴ "
            "EBIT = 233'800 + 66'200 + (15'600 - 2'400) + 0 + (0 - 24'900) = 288'300"),
},
{
     "q": "Un comptable prévoit un montant d'EBIT supérieur à l'EBITDA pour l'année N+2. " 
          "Est-ce possible ?",
        "choices": [
            "Oui si les amortissements N+2 sont inférieurs à ceux de l’année N+1.",
            "Oui si les amortissements N+2 sont supérieurs à ceux de l’année N+1.",
            "Oui si l’entreprise a vendu des actifs immobilisés complètement amortis.",
            "Non cette situation est impossible.",
        ],
        "answer": 3,
        "explain": (
            "EBITDA = EBIT + amortissements. Si amortissements ≥ 0 al. EBITDA ≥ EBIT ∴ EBIT > EBITDA est impossible."),   
},
{
     "q": "Parmi les passifs suivants, lesquels pourraient être inclus dans la section des passifs à court terme du bilan ?",
        "choices": [
            "Dettes de loyer, emprunt, capital-actions.",
            "Dettes fournisseurs, dette financière à court terme, produits constatés d’avance.",
            "Charges à payer, produits reçus d’avance, bénéfices non distribués.",
            "Partie courante de la dette à long terme, prime d’émission, obligations liées aux prestations de retraite.",
        ],
        "answer": 1,
        "explain": (
            "Les passifs à c-t sont des dettes/exigibilités qui seront réglées dans l’année (≤ 12 mois)."),
    "highlight_color": "#ffc107", #jaune
},
{
     "q": "Comment une entreprise peut-elle être rentable et faire faillite ?",
        "choices": [
            "Les bénéfices ont augmenté plus rapidement que les ventes.",
            "L'entreprise a un résultat net positif mais n'a pas réussi à générer des liquidités à partir de ses activités.",
            "Le résultat net a été ajusté pour tenir compte de l'inflation.",
            "Les ventes ne se sont pas améliorées malgré l'assouplissement des politiques de crédit.",
        ],
        "answer": 1,
        "explain": (
            "Une entreprise est dite rentable si elle réalise un résultat net positif (bénéfice) dans son compte de résultat. "
            "Mais pour survivre, elle doit aussi avoir assez de trésorerie (cash) pour payer ses passifs à c-t."),
    "highlight_color": "#ffc107", #jaune
},
{
     "q": "Que signifie le montant du chiffre d'affaires net ?",
        "choices": [
            "Le résultat des ventes après déduction des charges d'exploitation.",
            "Le montant total des ventes après déduction des réductions accordées.",
            "La marge brute après déduction des charges d'exploitation.",
            "Aucune réponse.",
        ],
        "answer": 1,
        "explain": (
            "Le résultat des ventes (CAN) après déduction des charges d'exploitation (avec amortissements) donne le résutat d'exploitation donc plutôt l'EBIT."
            "La marge brute après déduction des charges d'exploitation parle d’une marge après les charges donc n'est pas le CAN."),
},
{
     "q": "Sachant : Diminution du stock de marchandises = 15'000 / Achats de marchandises = 385'000 / Déductions accordées aux clients = 17'000 / Total des frais d’achat = 10'000 "
          "Ventes brutes de marchandises = 517'000 / Rabais obtenus des fournisseurs = 10'000. \n"
          "Quel est le montant de la marge brute ?",
        "choices": [
            "100'000",
            "117'000",
            "130'000",
            "147'000",
        ],
        "answer": 0,
        "explain": (
            "Ventes nettes de marchandises = Ventes brutes de marchandises - déductions accordées = 517'000 - 17'000 = 500'000|   "
            "PRAMA = Achats de marchandises + frais d'achat - rabais obtenus des fournisseurs = 385'000 + 10'000 - 10'000 = 385'000|   "
            "PRAMV = PRAMA + diminution du stock de marchandises = 385'000 + 15'0000 = 400'0000|   "
            "Marges brutes (MB) = Ventes nettes - PRAMV = 500'000 - 400'000 = 100'000"),
},
{
    "q": "01.01.N, stock de marchandises = 24'0000 mais au 31.12.N, il s’élève à 30'000. Quelle écriture l’entreprise doit-elle comptabiliser au 31.12.N ?",
        "choices": [
            "De variation de stock à stock de marchandises pour 30'000.",
            "De variation de stock à stock de marchandises pour 6'000.",
            "De stock de marchandises à variation de stock pour 30'000.",
            "De stock de marchandises à variation de stock pour 6'000.",
        ],
        "answer": 3,
        "explain": (
            "Stock 01.01.N = 24'000 & Stock 31.12.N = 30'000 ∴ Stock augmente de 6'000. "
            "Quand le stock augmente, on comptabilise stock de marchandises au débit (compte d'actif) à variation de stock au crédit (compte de charge) pour 6'000."),
},
{
     "q": "Sachant : impôts = 100'000 / Créances résultant de ventes = 246'800 / Loyer = 1'000'000 / Frais de télécommunication = 150'000 / "
          "Cha. fin = 23'000 / Frais de déplacement = 800'000 / amortissements = 482'000 / Stocks de marchandises = 982'000 / "
          "Frais de personnel = 36'000'000 / Frais de publicité = 45'000 / Ventes réalisées = 39'000'000. \n"
          "Quel est le montant du résultat avant amortissement ?",
        "choices": [
            "882'000",
            "905'000",
            "1'005'000",
            "Aucunes réponses",
        ],
        "answer": 0,
        "explain": (
            "On cherche le résultat avant amortissement (et non pas l'EBITDA) donc Ventes réalisées - Charges sauf amortissement. "
            "Ventes réalisées - Impôts - Loyer - Frais télécommunication - Cha. fin - Frais déplacement - Frais personnel - Frais publicité = "
            "39'000'000 - 100'000 - 1'000'000 - 150'000 - 23'000 - 800'000 - 36'000'000 - 45'000 = 882'000 "
            "On exclut créances résultant de ventes & stocks de marchandises car se sont des comptes d'actifs."),
},
{
     "q": "Une entreprise soumise à la TVA réalise des ventes pour un montant de 200'000 + TVA 15'400. "
          "Cette même entreprise a payé des charges et investissements pour un montant de 70'000 + TVA 5'390. \n"
          "Quel montant de TVA cette entreprise doit-elle verser à l’administration fédérale des contributions ?",
        "choices": [
            "10'010",
            "15'400",
            "20'790",
            "Aucunes réponses",
        ],
        "answer": 0,
        "explain": (
            "TVA due = TVA collecté sur ventes - TVA récupérable sur achats = 15'400 - 5'390 = 10'010 étant la TVA que l'entreprise doit verser."),
},
{
     "q": "Le 30.09.N, les ventes d’articles durant le 3ème trimestre sont de CHF 25'000. L’entreprise a octroyé à son client le plus important une remise de 5 %. "
          "Ce client représente 10 % du total des ventes du 3ème trimestre. L’entreprise émet une note de crédit sur ce montant. \n"
          "Quel est le montant de la remise de 5% au 30.09.N ? ",
        "choices": [
            "125",
            "1'250",
            "2'500",
            "2'625",
        ],
        "answer": 0,
        "explain": (
            "Le client représente 10 % de ces ventes ⇒ 25′000 × 10% = 2'500 puis remise accordée de 5 % sur ses achats ⇒ 2'500 × 5% = 125"),
},
{
     "q": "Le matériel et mobilier est amorti de manière indirecte et décroissante au taux de 25%. Sachant que sa valeur comptable au 31.12.N avant amortissements : "
          "Mat.&mob. = 99'000 tandis que Amortissement & correction de valeur (cumul) s/mat.&mob. = 36'800. \n"
          "Quel écriture l'entreprise doit-elle comptabiliser le 31.12.N ?",
        "choices": [
            "Amortissement & correction de valeur (cumul) s/mat.&mob à Mat.&mob. pour 15'550",
            "Amortissement à Amortissement & correction de valeur (cumul) s/mat.&mob. pour 24'750",
            "Amortissement à Amortissement & correction de valeur (cumul) s/mat.&mob. pour 15'550",
            "Amortissement à Mat.&mob. pour 24'750",
        ],
        "answer": 1,
        "explain": (
            "L’amortissement dégressif se calcule sur la valeur comptable nette avant amortissement de l'année ∴ Amortissement N = 99'000 × 25% = 24'750 "
            "Méthode indirecte : on crédite le compte d’amortissement cumulé (actif correcteur) & on débite Amortissement N (Charge) pour 24'750."),
},
{
     "q": "Un immeuble, acquis le 01.01.N-1, est amorti de manière directe et constante au taux de 4%. Sachant que sa valeur comptable au 31.12.N avant amortissements : "
          "Immeuble = 1'440'000 \n"
          "A quel montant s'élève l'amortissement au 31.12.N ?",
        "choices": [
            "57'600",
            "60'000",
            "62'608.70",
            "Aucune réponses",
        ],
        "answer": 1,
        "explain": (
            "Il faut retrouver la valeur d’acquisition de l'immeuble qu'on note Y ∴ après 1 an (31.12.N-1), valeur nette = Y - Y × 4% = Y - 0.04Y = (1 - 0.04)Y = 0.96Y "
            "∴ si 1'440'000 = 0.96Y al. Y = 1'440'00/0.96 = 1'500'000 ∴ l'amortissement constant N = Immeuble N-1 × 4% = 1'500'000 × 4% = 60'000" ),
},
{
     "q": "Quelle est la différence entre un amortissement constant et un amortissement dégressif ?",
        "choices": [
            "L’amortissement dégressif est calculé sur la valeur résiduelle (comptable) de l’actif immobilisé.",
            "L’actif immobilisé est amorti chaque année d’un montant identique avec un amortissement dégressif.",
            "L’actif immobilisé est amorti de manière indirecte avec un amortissement dégressif.",
            "Aucune réponses",
        ],
        "answer": 0,
        "explain": (
            "Amortissement constant : Base de calcul = val. d'acquisition & Montant d'amortissement = similaire chaque année"
            "Amortissement dégressif : Base de calcul = val. résiduelle & Montant d'amortissement = décroissant chaque année" ),
},
{
     "q": "De quelle manière un amortissement constant indirect d’un actif immobilisé est-il calculé ?",
        "choices": [
            "Sur la valeur résiduelle de l’actif immobilisé",
            "Sur la valeur comptable de l’actif immobilisé",
            "Sur la valeur d’achat de l’actif immobilisé moins les amortissements cumulés déjà comptabilisés",
            "Aucune réponses",
        ],
        "answer": 3,
        "explain": (
            "Le calcul de l'amortissement constant indirect se fait avec la val. d'acquisition -val. résiduelle. "
            "..."),
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
            # Essaye de charger l'image depuis le chemin spécifié
            st.image(q["image"], use_container_width=True, caption="Document de référence")
        except Exception as e:
            st.warning(f"⚠️ Impossible de charger l'image {q['image']} : {e}")
            # Affiche le chemin pour debug
            st.info(f"Chemin essayé : {q['image']}")
    
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
