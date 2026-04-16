---
name: documents
description: Create professional DOCX, PDF, Excel and Markdown documents programmatically
---

# Documents — Professional Document Creation

## DOCX via python-docx
```python
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

def create_report(title: str, sections: list, output_path: str):
    doc = Document()

    # Title
    title_para = doc.add_heading(title, 0)
    title_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Sections
    for section in sections:
        doc.add_heading(section["title"], level=1)

        for paragraph in section.get("paragraphs", []):
            doc.add_paragraph(paragraph)

        if "table" in section:
            table_data = section["table"]
            table = doc.add_table(rows=len(table_data), cols=len(table_data[0]))
            table.style = 'Table Grid'
            for i, row in enumerate(table_data):
                for j, cell_text in enumerate(row):
                    table.cell(i, j).text = str(cell_text)

        if "bullets" in section:
            for bullet in section["bullets"]:
                doc.add_paragraph(bullet, style='List Bullet')

        if "code" in section:
            p = doc.add_paragraph(section["code"])
            p.style.font.name = 'Courier New'
            p.style.font.size = Pt(10)

    doc.save(output_path)
    return output_path

# Usage
sections = [
    {
        "title": "Resumen Ejecutivo",
        "paragraphs": ["Este informe presenta los resultados del análisis..."],
    },
    {
        "title": "Datos Clave",
        "table": [
            ["Métrica", "Valor", "Cambio"],
            ["Usuarios", "12,847", "+12%"],
            ["Ingresos", "€45,200", "+8%"],
        ],
    },
    {
        "title": "Conclusiones",
        "bullets": ["Crecimiento sostenido en Q1", "Reducción de costos operativos"],
    },
]
create_report("Informe Mensual", sections, "informe.docx")
```

## PDF Generation via ReportLab
```python
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import cm

def create_pdf(title: str, content: list, output_path: str):
    doc = SimpleDocTemplate(output_path, pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)

    styles = getSampleStyleSheet()
    PRIMARY = HexColor('#6750A4')

    title_style = ParagraphStyle('Title', parent=styles['Title'],
                                  textColor=PRIMARY, fontSize=24)
    story = [Paragraph(title, title_style), Spacer(1, 0.5*cm)]

    for item in content:
        if item["type"] == "heading":
            story.append(Paragraph(item["text"], styles['Heading1']))
        elif item["type"] == "paragraph":
            story.append(Paragraph(item["text"], styles['Normal']))
        elif item["type"] == "table":
            t = Table(item["data"])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), PRIMARY),
                ('TEXTCOLOR', (0,0), (-1,0), HexColor('#FFFFFF')),
                ('GRID', (0,0), (-1,-1), 0.5, HexColor('#E8DEF8')),
                ('ROWBACKGROUNDS', (0,1), (-1,-1), [HexColor('#FEF7FF'), HexColor('#FFFFFF')]),
            ]))
            story.append(t)
        story.append(Spacer(1, 0.3*cm))

    doc.build(story)
    return output_path
```

## Excel via openpyxl
```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.chart import BarChart, Reference

def create_spreadsheet(data: dict, output_path: str):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = data.get("sheet_name", "Datos")

    # Header row with styling
    headers = data["headers"]
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill(fill_type="solid", fgColor="6750A4")
        cell.alignment = Alignment(horizontal="center")
        ws.column_dimensions[cell.column_letter].width = 15

    # Data rows
    for row_idx, row_data in enumerate(data["rows"], 2):
        for col_idx, value in enumerate(row_data, 1):
            ws.cell(row=row_idx, column=col_idx, value=value)

    # Add chart if requested
    if data.get("chart"):
        chart = BarChart()
        chart.title = data["chart"].get("title", "Gráfico")
        chart.y_axis.title = data["chart"].get("y_label", "Valor")
        chart.x_axis.title = data["chart"].get("x_label", "Categoría")
        data_ref = Reference(ws, min_col=2, min_row=1,
                             max_row=len(data["rows"]) + 1)
        cats = Reference(ws, min_col=1, min_row=2,
                         max_row=len(data["rows"]) + 1)
        chart.add_data(data_ref, titles_from_data=True)
        chart.set_categories(cats)
        ws.add_chart(chart, "E2")

    wb.save(output_path)
    return output_path
```

## Markdown to HTML
```python
import markdown
import re

def md_to_html(md_content: str, title: str = "Document") -> str:
    html_body = markdown.markdown(md_content, extensions=[
        'tables', 'fenced_code', 'codehilite', 'toc', 'nl2br'
    ])
    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>{title}</title>
<link href="https://cdn.jsdelivr.net/npm/beercss@3/dist/cdn/beer.min.css" rel="stylesheet">
</head><body><main class="responsive padding">{html_body}</main></body></html>"""
```
