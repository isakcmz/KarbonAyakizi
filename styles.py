import streamlit as st


def inject_custom_css():
    st.markdown(
        """
        <style>

        /* GENEL ARKA PLAN (Mint Theme) */
        .stApp {
            background: linear-gradient(135deg, #ccfbf1, #f0fdfa);
            color: #1e293b;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        }

        /* ANA BLOK (Container Kart Tasarımı) */
        .block-container {
            max-width: 1100px;
            padding-top: 1.5rem !important;
            padding-bottom: 3rem !important;
            padding-left: 2.5rem !important;
            padding-right: 2.5rem !important;
            background: rgba(255, 255, 255, 0.75);
            backdrop-filter: blur(6px);
            border-radius: 18px;
            box-shadow: 0 12px 28px rgba(0,0,0,0.15);
            border: 1px solid rgba(203,213,225,0.6);
        }

        /* SIDEBAR (Mint uyumlu) */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #ccfbf1, #f0fdfa);
            border-right: 1px solid rgba(148,163,184,0.45);
        }
        section[data-testid="stSidebar"] * {
            color: #065f46 !important;
            font-weight: 500;
        }

        /* BAŞLIKLAR */
        h1 {
            font-size: 2.0rem !important;
            font-weight: 800 !important;
            background: -webkit-linear-gradient(#10b981, #047857);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        h2, h3 {
            font-weight: 700 !important;
            color: #065f46 !important;
        }

        /* ROZETLER */
        .badge-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-top: 0.75rem;
        }
        .badge {
            padding: 0.25rem 0.6rem;
            border-radius: 999px;
            background: #d1fae5;
            border: 1px solid #6ee7b7;
            color: #047857;
            font-size: 0.8rem;
            display: inline-flex;
            align-items: center;
            gap: 0.25rem;
        }

        /* KART TASARIMI */
        .info-card {
            background: #ffffffee;
            border-radius: 16px;
            padding: 1.1rem 1.3rem;
            border: 1px solid #e2e8f0;
            box-shadow: 0 8px 18px rgba(0,0,0,0.12);
        }
        .info-card h3 {
            margin-top: 0;
            margin-bottom: 0.3rem;
            color: #047857;
        }

        /* ALERT BOX */
        .stAlert {
            border-radius: 12px;
            border: 1px solid rgba(148,163,184,0.6);
            background: rgba(240, 253, 244, 0.85);
            color: #065f46 !important;
        }

        /* METRIC KARTLARI */
        div[data-testid="stMetric"] {
            background: #ffffffdd;
            border-radius: 14px;
            padding: 0.9rem 0.9rem;
            border: 1px solid rgba(148,163,184,0.45);
            box-shadow: 0 6px 15px rgba(0,0,0,0.10);
            color: #065f46 !important;
        }

        /* SEKMELER (Mint Tema) */
        button[role="tab"] {
            border-radius: 999px !important;
            padding: 0.5rem 1rem !important;
            background: #ecfdf5 !important;   
            color: #047857 !important;
            border: 1px solid #a7f3d0 !important;
        }
        button[role="tab"][aria-selected="true"] {
            background: #10b981 !important;
            color: white !important;
            border: none !important;
        }

        /* HEADER (Şeffaf, temiz) */
        header[data-testid="stHeader"] {
            background: transparent !important;
            box-shadow: none !important;
        }

        /* DEPLOY - MENU - SETTINGS gizle */
        #MainMenu {
            visibility: hidden;
        }

        /* --- SIDEBAR BAŞLIK KARTI --- */
        .sidebar-card {
            background: #ffffffcc;
            border-radius: 14px;
            padding: 0.9rem 1rem;
            margin-bottom: 1rem;
            border: 1px solid #a7f3d0;
            box-shadow: 0 4px 10px rgba(15,23,42,0.12);
        }
        .sidebar-card-title {
            margin: 0;
            font-size: 1.0rem;
            font-weight: 700;
            color: #065f46;
        }
        .sidebar-card-sub {
            margin: 0.2rem 0 0;
            font-size: 0.8rem;
            color: #047857;
        }

        /* RADIO MENÜ – Mint hover */
        section[data-testid="stSidebar"] .stRadio > div {
            gap: 0.35rem;
        }

        section[data-testid="stSidebar"] div[role="radiogroup"] > label {
            padding: 0.35rem 0.75rem;
            border-radius: 999px;
            margin-bottom: 0.2rem;
            transition: all 0.15s ease-in-out;
            cursor: pointer;
            border: 1px solid transparent;
        }

        section[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
            background: #ccfbf1;
            border-color: #6ee7b7;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )
