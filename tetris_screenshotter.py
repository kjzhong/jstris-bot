from PIL import Image
import pyautogui

# Goal of this code is to be able to screenshot then process the next pieces from jstris.
# The idea is to then feed the "code" of each piece to the nextpiece function in this code, essentially plugging it in
# If we can grab this right, then the logical flow of the program can be changed to:
# 1. Read next piece from jstris
# 2. What is best move?
# 3. Enter best move in tetris and in jstris
# 4. Repeat 1-3
