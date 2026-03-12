# Importación de librerías para generar el pdf
from reportlab.pdfgen import canvas

# Función para crear el pdf
def create_pdf():
    """
    Genera un archivo PDF simple que actúa como reporte del dashboard.

    Descripción
    -----------
    Esta función crea un documento PDF utilizando la librería ReportLab 
    y escribe en él un pequeño contenido de ejemplo.

    Resultado
    ---------
    Se genera el archivo: performance_report.pdf en el directorio donde se ejecuta el script.
    """
    # Crea el objeto Canvas que representará el documento PDF
    c = canvas.Canvas("performance_report.pdf")

    # Escribe el título principal del reporte en la coordenada (100, 750)
    c.drawString(100, 750, "Performance Dashboard Report")

    # Escribe una segunda línea de texto que describe el origen del reporte
    c.drawString(100, 720, "Generated from Dash App")

    # Guarda el archivo PDF generado
    c.save()