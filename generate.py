from reportlab.graphics.barcode import createBarcodeDrawing,code39, code128, code93
from reportlab.graphics.shapes import Drawing
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm, inch
from reportlab.pdfgen import canvas
from reportlab.graphics import renderPDF
from reportlab.platypus import Paragraph, Frame, KeepInFrame
from reportlab.pdfbase.pdfmetrics import stringWidth
from collections import defaultdict
import json
from pprint import pprint
with open('label.json') as data_file:
    data = json.load(data_file)
inch_point_ratio = 72
c = canvas.Canvas("hello.pdf")
for page in data['pages']:
    width = page['width'] * inch
    height = page['height'] * inch
    c.setPageSize((width, height))
    for element in page['elements']:
        element_type = element.setdefault('type', 'text')
        fontSize = element.setdefault('fontSize', 10)
        fontType = element.setdefault('fontType', 'Courier')
        element_width = element.setdefault('width', 30)
        element_height = element.setdefault('height', 30)
        text = element.setdefault('text', '')
        if element_type == "barcode":
            barcode = createBarcodeDrawing(
                'Code128', height=element_height, value=text, barWidth=1, humanReadable=True)
            drawing_width = element_width
            barcode_scale = drawing_width / barcode.width
            drawing_height = barcode.height * barcode_scale
            drawing = Drawing(drawing_width, drawing_height)
            drawing.scale(barcode_scale, barcode_scale)
            drawing.add(barcode, name='barcode')
            c.setFont(fontType, fontSize)
            renderPDF.draw(drawing, c, element['x'], element['y'])
        elif element_type == "text":
            text_width = stringWidth(text, fontType ,fontSize )
            font_ratio = element_width/text_width
            if (font_ratio<=1):
                fontSize = fontSize*font_ratio
                pprint(font_ratio)


            c.setFont(fontType, fontSize)
            c.drawString(element['x'], element['y'], element['text'])
    c.showPage()
c.save()
