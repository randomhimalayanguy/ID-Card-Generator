from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM
drawing = svg2rlg("new_code.svg")
renderPM.drawToFile(drawing, "file.png", fmt="PNG")