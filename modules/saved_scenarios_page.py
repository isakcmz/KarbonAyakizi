# modules/saved_scenarios_page.py

import streamlit as st
import pandas as pd
import plotly.express as px
from logic.scenario_store import load_scenarios


def page_saved_scenarios():
    st.title("Kaydedilen Senaryolar")

    scenarios = load_scenarios()

    if not scenarios:
        st.info("Henüz kaydedilmiş bir senaryo bulunmuyor. Azaltım Senaryoları sayfasından senaryo oluşturabilirsin.")
        return

    # --- Tablo görünümü ---
    df = pd.DataFrame([
        {
            "Tarih": s["date"],
            "Mevcut (kg/yıl)": s["base_total_kg"],
            "Senaryo (kg/yıl)": s["scenario_total_kg"],
            "Azalma (kg/yıl)": s["reduction_kg"]
        }
        for s in scenarios
    ])

    st.subheader("Senaryo Listesi")
    st.dataframe(df)

    # --- Grafik görünümü ---
    fig = px.bar(
        df,
        x="Tarih",
        y=["Mevcut (kg/yıl)", "Senaryo (kg/yıl)"],
        barmode="group",
        title="Senaryoların Zaman İçindeki Değişimi",
        text_auto=True,
        color_discrete_map={
            "Mevcut (kg/yıl)": "#3b82f6",
            "Senaryo (kg/yıl)": "#93c5fd",
        }
    )

    fig.update_layout(height=500, bargap=0.25)
    st.plotly_chart(fig, width="stretch")

    # Azalma grafiği
    fig2 = px.line(
        df,
        x="Tarih",
        y="Azalma (kg/yıl)",
        title="Zaman İçinde Emisyon Azalması",
        markers=True
    )
    st.plotly_chart(fig2, width="stretch")
