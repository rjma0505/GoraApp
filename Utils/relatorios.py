import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def exportar_excel(df: pd.DataFrame, path: str):
    df.to_excel(path, index=False)

def exportar_pdf(df: pd.DataFrame, path: str):
    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4
    x, y = 40, height - 40

    # Cabeçalhos
    for col in df.columns:
        c.drawString(x, y, col)
        x += 100
    y -= 20
    x = 40

    # Linhas
    for _, row in df.iterrows():
        for value in row:
            c.drawString(x, y, str(value))
            x += 100
        y -= 20
        x = 40
        if y < 40:
            c.showPage()
            y = height - 40
    c.save()
