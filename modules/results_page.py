import streamlit as st
import pandas as pd

from logic.calculations import calc_total_co2


def page_results():
    st.title("Sonuç & Analiz")

    results = calc_total_co2()
    total_kg = results["total"]
    total_ton = total_kg / 1000  # kg → ton

    st.metric("Yıllık Karbon Ayak İzin", f"{total_ton:.2f} ton CO₂")

    st.markdown("### Kategorilere Göre Dağılım (kg/yıl)")
    df = pd.DataFrame(
        {
            "Kategori": ["Ulaşım", "Enerji", "Su", "Beslenme", "Atık"],
            "CO₂ (kg/yıl)": [
                results["transport"],
                results["energy"],
                results["water"],
                results["food"],
                results["waste"],
            ],
        }
    )

    st.bar_chart(df.set_index("Kategori"))

    # Ağaç eşdeğeri (kabaca 1 ağaç ~ 22 kg CO2/yıl)
    trees = total_kg / 22
    st.info(
        f"Bu miktar yaklaşık **{trees:.0f} adet ağacın** bir yılda emeceği CO₂'ye eşdeğerdir."
    )

    st.markdown(
        "Soldaki menüden **Azaltım Senaryoları** sayfasına geçerek "
        "alışkanlıklarını değiştirirsen ne kadar tasarruf edebileceğini görebilirsin."
    )
