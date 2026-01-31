# OLD. This looks at ALL layers if you run it with "python3 check_all_layers.py <filename>.psd"
import sys
import checker
from PIL import Image
from psd_tools import PSDImage
from psd_tools.constants import ColorMode

if len(sys.argv) <= 1:
    print("Please add a file path (absolute or relative to this python script)!")
    exit()

# Verify that it is a valid PSD file
filename = sys.argv[1]
if not filename.lower().endswith('psd'):
    print("Please use a valid *.psd file!")
    exit()
try:
    Image.open(filename).verify()
except Exception as e:
    print("Please use a valid *.psd file!")
    exit()

# Retrieve the PSD file data
psd_file = PSDImage.open(sys.argv[1])

# Check that the PSD file is in CMYK
if psd_file.color_mode == ColorMode.CMYK:
    print("CMYK Check: File is CMYK confirmed!")
else:
    print("ERROR: Input file is not in CMYK format. Come back after converting to CMYK.")
    exit()

# Begin checking layers
print("Processing Layers...")
for layer in psd_file:
    # Retrieve all layer data, and convert to a PIL Image object,
    # WITHOUT applying any ICC profiles (such as converting to sRGB)
    layer_image = layer.topil(None, False)
    
    # Check each pixel in the layer's Image object, and
    # create a file named "output_<layer_name>.png" that
    # shows any areas where CMYK is > 240% in black
    # (safe areas are in white, MARGIN OF ERROR TO BE DETERMINED).
    checker.check_img(layer_image, f"output_{layer.name}.png")
    print(f"Finished processing layer \"{layer.name}\"!")