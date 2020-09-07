from PIL import Image, ImageGrab
import pyautogui
from selenium import webdriver


def get_pos():
    '''Prints current position of cursor'''
    currentMouseX, currentMouseY = pyautogui.position()
    print(currentMouseX, currentMouseY)


def wait_go():
    '''Waits until Go! appears'''
    go_x = 1560
    go_y = 765
    go_red = 203
    go_colour = 10
    while not go_colour in set([i for i in range(go_red-10, go_red + 10)]):
        go_colour = ImageGrab.grab().getpixel((go_x, go_y))[0]
    while not go_colour == 0:
        go_colour = ImageGrab.grab().getpixel((go_x, go_y))[0]


def identify_mouse():
    '''Prints the RGB tuple of pixel under cursor'''
    pos = pyautogui.position()
    pix = ImageGrab.grab().getpixel((pos[0], pos[1]))
    print(pix)


def identify_first():
    '''Identifies the first piece in jstris based on the top row'''
    colour = {
        (227, 91, 2): 'L',
        (227, 159, 2): 'O',
        (215, 15, 55): 'Z',
        (15, 155, 215): 'I',
        (33, 65, 198): 'J',
        (89, 177, 1): 'S',
        (175, 41, 138): 'T'}

    shape = {
        'I': 1,
        'L': 2,
        'J': 3,
        'T': 4,
        'O': 5,
        'S': 6,
        'Z': 7
    }
    left = 1480
    top = 344
    width = 120
    height = 100

    im = pyautogui.screenshot(region=(left, top, width, height))
    for i in range(width):
        for j in range(height):
            if im.getpixel((i, j)) in colour:
                print(f'first shape is {colour[im.getpixel((i, j))]}')
                return (shape[colour[im.getpixel((i, j))]])


def identify_next():
    '''Identifies the piece in the next slot and returns the corresponding letter'''
    colour = {
        (227, 91, 2): 'L',
        (227, 159, 2): 'O',
        (215, 15, 55): 'Z',
        (15, 155, 215): 'I',
        (33, 65, 198): 'J',
        (89, 177, 1): 'S',
        (175, 41, 138): 'T'}

    shape = {
        'I': 1,
        'L': 2,
        'J': 3,
        'T': 4,
        'O': 5,
        'S': 6,
        'Z': 7
    }

    left = 1786
    top = 375
    width = 70
    height = 30
    # Saves the screenshot as next.png for easier debugging
    im = pyautogui.screenshot(region=(left, top, width, height))
    for i in range(width):
        for j in range(height):
            if im.getpixel((i, j)) in colour:
                return (shape[colour[im.getpixel((i, j))]])
