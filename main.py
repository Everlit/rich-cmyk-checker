from tkinter import *
from tkinter import filedialog as fd
from PIL import Image
from psd_tools import PSDImage
from psd_tools.constants import ColorMode
import checker
import os

# I am sorry for anyone who actually knows how to use tkinter for what you are about to see.

if not os.path.exists("./output"):
    os.makedirs("./output")

errorlabel = None
listboxoptions = []
listbox = None
label2 = None
checkbutton = None
frame = None
psdfile = None
success_message = None

def delete(element):
    element.destroy()

def start_check():
    global psdfile, listbox, errorlabel, success_message
    if errorlabel:
        errorlabel.destroy()
        errorlabel = None
    if success_message:
        success_message.destroy()
        success_message = None
    if psdfile is None:
        errorlabel = Label(frame, text="Unexpected Error!", fg="red")
        errorlabel.grid(column=0, row=2)
        return
    if listbox is None:
        errorlabel = Label(frame, text="Unexpected Error!", fg="red")
        errorlabel.grid(column=0, row=2)
        return
    

    selectedlayers = list(map(lambda index: listbox.get(index), listbox.curselection()))

    all_clear = True
    for layer in psdfile:
        # If the layer is not among those selected, pass by it and look at the next layer
        if not layer.name in selectedlayers:
            continue
    
        # Retrieve all layer data, and convert to a PIL Image object,
        # WITHOUT applying any ICC profiles (such as converting to sRGB)
        layer_image = layer.topil(None, False)
        
        # Check each pixel in the layer's Image object, and
        # create a file named "output_<layer_name>.png" that
        # shows any areas where CMYK is > 240% in black
        # (safe areas are in white, MARGIN OF ERROR TO BE DETERMINED).
        all_clear = all_clear and checker.check_img(layer_image, f"./output/output_{layer.name}")
        print(f"Finished processing layer \"{layer.name}\"!")
    if all_clear:
        success_message = Label(frame, fg="green", text="Output generated. Check the \"output\" folder.")
    else:
        success_message = Label(frame, fg="red", text="Output generated. Check the \"output\" folder.")
    success_message.grid(column=0, row=7)

def get_file():
    global psdfile, errorlabel, listbox, label2, listboxoptions, checkbutton, success_message
    if errorlabel:
        errorlabel.destroy()
        errorlabel = None
    if success_message:
        success_message.destroy()
        success_message = None
    if listbox:
        listbox.destroy()
        listbox = None
        label2.destroy()
        label2 = None
    if checkbutton:
        checkbutton.destroy()
        checkbutton = None
    if listboxoptions:
        listboxoptions = None

    filename = fd.askopenfilename(initialdir=".",
                                  title="Select a File",
                                  filetypes=[("psd", "*.psd")]
                                  )
    # Verify that it is a valid PSD file
    if not filename.lower().endswith('psd'):
        errorlabel = Label(frame, text="Please use a valid *.psd file!", fg="red")
        errorlabel.grid(column=0, row=2)
        return
    try:
        Image.open(filename).verify()
    except Exception as e:
        errorlabel = Label(frame, text="Please use a valid *.psd file!", fg="red")
        errorlabel.grid(column=0, row=2)
        return

    # Retrieve the PSD file data
    psdfile  = PSDImage.open(filename)

    # Check that the PSD file is in CMYK
    if psdfile.color_mode == ColorMode.CMYK:
        print("CMYK Check: File is CMYK confirmed!")
    else:
        errorlabel = Label(frame, text="This file is not CMYK!", fg="red")
        errorlabel.grid(column=0, row=2)
        return

    layeroptions = list(psdfile.descendants())
    layeroptions = list(map(lambda layer: layer.name, layeroptions))
    listboxoptions = StringVar(value=layeroptions)
    if len(layeroptions) == 0:
        print("Either you have no layers in this PSD file, or you have some default layer that needs to be explicitly named.")
    label2=Label(frame, text="Select Layers to Check")
    label2.grid(column=0, row=3)
    listbox= Listbox(frame, listvariable=listboxoptions, selectmode="multiple")
    listbox.grid(column=0, row=4)

    button2 = Button(frame, text="Check Layers", command=lambda: start_check())
    button2.grid(column=0, row=5, pady=16)

root = Tk()
root.title("CMYK Checker")
# Configure grid to center the label
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)

root.geometry("500x500")

frame = Frame(root, pady=32, padx=32, relief="ridge")
frame.grid(column=1, row=0)
label1=Label(frame, text="SELECT FILE")
label1.grid(column=0, row=0)

button1 = Button(frame, text="Browse...", command=lambda: get_file())
button1.grid(column=0, row=1)

root.mainloop()
