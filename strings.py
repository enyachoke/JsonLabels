
import os
import sys
import datetime
import platform

import reportlab
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import colors
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import (stringWidth, getAscent, getDescent,
registerFont, registerFontFamily)

from reportlab.graphics.charts.textlabels import _text2Path
from reportlab.pdfbase import pdfmetrics, ttfonts



def create_page(out_path, text, width, fns, col, verbose=False):
c = Canvas(out_path, pagesize=landscape(A4))

c.setLineWidth(1)
c.setFillColor(col)

fs = 72
width = 800
x = 275

fnl, fsl = "Helvetica", fs/7.2

for i, fn in enumerate(fns):
y = A4[0]-110 - i * fs * 2

asc, dsc = getAscent(fn), getDescent(fn)

# draw background box plus text
c.setFont(fn, fs)
d = fs*asc/1000.
w = stringWidth(text, fn, fs)
c.setFillColor(colors.lightgrey)
c.rect(x, y, w, d, stroke=0, fill=1)
c.setFillColor(colors.black)
c.drawString(x, y, text)

# base line
c.setStrokeColor(colors.red)
c.line(x, y, width, y)
c.setFont(fnl, fsl)
c.drawString(x-125, y, "baseline (0)")

# base line + font size
c.setStrokeColor(colors.green)
d = fs
c.line(x, y+d, width, y+d)
c.drawString(x-125, y+d, "baseline + fontsize")
# fontname
c.drawString(x-225, y+d, fn)

# base line - descent
c.setStrokeColor(colors.blue)
d = fs*dsc/1000.
c.line(x, y+d, width, y+d)
c.drawString(x-125, y+d, "baseline + descent")

# base line + ascent
c.setStrokeColor(colors.grey)
d = fs*asc/1000.
c.line(x, y+d, width, y+d)
c.drawString(x-125, y+d, "baseline + ascent")

# mean line (approximated)
c.setStrokeColor(colors.orange)
c.setDash([5, 5])
#d = stringWidth("x", fn, fs)
bx0,by0,bx1,by1 = _text2Path('x',fontName=fn,fontSize=2048).getBounds()
d = fs * (max(0,by1)-max(0,by0))/2048.
c.line(x, y+d, width, y+d)
c.drawString(x-125, y+d, "mean line?")


d = datetime.datetime.now().isoformat()
d = d[:d.rfind(":")]
args = (reportlab.Version, platform.python_version(), d)
s = "Reportlab v. %s, Python v. %s, Date/Time: %s" % args
c.drawString(width - stringWidth(s, fnl, fsl), A4[0]-2*fsl, s)

c.showPage()
c.save()
