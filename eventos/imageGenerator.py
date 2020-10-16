import os

from PIL import Image, ImageDraw, ImageFont
import qrcode
import shutil

from config.settings import BASE_DIR

def genImage(nombre,id):
    logo = qrcode.make(id+nombre)
    logo = logo.resize((380, 380))
    logo = logo.crop((25, 25, 360, 360))

    img = Image.open(BASE_DIR + '/static/' + "flyer.png")
    # Escribe el Nombre
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(BASE_DIR + '/static/' + "arial.ttf", 130)
    texto = str(nombre)

    # Centrar texto vertical y horizontalmente.
    lines = texto.splitlines()
    w = font.getsize(max(lines, key=lambda s: len(s)))[0]
    h = font.getsize(texto)[1] * len(lines)
    x, y = img.size
    x /= 2
    x -= w / 2
    y /= 2
    y -= h / 2


    draw.multiline_text((x, 1450), texto, font=font, fill="white", align="center")

    # Pega el Qr
    img.convert('RGBA')
    img.paste(logo, (370, 1075), logo)

    # guarda
    f = open(BASE_DIR + '/static/invitaciones/' + str(id) +nombre + '.png', 'wb')

    img.save(f)
    f.close()

    return "{}{}.png".format(str(id),nombre)

def deleteImgs():
    folder = BASE_DIR + '/static/invitaciones/'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


