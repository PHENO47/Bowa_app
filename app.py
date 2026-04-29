import streamlit as st
from datetime import datetime

from services.data_service import load_data, add_signalement, clean_data
from models.prediction import predict_by_zone
from utils.validation import validate_input

st.set_page_config(page_title="BOWA", layout="wide")

st.title("⚡ BOWA - Coupures Électriques")

menu = st.sidebar.radio("Menu", [
    "📊 Tableau de bord",
    "📝 Nouveau signalement",
    "🔮 Prédictions"
])

# ======================
# LOAD DATA
# ======================
@st.cache_data
def get_data():
    return load_data()

df = get_data()
df = clean_data(df)

# ======================
# DASHBOARD
# ======================
if menu == "📊 Tableau de bord":

    st.subheader("📊 Aperçu des données")

    if df.empty:
        st.warning("Aucune donnée disponible")
    else:
        col1, col2, col3 = st.columns(3)

        col1.metric("Total incidents", len(df))
        col2.metric("Durée moyenne", f"{df['duree_heures'].mean():.1f} h")
        col3.metric("Impact moyen", f"{df['impact_numerique'].mean():.0f}")

        st.dataframe(df, use_container_width=True)

# ======================
# FORMULAIRE
# ======================
elif menu == "📝 Nouveau signalement":

    st.subheader("Ajouter un signalement")

    ville = st.text_input("Ville")
    zone = st.selectbox("Zone", df["zone"].unique() if not df.empty else ["Centre"])
    duree = st.slider("Durée (h)", 0.5, 48.0, 4.0)

    impact = st.selectbox("Impact", ["50-200", "200-500", "500+"])
    frequence = st.selectbox("Fréquence", ["Rare", "Fréquente"])

    if st.button("Enregistrer"):

        errors = validate_input(ville, duree)

        if errors:
            for e in errors:
                st.error(e)
        else:
            impact_map = {"50-200": 125, "200-500": 350, "500+": 800}
            frequence_map = {"Rare": 1, "Fréquente": 10}

            new_row = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "ville": ville,
                "zone": zone,
                "type_zone": "Urbaine",
                "duree_heures": duree,
                "cause": "Inconnue",
                "frequence": frequence,
                "impact": impact,
                "impact_numerique": impact_map[impact],
                "frequence_numerique": frequence_map[frequence],
                "commentaire": ""
            }

            add_signalement(new_row)

            st.success("✅ Signalement ajouté")
            st.cache_data.clear()

# ======================
# PRÉDICTIONS
# ======================
elif menu == "🔮 Prédictions":

    st.subheader("Prédiction (coupure de 5h)")

    predictions = predict_by_zone(df)

    if not predictions:
        st.warning("Pas assez de données")
    else:
        for zone, val in predictions.items():
            st.write(f"📍 {zone} → ~ {int(val)} personnes")