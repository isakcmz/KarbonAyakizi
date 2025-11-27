# logic/report_generator.py

from fpdf import FPDF
from datetime import datetime
import tempfile
from typing import Dict, List, Optional


# -------------------------------------------------
# Yardımcı: Türkçe karakterleri Latin-1 uyumlu hale getir
# -------------------------------------------------
def _latinize(text: str) -> str:
    """
    FPDF varsayılan olarak Latin-1 kullandığı için,
    Türkçe karakterleri en yakın İngilizce karşılıklarına çeviriyoruz.
    Ayrıca CO₂ gibi karakterleri de CO2 yapıyoruz.
    """
    if text is None:
        return ""

    mapping = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")
    t = str(text).translate(mapping)
    t = t.replace("CO₂", "CO2").replace("°", " derece")
    return t


class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.set_text_color(0, 100, 0)
        # Başlıkta Türkçe karakter kullanmıyoruz
        self.cell(0, 10, _latinize("Karbon Ayak Izi Raporu"), 0, 1, "C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, _latinize(f"Sayfa {self.page_no()}"), 0, 0, "C")


def create_pdf_report(
    results: Dict[str, float],
    scenario: Optional[Dict[str, float]] = None,
    chart_paths: Optional[List[str]] = None,
) -> str:
    """
    Sonuc verilerinden basit bir PDF olusturur ve
    gecici bir dosya yolu dondurur.
    """
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # --- Rapor Tarihi ---
    pdf.set_font("Arial", "", 11)
    pdf.set_text_color(0, 80, 0)
    pdf.multi_cell(
        0,
        8,
        _latinize(f"Rapor Tarihi: {datetime.now().strftime('%Y-%m-%d %H:%M')}"),
    )
    pdf.ln(5)

    # --- Toplam CO2 ---
    pdf.set_font("Arial", "B", 12)
    pdf.set_text_color(0, 60, 0)
    pdf.cell(0, 10, _latinize("Yillik Toplam Karbon Ayak Izi"), 0, 1)

    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(
        0,
        8,
        _latinize(f"Toplam CO2: {results.get('total', 0) / 1000:.2f} ton/yil"),
    )
    pdf.ln(3)

    # --- Kategorilere gore dagilim ---
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, _latinize("Kategorilere Gore Dagilim"), 0, 1)

    pdf.set_font("Arial", "", 11)
    labels = {
        "transport": "Ulasim",
        "energy": "Enerji",
        "water": "Su",
        "food": "Beslenme",
        "waste": "Atik",
    }
    for key, label in labels.items():
        value = results.get(key, 0.0)
        pdf.multi_cell(0, 8, _latinize(f"{label}: {value:.1f} kg/yil"))

    pdf.ln(5)

    # --- Grafik Gorselleri (istege bagli) ---
    if chart_paths:
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, _latinize("Grafikler"), 0, 1)

        for img_path in chart_paths:
            try:
                pdf.image(img_path, w=170)
                pdf.ln(5)
            except Exception:
                # Gorsel okunamazsa sessizce atla
                continue

    # --- Senaryo bilgisi (varsa) ---
    if scenario is not None:
        pdf.add_page()
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, _latinize("Senaryo Karsilastirmasi"), 0, 1)

        pdf.set_font("Arial", "", 11)
        base_total = scenario.get("base_total", 0.0)
        new_total = scenario.get("new_total", 0.0)
        diff = base_total - new_total

        txt = (
            f"Mevcut: {base_total / 1000:.2f} ton/yil\n"
            f"Senaryo: {new_total / 1000:.2f} ton/yil\n"
            f"Azalma: {diff / 1000:.2f} ton/yil"
        )
        pdf.multi_cell(0, 8, _latinize(txt))

    # --- PDF gecici dosyaya yaziliyor ---
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        pdf.output(tmp_file.name)
        return tmp_file.name
