from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import datetime

def generate_pdf(filename: str):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    c.setFont("Helvetica-Bold", 16)
    c.drawString(1*inch, height-1*inch, "CloudNavigator Migration Plan")
    c.setFont("Helvetica", 12)
    c.drawString(1*inch, height-1.5*inch, f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
    c.drawString(1*inch, height-2*inch, "Runbook & Cost Comparison attached.")
    c.save()
