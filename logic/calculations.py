import streamlit as st

from logic.load_factors import load_factors

# Emisyon katsayılarını yükle
FACTORS = load_factors()


def calc_transport_co2(data: dict) -> float:
    """Ulaşım kaynaklı yıllık CO2 hesabı (kg)."""
    total = 0.0

    # Araba
    if data.get("use_car"):
        car_type = data.get("car_type", "petrol")
        daily_km = data.get("car_daily_km", 0)
        days_per_week = data.get("car_days_per_week", 0)
        yearly_km = daily_km * days_per_week * 52  # 52 hafta
        factor_key = f"car_{car_type}_kg_per_km"
        factor = FACTORS.get(factor_key, 0)
        total += yearly_km * factor

    # Otobüs
    bus_km_per_week = data.get("bus_km_per_week", 0)
    total += bus_km_per_week * 52 * FACTORS["bus_kg_per_km"]

    # Metro
    metro_km_per_week = data.get("metro_km_per_week", 0)
    total += metro_km_per_week * 52 * FACTORS["metro_kg_per_km"]

    # Uçak
    plane_hours_per_year = data.get("plane_hours_per_year", 0)
    total += plane_hours_per_year * FACTORS["plane_kg_per_hour"]

    return total


def calc_energy_co2(data: dict) -> float:
    """Elektrik + doğalgaz kaynaklı yıllık CO2 (kg)."""
    total = 0.0

    monthly_kwh = data.get("electricity_kwh_per_month", 0)
    renewable_pct = data.get("renewable_pct", 0)  # YENİ
    renewable_ratio = renewable_pct / 100

    # Elektrik: yenilenebilir kısmı 0 kabul edilir
    yearly_kwh = monthly_kwh * 12
    base_elec = yearly_kwh * FACTORS["electricity_kg_per_kwh"]
    adj_elec = base_elec * (1 - renewable_ratio)

    total += adj_elec

    monthly_gas_m3 = data.get("gas_m3_per_month", 0)
    total += monthly_gas_m3 * 12 * FACTORS["natural_gas_kg_per_m3"]

    return total


def calc_water_co2(data: dict) -> float:
    """Su tüketimi kaynaklı yıllık CO2 (kg)."""
    monthly_m3 = data.get("water_m3_per_month", 0)
    return monthly_m3 * 12 * FACTORS["water_kg_per_m3"]


def calc_food_co2(data: dict) -> float:
    """Beslenme kaynaklı yıllık CO2 (kg)."""
    total = 0.0

    beef_kg = data.get("beef_kg_per_week", 0)
    chicken_kg = data.get("chicken_kg_per_week", 0)
    veg_kg = data.get("veg_kg_per_week", 0)
    dairy_kg = data.get("dairy_kg_per_week", 0)

    total += beef_kg * 52 * FACTORS["beef_kg_per_kg"]
    total += chicken_kg * 52 * FACTORS["chicken_kg_per_kg"]
    total += veg_kg * 52 * FACTORS["vegetable_kg_per_kg"]
    total += dairy_kg * 52 * FACTORS["dairy_kg_per_kg"]

    return total


def calc_waste_co2(data: dict) -> float:
    """Atık & geri dönüşüm kaynaklı yıllık CO2 (kg)."""
    weekly_kg = data.get("mixed_waste_kg_per_week", 0)
    recycle_level = data.get("recycle_level", "none")  # none / partial / high

    yearly_kg = weekly_kg * 52
    base_emission = yearly_kg * FACTORS["waste_mixed_kg_per_kg"]

    # Geri dönüşümle sağlanan tasarruf
    if recycle_level == "partial":
        saving = yearly_kg * 0.3 * FACTORS["waste_recycled_saving_kg_per_kg"]
    elif recycle_level == "high":
        saving = yearly_kg * 0.6 * FACTORS["waste_recycled_saving_kg_per_kg"]
    else:
        saving = 0.0

    total = base_emission - saving
    return max(total, 0)


def calc_total_co2():
    """
    session_state içindeki tüm kategorilerden
    yıllık toplam CO2 (kg) değerlerini hesaplar.
    """
    t = calc_transport_co2(st.session_state["transport"])
    e = calc_energy_co2(st.session_state["energy"])
    w = calc_water_co2(st.session_state["water"])
    f = calc_food_co2(st.session_state["food"])
    wa = calc_waste_co2(st.session_state["waste"])

    return {
        "transport": t,
        "energy": e,
        "water": w,
        "food": f,
        "waste": wa,
        "total": t + e + w + f + wa,
    }
