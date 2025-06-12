import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# --- Configuration de la page Streamlit ---
st.set_page_config(
    page_title="Dépistage de la Fragilité en Maison de Retraite",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Titre et Avertissement ---
st.title("👵👴 Dépistage de la Fragilité Motrice à l'Arrivée en Maison de Retraite")
st.subheader("Basé sur le Guide de Prévention Primaire de l'Ordre des Masseurs-Kinésithérapeutes")
st.write("---")

st.warning("""
    ⚠️ **AVERTISSEMENT CRUCIAL :**
    Cette application est une **démonstration conceptuelle à des fins éducatives uniquement crée par ADRIEN PRATMARTY dans le cadre de son mémoire**.
    Elle simule un dépistage de la fragilité motrice en se basant sur le "Guide Prévention primaire" de l'Ordre des Masseurs-Kinésithérapeutes.
    Elle **ne remplace pas une évaluation clinique professionnelle** par un médecin, un gériatre ou un kinésithérapeute.
    **Ne pas utiliser cette application pour prendre des décisions médicales ou de prise en charge.**
    Consultez toujours un professionnel de la santé qualifié pour une évaluation complète et des conseils personnalisés.
""")
st.write("---")

# --- Section Informations Personnelles ---
st.header("1. Informations sur la Personne")
col1, col2, col3 = st.columns(3)

with col1:
    age = st.slider("Âge (années)", 65, 100, 75, help="Dépistage pour les personnes de 65 ans et plus.")
    sexe = st.selectbox("Sexe", ["Homme", "Femme"], help="Influe sur les normes du Grip Test.")
    
with col2:
    st.write("---")
    st.markdown("**Statut de vie (avant l'arrivée en maison de retraite) :**")
    vivait_seul = st.checkbox("Vivait seul(e) à domicile ?", help="La fragilité peut augmenter le risque de désinsertion sociale.")

# --- Section Interrogatoire (Questions Clés) ---
st.header("2. Interrogatoire (Questions Clés)")
st.info("Répondez aux questions sur la base de l'entretien avec la personne ou son entourage.")

col_q1, col_q2 = st.columns(2)

with col_q1:
    chute_annee = st.radio(
        "A. Avez-vous chuté au cours des 12 derniers mois ?",
        ("Non", "Oui"), help="Même si la chute n'a pas eu de conséquence physique immédiate, elle doit être prise en compte. "
    )
    nb_chutes = 0
    if chute_annee == "Oui":
        nb_chutes = st.number_input("Combien de fois avez-vous chuté ?", min_value=1, max_value=20, value=1, step=1)
    
    peur_chuter = st.radio(
        "B. Avez-vous peur de chuter ?",
        ("Non", "Oui"), help="La peur de chuter augmente la probabilité de nouvelles chutes et peut entraîner une restriction des activités. "
    )
    
    douleurs_chroniques = st.radio(
        "C. Avez-vous des douleurs chroniques dans les jambes ou le dos ?",
        ("Non", "Oui"), help="Douleurs liées à l'arthrose, rhumatismes, altérant les capacités locomotrices. "
    )

with col_q2:
    troubles_cognitifs = st.radio(
        "D. Avez-vous constaté des troubles cognitifs ?",
        ("Non", "Oui"), help="Difficultés à retenir des mots simples, problèmes d'orientation spatio-temporelle. "
    )
    
    prise_medicaments = st.radio(
        "E. Prenez-vous des psychotropes ou plus de 4 médicaments ?",
        ("Non", "Oui"), help="Les psychotropes (sommeil, anxiété, angoisse, dépression) et certains diurétiques/anti-arythmiques favorisent le risque de chute. "
    )

# --- Section Tests Fonctionnels ---
st.header("3. Tests Fonctionnels (Réalisés par un Professionnel)")
st.info("Les tests suivants doivent être réalisés dans des conditions sécurisées par un kinésithérapeute ou un professionnel de santé.")

col_test1, col_test2 = st.columns(2)

with col_test1:
    appui_unipodal_s = st.number_input(
        "Temps d'Appui Unipodal (secondes)",
        min_value=0.0, max_value=60.0, value=10.0, step=0.5,
        help="Maintenir l'équilibre sur une jambe. < 5s = très haut risque de chute. "
    )
    
    tug_s = st.number_input(
        "Timed Up and Go (secondes)",
        min_value=0.0, max_value=60.0, value=12.0, step=0.1,
        help="Se lever d'une chaise, marcher 3m, revenir et s'asseoir. > 14s (ou > 20s pour les plus âgés/en institution) = anormal. "
    )
    
    lever_chaise_s = st.number_input(
        "Temps de Lever de Chaise (5 répétitions, secondes)",
        min_value=0.0, max_value=30.0, value=10.0, step=0.1,
        help="Se lever 5 fois d'une chaise sans les bras. > 14s = probable sarcopénie. "
    )

with col_test2:
    vitesse_marche_ms = st.number_input(
        "Vitesse de Marche sur 4 mètres (m/s)",
        min_value=0.0, max_value=2.0, value=1.0, step=0.05,
        help="Vitesse habituelle sur 4m (parcours de 6m). < 0.65 m/s = prédicteur de chute. "
    )
    
    grip_test_kg = st.number_input(
        "Grip Test (Force de préhension main dominante, Kg)",
        min_value=0.0, max_value=50.0, value=25.0, step=0.5,
        help="Indicateur de force musculaire globale et sarcopénie. Normes: >16 Kg femme, >27 Kg homme. "
    )
    
    difficulte_relever_sol = st.radio(
        "Difficulté à se relever du sol ?",
        ("Non", "Oui"), help="Révèle des capacités motrices et cognitives associées. Un temps passé au sol est un marqueur de gravité. "
    )
    
    anomalies_orthopediques = st.radio(
        "Anomalies orthopédiques (pied, chevilles, douleurs articulaires) ?",
        ("Non", "Oui"), help="Ex: déficit de flexion dorsale de la cheville, douleurs d'arthrose gênant la marche. "
    )

st.write("---")

# --- Logique de Dépistage et Calcul du Score ---
st.header("4. Analyse du Dépistage")

if st.button("Évaluer la Fragilité"):
    score_fragilite = 0
    facteurs_fragilite_detectes = []
    recommandations = []

    # --- Interrogatoire ---
    if chute_annee == "Oui":
        score_fragilite += 10
        facteurs_fragilite_detectes.append(f"Chutes au cours de l'année ({nb_chutes} fois)")
        if nb_chutes >= 2:
            score_fragilite += 5 # Risque accru si plusieurs chutes
            recommandations.append("- Évaluer le contexte et les circonstances des chutes répétées.")
        recommandations.append("- Un antécédent de chute est un facteur de risque majeur. Mise en place de mesures préventives à considérer. ")
    
    if peur_chuter == "Oui":
        score_fragilite += 8
        facteurs_fragilite_detectes.append("Peur de chuter")
        recommandations.append("- La peur de chuter peut entraîner une restriction d'activités, nécessitant un accompagnement. ")
    
    if douleurs_chroniques == "Oui":
        score_fragilite += 5
        facteurs_fragilite_detectes.append("Douleurs chroniques aux jambes/dos")
        recommandations.append("- Gestion de la douleur pour améliorer les capacités locomotrices. ")
        
    if troubles_cognitifs == "Oui":
        score_fragilite += 10
        facteurs_fragilite_detectes.append("Troubles cognitifs suspectés")
        recommandations.append("- Orientation vers le médecin traitant pour un bilan cognitif spécifique. ")
        
    if prise_medicaments == "Oui":
        score_fragilite += 7
        facteurs_fragilite_detectes.append("Prise de psychotropes ou > 4 médicaments")
        recommandations.append("- Revoir la liste des médicaments avec le médecin pour limiter les risques iatrogènes. ")

    # --- Tests Fonctionnels ---
    if appui_unipodal_s < 5:
        score_fragilite += 15
        facteurs_fragilite_detectes.append(f"Appui unipodal < 5s ({appui_unipodal_s}s)")
        recommandations.append("- Très haut risque de chute lié à l'équilibre. Travailler spécifiquement l'équilibre. ")
    elif appui_unipodal_s < 30:
        score_fragilite += 5
        facteurs_fragilite_detectes.append(f"Appui unipodal < 30s ({appui_unipodal_s}s)")
        recommandations.append("- Améliorer l'équilibre pour réduire le risque de chute. ")

    if tug_s > 14: # Seuil général. Pour les plus âgés/institution, ce serait >20s.
        score_fragilite += 12
        facteurs_fragilite_detectes.append(f"Timed Up and Go > 14s ({tug_s}s)")
        recommandations.append("- Améliorer la mobilité fonctionnelle et la vitesse de transition (assis-debout, marche). ")
    
    if lever_chaise_s > 14:
        score_fragilite += 10
        facteurs_fragilite_detectes.append(f"Lever de chaise (5 rép.) > 14s ({lever_chaise_s}s)")
        recommandations.append("- Indice de sarcopénie probable. Travailler le renforcement des membres inférieurs. ")
        
    if vitesse_marche_ms < 0.65:
        score_fragilite += 15
        facteurs_fragilite_detectes.append(f"Vitesse de marche < 0.65 m/s ({vitesse_marche_ms} m/s)")
        recommandations.append("- Forte prédiction de chutes, perte d'indépendance, déclin. Nécessite une intervention urgente sur la mobilité. ")
    elif vitesse_marche_ms < 0.8:
        score_fragilite += 10
        facteurs_fragilite_detectes.append(f"Vitesse de marche < 0.8 m/s ({vitesse_marche_ms} m/s)")
        recommandations.append("- Prédit des problèmes de mobilité et de chutes. Travailler l'endurance à la marche. ")
    elif vitesse_marche_ms < 1.0:
        score_fragilite += 5
        facteurs_fragilite_detectes.append(f"Vitesse de marche < 1.0 m/s ({vitesse_marche_ms} m/s)")
        recommandations.append("- Marqueur de fragilité. Maintenir et améliorer la vitesse de marche. ")

    grip_norme = 0
    if sexe == "Femme":
        grip_norme = 16
    else: # Homme
        grip_norme = 27
    
    if grip_test_kg < grip_norme:
        score_fragilite += 12
        facteurs_fragilite_detectes.append(f"Grip Test < norme ({grip_test_kg} Kg vs norme {grip_norme} Kg)")
        recommandations.append("- Risque de sarcopénie. Orientation vers un médecin pour évaluation nutritionnelle et renforcement global. ")

    if difficulte_relever_sol == "Oui":
        score_fragilite += 8
        facteurs_fragilite_detectes.append("Difficulté à se relever du sol")
        recommandations.append("- Travailler la capacité à se relever du sol en toute sécurité. ")
        
    if anomalies_orthopediques == "Oui":
        score_fragilite += 7
        facteurs_fragilite_detectes.append("Anomalies orthopédiques (pied, cheville, articulations)")
        recommandations.append("- Examen orthopédique approfondi et prise en charge spécifique des anomalies (ex: dorsiflexion cheville). ")

    # --- Détermination du Niveau de Fragilité ---
    # Ces seuils sont illustratifs et doivent être interprétés avec prudence.
    # Le guide ne donne pas de score total pondéré avec des seuils fixes pour la fragilité,
    # mais une combinaison de facteurs. Nous adaptons pour la démo.
    niveau_fragilite_text = ""
    if score_fragilite >= 50:
        niveau_fragilite_text = "FRAGILE 🔴"
        st.error(f"### Niveau de Fragilité Simulé : {niveau_fragilite_text}")
        st.write("La personne présente de nombreux indicateurs de fragilité motrice et un risque élevé de chute. Une évaluation multidisciplinaire urgente et une prise en charge complète sont nécessaires.")
    elif score_fragilite >= 25:
        niveau_fragilite_text = "PRÉ-FRAGILE 🟠"
        st.warning(f"### Niveau de Fragilité Simulé : {niveau_fragilite_text}")
        st.write("La personne présente plusieurs indicateurs de fragilité. Des interventions ciblées et un programme de préservation des capacités locomotrices sont fortement recommandés pour prévenir l'entrée dans la fragilité avérée. ")
    else:
        niveau_fragilite_text = "NON FRAGILE / ROBUTE 🟢"
        st.success(f"### Niveau de Fragilité Simulé : {niveau_fragilite_text}")
        st.write("La personne est actuellement considérée comme non fragile ou robuste. Un programme de maintien des capacités physiques est conseillé pour préserver cette autonomie. ")

    st.write(f"**Score de Fragilité Simulé :** {score_fragilite} points")

    if facteurs_fragilite_detectes:
        st.write("**Facteurs de Fragilité et Risques Détectés :**")
        for facteur in sorted(list(set(facteurs_fragilite_detectes))):
            st.markdown(f"- {facteur}")
    else:
        st.info("Aucun facteur de fragilité majeur n'a été détecté selon les critères renseignés.")

    st.write("---")
    st.header("5. Recommandations Ciblées")
    if recommandations:
        for rec in sorted(list(set(recommandations))):
            st.markdown(rec)
        st.markdown("""
        **Orientation Professionnelle :**
        * Selon le score obtenu, des conseils et un programme de préservation des capacités locomotrices doivent être mis en place par un **kinésithérapeute**. 
        * Une orientation vers le **médecin traitant** ou le **gériatre** est essentielle pour les personnes entrant dans la fragilité ou pré-fragiles, afin d'évaluer l'état général et d'ajuster la prise en charge. 
        """)
    else:
        st.info("Aucune recommandation spécifique ne ressort des entrées actuelles. Encouragez le maintien de l'activité physique et un suivi régulier.")

    st.write("---")
    st.markdown("""
    <small>Application développée à des fins de démonstration par votre assistant IA, basée sur le guide "Prévention primaire" de l'Ordre des Masseurs-Kinésithérapeutes (Juin 2022).</small>
    """, unsafe_allow_html=True)
