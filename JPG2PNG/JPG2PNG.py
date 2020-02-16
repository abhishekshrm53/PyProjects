from PIL import Image
import sys
import os

image_folder = sys.argv[1]
dest_folder = sys.argv[2]

if not (os.path.exists(dest_folder)):
    os.makedirs(dest_folder)

for file in os.listdir(image_folder):
    img = Image.open(f'{image_folder}{file}')
    clean_name = os.path.splitext(file)[0]
    img.save(f'{dest_folder}{clean_name}.png', 'png')
    print('All Done!')
