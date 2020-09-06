# Tetris Bot

This is a python implementation of a tetris bot.

The goal of this code is to automatically play jstris with a simple AI.

# Requirements
* Python3 (I use 3.8.5)
* pyqt5
* numpy
* Pillow
* pyautogui

# Disclosure
This code builds heavily from the work done by LoveDaisy (https://github.com/LoveDaisy/tetris_game)

# To Do
* Understand code base
* Create screenshotter to read jstris board
* Plug screenshotter to codebase
* Take next move from AI and plug into jstris

## Approach
1. Read piece from jstris
2. Copy next piece to ai
3. Intercept best move from ai
4. Input strategy into jstris
5. Repeat 1-4