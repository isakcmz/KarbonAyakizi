import streamlit as st


def page_home():
    st.markdown(
        '<div class="section-label">Sürdürülebilir Yaşam Asistanı</div>',
        unsafe_allow_html=True,
    )

    # Başlık ve dünya ikonunu iki kolona bölelim
    col_title, col_icon = st.columns([5, 1])
    with col_title:
        st.title("Karbon Ayak İzi Hesaplama ve Azaltım Senaryosu Sistemi")
    with col_icon:
        st.markdown(
            "<div style='font-size:3rem; text-align:right; margin-top:0.2rem;'>🌍</div>",
            unsafe_allow_html=True,
        )

    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.markdown(
            """
            <div class="info-card">
                <h3>Günlük alışkanlıklarının iklim üzerindeki etkisini gör.</h3>
                <p>
                Ulaşım, enerji, su tüketimi, beslenme ve atık üretimini girerek
                yıllık karbon ayak izini hesapla. Farklı senaryolar deneyerek,
                küçük değişikliklerle ne kadar CO₂ azaltabileceğini keşfet.
                </p>
                <p style="font-size:0.85rem;opacity:0.85;">
                Bu uygulama, sosyal sorumluluk kapsamında bireysel farkındalık oluşturmak için tasarlanmış
                interaktif bir simülasyon sistemidir.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("### Başlamak için 3 adım:")
        st.markdown(
            "- 🔹 Soldan **Veri Girişi** menüsüne tıkla\n"
            "- 🔹 Her sekmede temel bilgilerini gir\n"
            "- 🔹 **Sonuç & Analiz** bölümünde yıllık karbon ayak izini gör"
        )

        st.markdown("#### Kategoriler")
        st.markdown(
            """
            <div class="badge-row">
                <div class="badge">🚗 Ulaşım</div>
                <div class="badge">💡 Ev Enerjisi</div>
                <div class="badge">💧 Su Kullanımı</div>
                <div class="badge">🍽 Beslenme</div>
                <div class="badge">🗑 Atık & Geri Dönüşüm</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_right:
        st.markdown(
            """
            <div class="info-card">
                <h3>Bu sistemle neler görebilirsin?</h3>
                <p>• Yıllık toplam karbon ayak izin (ton CO₂)</p>
                <p>• Hangi kategori ne kadar paya sahip?</p>
                <p>• Et tüketimi, araba kullanımı, elektrik ve suyun etkisi</p>
                <p>• Senaryolar ile <b>önce/sonra</b> karşılaştırma</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(" ")
        st.info(
            "👉 Başlamak için sol menüden **Veri Girişi**'ni seç. "
            "Verileri girdikten sonra **Sonuç & Analiz** sayfasında detaylı grafikleri görebilirsin."
        )
