import streamlit as st
from logic.calculations import calc_total_co2
from logic.config import FACTORS


def generate_recommendations(results):
    """
    Kullanıcının kategori dağılımına göre akıllı öneriler üretir.
    """
    transport = results["transport"]
    energy = results["energy"]
    water = results["water"]
    food = results["food"]
    waste = results["waste"]
    total = results["total"]

    share = {
        "transport": transport / total,
        "energy": energy / total,
        "water": water / total,
        "food": food / total,
        "waste": waste / total,
    }

    suggestions = []

    # --- ULAŞIM ---
    if share["transport"] > 0.35:
        suggestions.append("🚗 **Ulaşımı azalt:** Haftada 1-2 gün toplu taşıma veya ortak araç kullan.")
    elif share["transport"] > 0.20:
        suggestions.append("🚗 **Yakıt verimliliği:** Aracının lastik basınçlarını düzenli kontrol et.")

    # --- ENERJİ ---
    if share["energy"] > 0.30:
        suggestions.append("💡 **LED ampule geç:** Aylık elektrik tüketimini %10–20 azaltabilirsin.")
        suggestions.append("🔌 **Stand-by cihazları kapat:** Yıllık 60–120 kWh tasarruf sağlar.")
    elif share["energy"] > 0.15:
        suggestions.append("💡 **Enerji verimli cihazlar kullanmaya çalış.**")

    # --- SU ---
    if share["water"] > 0.12:
        suggestions.append("💧 **Kısa duş alışkanlığı:** 1 dakikalık azalma yılda yüzlerce litre su tasarrufu sağlar.")
    else:
        suggestions.append("💧 Su tüketimin oldukça iyi durumda — böyle devam et!")

    # --- BESLENME ---
    if share["food"] > 0.30:
        suggestions.append("🍽 **Kırmızı et tüketimini azalt:** Haftada 1 kg azaltmak yılda 1000+ kg CO₂ tasarrufu sağlar.")
    elif share["food"] > 0.15:
        suggestions.append("🥗 **Bitki ağırlıklı beslenmeyi artırabilirsin.**")

    # --- ATIK ---
    if share["waste"] > 0.15:
        suggestions.append("🗑 **Geri dönüşüme başla:** Atık kaynaklı emisyonu %40'a kadar düşürebilirsin.")
    elif share["waste"] > 0.08:
        suggestions.append("♻️ **Geri dönüşüm seviyeni biraz daha artırarak iyileştirme sağlayabilirsin.**")
    else:
        suggestions.append("♻️ Atık yönetimin çok iyi — tebrikler!")

    return suggestions


def page_recommend():

    results = calc_total_co2()
    total = results["total"]

    # hata önlem kısmı
    if total == 0:
        st.warning(
            "⚠️ Henüz veri girilmedi.\n\n"
            "Kişisel önerilerin oluşturulabilmesi için önce **Veri Girişi** bölümünden alışkanlıklarını girmen gerekiyor."
        )
        return



    st.title("🌱 Kişisel Sürdürülebilirlik Önerileri")

    st.write(
        "Aşağıdaki öneriler günlük alışkanlıklarına göre otomatik olarak üretilmiştir. "
        "Bu önerileri uygulayarak karbon ayak izini önemli ölçüde azaltabilirsin."
    )

    # Hesaplamaları al
    results = calc_total_co2()
    total = results["total"]

    st.metric("Mevcut Yıllık CO₂", f"{total/1000:.2f} ton")

    # Öneri listesi
    st.subheader("🌿 Kişisel Önerilerin")

    suggestions = generate_recommendations(results)

    for sug in suggestions:
        st.markdown(f"- {sug}")

    # Tahmini CO₂ kazancı
    potential_saving = 0

    if results["transport"] > 1000:
        potential_saving += 150  # kg
    if results["energy"] > 800:
        potential_saving += 120
    if results["food"] > 900:
        potential_saving += 200
    if results["waste"] > 200:
        potential_saving += 80

    st.markdown("---")
    st.subheader("📉 Önerileri Uygularsan Tahmini CO₂ Azalımı")

    st.info(
        f"Bu önerilerin yarısını uygulaman, yılda yaklaşık **{potential_saving:.0f} kg CO₂** azaltmanı sağlar."
    )

    st.success("Öneriler başarıyla hesaplandı!")
