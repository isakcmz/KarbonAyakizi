import streamlit as st
import pandas as pd
import plotly.express as px


from logic.calculations import calc_total_co2


# Bu projede referans alınan yaklaşık kişi başı yıllık CO₂ değerleri (ton/yıl)
TURKEY_AVG_TON = 4.4   # Türkiye ortalaması (örnek referans değer)
WORLD_AVG_TON = 4.7    # Dünya ortalaması (örnek referans değer)
EU_AVG_TON = 7.0       # AB ortalaması (kabaca)


def page_results():
    st.title("Sonuç & Analiz")

    # --- 1) Kendi sonucunu hesapla ---
    results = calc_total_co2()
    total_kg = results["total"]
    total_ton = total_kg / 1000  # kg → ton

    st.metric("Yıllık Karbon Ayak İzin", f"{total_ton:.2f} ton CO₂")

    # --- 2) Kategorilere göre dağılım (kg/yıl) ---
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

    # Ağaç eşdeğeri (kabaca 1 ağaç ~ 22 kg CO₂/yıl emiyor varsayımı)
    trees = total_kg / 22
    st.info(
        f"Bu miktar yaklaşık **{trees:.0f} adet ağacın** bir yılda emeceği CO₂'ye eşdeğerdir."
    )

    st.markdown("---")

    # --- 3) Türkiye ve Dünya ile Karşılaştırma (ton/yıl) ---
    st.markdown("### Türkiye ve Dünya ile Karşılaştırma")

    
    ordered_df = pd.DataFrame(
        {
            "Grup": [
                "Senin Sonucun",
                "Türkiye Ortalaması",
                "Dünya Ortalaması",
                "AB Ortalaması",
            ],
            "CO₂ (ton/yıl)": [
                total_ton,
                TURKEY_AVG_TON,
                WORLD_AVG_TON,
                EU_AVG_TON,
            ],
        }
    )

    fig = px.bar(
        ordered_df,
        x="Grup",
        y="CO₂ (ton/yıl)",
        color="Grup",
        color_discrete_map = {
            "Senin Sonucun": "#10b981",       # yeşil (kullanıcı)
            "Türkiye Ortalaması": "#3b82f6", # mavi
            "Dünya Ortalaması": "#6366f1",   # mor-mavi
            "AB Ortalaması": "#0ea5e9",      # turkuaz
        },
        text="CO₂ (ton/yıl)",
    )

    fig.update_traces(texttemplate="%{text:.2f}", textposition="outside")
    fig.update_layout(
        yaxis_title="CO₂ (ton/yıl)",
        xaxis_title="",
        showlegend=False,
        height=500,
    )

    st.plotly_chart(fig, width="stretch")


    # Duruma göre kısa yorum
    yorum = ""
    if total_ton < TURKEY_AVG_TON * 0.7:
        yorum = "Türkiye ortalamasının oldukça **altındasın**. Oldukça sürdürülebilir bir yaşam tarzın var. 👏"
    elif total_ton < TURKEY_AVG_TON:
        yorum = "Türkiye ortalamasının **biraz altındasın**. İyi durumdasın, küçük iyileştirmelerle daha da düşürebilirsin. 🌱"
    elif total_ton < WORLD_AVG_TON:
        yorum = "Türkiye ortalamasının biraz üzerindesin ama dünya ortalamasına yakınsın. Bazı alışkanlıklarda ufak değişiklikler işe yarayabilir. 🤏"
    else:
        yorum = "Türkiye ve dünya ortalamasının **üzerindesin**. Ulaşım, et tüketimi ve enerji kullanımını gözden geçirerek emisyonunu ciddi oranda azaltabilirsin. 🔍"

    st.warning(yorum)

    st.caption(
        "Not: Karşılaştırma değerleri, literatürde sıkça kullanılan yaklaşık kişi başı yıllık CO₂ "
        "emisyon ortalamalarına göre alınmıştır ve bu uygulama için referans niteliğindedir."
    )

    st.markdown(
        "Soldaki menüden **Azaltım Senaryoları** sayfasına geçerek, alışkanlıklarını değiştirirsen "
        "emisyonunun bu ortalamalara göre nasıl değişeceğini inceleyebilirsin."
    )
