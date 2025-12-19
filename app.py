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
     "q": "Le matériel et mobilier est amorti de manière indirecte et décroissante au taux de 25%. Sachant que sa valeur comptable nette au 31.12.N avant amortissements : "
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
            "Sur la valeur d’achat de l’actif immobilisé moins sa valeur résiduelle",
        ],
        "answer": 3,
        "explain": (
            "Un amortissement constant indirect est calculé en répartissant chaque année le coût amortissable de l’actif (coût d’acquisition – valeur résiduelle) " 
            "via un compte d’amortissements cumulés."),
},
{
     "q": "Le 31.08.N, une entreprise a contracté une dette d’un montant de 233'000 dont le taux d’intérêt s’élève à 5%. \n"
          "Quelle écriture l’entreprise doit-elle comptabiliser au 31.12.N (résultat arrondi à 5 centimes) ?",
        "choices": [
            "Cha. fin. à Cha. payées d'avance pour 7'766.65",
            "Prod. à recevoir à Prod. fin. pour 3'883.35",
            "Cha. fin. à Cha. à payer pour 7'766.65",
            "Cha. fin. à Cha. à payer pour 3'883.35",
        ],
        "answer": 3,
        "explain": (
            "Il faut comptabiliser les intérêts courus non échus au 31.12.N, soit 233'000 × 5% × [(31.12.N - 31.08.N)/12] = 3'883.35 " 
            "en Cha. fin. à Cha. à payer (dette d'intérêts)"),
},
{
     "q": "Une entreprise est propriétaire d’un immeuble. Un locataire paiera le 30.01.N+1 la somme totale de 5'200 pour son loyer de décembre N & janvier N+1. \n"
          "Quelle écriture l’entreprise doit-elle comptabiliser au 31.12.N ?",
        "choices": [
            "Prod. à recevoir à Prod. d'immeuble pour 2'600",
            "Prod. à recevoir à Prod. d'immeuble pour 5'200",
            "Prod. d'immeuble à Prod. reçu d'avance pour 2'600",
            "Loyer à Prod. d'immeuble pour 5'200",
        ],
        "answer": 0,
        "explain": (
            "Sur les 5'200 de loyer couvrant décembre N et janvier N+1, seule la part du mois de décembre (5'200/2 = 2'600) doit être rattachée à l’exercice N comme produit à recevoir. "),
},
{
    "q": "Au 31.12.N, sur la base des informations ci-dessous, quel est le montant des intérêts courus sur la dette hypothécaire ? Sachant que le taux d’intérêt 4.25 % & échéance le 30 juin."
         "Valeurs comptables au 31.12.N : Immeuble acquis le 01.01.N-1 pour 1'440'000 & Dette hypothécaire 644'200",
        "choices": [
            "13'689.25",
            "14'494.50",
            "27'378.50",
            "Aucune réponses",
        ],
        "answer": 0,
        "explain": (
            "Les intérêts courus au 31.12.N correspondent aux intérêts de 6 mois (du 30.06.N au 31.12.N) sur la dette hypothécaire de 644'200 au taux annuel de 4.25 %, soit "
            "644'200 × 4.25% × 6/12 = 13'689.25"),
},
{
    "q": "Une prime annuelle de 1'500 d'assurance vol couvrant les risques liés au stock de marchandises a été payée le 31.03.N, valable jusqu'au 31.03.N+1. \n"
         "Quelle écriture l’entreprise doit-elle comptabiliser au 31.12.N ?",
        "choices": [
            "Assurances à Cha. à payer pour 375.",
            "Cha. payées d'avance à Assurances pour 1'125",
            "Assurances à Banque pour 1'125",
            "Cha. payées d'avance à Assurances pour 375",
        ],
        "answer": 3,
        "explain": (
            "On a payé une prime annuelle de 1'500 le 31.03.N pour la période du 31.03.N au 31.03.N+1 ∴ 31.03.N au 31.12.N = 9 mois pour l'exercice N & "
            "01.01.N+1 au 31.03.N+1 = 3 mois pour l'exercice N+1. Aisi, la part de la prime pour N : 1'500 × 9/12 = 1'125 (Assurances). "
            "La part de la prime pour N+1 : 1'500 × 3/12 = 375 (Cha. payer d'avance). "
            "Au 31.12.N, il faut reclasser la partie N+1 : Cha. payé d'avance à Assurances pour 375"),
},
{
    "q": "Quelle est la conséquence de la comptabilisation d’un actif transitoire ?",
        "choices": [
            "L’augmentation d’une charge d’exploitation.",
            "La diminution d’un produit d’exploitation.",
            "Une augmentation du résultat d’exploitation.",
            "Aucune réponses",
        ],
        "answer": 2,
        "explain": (
            "Quand on comptabilise un actif transitoire (cha. payées d’avance), on fait l’écriture : Actif transitoire (Cha. payées d’avance) à Cha. d’exp. "
            "Cette écriture diminue Cha. d’exp. car on retire de la charge la partie qui concerne N+1. "
            "Ainsi, moins de charge = résultat d'exploitation plus élevé."),
},
{
    "q": "La correction de valeur sur créances clients (ducroire) doit s’élever à 5% du montant des créances résultant de ventes. "
         "Sur la base des informations ci-dessous, quelle écriture l’entreprise doit-elle comptabiliser au 31.12.N ? "
         "Val. comptable au 31.12.N avant ajustement : Créances clients = 24'400 & Ducroire = 2'000",
        "choices": [
            "Pertes s/créances à Corr. de valeur s/créances clients pour 1'220",
            "Corr. de valeur s/créances clients à Créances clients pour 780",
            "Corr. de valeur s/créances clients à Pertes s/créances pour 780",
            "Corr. de valeur s/créances clients à Pertes s/créances pour 1'220",
        ],
        "answer": 2,
        "explain": (
            "Créances clients = 24'400 ∴ Corr. de valeur au 31.12.n : 24'400 × 5% = 1'220 ⇒ Ajustement du Ducroire : Corr. souhaitée - Corr. actuelle = 1'220 − 2'000 = −780. "
            "Si on réduit le ducroire, on comptabilise Corr. de valeur s/créances clients à Pertes s/créances pour 780 "),
},
{
    "q": "Lors de l’achat d’un titre de placement sous la forme d’une action qui supporte la charge des intérêts courus ? ",
        "choices": [
            "L'acheteur des titres.",
            "Le vendeur des titres.",
            "L'acheteur et le vendeur à parts égales.",
            "Il n'y a pas d'intérêts courus lors de l'achat d'actions.",
        ],
        "answer": 3,
        "explain": (
            "Les actions ne génèrent pas d’intérêts (seulement des dividendes éventuels), "
            "la notion d’intérêts courus ne s’applique qu’aux titres à intérêt comme les obligations, pas aux actions."),
},
{
    "q": "Quelle est la caractéristique d’un titre sous la forme d’une obligation ? ",
        "choices": [
            "C’est une part du capital de l’entreprise.",
            "Il est toujours remboursé en cas de faillite de l’entreprise.",
            "Le taux d'intérêt annuel est fixe.",
            "Aucune réponses",
        ],
        "answer": 2,
        "explain": (
            "L'obligation est un titre de créance qui verse des intérêts réguliers (souvent fixes) à son détenteur, "
            "contrairement aux actions qui représentent une part du capital et ne garantissent ni intérêt fixe ni remboursement automatique en cas de faillite."),
},
{
    "q": "Quelle est le montant des actifs circulants ? \n"
         "Informations comptables : Banque (100'000), Créances résultants des ventes (246'800), Pertes s/créances (24'500), Dettes résultant d’achats (150’000), "
         "Mobilier (235'000), Impôts anticipé à payer (16'500), Charges payées d’avance (2'900), Stock (169'800), Capital-actions (250'000), Licences (145'000), Produits à recevoir (32'500).",
        "choices": [
            "524'500",
            "527'500",
            "549'100",
            "552'000",
        ],
        "answer": 1,
        "explain": (
            "Actifs circulants = Banque (100'000) + Clients (246'800) - Pertes s/créances (24'500) + Charges payées d’avance (2'900) + Stock (169'800) + Produits à recevoir (32'500) = 527'500 "),
},
{
    "q": "Avant la clôture, le comptable a oublié de comptabiliser l’intérêt semestriel en faveur de la Banque Raiffeisen 1'522. "
         "Quelle écriture l’entreprise doit-elle comptabiliser ? ",
        "choices": [
            "Banque Raiffeisen à Prod.fin pour 1'522",
            "Cha.fin à Banque Raiffeisen pour 2'341.55",
            "Cha.fin à Banque Raiffeisen pour 1'522",
            "Banque Raiffeisen (1'522) et IA à récupérer (819.55) à Prod.fin pour 2'341.55",
        ],
        "answer": 2,
        "explain": (
            "L’intérêt semestriel en faveur de la Banque Raiffeisen signifie que l’entreprise doit payer 1'522 à la banque, "
            "ce qui constitue pour elle une charge financière (débit Cha.fin) et une diminution de la banque ou une dette envers la banque (crédit Banque Raiffeisen)."),
},
{
    "q": "Quel montant est comptabilisé lors du paiement d’une annuité hypothécaire ? ",
        "choices": [
            "Le montant des intérêts annuels est comptabilisé au débit du compte « Hypothèque ».",
            "Le montant de l’annuité hypothécaire est comptabilisé au débit du compte « Hypothèque »",
            "Le montant du remboursement de la dette hypothécaire est comptabilisé au crédit du compte « Hypothèque »",
            "Aucune réponses",
        ],
        "answer": 3,
        "explain": (
            "Lors du paiement d’une annuité, c’est la partie remboursant la dette qui est comptabilisée au crédit du compte Hypothèque "
            "(et la partie intérêts va en charges financières, pas dans Hypothèque). "),
},
{
    "q": "Une entreprise paie une annuité hypothécaire de CHF 3'000 le 30.06.N date d’échéance d’une hypothèque d’un montant de 75'000 à un taux d’intérêt de 2.5%. \n"
         "Quel est le montant du remboursement de l’hypothèque effectué le 30.06.N ?",
        "choices": [
            "1'125",
            "1'875",
            "3'000",
            "Aucune réponses",
        ],
        "answer": 0,
        "explain": (
            "L’annuité payée est 3'000. Les intérêts sur l’hypothèque se calculent ainsi : 75'000 × 2.5% = 1'875. "
            "Donc, dans l’annuité de 3'000, l'intérêt représente 1'875 & le reste du remboursement : 3'000 - 1'875 = 1′125. "
            "Le remboursement effectif de l’hypothèque le 30.06.N est donc de 1'125"),
},
{
    "q": "Que sont des tantièmes versés par une société anonyme ?",
        "choices": [
            "C’est une part du bénéfice versée aux actionnaires.",
            "C’est une part du bénéfice versée aux administrateurs.",
            "C’est un bonus versé aux collaborateurs.",
            "Aucune réponses",
        ],
        "answer": 1,
        "explain": (
            "C'est une rémunération prélevée sur le bénéfice et versée aux membres du conseil d’administration, pas aux actionnaires ni aux employés."),
},
{
    "q": "Quelle est la nature du compte « dividendes nets » avant leur versement aux actionnaires ?",
        "choices": [
            "C’est un compte d’actifs circulants.",
            "C’est un compte de charges.",
            "C’est un compte de capitaux propres.",
            "C’est un compte de capitaux étrangers à court terme.",
        ],
        "answer": 3,
        "explain": (
            "Avant leur versement, les dividendes nets représentent une dette envers les actionnaires, donc un passif à court terme."),
},
{ 
    "q": "Quelle est la nature du compte « impôt anticipé à récupérer » ?",
        "choices": [
            "C’est un compte de produits.",
            "C’est un compte de capitaux étrangers à court terme.",
            "C’est un compte de charges.",
            "C’est un compte d’actifs circulants.",
        ],
        "answer": 3,
        "explain": (
            "L’impôt anticipé à récupérer est une créance envers l’Etat, donc une somme que l’entreprise récupérera prochainement."),
},
{
    "q": "La TVA est un impôt fédéral indirect. Qui supporte la charge fiscale de cet impôt ?",
        "choices": [
            "Le consommateur final",
            "Les entreprises",
            "L'Etat",
            "Aucune réponses",
        ],
        "answer": 3,
        "explain": (
            "La TVA est un impôt indirect, les entreprises ne font que la collecter et la reverser à l’Etat, mais c’est le consommateur final qui en supporte réellement les coûts."),
},
{
    "q": "Au 31.12.N, selon l’avis de crédit de la banque, les intérêts nets sur le compte courant bancaire s’élèvent à 530. \n"
         "Quelle écriture l’entreprise doit-elle comptabiliser ? (montant arrondi à 5cts) ",
        "choices": [
            "Banque (530) à Prod.fin (344.50) et IA à récupérer (185.50)",
            "IA à récupérer (185.50) et Banque (344.50) à Prod.fin pour 530",
            "Cha.fin (344.50) et Impôt anticipé à récupérer (185.50) à Banque pour 530",
            "Banque (530) et IA à récupérer (285.40) à Prod.fin pour 815.40",
        ],
        "answer": 3,
        "explain": (
            "Les intérêts nets reçus (530) correspondent aux intérêts bruts après l'IA retenu de 35% (185.50), donc on doit recalculer les intérêts bruts : "
            "Banque ou intérêts nets (530) / 65% = 815.40 et l’IA à récupérer : intérêts bruts (815.40) × 35 % = 285.40. "
            "ce qui donne l’écriture : Banque (530) et IA à récupérer (285.40) à Prod.fin (815.40)."),
},
{
    "q": "Une entreprise a contracté le 01.01.N, une hypothèque de 1'200'000. Le montant de l’annuité hypothécaire pour l’année N s’élève à 64'000. "
         "Elle comprend un remboursement de CHF 40'000. \n"
         "Sur la base des informations précédentes, quel est le taux d’intérêt de l’hypothèque ?",
        "choices": [
            "2%",
            "3.33%",
            "5.33%",
            "Aucune réponses",
        ],
        "answer": 0,
        "explain": (
            "Intérêts = annuité (64'000) - remboursement (40'000) = 24'000. "
            "Taux d'intérêt de l'hypothèque = Intérêts (24'000) / Hypothèque (1'200'000) = 2% "),
},
{
    "q": "Une entreprise achète un nouveau véhicule pour 25'200. Le garagiste reprend un ancien véhicule pour 12'000. "
         "Ce dernier avait été acheté pour 24'000 il y a quelques années et les amortissements effectués à ce jour s’élèvent à 5'400. \n"
         "Quel résultat l’entreprise a-t-elle réalisé sur la reprise de son ancien véhicule ?",
        "choices": [
            "gain de 1'200",
            "perte de 6'600",
            "perte de 12'000",
            "Aucune réponses",
        ],
        "answer": 1,
        "explain": (
            "Valeur comptable de l’ancien véhicule = Ancien véhicule (24'000) - Amortissements (5'400) = 18'600 mais reprise du garagiste à 12'000 ∴ "
            "perte =  reprise (12'000) - Valeur comptable de l’ancien véhicule (18'600) = -6'600 "),
},
{
    "q": "Quel organe d’une société anonyme nomme le conseil d’administration ?",
        "choices": [
            "Le conseil de direction",
            "Le conseil de fondation",
            "L'assemblée générale",
            "Les associés",
        ],
        "answer": 2,
        "explain": (
            "L’assemblée générale des actionnaires élit et nomme les membres du conseil d’administration dans une société anonyme. "
            " Contrairement aux Sàrl où ce sont bien les associés qui nomment les gérants."),
},
{
    "q": "Complétez le texte : Les entreprises doivent atteindre 2 des 3 critères suivants pendant 2 années consécutives pour être soumises au contrôle ordinaire : "
         " chiffre d'affaires net ... millions, total du bilan ... millions, nombre de collaborateurs à plein temps ... en moyenne.",
        "choices": [
            "30/10/200",
            "30/15/250",
            "40/20/250",
            "50/25/300",
        ],
        "answer": 2,
        "explain": (
            "Selon le CO : CAN ≥ 40 millions, total du bilan ≥ 20 millions et ≥ 250  EPT en moyenne. "),
},
{
    "q": "Pour une entreprise de moins de 10 EPT quelle condition doit-elle respecter pour un opting out ?",
        "choices": [
            "L'unanimité des actionnaires.",
            "L'unanimité des administrateurs.",
            "La majorité des actionnaires.",
            "La majorité des administrateurs.",
        ],
        "answer": 0,
        "explain": (
            "Pour une entreprise de moins de 10 EPT, un opting-out (renonciation au contrôle restreint) n’est valable que si tous les actionnaires y consentent expressément, " 
            "la loi exige l’unanimité des actionnaires pour supprimer l’audit."),
},
{
    "q": "Sous quelle condition une entreprise soumise au contrôle ordinaire peut-elle réaliser un contrôle restreint ?",
        "choices": [
            "L'unanimité des actionnaires.",
            "L'unanimité des administrateurs.",
            "La majorité des actionnaires.",
            "Une entreprise sous contrôle ordinaire ne peut jamais réaliser un contrôle restreint",
        ],
        "answer": 3,
        "explain": (
            "Une société qui remplit les conditions du contrôle ordinaire est obligatoirement auditée selon le CO et ne peut pas la remplacer par un contrôle restreint, même avec l’accord des actionnaires."), 
},
{
    "q": "A la bourse suisse, quelle norme comptable doit respecter une entreprise cotée sur le marché international ?",
        "choices": [
            "Swiss Gaap ou IFRS",
            "Swiss Gaap ou US Gaap",
            "US Gaap ou IFRS",
            "Swiss Gaap RPC",
        ],
        "answer": 2,
        "explain": (
            "Une entreprise cotée sur un marché international doit appliquer une norme comptable reconnue mondialement, " 
            "ce qui n'est le cas que des IFRS ou US GAAP, alors que Swiss GAAP RPC est limité au marché suisse."),
},
{
    "q": "L’inventaire du stock de marchandises au 31.12.N indique une valeur de CHF 29'700. " 
         "Quel est l’effet sur le compte de résultat N ?",
        "choices": [
            "Charge de 3'300",
            "Produit de 3'300",
            "Charge de 29'700",
            "Produit de 29'700",
        ],
        "answer": 0,
        "explain": (
            "Variation de stock = 29'700 - 33'000 = -3'300 ∴ Diminution de stock ⇒ charge al. que augmentation de stock ⇒ produit."),
    "image": "serie_4_balance_soldes.png",
},
{
    "q": "En raison de la faillite d’un client, 10% des créances résultant de ventes doit être passé en pertes s/créances. " 
         "La provision pour pertes s/créances doit se monter à 6% du total des créances résultant des ventes & 100% des créances douteuses. \n "
         "Quel est l’effet sur le compte de résultat N ? ",
        "choices": [
            "Produit de 4'470",
            "Charge de 7'470",
            "Charge de 7'800",
            "Aucune réponses",
        ],
        "answer": 3,
        "explain": (
            "Pertes s/créances : Clients (55'000) × 10% = 5'500. Provision pertes s/créances : (Clients sains × 6%) + Cr. douteuses = "
            "[(55'000 - 5'500) × 6% + 4'500 = 7'470. Δ Provision pertes s/créances : Provision − Provision existante = 7'470 - 3'000 = 4'470. "
            "Effet sur le compte de résultat N : Pertes s/créances (5'500) ↑ + Provision pertes s/créances (4'470) ↑ = 9'970 de charge."),
    "image": "serie_4_balance_soldes.png",
},
{
    "q": "L'immeuble est amorti de manière constante. Quel est le taux d'amortissement utilisée ?" 
         " (résultat arrondi à deux décimales)",
        "choices": [
            "3%",
            "6%",
            "6.47%",
            "Aucune réponses",
        ],
        "answer": 0,
        "explain": (
            "Sachant que la val. d'acquisition est de 800'000 (N-2) & Amortissement & corr. de valeur s/Immeuble est de 48'000. "
            "En amortissement constant, l'annuité constant : amortssements cumulés (48'000) / 2ans  = 24'000. "
            "Le taux d'amortissement est alors annuité (24'000) / val. d'acquisition (800'000) = 0.03 = 3%"),
    "image": "serie_4_balance_soldes.png",
},
{
    "q": "Le matériel et mobilier est amorti de manière dégressive au taux de 25%. \n" 
         "Quelle est l’écriture que l’entreprise doit comptabiliser au 31.12.N ?",
        "choices": [
            "Amort. & corr. de val. s/mat.&mob. à Matériel & mobilier pour 1'687.50",
            "Amortissement à Amort. & corr. de val. s/mat.&mob. pour 1'687.50",
            "Amortissement à Matériel & mobilier pour 1'687.50 ",
            "Amortissement à Amort. & corr. de val. s/mat.&mob. pour 4'000",
        ],
        "answer": 1,
        "explain": (
            "Pour l'amortissement dégressif, on applique le taux dégressif sur la Valeur Comptable Nette (VCN). "
            "VCN début N : Matériel & mobilier (16'000) - Amort. & corr. de val. s/mat.&mob. (9'250) = 6'750. "
            "Le montant de l'amortissement net début N : VCN (6'750) × 25% = 1'687.50 ∴ "
            "En méthode indirecte, on débite une charge d’amortissement et on crédite la correction de valeur. "),
    "image": "serie_4_balance_soldes.png",
},
{
    "q": "Le compte véhicule est amorti de manière directe et constante au taux de 25%. \n" 
         "Quel est le montant de l’amortissement au 31.12.N ?",
        "choices": [
            "1'312.50",
            "2'625",
            "5'250",
            "Aucune réponses",
        ],
        "answer": 0,
        "explain": (
            "Véhicule au 31.12.N avant amortissement : 5'250 & taux constant sur la Valeur Comptable Nette (VCN) : 25% ∴ "
            "Amortissement N : Véhicule (5'250) × 25% = "
            "Le montant de l'amortissement net début N : VCN (6'750) × 25% = 1'312.50."),
    "image": "serie_4_balance_soldes.png",
},
{
    "q": "15.05.N-2, l’entreprise a accordé un prêt de 20'000 à son partenaire commercial au taux de 4%. " 
         "Quelle est l’opération de régularisation qui doit être comptabilisée au 31.12.N ?",
        "choices": [
            "Charge payée d'avance : 342.50",
            "Produit reçu d’avance : 342.50",
            "Produit à recevoir : 500",
            "Aucune réponses",
        ],
        "answer": 2,
        "explain": (
            "Prêt : 20'000 & taux d'intérêts : 4% ∴ intérêts annuels : 20'000 × 4% = 800. "
            "Intérêts à régulariser uniquement la partie de l’année en cours comprise entre la dernière échéance 15.05.N et le 31.12.N ∴ "
            "15.05.N au 31.12.N ⇒ 7.5 mois al. opération de régularisation : 800 ×  7.5/12 = 500. L'entreprise a gagné 500 d’intérêts non encore encaissés au 31.12.N (PàR)."),
},
{
    "q": "Au 31.12.N, à combien s’élève le montant de l’amortissement de l’immeuble locatif acquis au 1er janvier N-3 pour une valeur de 4'000'000 "
         "amorti de manière constante et directe ? ",
        "choices": [
            "60'000",
            "80'000",
            "240'000",
            "Aucune réponses",
        ],
        "answer": 0,
        "explain": (
            "Immeuble locatif N-3 : 4'000'000 sachant amortissements constants : valeur d’acquisition (4'000'000) – amortissements cumulés s/immeuble (3'760'000) = 240'000. "
            "L'immeuble a été amorti de N-3, N-2, N-1 & N ∴ 4 exercices al. Annuités = 240'000/4 = 60′000. "
            "Le montant de l’amortissement au 31.12.N est de 60'000 "),
    "image": "serie_4_balance_verification.png",
},
{
    "q": "Sachant que les intérêts courus sur l’hypothèque s’élèvent à CHF 11'250 au 31.12.N, quel est le taux de l’hypothèque ? \n "
         "(résultat arrondi à 2 décimales) ",
        "choices": [
            "1.13%",
            "1.50%",
            "4.50%",
            "Aucune réponses",
        ],
        "answer": 1,
        "explain": (
            "Hypothèque : 1'000'000 sachant Intérêts courus au 31.12.N pour la période du 31.03.N au 31.12.N ⇒ 9 mois al. "
            "Intérêts (I) = Capital (C) × Taux (T) × Durée (N) = C × T × N = 11'250 ∴ T = I / (C × N) = 11'250 / (1'000'000 × 9/12) = 0.015 = 1.5%"),
    "image": "serie_4_balance_verification.png",
},
{
    "q": "Au 31.12.N, la correction de valeur sur créances clients doit s’élever à 5 % du montant des créances résultant des ventes aux clients suisses "
         "et 10 % du montant des créances résultant des ventes aux clients étrangers. \n "
         "Quelle écriture doit être comptabilisée au 31.12.N ? ",
        "choices": [
            "Corr. de val. s/cr. clients à Perte s/cr. clients pour 2'000",
            "Perte s/cr. clients à Corr. de val. s/cr. clients pour 2'000",
            "Corr. de val. s/cr. clients à Perte s/cr. clients pour 5'000",
            "Perte s/cr. clients à Corr. de val. s/cr. clients pour 5'000",
        ],
        "answer": 0,
        "explain": (
            "Corr. de val. s/cr. clients suisses : 60'000 × 5% = 3'000 & Corr. de val. s/cr. clients étrangers : 20'000 × 10% = 2'000 ∴ Total : 3'000 + 2'000 = 5'000."
            "Corr. de val. s/cr. clients : Solde Final (5'000) - Solde initial (7'000) = -2'000 (au débit) ⇒ diminution de la correction (produit)."),
    "image": "serie_4_balance_verification.png",
},
{
    "q": "Quelle est l’écriture de comptabilisation de l’amortissement dégressif de 20% des véhicules au 31.12.N ?",
        "choices": [
            "Amortissements à Véhicules pour 6'000",
            "Amort. & corr. de val. s/véhicules à Véhicules pour 6'000",
            "Amortissements à Amort. & corr. de val. s/véhicules pour 13'000",
            "Aucune réponses",
        ],
        "answer": 3,
        "explain": (
            "Véhicule au 31.12.N avant amortissement (VCN) : Véhicules (65'000) - Amort. & corr. de val. s/véhicules (35'000) = 30'000 "
            "Taux dégressif : 20% que l'on applique à la VCN ∴ Amortissement N : VCN (30'000) × 20% = 6'000. Sachant qu'il existe un compte Amort. & corr. de val. s/véhicules, "
            "on se en méthode indirecte. L’écriture d’amortissement devrait être Amortissements à Amort. & corr. de val. s/véhicules pour 6'000"),
    "image": "serie_4_balance_verification.png",
},
{
    "q": "L'inventaire final du stock de marchandises au 31.12.N est 19'200. En tenant compte de cette information, quelle est l’incidence de la variation du stock sur l'EBITDA ? ",
        "choices": [
            "EBITDA ↑ de 2'400",
            "EBITDA ↓ de 2'400",
            "EBITDA ↑ de 19'200",
            "EBITDA ↓ de 19'200",
        ],
        "answer": 0,
        "explain": (
            "Var. de stock : SF (19'200) - SI (16'800) = 2'400 d'augmentation comptabilisé en prod. d'exploitation ∴ l'EBITDA ↑"),
    "image": "serie_4_balance_verification.png",
},
{
    "q": "Au 31.12.N, quelle écriture doit être comptabilisée pour tenir compte de l’intérêt couru sur les obligations Brest SA ? ",
        "choices": [
            "Prod. fin. à Produit à recevoir pour 50",
            "Produit à recevoir à Prod. fin. pour 150",
            "Prod. fin. à Produit à recevoir pour 155.25",
            "Produit à recevoir à Prod. fin. pour 155.25",
        ],
        "answer": 1,
        "explain": (
            "L’intérêt couru sur les obligations Brest SA est un prod. fin. car intérêt gagné, il n'est pas encore encaissé au 31.12 ∴ PàR."
            "Calcul intérêt couru : I = C × T × N sachant que C = 20'000, T = 1% & N : du 31.03.N au 31.12.N ⇒ 9 mois ∴ "
            "I = 20'000 × 1% × 9/12 = 150"),
    "image": "serie_4_balance_verification.png",
},
{
    "q": "Au 31.12.N, le comptable a enregistré l’écriture suivante : Corr. de val. s/créances à Perte s/créances pour 2'000. \n"
         "A quelle opération comptable correspond cette écriture ?",
        "choices": [
            "Une diminution de 2'000 du compte Corr. de val. s/créances.",
            "Une augmentation de 2'000 du compte Perte s/créances.",
            "La perte d’une créance de 2'000 suite à la faillite d’un client.",
            "Une augmentation de 2'000 du compte Corr. de val. s/créances.",
        ],
        "answer": 0,
        "explain": (
            "Débit : Corr. de val. s/créances qui diminue de 2'000 (provision) & "
            "Crédit : Perte s/créances qui diminue aussi de 2'000 (charge) ∴ c'est une diminution de 2'000 du compte Corr. de val. s/créances."),
},
{
    "q": "Le 01.01.N, la société X a acquis du mobilier pour une valeur 30'000. Il a été amorti selon la méthode de l’amortissement direct constant à un taux de 10%. \n"
         "Quel est le montant du compte « Amort.&Corr. de val. s/mobilier » au 01.01.N+3 ? ",
        "choices": [
            "0",
            "3'000",
            "6'000",
            "9'000",
        ],
        "answer": 3,
        "explain": (
            "On nous dit que le mobilier est amorti selon la méthode constante à 10% de la VCN. "
            "Amortissement annuel = 30'000 × 10% = 3'000 & on a comptabilisé 3 exercices complets : 3'000 × 3 = 9'000."), 
},
{
    "q": "L'entreprise Y a payé le 30.04.N une prime annuelle pour son assurance incendie et dégâts d’eau. "
         "Au 31.12.N, le comptable a enregistré correctement l’écriture de régularisation suivante : Charge payée d'avance à Assurance pour 2'400. \n"
         "Quel est le montant annuel de la prime d'assurance ?",
        "choices": [
            "300",
            "600",
            "3'600",
            "7'200",
        ],
        "answer": 3,
        "explain": (
            "Prime d'assurance payée le 30.04.N couvre 12 mois jusqu’au 30.04.N+1. Au 31.12.N, CPA enregistrée est de 2'400 ⇒ 4 mois d'assurance à payer car "
            "on a déjà cosommé du 30.04.N au 31.12.N sur 30.04.N+1 ⇒ 8 mois sur 12 consommés ∴ Coût mensuel de la prime : 2'400/4 = 600 ∴ "
            "Coût annuel de la prime : 600 × 12 = 7'200"),
},
{
    "q": "Début 01.N, Dupont SA a acquis des véhicules pour une valeur de 80'000. Leur valeur résiduelle avant l’enregistrement de l’amortissement constant au 31.12.N+2 s’élève à CHF 48'000. \n"
         "Quelle écriture le comptable de Dupont SA doit-il enregistrer pour tenir compte de l’amortissement indirect de cet actif immobilisé ? ",
        "choices": [
            "Amortissement à Véhicules pour 32'000",
            "Amortissement à Amort.&Corr. de val. s/véhicules pour 16'000",
            "Amortissement à Amort.&Corr. de val. s/véhicules pour 32'000",
            "Amortissement à Véhicule pour 16'000",
        ],
        "answer": 1,
        "explain": (
            "Val. d'acquisition véhicule à N : 80'000 & Val. résiduelle véhicule à N+2 : 48'000 ∴ Amortissement cumulé de 2 ans = 80'000 - 48'000 = 32'000 al. amortissement annuel constant : 32'000/2 = 16'000. "
            "En amortissement indirect, on débite le compte charge : Amortissement & on crédite le compte correcteur d'actif : Amort.&Corr. de val. s/véhicules."),
},
{
    "q": "La Corr. de val. s/clients au 31.12.N s'élevait à 50'000. Au 31.12.N+1, la Corr. de val. s/clients doit augmenter de 10'000. "
         "Après la clôture des comptes, la comptable s’aperçoit que cette var. de correction de valeur n'a pas été comptabilisé. \n "
         "Quelle est l’incidence de cette variation sur le résultat EBIT ? ",
        "choices": [
            "EBIT ↑ de 10'000",
            "EBIT ↓ de 10'000",
            "EBIT ↑ de 60'000",
            "EBIT n'est pas modifié",
        ],
        "answer": 1,
        "explain": (
            "La Corr. de val. s/clients ⇒ Ducroire : Charge si ↑ (Perte s/créance) mais un Produit si ↓ (Corr. de val.). "
            "Dans notre cas, une ↑ 10'000  aurait dû être comptabilisée en Pertes s/créance mais cette Charge n’a pas été comptabilisée, le résultat EBIT a été artificiellement trop élevé de 10'000 ∴ "
            "L’incidence correcte est EBIT ↓ de 10'000 car si l’écriture avait été passée, l’EBIT aurait diminué de ce montant"),
},
{
    "q": "Dans son rapport annuel au 31.12.N, Ouspa SA présente la note ci-dessous pour détailler ses actifs immobilisés : \n"
         "A combien s’élève le montant des immobilisations incorporelles présentées selon la manière directe dans le bilan au 31.12.N ?  ",
        "choices": [
            "1'050'000",
            "1'900'000",
            "12'050'000",
            "Aucune réponses",
        ],
        "answer": 3,
        "explain": (
            "Au bilan en “manière directe”, on présente : VCN = Valeur d’acquisition − Amortissements cumulés sachant que "
            "Valeur d’acquisition au 31.12.N = 1'400'000 + 500'000 - 0 = 1'900'000 & Amortissements cumulés au 31.12.N = 700'000 + 350'000 - 0 = 1'050'000 ∴" 
            "VCN = 1'900'000 - 1'050'000 = 850'000"),
    "image": "tableau_immobilisations.png",
},
{
    "q": "Sur la base du décompte de salaire présenté, quelle est l’écriture de comptabilisation du salaire et des charges sociales de l’employé ?",
        "choices": [
            "Salaires (6'000) à Cha. sociales (877.90) et Banque (5'122.10)",
            "Salaires (6'000) et Dettes à c-t (877.90) à Banque (6'877.90)",
            "Salaires (6'000) et Cha. sociales (877.90) à Banque (6'877.90)",
            "Salaires (5'122.10) et Cha. sociales (877.90) à Banque (6'000)",
        ],
        "answer": 0,
        "explain": (
            "Salaire brut = 6'000 & total des déductions (Cha. social des employés) = 877.90 ∴ Salaire net (Banque) = 6'000 - 877.90 = 5'122.10"),
    "image": "fiche_salaire.png",
},
{
    "q": "Sur la base du décompte de salaire présenté, quel est le montant total que l’employeur devra verser à la caisse AVS/AI/APG (montant total incluant " 
    "la part employé et employeur) ?",
        "choices": [
            "318",
            "636",
            "878.60",
            "Aucune réponses",
        ],
        "answer": 1,
        "explain": (
            "AVS/AI/APG en part employeur 10.60% et part employé 5.30% ∴ Montant retenu part employeur : 6'000 × 10.60% = 636 & "
            "Montant retenu part employé : 6'000 × 5.30% = 318 al. total à verser 318 + 318 = 636"),
    "image": "fiche_salaire.png",
},
{
    "q": "Sur la base du décompte de salaire présenté, quel est le montant minimum l’employeur doit-il prendre en charge pour la cotisation au deuxième pilier (LPP) ?" 
    "la part employé et employeur) ?",
        "choices": [
            "360",
            "720",
            "Aucune part minimale à charge de l’employeur",
            "Aucune réponses",
        ],
        "answer": 0,
        "explain": (
            "Pour le 2e pilier (LPP), l’employeur doit payer au minimum 50% de la cotisation totale. "
            "Si la part employé est de 360, al. Total LPP : 360 + 360 = 720 ∴ Costiation LPP part employeur : 720 × 50% = 360"),
    "image": "fiche_salaire.png",
},
{
    "q": "Sur la base du décompte de salaire présenté, quel serait le montant de la cotisation pour l’assurance chômage (AC) "
    "à la charge de l’employeur si le salaire brut était augmenté à 6'200 ?",
        "choices": [
            "66",
            "68.20",
            "132",
            "136.40",
        ],
        "answer": 1,
        "explain": (
            "Pour AC, on sait que le taux total = 2.20% & la part employé 1.10% al. la part employeur 1.10% (Car partage la moitié du taux total). "
            "Si le salaire brute est de 6'200 al. AC part employeur : 6'200 × 1.10% = 68.20."),
    "image": "fiche_salaire.png",
},
{
    "q": "Sur la base du décompte de salaire présenté, pour quelle raison aucune cotisation pour l’assurance accidents professionnels n’est-elle prélevée ?",
        "choices": [
            "Car le salaire annuel ne dépasse pas CHF 22'680",
            "Car l’employeur a oublié de la prendre en compte",
            "Car la cotisation est à la charge de l’employeur",
            "Car l’employée réalise un travail administratif dans un bureau et la cotisation n’est pas obligatoire pour ce domaine d’activité",
        ],
        "answer": 2,
        "explain": (
            "La prime accidents professionnels (AP) est entièrement payée par l’employeur, donc elle n’est pas prélevée sur le salaire de l’employé. "
            "Cependant, l'assurance accidents non professionnels (AANP) est entièrement payée par l'employé étant dans ce fichier de 78.-"),
    "image": "fiche_salaire.png",
},
{
    "q": "Sur la base du décompte de salaire présenté, pour quelle raison aucune cotisation pour le 3e pilier A n’est-elle prélevée ?",
        "choices": [
            "Car le salaire annuel ne dépasse pas CHF 22'680",
            "Car l’employeur a oublié de la prendre en compte",
            "Car la cotisation est à la charge de l’employeur",
            "Car le 3ème pilier A est facultatif et à charge de l’employé",
        ],
        "answer": 3,
        "explain": (
            "Le 3e pilier A n’est pas une assurance sociale obligatoire comme AVS/AI/APG ou AC. C’est une épargne retraite volontaire."),
    "image": "fiche_salaire.png",
},
{
    "q": "Un employé s’interroge sur sa retraite et se demande quelle assurance sociale lui permettra d'augmenter ses revenus à l'âge de la retraite ?",
        "choices": [
            "L'AVS car elle lui assurera une rente équivalente à son dernier salaire.",
            "La LPP car elle lui assurera une rente fixe identique à celle de tous les salariés.",
            "L'APG car elle lui assurera une part plus élevée de son dernier salaire.",
            "Aucune réponses",
        ],
        "answer": 3,
        "explain": (
            "Premièrement, l'AVS (1er pilier) ne garantit pas une rente équivalente au dernier salaire ; elle assure un minimum vital (rente plafonnée). "
            "Deuxièmement, la LPP (2e pilier) ne donne pas une rente fixe identique pour tous ; elle dépend de l’avoir vieillesse accumulé (cotisations + intérêts). "
            "Pour finir, l'assurance perte de gain couvre surtout des situations comme service, maternité, etc., pas la retraite."),
},
{
    "q": "Si l'employée habite en France, quelle part d’impôt à la source serait à la charge de l'employeur ?",
        "choices": [
            "La part dépend de la situation personnelle de l'employé (enfants, mariage).",
            "L'impôt à la source n’est pas à la charge de l'employeur.",
            "L'intégralité de l’impôt à la source est à la charge de l'employeur.",
            "Aucune réponses",
        ],
        "answer": 1,
        "explain": (
            "En France, le prélèvement à la source (PAS) est : "
            "un impôt dû par l’employé prélevé sur son salaire et simplement versé par l’employeur à l’État (rôle d’intermédiaire). "
            "donc l'employeur ne “paye” pas l'impôt : il le retient sur le net de l'employé."),
},
{
    "q": "Si l'employée habite en France, quelle part d’impôt à la source serait à la charge de l'employeur ?",
        "choices": [
            "La part dépend de la situation personnelle de l'employé (enfants, mariage).",
            "L'impôt à la source n’est pas à la charge de l'employeur.",
            "L'intégralité de l’impôt à la source est à la charge de l'employeur.",
            "Aucune réponses",
        ],
        "answer": 1,
        "explain": (
            "En France, le prélèvement à la source (PAS) est : "
            "un impôt dû par l’employé prélevé sur son salaire et simplement versé par l’employeur à l’État (rôle d’intermédiaire). "
            "donc l'employeur ne “paye” pas l'impôt : il le retient sur le net de l'employé."),
},
    






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
    user_name = st.text_input("Votre nom (obligatoire)", "")
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
# Vérification du nom obligatoire
if not user_name.strip():
    st.warning("⚠️ Veuillez entrer votre nom dans la barre latérale pour commencer le QCM.")
    st.info("👈 Ouvrez le menu latéral et remplissez le champ 'Votre nom'")
    st.stop()  # Arrête l'exécution du reste du code


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
                file_name="results_qcm_comptabilite.csv",
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
