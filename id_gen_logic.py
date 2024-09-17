from PIL import Image, ImageFont, ImageDraw
import gdown
import pandas as pd
from barcode import Gs1_128
from barcode.writer import ImageWriter
import os
import sys


def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller. """
    try:
        # PyInstaller creates a temporary folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# Use resource_path to access SampleIDCard.png
image_path = resource_path("SampleIDCard.png")

# x and y signifies location of 'Name'
# (x, y) for the first detail (i.e name), x -> const, y -> changes
X, Y = 326, 155
# line spacing, to update y
DIS = 21

# To create a folder in desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
folder_name = "GeneratedIDCards"
folder_path = os.path.join(desktop_path, folder_name)

if not os.path.exists(folder_path):
    os.mkdir(folder_path)


# Func imp -> If Residential Address is too long, it will wrap to next line
def wrap(text):
    wrapped_text = ""
    line_length = 0
    for word in text.split():
        if line_length + len(word) + 1 > 60:
            wrapped_text += "\n"
            line_length = 0
        wrapped_text += word + " "
        line_length += len(word) + 1
    return wrapped_text


# To generate barcodes
def barcode_gen(barcode_num):
    my_code = Gs1_128(barcode_num, writer=ImageWriter())
    my_code.save("amazingBarcode")


def pic_download(url, filename):
    try:
        url = url.replace("open", "uc")
        output_path = f"{filename}.jpg"
        gdown.download(url, output_path)
        return True

    except Exception as e:
        print("Can't download file")
        return False


def pic_to_place(img, pic_name, resize_tuple, loc_tuple, output_name, to_crop=False):
    if type(img) == str:
        img = Image.open(f"{folder_path}/{img}.png")

    dp = Image.open(f"{pic_name}")

    if to_crop:
        dp = dp.crop((10, 150, 300, 180))

    dp = dp.resize(resize_tuple)  # To fill into the size
    new_image = img.copy()  # So that it doesn't effect the real imamge
    new_image.paste(dp, loc_tuple)  # Pasting the dp on new_img(copy of img), at (30, 160)
    filepath = os.path.join(folder_path, f"{output_name}.png")
    new_image.save(filepath)


def generate(csv_path, batch_year):
    font = ImageFont.truetype("arial.ttf", 14)
    data = pd.read_csv(csv_path)
    df = pd.DataFrame(data)
    df = df.iloc[:, 1:]

    for i in range(len(df)):
        rank = str(df.iloc[i, 3])
        year = batch_year
        output_name = f"{df.iloc[i, 0]}-{rank}"

        img = Image.open(image_path)
        editing = ImageDraw.Draw(img)
        for j in range(len(df.iloc[i])):
            if j <= 4:
                editing.text((X, Y + DIS * j), wrap(str(df.iloc[i,j])), (0, 0, 0), font)
            elif j == 5:
                editing.text((X, Y + DIS * j), year, (0,0,0), font)
            elif j <= 7:
                editing.text((X, Y + DIS * j), wrap(str(df.iloc[i,j-1])), (0,0,0), font)
            else:
                url = df.iloc[i, j-1]
                can_donwload = pic_download(url, "dp")
                if not can_donwload:
                    return "Can't download the img, check the visibility mode"
                # base-img, resize tuple, location tuple, output name
                pic_to_place(img, "dp.jpg", (150, 158), (27, 154), output_name)

                url = df.iloc[i, j]
                pic_download(url, "signature")
                pic_to_place(output_name, "Signature.jpg", (150, 31), (25, 350), output_name)

        year = "".join(year.split("-"))
        barcode_num = "0" * (10 - (len(rank) + 4)) + f"{rank}{year}"
        barcode_gen(barcode_num)

        # Placing the barcode
        pic_to_place(output_name, "amazingBarcode.png", (220, 40), (259, 349), output_name, True)

        # Adding the barcode number
        img = Image.open(f"{folder_path}/{output_name}.png")
        editing = ImageDraw.Draw(img)
        editing.text((314,389), barcode_num, (0,0,0), font)
        filepath = os.path.join(folder_path, f"{output_name}.png")
        img.save(filepath)

    return "Completed"

