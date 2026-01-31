# Checker module
from PIL import Image

def check_img(old_img: Image, new_img_name: str) -> bool:
    """
    Function that checks the CMYK totals of each pixel in the image.
    The PNG that is created as output points out each pixel that
    exceeds 240% CMYK (margin of error TBD).
    
    old_img: The Image object representing the image to be checked

    new_img_name: Name of new image PNG (without .png extension)
    
    *Note: The new_img_name will have "good" or "bad" appended at the end
    depending on if it passes the check or not.

    Returns True if the img is clear, False otherwise
    """
    all_good = True
    if old_img.mode != "CMYK":
        print("ERROR: Input file is not in CMYK format. Come back after converting to CMYK.")
        exit()

    # PIL accesses images in Cartesian co-ordinates, so it is Image[columns, rows]

    new_img = Image.new('RGBA', old_img.size, (255, 255, 255, 255)) # create a new white image
    pixels = new_img.load() # create the pixel map

    (width, height) = new_img.size
    # for each pixel in each colum and row, LOOK AT IT!!!
    # and if the CMYK % value sum is greater than 240,
    # color the new_img (that should be a white blank canvas if each
    # color is <240 CMYK %) at that spot with a black pixel.
    for i in range(width):    # for every col:
        for j in range(height):    # for every row:
            t = old_img.getpixel((i,j))
            (c,m,y,k) = tuple((ti/255)*100 for ti in t)
            if c+m+y+k > 240:
                all_good = False
                pixels[i,j] = (0, 0, 0, 255) # mark that spot with a black pixel

    new_img.save(f"{new_img_name}-{'good' if all_good else 'bad'}.png")
    return all_good

def check_file(old_img_name: str, new_img_name: str):
    """
    Function that checks the CMYK totals of each pixel in the image.
    The PNG that is created as output points out each pixel that
    exceeds 240% CMYK (margin of error TBD).
    
    old_img_name: Name of the old image PSD (with .psd extension)

    new_img_name: Name of new image PNG (with .png extension)
    """
    old_img = Image.open(old_img_name)

    if old_img.mode != "CMYK":
        print("ERROR: Input file is not in CMYK format. Come back after converting to CMYK.")
        exit()

    # PIL accesses images in Cartesian co-ordinates, so it is Image[columns, rows]

    new_img = Image.new('RGBA', old_img.size, (255, 255, 255, 255)) # create a new white image
    pixels = new_img.load() # create the pixel map

    (width, height) = new_img.size
    # for each pixel in each colum and row, LOOK AT IT!!!
    # and if the CMYK % value sum is greater than 240,
    # color the new_img (that should be a white blank canvas if each
    # color is <240 CMYK %) at that spot with a black pixel.
    for i in range(width):    # for every col:
        for j in range(height):    # for every row:
            t = old_img.getpixel((i,j))
            (c,m,y,k) = tuple((ti/255)*100 for ti in t)
            if c+m+y+k > 240:
                pixels[i,j] = (0, 0, 0, 255) # mark that spot with a black pixel

    new_img.save(new_img_name)