import streamlit as st
import pandas as pd

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
    st.bar_chart(comp_df.set_index("Kategori"))

    diff = base_total - new_results["total"]
    st.success(
        f"Bu senaryoda yıllık CO₂ emisyonunu **{diff/1000:.2f} ton** azaltmış oluyorsun."
    )
