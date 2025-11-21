import streamlit as st


def page_input():
    st.markdown('<div class="section-label">Adım 1</div>', unsafe_allow_html=True)
    st.title("Veri Girişi – Günlük Alışkanlıkların")

    st.write(
        "Aşağıdaki sekmelerde günlük/haftalık/aylık alışkanlıklarını gir. "
        "Bu bilgiler sadece **yıllık CO₂ hesabı** için kullanılacak, herhangi bir yere kaydedilmeyecektir."
    )

    st.markdown("---")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["🚗 Ulaşım", "💡 Enerji", "💧 Su", "🍽 Beslenme", "🗑 Atık"]
    )

    # -------------------------
    # 1) ULAŞIM
    # -------------------------
    with tab1:
        st.subheader("Ulaşım Alışkanlıkları")

        st.info(
            "Araba, toplu taşıma ve uçak yolculukların; karbon ayak izinin önemli bir kısmını oluşturur. "
            "Buradaki değerler yıllık km/saat hesabına dönüştürülerek CO₂'ye çevrilecektir."
        )

        use_car = st.checkbox(
            "Araba kullanıyorum",
            value=st.session_state["transport"].get("use_car", False),
        )
        st.session_state["transport"]["use_car"] = use_car

        if use_car:
            col1, col2 = st.columns(2)
            with col1:
                car_type = st.selectbox(
                    "Araç tipi",
                    options=["petrol", "diesel", "hybrid", "ev"],
                    format_func=lambda x: {
                        "petrol": "Benzinli",
                        "diesel": "Dizel",
                        "hybrid": "Hibrit",
                        "ev": "Elektrikli",
                    }[x],
                    index=["petrol", "diesel", "hybrid", "ev"].index(
                        st.session_state["transport"].get("car_type", "petrol")
                    ),
                )
                st.session_state["transport"]["car_type"] = car_type

            with col2:
                days_per_week = st.number_input(
                    "Haftada kaç gün araba kullanıyorsun?",
                    min_value=0,
                    max_value=7,
                    value=int(
                        st.session_state["transport"].get("car_days_per_week", 5)
                    ),
                    step=1,
                )
                st.session_state["transport"]["car_days_per_week"] = days_per_week

            daily_km = st.number_input(
                "Bu günlerde ortalama kaç km yol yapıyorsun? (günlük)",
                min_value=0.0,
                value=float(
                    st.session_state["transport"].get("car_daily_km", 0.0)
                ),
                step=1.0,
            )
            st.session_state["transport"]["car_daily_km"] = daily_km

        st.markdown("##### Toplu Taşıma ve Uçak")

        col_bus, col_metro = st.columns(2)
        with col_bus:
            bus_km = st.number_input(
                "Haftalık otobüs kullanımı (km)",
                min_value=0.0,
                value=float(
                    st.session_state["transport"].get("bus_km_per_week", 0.0)
                ),
                step=1.0,
            )
        with col_metro:
            metro_km = st.number_input(
                "Haftalık metro/tren kullanımı (km)",
                min_value=0.0,
                value=float(
                    st.session_state["transport"].get("metro_km_per_week", 0.0)
                ),
                step=1.0,
            )

        plane_hours = st.number_input(
            "Yılda uçak yolculuğu süresi (saat)",
            min_value=0.0,
            value=float(
                st.session_state["transport"].get("plane_hours_per_year", 0.0)
            ),
            step=1.0,
        )

        st.session_state["transport"]["bus_km_per_week"] = bus_km
        st.session_state["transport"]["metro_km_per_week"] = metro_km
        st.session_state["transport"]["plane_hours_per_year"] = plane_hours

    # -------------------------
    # 2) ENERJİ
    # -------------------------
    with tab2:
        st.subheader("Ev Enerjisi (Elektrik + Isınma)")

        st.info(
            "Evde tükettiğin elektrik ve ısınma (doğalgaz vb.), enerji kaynaklı karbon ayak izini oluşturur. "
            "Buradaki değerler aylıktan yıllığa çevrilir."
        )

        col1, col2 = st.columns(2)
        with col1:
            monthly_kwh = st.number_input(
                "Aylık elektrik tüketimi (kWh)",
                min_value=0.0,
                value=float(
                    st.session_state["energy"].get(
                        "electricity_kwh_per_month", 200
                    )
                ),
                step=10.0,
            )
        with col2:
            gas_m3 = st.number_input(
                "Aylık doğalgaz tüketimi (m³)",
                min_value=0.0,
                value=float(
                    st.session_state["energy"].get("gas_m3_per_month", 0)
                ),
                step=5.0,
            )

        st.session_state["energy"]["electricity_kwh_per_month"] = monthly_kwh
        st.session_state["energy"]["gas_m3_per_month"] = gas_m3

    # -------------------------
    # 3) SU
    # -------------------------
    with tab3:
        st.subheader("Su Kullanımı")

        st.info(
            "Su tüketimi; arıtma, pompalama ve dağıtım süreçleri nedeniyle enerji harcar ve CO₂ emisyonu oluşturur."
        )

        water_m3 = st.number_input(
            "Aylık su tüketimi (m³)",
            min_value=0.0,
            value=float(
                st.session_state["water"].get("water_m3_per_month", 10)
            ),
            step=1.0,
        )

        st.session_state["water"]["water_m3_per_month"] = water_m3

    # -------------------------
    # 4) BESLENME
    # -------------------------
    with tab4:
        st.subheader("Beslenme Alışkanlıkları (Haftalık)")

        st.info(
            "Özellikle kırmızı et tüketimi, gıda kaynaklı karbon ayak izinin en büyük kalemlerinden biridir. "
            "Haftalık tüketimini yaklaşık olarak yazman yeterli."
        )

        col1, col2 = st.columns(2)
        with col1:
            beef = st.number_input(
                "Kırmızı et tüketimi (kg/hafta)",
                min_value=0.0,
                max_value=10.0,
                value=float(
                    st.session_state["food"].get("beef_kg_per_week", 0.5)
                ),
                step=0.1,
            )
            veg = st.number_input(
                "Sebze/meyve tüketimi (kg/hafta)",
                min_value=0.0,
                max_value=50.0,
                value=float(
                    st.session_state["food"].get("veg_kg_per_week", 2.0)
                ),
                step=0.5,
            )
        with col2:
            chicken = st.number_input(
                "Beyaz et (tavuk/balık) tüketimi (kg/hafta)",
                min_value=0.0,
                max_value=10.0,
                value=float(
                    st.session_state["food"].get(
                        "chicken_kg_per_week", 0.5
                    )
                ),
                step=0.1,
            )
            dairy = st.number_input(
                "Süt ürünleri tüketimi (kg/hafta)",
                min_value=0.0,
                max_value=20.0,
                value=float(
                    st.session_state["food"].get("dairy_kg_per_week", 1.0)
                ),
                step=0.5,
            )

        st.session_state["food"]["beef_kg_per_week"] = beef
        st.session_state["food"]["chicken_kg_per_week"] = chicken
        st.session_state["food"]["veg_kg_per_week"] = veg
        st.session_state["food"]["dairy_kg_per_week"] = dairy

    # -------------------------
    # 5) ATIK
    # -------------------------
    with tab5:
        st.subheader("Atık & Geri Dönüşüm")

        st.info(
            "Çöplerin depolanması ve yakılması da karbon salınımına neden olur. "
            "Geri dönüşüm seviyesi arttıkça, bu etki azalır."
        )

        weekly_waste = st.number_input(
            "Haftalık karışık çöp miktarı (kg)",
            min_value=0.0,
            value=float(
                st.session_state["waste"].get(
                    "mixed_waste_kg_per_week", 5.0
                )
            ),
            step=0.5,
        )

        recycle_level = st.selectbox(
            "Geri dönüşüm seviyesi",
            options=["none", "partial", "high"],
            format_func=lambda x: {
                "none": "Hiç geri dönüşüm yapmıyorum",
                "partial": "Bazen geri dönüşüm yapıyorum",
                "high": "Düzenli geri dönüşüm yapıyorum",
            }[x],
            index=["none", "partial", "high"].index(
                st.session_state["waste"].get("recycle_level", "none")
            ),
        )

        st.session_state["waste"]["mixed_waste_kg_per_week"] = weekly_waste
        st.session_state["waste"]["recycle_level"] = recycle_level

    st.success(
        "Veriler kaydedildi. Soldan **Sonuç & Analiz** sayfasına geçerek hesabı görebilirsin."
    )
