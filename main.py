from PIL import Image, ImageFont, ImageDraw

img = Image.open("SampleIDCard.png")
ed = ImageDraw.Draw(img)
font = ImageFont.truetype("arial.ttf", 14)

name = "Ankita"
fath = "Madan Singh Rawat"
dob = "15/11/2002"
cet = "1"
course = "BCA M"
batch = "2022-2025"
phn = "9354739677"

# name = input("Enter your name : ")
# fath = input("Enter your father's name : ")
# dob = input("Enter your dob : ")
# cet = input("Enter your CET rank : ")
# course = input("Enter your course : ")
# batch = input("Enter your batch : ")
# phn = input("Enter your phone no : ")

li = [name, fath, dob, cet, course, batch, phn]

x,y = 330, 158
dis = 21

for i in range(len(li)):
    ed.text((x, y+dis*i), li[i], (0,0,0), font)

# #Name
# ed.text((x,y+dis*0), "Aditya Rawat", (0,0,0), font)
#
# #Father's name
# ed.text((x,y+dis*1), "Madan Singh Rawat", (0,0,0), font)

img.save("res.png")
