import streamlit as st
import pandas as pd
import plotly.express as px
from logic.scenario_store import add_scenario
from logic.report_generator import create_pdf_report

from logic.calculations import (
    calc_total_co2,
    calc_transport_co2,
    calc_energy_co2,
    calc_water_co2,
    calc_food_co2,
    calc_waste_co2,
)


def page_scenarios():
    st.title("Azaltım Senaryoları")
    st.write(
        "Aşağıdaki ayarlarla oynayarak bazı alışkanlıklarını değiştirirsen "
        "yıllık CO₂ emisyonunun ne kadar azalacağını görebilirsin."
    )

    # Mevcut durumu hesapla
    base = calc_total_co2()
    base_total = base["total"]

    st.markdown("### Senaryo Ayarları")

    col1, col2 = st.columns(2)

    with col1:
        reduce_car_days = st.slider(
            "Arabayı haftada kaç gün daha az kullanırsın?",
            min_value=0,
            max_value=7,
            value=2,
            step=1,
        )

        reduce_beef_percent = st.slider(
            "Kırmızı et tüketimini yüzde kaç azaltırsın?",
            min_value=0,
            max_value=100,
            value=50,
            step=10,
        )

    with col2:
        led_change = st.checkbox("Evde LED ampullere geçiyorum")
        better_recycling = st.checkbox("Geri dönüşüm seviyemi artırıyorum")

    # --- Yeni veri kopyaları (mevcut veriyi bozmamak için) ---
    new_transport = st.session_state["transport"].copy()
    new_food = st.session_state["food"].copy()
    new_energy = st.session_state["energy"].copy()
    new_waste = st.session_state["waste"].copy()

    # 1) Arabayı azaltma
    if new_transport.get("use_car"):
        old_days = new_transport.get("car_days_per_week", 0)
        new_transport["car_days_per_week"] = max(old_days - reduce_car_days, 0)

    # 2) Kırmızı eti azaltma
    old_beef = new_food.get("beef_kg_per_week", 0)
    new_food["beef_kg_per_week"] = old_beef * (1 - reduce_beef_percent / 100)

    # 3) LED ampullere geçiş → elektrik %15 azalır varsayımı
    if led_change:
        old_kwh = new_energy.get("electricity_kwh_per_month", 0)
        new_energy["electricity_kwh_per_month"] = old_kwh * 0.85

    # 4) Geri dönüşümü artırma
    if better_recycling:
        new_waste["recycle_level"] = "high"

    # --- Yeni senaryo sonuçlarını hesapla ---
    new_results = {
        "transport": calc_transport_co2(new_transport),
        "energy": calc_energy_co2(new_energy),
        "water": calc_water_co2(st.session_state["water"]),
        "food": calc_food_co2(new_food),
        "waste": calc_waste_co2(new_waste),
    }
    new_results["total"] = sum(new_results.values())

    st.markdown("### Önce / Sonra Karşılaştırması")

    comp_df = pd.DataFrame(
        {
            "Kategori": ["Ulaşım", "Enerji", "Su", "Beslenme", "Atık", "Toplam"],
            "Mevcut (kg/yıl)": [
                base["transport"],
                base["energy"],
                base["water"],
                base["food"],
                base["waste"],
                base_total,
            ],
            "Senaryo (kg/yıl)": [
                new_results["transport"],
                new_results["energy"],
                new_results["water"],
                new_results["food"],
                new_results["waste"],
                new_results["total"],
            ],
        }
    )

    st.dataframe(comp_df.set_index("Kategori"))
    
    # --- Önce / Sonra karşılaştırma grafiği ---
    fig = px.bar(
        comp_df,
        x="Kategori",
        y=["Mevcut (kg/yıl)", "Senaryo (kg/yıl)"],
        barmode="group",     # BURASI YAN YANA YAPAN KISIM
        text_auto=True,
        color_discrete_map={
            "Mevcut (kg/yıl)": "#3b82f6",    # mavi
            "Senaryo (kg/yıl)": "#93c5fd",   # açık mavi
        },
    )

    fig.update_layout(
        title="Önce / Sonra Karşılaştırması",
        yaxis_title="CO₂ (kg/yıl)",
        xaxis_title="Kategori",
        height=500,
        bargap=0.25,
    )
    st.plotly_chart(fig, width="stretch")

    diff = base_total - new_results["total"]
    st.success(
        f"Bu senaryoda yıllık CO₂ emisyonunu **{diff/1000:.2f} ton** azaltmış oluyorsun."
    )

    if st.button("💾 Senaryoyu Kaydet"):
        add_scenario(
            base_total=base_total,
            new_total=new_results["total"],
            base_data=base,
            new_data=new_results
        )
        st.success("Senaryo başarıyla kaydedildi! 🎉")


    if st.button("📄 Bu Senaryonun PDF Raporunu Oluştur"):
        pdf_path = create_pdf_report(
            results=base,
            scenario={
                "base_total": base_total,
                "new_total": new_results["total"]
            }
        )
        with open(pdf_path, "rb") as f:
            st.download_button(
                label="📄 PDF Raporu İndir",
                data=f,
                file_name="senaryo_raporu.pdf",
                mime="application/pdf"
            )


    
