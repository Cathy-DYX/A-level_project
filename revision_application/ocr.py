# from PIL import Image
# import pytesseract
# import pdftotext
# import io
# from wand.image import Image as wi
#
#
# def pdf_to_text(f):
#     with open(f, "rb") as f:
#         pdf = pdftotext.PDF(f)
#     # for page in pdf:
#     #     print(page)
#     print("\n\n".join(pdf))
#
#
# def img_to_text(f):
#     # Simple image to string
#     print(pytesseract.image_to_string(Image.open(f)))
