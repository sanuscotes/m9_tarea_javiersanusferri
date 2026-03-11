from reportlab.pdfgen import canvas


def create_pdf():

    c = canvas.Canvas("performance_report.pdf")

    c.drawString(100, 750, "Performance Dashboard Report")

    c.drawString(100, 720, "Generated from Dash App")

    c.save()