from PIL import Image, ImageFont, ImageDraw
import gdown
import pandas as pd
from barcode import Gs1_128
from barcode.writer import ImageWriter
import os


folder = "ExportedImg"
if not os.path.exists(folder):
    os.mkdir(folder)


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


def barcode_gen(barcode_num):
    my_code = Gs1_128(barcode_num, writer=ImageWriter())
    my_code.save("amazingBarcode")


def pic_download(url, filename):
    try:
        url = url.replace("open", "uc")
        output_path = f"{filename}.jpg"
        gdown.download(url, output_path)

    except Exception as e:
        print(f"Failed to downaload the img : {e}")


def pic_to_place(img, pic_name, resize_tuple, loc_tuple, output_name, to_crop=False):
    if type(img) == str:
        img = Image.open(f"{folder}/{img}.png")
    dp = Image.open(f"{pic_name}")
    if to_crop:
        dp = dp.crop((10, 150, 300, 180))
    dp = dp.resize(resize_tuple)  # To fill into the size
    new_image = img.copy()  # So that it doesn't effect the real imamge
    new_image.paste(dp, loc_tuple)  # Pasting the dp on new_img(copy of img), at (30, 160)
    filepath = os.path.join(folder, f"{output_name}.png")
    new_image.save(filepath)


# font
font = ImageFont.truetype("arial.ttf", 14)


data = pd.read_csv("Form Test - Form Responses 1.csv")
df = pd.DataFrame(data)
df = df.iloc[:, 1:]

li = []

for i in range(len(df)):
    temp = []
    for j in df.iloc[i]:
        temp.append(j)

    li.append(temp)

print(li)
#
#
# (x, y) for the first detail (i.e name), x -> const, y -> changes
x, y = 330, 158
# line spacing, to update y
dis = 21


for i in range(len(li)):
    rank = (str(li[i][3]))
    year = (str(li[i][5])[:4])
    output_name = f"{li[i][0]}-{rank}"

    img = Image.open("SampleIDCard.png")
    editing = ImageDraw.Draw(img)

    for j in range(len(li[0])):
        if j < len(li[0])-1:
            editing.text((x, y + dis * j), wrap(str(li[i][j])), (0,0,0), font)

        # # Remove comment in the end
        else:
            url = li[i][j]
            pic_download(url, "dp")
            # base-img, resize tuple, location tuple, output name
            pic_to_place(img, "dp.jpg", (144, 153), (30, 160), output_name)

    barcode_num = "0" * (10 - (len(rank) + 4)) + f"{rank}{year}"
    barcode_gen(barcode_num)

    # Placing the barcode
    pic_to_place(output_name, "amazingBarcode.png", (220, 40), (262, 352), output_name, True)

    # Adding the signature
    pic_to_place(output_name, "Signature.jpg", (150, 30), (26, 352), output_name)

    # Adding the barcode number
    img = Image.open(f"{folder}/{output_name}.png")
    editing = ImageDraw.Draw(img)
    editing.text((320,395), barcode_num, (0,0,0), font)
    filepath = os.path.join(folder, f"{output_name}.png")
    img.save(filepath)
