# rich-cmyk-checker
<sub>Wherein every programmer ever will judge how I coded this.</sub>

Checks art files and identifies where total CMYK % exceeds 240% (now with support for individual layers).

I still have no clue what rich black is still so I can't help you with that...
(though, if requested, I could add a feature to spot areas where K=100% and there are other CMY values).

This is assuming you have python3 installed; Ubuntu came with it for me.
In the case you don't have it though, you can probably just run a "sudo apt install python3" or something.

# Quick Disclaimers
- I think there might be a margin of error here somewhere, but I haven't tested it enough.
- Due to the nature of the python image processing library using CMYK 8-bit (instead of %), the CMYK % gets calculated using the formula (n/255)*100%. In contrast, in an art program the values are integers. This means that there is probably going to be some difference in the values you see in the art program, versus the values that are calculated here. Though how large the difference can be, I am not sure (needs testing).
- There has been one test with 62/62/62/60 and it has successfully been detected as >240% CMYK, but I haven't done any other tests aside from with my own files
- To this day I have no clue what rich black is (I just know that standard black is CMYK of [0%, 0%, 0%, 100%]) so there is currently no support for detecting rich black colors. However, this can easily be added...someone just please tell me what CMYK's are considered rich black LOL.
  - <sub>Will the real rich black please stand up?</sub>

# Commands used for set-up (I'm on ubuntu):
- `sudo apt-get update`
- `sudo apt install python3-pip`
  - You probably don't need this...I just did not know where to get pip at the time (BUT I APPARENTLY HAD PIP?????)
- `python3 -m pip install --upgrade pip`
- `python3 -m pip install --upgrade Pillow`
- `pip install psd-tools`

# How do I run this?
- In the repository root directory (inside the repository folder), run `python3 main.py`

# Can I make this an executable?
- Yes! You can run `pip install pyinstaller` and run `pyinstaller main.py` to create an executable. The bundled application should be in the generated _dist_ folder (see pyinstaller here for more info: https://github.com/pyinstaller/pyinstaller)
- I would have made the executable, but I imagine most people would prefer seeing the code for themselves and making it themselves instead of running a random executable someone gave them.

# Why do you have no comments in some spots and comments in others?
- I got lost in the code zone sorry, I can add more comments later explaining the step-by-step process in the code.

# How does this work?
- To summarize what this really does:
  - There is a function in the checker.py file (checker module) that looks at a PIL Image object and peeks at the CMYK data of each and every pixel on that Image object, sums up the CMYK % values and places a black pixel wherever the CMYK % exceeds 240%...and in the main.py file we use the psd_tools python package to separate your image into layers (and let you select which layers to check in the very ugly user interface), convert those layer(s) into PIL Image object(s) that can be taken by the checker module's function, and give the output to show you where each spot of concern is (margin of error TBD) with a black pixel.
- If your output is good, there will be a message that is green that says the output is in the "output" folder. If ANY of your layers selected is bad, that message will be red (I will probably have to change the text to account for red-green color-blindness).
- In the output folder, files that have "-good.png" at the end have passed the check, whereas files that have "-bad.png" at the end have not passed the check.
- Again, there may or may not be slight margin of error (for reasons stated in disclaimers), but this should theoretically provide a faster check than you yourself individually color picking everything in your file.

# License
This uses the MIT license. My pseudonym is Everlit (though it might also happen to show as "meow" due to my github screen name being set that way).

# Credits/Third-Party Licenses:
- Python Imagine Library (fork):
  - https://python-pillow.github.io
  - https://github.com/python-pillow/Pillow
  - Author(s) of Pillow: Jeffrey A. Clark and contributors (2010)
  - Author(s) of Python Imaging Library (PIL): Secret Labs AB (1997-2011), Fredrik Lundh and contributors (1995-2011)
  - License: https://github.com/python-pillow/Pillow/blob/main/LICENSE

- psd-tools:
  - https://github.com/psd-tools/psd-tools
  - Author(s): Kota Yamaguchi (2019)
  - License: https://github.com/psd-tools/psd-tools/blob/main/LICENSE

- pip:
  - https://github.com/pypa/pip
  - Author(s): The pip developers (2008-present)
  - License: https://github.com/pypa/pip/blob/main/LICENSE.txt

# Languages Used:
- Python (https://www.python.org/)