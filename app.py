import streamlit as st

from styles import inject_custom_css
from logic.state import init_session_state

from modules.home import page_home
from modules.input_page import page_input
from modules.results_page import page_results
from modules.scenario_page import page_scenarios
from modules.about_page import page_about
from modules.saved_scenarios_page import page_saved_scenarios


def main():
    st.set_page_config(
        page_title="Karbon Ayak İzi Hesaplama",
        page_icon="🌱",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Tasarım CSS
    inject_custom_css()

    # İlk açılışta session_state'i hazırla
    init_session_state()

    # Sol taraftaki menü – ikonlu
    menu_labels = {
        "🏠 Anasayfa": "Anasayfa",
        "📝 Veri Girişi": "Veri Girişi",
        "📊 Sonuç & Analiz": "Sonuç & Analiz",
        "🔄 Azaltım Senaryoları": "Azaltım Senaryoları",
        "🗂 Kaydedilen Senaryolar": "Kaydedilen Senaryolar",
        "ℹ️ Hakkında": "Hakkında",
    }

    choice = st.sidebar.radio("Menü", options=list(menu_labels.keys()))
    menu = menu_labels[choice]

    # Menüden SONRA açıklama kartı
    st.sidebar.markdown(
        """
        <div class="sidebar-card">
            <p class="sidebar-card-title">🌱 Karbon Asistanı</p>
            <p class="sidebar-card-sub">
                Günlük alışkanlıklarını gir, yıllık karbon ayak izini ve
                azaltım senaryolarını keşfet.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Sayfa yönlendirme
    if menu == "Anasayfa":
        page_home()
    elif menu == "Veri Girişi":
        page_input()
    elif menu == "Sonuç & Analiz":
        page_results()
    elif menu == "Azaltım Senaryoları":
        page_scenarios()
    elif menu == "Kaydedilen Senaryolar":
        page_saved_scenarios()    
    elif menu == "Hakkında":
        page_about()


if __name__ == "__main__":
    main()
