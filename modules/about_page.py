import streamlit as st


def page_about():
    st.title("Hakkında")
    st.write(
        """
Bu proje, **Sosyal Sorumluluk** dersi kapsamında geliştirilmiş bir
**Sürdürülebilir Çevre Teknolojileri** uygulamasıdır.

Amaç, bireylerin günlük yaşam alışkanlıklarının iklim değişikliği
üzerindeki etkisini somut hâle getirmek ve farkındalık oluşturmaktır.

Hesaplamalarda kullanılan emisyon katsayıları; IPCC, Avrupa Çevre Ajansı (EEA)
ve çeşitli açık veri kaynaklarında belirtilen ortalama değerlere dayanmaktadır.
        """
    )
    st.markdown("**Tema:** Sürdürülebilir Çevre – Karbon Ayak İzi")
    st.markdown("**Teknoloji:** Python + Streamlit (Web Uygulaması)")
