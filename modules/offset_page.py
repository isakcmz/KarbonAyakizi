import streamlit as st
import pandas as pd

from logic.calculations import calc_total_co2
from logic.config import FACTORS


def page_offset():
    st.title("🌿 Karbon Temizleme / Offset Hesaplama")

    st.write(
        """
        Karbon ayak izinizi yalnızca azaltmak değil, aynı zamanda **telafi etmek** de mümkündür.
        Ağaç dikimi, yenilenebilir enerji projeleri ve karbon kredisi kullanarak
        toplam CO₂ emisyonunu dengeleyebilirsiniz.
        """
    )

    # Mevcut CO2 toplamını al
    results = calc_total_co2()
    total = results["total"]

    # --- VERİ YOKSA HATA YERİNE UYARI GÖSTER ---
    if total == 0:
        st.warning(
            "⚠️ Henüz veri girilmedi.\n\n"
            "**Offset hesaplaması yapabilmek için önce Veri Girişi bölümünden alışkanlıklarını girmen gerekiyor.**"
        )
        return

    st.subheader("Mevcut Yıllık Karbon Ayak İzin")
    st.metric("Toplam CO₂:", f"{total/1000:.2f} ton / yıl")

    st.markdown("---")
    st.subheader("1) Ağaç Dikimi")

    trees = st.slider(
        "Yılda kaç adet ağaç dikmeyi planlıyorsun?",
        min_value=0,
        max_value=500,
        value=10,
        step=5,
    )

    tree_offset = trees * 22  # 1 ağaç ~ 22 kg CO2/yıl

    st.info(f"🌳 {trees} ağaç → yıllık **{tree_offset} kg CO₂** telafisi sağlar.")

    st.markdown("---")
    st.subheader("2) Yenilenebilir Enerji Projesi Katkısı (kWh offset)")

    green_kwh = st.number_input(
        "Yıllık kaç kWh yenilenebilir enerji projesine destek veriyorsun?",
        min_value=0.0,
        value=0.0,
        step=10.0,
    )

    green_offset = green_kwh * 0.45  # ortalama CO2 offset değeri

    st.info(f"⚡ {green_kwh} kWh yeşil enerji → **{green_offset:.0f} kg CO₂** telafisi.")

    st.markdown("---")
    st.subheader("3) Doğrudan Karbon Kredisi")

    carbon_credit = st.number_input(
        "Kaç kg CO₂ karbon kredisi almak istersin?",
        min_value=0.0,
        value=0.0,
        step=50.0,
    )

    st.success(f"💳 Seçilen karbon kredisi → **{carbon_credit:.0f} kg CO₂** telafisi.")

    st.markdown("---")

    # TOPLAM OFFSET
    total_offset = tree_offset + green_offset + carbon_credit
    new_total = max(total - total_offset, 0)

    st.subheader("🌎 Net Sonuç")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Telafi Edilen CO₂", f"{total_offset:.0f} kg / yıl")
    with col2:
        st.metric("Yeni Net CO₂", f"{new_total/1000:.2f} ton / yıl")

    # --- % iyileşme (0'a bölme kontrolü eklendi!) ---
    percent = (total_offset / total) * 100 if total > 0 else 0

    st.write(f"🔽 Toplam karbon ayak izinde **%{percent:.1f}** iyileşme sağlandı.")

    # Grafik
    df = pd.DataFrame(
        {"Durum": ["Mevcut CO₂", "Net CO₂"], "Değer": [total, new_total]}
    ).set_index("Durum")

    st.bar_chart(df, width="content")

    st.success("Karbon telafisi işlemleri başarıyla hesaplandı!")
