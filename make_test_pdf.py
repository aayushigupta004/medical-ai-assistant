from reportlab.pdfgen import canvas

c = canvas.Canvas("data/pdfs/test.pdf")
c.drawString(100, 750, "Page 1: Dengue is a viral infection spread by mosquitoes.")
c.showPage()
c.drawString(100, 750, "Page 2: Common symptoms include high fever and headache.")
c.showPage()
c.save()

print("Test PDF created successfully at data/pdfs/test.pdf")