import streamlit as st
import pandas as pd
from logic.calculations import calc_total_co2


def get_global_data():
    """Küresel ve ülke bazlı ortalama karbon ayak izi (ton CO₂/yıl)."""
    return {
        "Sen": None,  # hesaplanacak
        "Türkiye": 6.1,
        "Dünya": 4.7,
        "AB Ortalaması": 7.2,
        "ABD": 15.0,
        "Hindistan": 1.9
    }


def determine_level(total_ton):
    """Kullanıcıya seviye belirleme."""
    if total_ton < 3:
        return "Yeşil Seviye – Çok Sürdürülebilir 🌿", "#d1fae5"
    elif total_ton < 6:
        return "Sarı Seviye – Orta Emisyon 🙂", "#fef9c3"
    elif total_ton < 10:
        return "Turuncu Seviye – Yüksek Emisyon ⚠️", "#ffedd5"
    else:
        return "Kırmızı Seviye – Kritik Emisyon 🚨", "#fee2e2"


def percentile_rank(user, country_avg):
    """Kullanıcının Türkiye ortalamasına göre yüzdelik dilimini hesaplama."""
    # Basit bir modele göre:
    # 0 ton = %100 sürdürülebilir
    # Türkiye ortalaması = %50
    # 12 ton = %0
    if user <= 0:
        return 100
    if user >= 12:
        return 5

    # Lineer yüzdelik
    percent = 100 - (user / 12 * 100)
    return max(5, min(100, percent))


def page_comparison():
    st.title("🌍 Global Karşılaştırma & Sıralama")

    # Kullanıcı verisi
    results = calc_total_co2()
    total_kg = results["total"]
    total_ton = total_kg / 1000

    # Veri yoksa uyarı
    if total_kg == 0:
        st.warning(
            "⚠️ Henüz veri girilmedi.\n\n"
            "Global karşılaştırma yapabilmek için önce **Veri Girişi** bölümünden alışkanlıklarını girmen gerekiyor."
        )
        return

    st.metric("Yıllık Karbon Ayak İzin", f"{total_ton:.2f} ton CO₂")

    # Seviye belirleme
    level_text, level_color = determine_level(total_ton)

    st.markdown(
        f"""
        <div style="
            background:{level_color};
            padding:15px;
            border-radius:12px;
            border:1px solid #cbd5e1;
            margin-top:10px;
        ">
        <h3 style="margin:0;">{level_text}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.subheader("📊 Global Karşılaştırma Tablosu")

    # Veri hazırlama
    global_data = get_global_data()
    global_data["Sen"] = total_ton

    df = pd.DataFrame(
        {"Ülke / Bölge": list(global_data.keys()),
         "Ortalama CO₂ (ton/yıl)": list(global_data.values())}
    )

    st.dataframe(df)

    # Grafik
    st.bar_chart(df.set_index("Ülke / Bölge"))

    st.markdown("---")
    st.subheader("📈 Türkiye İçindeki Sıralama Tahmini")

    rank = percentile_rank(total_ton, 6.1)

    st.info(
        f"Türkiye'deki bireylerin yaklaşık **%{rank:.0f}**'inden daha düşük karbon ayak izine sahipsin."
    )

    st.write(
        "Bu skor, bireysel karbon ayak izinin Türkiye ortalamasına göre konumunu gösteren "
        "basitleştirilmiş bir sıralama modelidir."
    )

    st.success("Global ve ulusal karşılaştırmalar hazır!")
