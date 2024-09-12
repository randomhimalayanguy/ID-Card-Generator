from barcode import Gs1_128
import os

folder = "NewFolderCheck"

if not os.path.exists(folder):
    os.mkdir(folder)

num = "123456789"
gen = Gs1_128(num)
filepath = os.path.join(folder, "ranbarcode")
gen.save(filepath)
