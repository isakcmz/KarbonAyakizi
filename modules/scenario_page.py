# modules/scenario_page.py

import streamlit as st
import pandas as pd
import plotly.express as px

from logic.calculations import (
    calc_total_co2,
    calc_transport_co2,
    calc_energy_co2,
    calc_water_co2,
    calc_food_co2,
    calc_waste_co2,
)
from logic.scenario_store import add_scenario
from logic.report_generator import create_pdf_report
from logic.config import FACTORS



def page_scenarios():
    st.title("Azaltım Senaryoları")

    st.write(
        "Aşağıdaki ayarlarla oynayarak bazı alışkanlıklarını değiştirirsen "
        "yıllık CO₂ emisyonunun ne kadar azalacağını görebilirsin."
    )

    # --- Mevcut durumu hesapla ---
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

    # --- Yan yana (grouped) bar grafiği ---
    fig = px.bar(
        comp_df,
        x="Kategori",
        y=["Mevcut (kg/yıl)", "Senaryo (kg/yıl)"],
        barmode="group",
        text_auto=True,
        color_discrete_map={
            "Mevcut (kg/yıl)": "#3b82f6",    # mavi
            "Senaryo (kg/yıl)": "#93c5fd",   # açık mavi
        },
        title="Mevcut ve Senaryo Karşılaştırması",
    )
    fig.update_layout(
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

    # --- Senaryoyu kaydet butonu ---
    if st.button("💾 Senaryoyu Kaydet"):
        add_scenario(
            base_total=base_total,
            new_total=new_results["total"],
            base_data=base,
            new_data=new_results,
        )
        st.success("Senaryo başarıyla kaydedildi! 🎉")

    # --- PDF raporu oluştur butonu ---
    st.markdown("#### Bu Senaryonun PDF Raporu")
    if st.button("📄 Bu Senaryonun PDF Raporunu Oluştur"):
        pdf_path = create_pdf_report(
            results=base,
            scenario={
                "base_total": base_total,
                "new_total": new_results["total"],
            },
        )
        with open(pdf_path, "rb") as f:
            st.download_button(
                label="📄 PDF Raporu İndir",
                data=f,
                file_name="senaryo_raporu.pdf",
                mime="application/pdf",
            )

    st.markdown("---")

    # ====================================================
    #   ANINDA SİMÜLASYON – ULAŞIM ODAKLI
    # ====================================================
    st.markdown("### 🚗 Anında Simülasyon – Ulaşım Odaklı")

    transport_state = st.session_state.get("transport", {})
    use_car = transport_state.get("use_car", False)
    old_days = transport_state.get("car_days_per_week", 0)

    if not use_car or old_days == 0:
        st.info(
            "Ulaşım simülasyonu için araba kullanım bilgisi bulunamadı veya haftalık araba kullanımın 0. "
            "Veri Girişi → Ulaşım sekmesinden araba kullanımını tanımlarsan burada anında etkiyi görebilirsin."
        )
        return

    st.write(
        "Aşağıdaki slider ile, haftada kaç gün daha az araba kullanırsan "
        "toplam yıllık CO₂ emisyonunun nasıl değişeceğini anında görebilirsin."
    )

    sim_reduce_days = st.slider(
        "Arabayı haftada kaç gün azaltmayı düşünüyorsun?",
        min_value=0,
        max_value=min(7, old_days),
        value=2,
        step=1,
    )

    # 0'dan old_days'e kadar tüm azaltım senaryolarını hesaplayalım
    rows = []
    for d in range(0, min(7, old_days) + 1):
        tmp_transport = transport_state.copy()
        tmp_transport["car_days_per_week"] = max(old_days - d, 0)

        t = calc_transport_co2(tmp_transport)
        e = calc_energy_co2(st.session_state["energy"])
        w = calc_water_co2(st.session_state["water"])
        f = calc_food_co2(st.session_state["food"])
        wa = calc_waste_co2(st.session_state["waste"])

        total = t + e + w + f + wa

        rows.append(
            {
                "Azaltılan Gün": d,
                "Toplam CO₂ (kg/yıl)": total,
            }
        )

    sim_df = pd.DataFrame(rows)

    # Seçilen değere karşılık gelen satır
    current_row = sim_df[sim_df["Azaltılan Gün"] == sim_reduce_days].iloc[0]
    current_total = current_row["Toplam CO₂ (kg/yıl)"]

    # Çizgi grafik
    fig_sim = px.line(
        sim_df,
        x="Azaltılan Gün",
        y="Toplam CO₂ (kg/yıl)",
        markers=True,
        title="Arabayı Daha Az Kullanmanın Toplam CO₂ Üzerindeki Etkisi",
    )
    fig_sim.update_layout(height=450)

    st.plotly_chart(fig_sim, width="stretch")

    st.info(
        f"Şu anda haftada **{old_days} gün** araba kullanıyorsun. "
        f"Eğer bunu **{sim_reduce_days} gün azaltırsan**, toplam yıllık CO₂ emisyonun "
        f"yaklaşık **{current_total/1000:.2f} ton** seviyesine iner "
        f"(mevcut: {base_total/1000:.2f} ton)."
    )




    # ====================================================
    #   ANINDA SİMÜLASYON – YENİLENEBİLİR ENERJİ
    # ====================================================
    st.markdown("### ⚡ Anında Simülasyon – Yenilenebilir Enerji Etkisi")

    energy_state = st.session_state.get("energy", {})
    old_pct = energy_state.get("renewable_pct", 0)
    monthly_kwh = energy_state.get("electricity_kwh_per_month", 0)

    if monthly_kwh == 0:
        st.info("Yenilenebilir enerji etkisini görebilmek için elektrik tüketimi girmen gerekiyor.")
    else:
        sim_pct = st.slider(
            "Elektriğinin yüzde kaçını yenilenebilir yapmak istersin?",
            min_value=0,
            max_value=100,
            value=old_pct,
            step=5,
        )

        yearly_kwh = monthly_kwh * 12
        base_elec = yearly_kwh * FACTORS["electricity_kg_per_kwh"]
        new_elec = base_elec * (1 - sim_pct / 100)

        st.write(f"Mevcut elektrik CO₂: **{base_elec:.0f} kg/yıl**")
        st.write(f"Yeni seçime göre CO₂: **{new_elec:.0f} kg/yıl**")

        st.success(
            f"Bu seçimle elektrik kaynaklı CO₂ emisyonun **{(base_elec - new_elec):.0f} kg/yıl** azalır."
        )


