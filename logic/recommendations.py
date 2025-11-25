from typing import Dict, List


def generate_recommendations(results: Dict[str, float]) -> List[str]:
    """
    calc_total_co2() çıktısını alır ve metinsel öneriler döndürür.

    results örneği:
    {
        "transport": ...,
        "energy": ...,
        "water": ...,
        "food": ...,
        "waste": ...,
        "total": ...
    }
    """
    total = results.get("total", 0.0)

    if total <= 0:
        return [
            "Henüz veri girmediğin için öneri oluşturulamıyor. "
            "Önce **Veri Girişi** bölümünü doldur."
        ]

    shares = {
        "transport": results["transport"] / total,
        "energy": results["energy"] / total,
        "water": results["water"] / total,
        "food": results["food"] / total,
        "waste": results["waste"] / total,
    }

    # En yüksek paydan en düşüğe sırala
    sorted_cats = sorted(shares.items(), key=lambda x: x[1], reverse=True)

    recommendations: List[str] = []

    for cat, share in sorted_cats:
        pct = share * 100
        saving_kg = results[cat] * 0.20  # %20 azaltım senaryosu varsayımı
        saving_ton = saving_kg / 1000

        # Payı çok az olan kategoriler için (örn. %10'dan küçük) ve
        # zaten birkaç öneri yazmışsak çıkabiliriz.
        if pct < 10 and len(recommendations) >= 3:
            break

        if cat == "transport":
            text = (
                f"**Ulaşım**, toplam karbon ayak izinin yaklaşık **%{pct:.0f}**'ini oluşturuyor. "
                f"Arabayı daha az kullanıp toplu taşıma, yürüyüş veya bisiklete yönelerek ulaşımdan kaynaklı "
                f"emisyonunu sadece **%20 azaltman**, yılda yaklaşık "
                f"**{saving_kg:.0f} kg ({saving_ton:.2f} ton) CO₂** tasarrufu sağlayabilir."
            )
        elif cat == "energy":
            text = (
                f"**Ev enerjisi (elektrik/doğalgaz)** ayak izin içinde yaklaşık **%{pct:.0f}** paya sahip. "
                f"LED ampullere geçiş, gereksiz ışıkları kapatma ve ısıtma derecesini 1°C düşürme gibi adımlarla "
                f"enerji kaynaklı emisyonunu **%20 azaltman**, yılda yaklaşık "
                f"**{saving_kg:.0f} kg ({saving_ton:.2f} ton) CO₂** düşüş anlamına gelir."
            )
        elif cat == "water":
            text = (
                f"**Su kullanımı**, toplam emisyonunun yaklaşık **%{pct:.0f}**’ini oluşturuyor. "
                f"Daha kısa duşlar, damlatan muslukları onarma ve su verimli cihazlar kullanarak bu alanda "
                f"**%20 iyileşme** sağlaman, yılda yaklaşık "
                f"**{saving_kg:.0f} kg ({saving_ton:.2f} ton) CO₂** tasarrufu demektir."
            )
        elif cat == "food":
            text = (
                f"**Beslenme (özellikle kırmızı et tüketimi)** karbon ayak izinin yaklaşık **%{pct:.0f}**’ini oluşturuyor. "
                f"Haftada birkaç öğünü bitki temelli tercih edip kırmızı et tüketimini azaltarak bu kategoride "
                f"**%20 azalma** sağlaman, yılda yaklaşık "
                f"**{saving_kg:.0f} kg ({saving_ton:.2f} ton) CO₂** azaltımı sağlayabilir."
            )
        elif cat == "waste":
            text = (
                f"**Atık ve geri dönüşüm**, toplam emisyonunun yaklaşık **%{pct:.0f}**’ini oluşturuyor. "
                f"Geri dönüşüm oranını artırıp tek kullanımlık ürünlerden kaçınarak bu alanda "
                f"**%20 iyileşme** sağlaman, yılda yaklaşık "
                f"**{saving_kg:.0f} kg ({saving_ton:.2f} ton) CO₂** tasarrufu anlamına gelir."
            )
        else:
            continue

        recommendations.append(text)

    # Eğer bir şekilde hiç öneri oluşmadıysa genel bir öneri dönelim
    if not recommendations:
        recommendations.append(
            "Karbon ayak izin oldukça dengeli görünse de, özellikle **ulaşım, elektrik tüketimi ve kırmızı et** "
            "alanlarında küçük iyileştirmelerle toplam emisyonunu anlamlı ölçüde azaltabilirsin."
        )

    return recommendations