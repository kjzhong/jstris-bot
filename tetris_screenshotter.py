from PIL import Image, ImageGrab
import pyautogui
from mss import mss

# Which library should I use?

# Goal of this code is to be able to screenshot then process the next pieces from jstris.
# The idea is to then feed the "code" of each piece to the nextpiece function in this code, essentially plugging it in
# If we can grab this right, then the logical flow of the program can be changed to:
# 1. Read next piece from jstris
# 2. What is best move?
# 3. Enter best move in tetris and in jstris
# 4. Repeat 1-3

# Lets use monitor 1 (my big monitor) in mss
# The jstris screen is snapped to the right half, with zoom = 100%


def get_pos():
    '''Prints current position of cursor'''
    currentMouseX, currentMouseY = pyautogui.position()
    print(currentMouseX, currentMouseY)


def wait_go():
    '''Waits until Go! appears'''
    go_x = 2513
    go_y = 711
    go_red = 203
    go_colour = 0
    while not go_colour == go_red:
        go_colour = ImageGrab.grab().getpixel((go_x, go_y))[0]
    print('Found go!')


def identify_mouse():
    '''Prints the RGB tuple of pixel under cursor'''
    pos = pyautogui.position()
    pix = ImageGrab.grab().getpixel((pos[0], pos[1]))
    print(pix)


def identify_next():
    '''Identifies the piece in the next slot'''
    colour = {
        (227, 91, 2): 'L',
        (227, 159, 2): 'O',
        (215, 15, 55): 'Z',
        (15, 155, 215): 'I',
        (33, 65, 198): 'J',
        (89, 177, 1): 'S',
        (175, 41, 138): 'T'}

    # Saves the screenshot as myscreenshot.png for easier debugging
    im = pyautogui.screenshot('myscreenshot.png', region=(2747, 327, 70, 30))
    for i in range(70):
        for j in range(30):
            if im.getpixel((i, j)) in colour:
                return (colour[im.getpixel((i, j))])

                # x = 2747 + i
                # y = 327 + j
