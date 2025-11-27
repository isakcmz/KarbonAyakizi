# logic/sustainability_score.py

"""
Kullanıcının karbon ayak izi verilerine göre
0-100 arası bir sürdürülebilirlik skoru hesaplar.
"""

def compute_sustainability_score(results: dict) -> dict:
    """
    results: calc_total_co2() çıktısı

    Dönen:
    {
        "score": int,
        "level": "excellent/good/medium/low",
        "message": "..."
    }
    """
    transport = results.get("transport", 0)
    energy = results.get("energy", 0)
    water = results.get("water", 0)
    food = results.get("food", 0)
    waste = results.get("waste", 0)
    total = results.get("total", 0)

    if total <= 0:
        return {
            "score": 0,
            "level": "low",
            "message": "Veri girilmediği için skor hesaplanamadı."
        }

    # Her kategoriden yüzdesel pay
    shares = {
        "transport": transport / total,
        "energy": energy / total,
        "water": water / total,
        "food": food / total,
        "waste": waste / total,
    }

    score = 100

    # Ulaşım
    if shares["transport"] > 0.40:
        score -= 30
    elif shares["transport"] > 0.25:
        score -= 15
    elif shares["transport"] < 0.10:
        score += 5

    # Enerji
    if shares["energy"] > 0.30:
        score -= 20
    elif shares["energy"] < 0.10:
        score += 5

    # Su
    if shares["water"] > 0.15:
        score -= 10
    elif shares["water"] < 0.05:
        score += 5

    # Beslenme (özellikle et tüketimi)
    if shares["food"] > 0.30:
        score -= 20
    elif shares["food"] < 0.15:
        score += 5

    # Atık
    if shares["waste"] > 0.15:
        score -= 10
    elif shares["waste"] < 0.05:
        score += 5

    # Skoru sınırlayalım
    score = max(0, min(100, score))

    # Seviye belirleme
    if score >= 85:
        level = "excellent"
        message = "Harika! Yaşam tarzın oldukça sürdürülebilir. 🌿"
    elif score >= 65:
        level = "good"
        message = "İyi durumdasın! Birkaç küçük değişiklikle mükemmel olabilirsin. 🙂"
    elif score >= 45:
        level = "medium"
        message = "Orta seviyedesin. Bazı alışkanlıkları iyileştirebilirsin. 🔍"
    else:
        level = "low"
        message = "Sürdürülebilirlik seviyen düşük. Ulaşım, enerji ve beslenme tarafına özellikle dikkat etmelisin. ⚠️"

    return {
        "score": score,
        "level": level,
        "message": message
    }
