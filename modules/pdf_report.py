from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from datetime import datetime

def generate_pdf_report(filename, report_text):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rigthMargin=40,
        lefMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    story = []

    title = "<b>OSINT REPORT</b>"
    date = f"<i>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}</i>"

    story.append(Paragraph(title, styles["Title"]))
    story.append(Spacer(1, 20))
    story.append(Paragraph(date, styles["Normal"]))
    story.append(Spacer(1, 30))

    for line in report_text.split("\n"):
        if line.strip():
            story.append(Paragraph(line, styles["Normal"]))
            story.append(Spacer(1, 6))
    
    doc.build(story)