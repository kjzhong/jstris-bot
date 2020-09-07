#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys

from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from tetris_model import BOARD_DATA, Shape
from tetris_ai import TETRIS_AI
from tetris_screenshotter import wait_go, identify_next, identify_first


# TETRIS_AI = None


class Tetris(QMainWindow):
    def __init__(self):
        super().__init__()
        self.isStarted = False
        self.isPaused = False
        self.nextMove = None
        self.lastShape = Shape.shapeNone

        self.initUI()

    def initUI(self):
        self.gridSize = 22
        # This controls the game speed (lower is faster)
        self.speed = 200

        self.timer = QBasicTimer()
        self.setFocusPolicy(Qt.StrongFocus)

        hLayout = QHBoxLayout()
        self.tboard = Board(self, self.gridSize)
        hLayout.addWidget(self.tboard)

        self.sidePanel = SidePanel(self, self.gridSize)
        hLayout.addWidget(self.sidePanel)

        self.statusbar = self.statusBar()
        self.tboard.msg2Statusbar[str].connect(self.statusbar.showMessage)

        self.start()

        self.center()
        self.setWindowTitle('Tetris')
        # This shows the pygame window
        # self.show()

        self.setFixedSize(self.tboard.width() + self.sidePanel.width(),
                          self.sidePanel.height() + self.statusbar.height())

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2,
                  (screen.height() - size.height()) // 2)

    def start(self):
        if self.isPaused:
            return

        self.isStarted = True
        self.tboard.score = 0
        BOARD_DATA.clear()

        self.tboard.msg2Statusbar.emit(str(self.tboard.score))

        BOARD_DATA.createNewPiece()
        self.timer.start(self.speed, self)

    def pause(self):
        if not self.isStarted:
            return

        self.isPaused = not self.isPaused

        if self.isPaused:
            self.timer.stop()
            self.tboard.msg2Statusbar.emit("paused")
        else:
            self.timer.start(self.speed, self)

        self.updateWindow()

    def updateWindow(self):
        self.tboard.updateData()
        self.sidePanel.updateData()
        self.update()

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            # Pieces in the game are created in different positions and rotations than in jstris
            # I fix rotation, then fix position
            # Number of times we need to rotate right IN JSTRIS to match the game
            extra_rot = {
                'L': 1,
                'I': 1,
                'T': 1,
                'S': 0,
                'Z': 0,
                'O': 0,
                'J': 3
            }
            # Number of times you need to move right IN JSTRIS to match the game
            extra_position = {
                'I': 0,
                'Z': 1,
                'J': 1,
                'O': 1,
                'L': 1,
                'T': 1,
                'S': 1
            }
            # Just a dictionary to convert shape numbers back to tetromino pieces
            shape = {
                1: 'I',
                2: 'L',
                3: 'J',
                4: 'T',
                5: 'O',
                6: 'S',
                7: 'Z'
            }
            # This fixes rotation
            for i in range(extra_rot[shape[BOARD_DATA.currentShape.shape]]):
                driver.switch_to.active_element.send_keys(Keys.UP)

            # This fixes position after fixing rotation
            k = extra_position[shape[BOARD_DATA.currentShape.shape]]
            # print(f'{k=}, {shape[BOARD_DATA.currentShape.shape]=}')
            if k < 0:
                for i in range(-k):
                    driver.switch_to.active_element.send_keys(Keys.LEFT)
            if k > 0:
                for i in range(k):
                    driver.switch_to.active_element.send_keys(Keys.RIGHT)

            # Complex bug where the next shape was being identified at the wrong time (because of bad integration)
            # This is a hacky fix
            BOARD_DATA.nextShape = Shape(identify_next())

            if TETRIS_AI and not self.nextMove:
                self.nextMove = TETRIS_AI.nextMove()
            if self.nextMove:
                while BOARD_DATA.currentDirection != self.nextMove[0]:
                    BOARD_DATA.rotateRight(driver)
                while BOARD_DATA.currentX != self.nextMove[1]:
                    if BOARD_DATA.currentX > self.nextMove[1]:
                        BOARD_DATA.moveLeft(driver)
                    elif BOARD_DATA.currentX < self.nextMove[1]:
                        BOARD_DATA.moveRight(driver)

            # Dropdown is a space input, move down is just waiting for the pieces to fall
            lines = BOARD_DATA.dropDown(driver)
            # lines = BOARD_DATA.moveDown()
            self.tboard.score += lines
            if self.lastShape != BOARD_DATA.currentShape:
                self.nextMove = None
                self.lastShape = BOARD_DATA.currentShape
            self.updateWindow()
        else:
            super(Tetris, self).timerEvent(event)

    def keyPressEvent(self, event):
        if not self.isStarted or BOARD_DATA.currentShape == Shape.shapeNone:
            super(Tetris, self).keyPressEvent(event)
            return

        key = event.key()

        if key == Qt.Key_P:
            self.pause()
            return

        if self.isPaused:
            return
        elif key == Qt.Key_Left:
            BOARD_DATA.moveLeft(driver)
        elif key == Qt.Key_Right:
            BOARD_DATA.moveRight(driver)
        elif key == Qt.Key_Up:
            BOARD_DATA.rotateLeft(driver)
        elif key == Qt.Key_Space:
            self.tboard.score += BOARD_DATA.dropDown(driver)
        else:
            super(Tetris, self).keyPressEvent(event)

        self.updateWindow()


def drawSquare(painter, x, y, val, s):
    colorTable = [0x000000, 0xCC6666, 0x66CC66, 0x6666CC,
                  0xCCCC66, 0xCC66CC, 0x66CCCC, 0xDAAA00]

    if val == 0:
        return
    color = QColor(colorTable[val])
    painter.fillRect(x + 1, y + 1, s - 2, s - 2, color)

    painter.setPen(color.lighter())
    painter.drawLine(x, y + s - 1, x, y)
    painter.drawLine(x, y, x + s - 1, y)

    painter.setPen(color.darker())
    painter.drawLine(x + 1, y + s - 1, x + s - 1, y + s - 1)
    painter.drawLine(x + s - 1, y + s - 1, x + s - 1, y + 1)


class SidePanel(QFrame):
    def __init__(self, parent, gridSize):
        super().__init__(parent)
        self.setFixedSize(gridSize * 5, gridSize * BOARD_DATA.height)
        self.move(gridSize * BOARD_DATA.width, 0)
        self.gridSize = gridSize

    def updateData(self):
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        minX, maxX, minY, maxY = BOARD_DATA.nextShape.getBoundingOffsets(0)

        dy = 3 * self.gridSize
        dx = (self.width() - (maxX - minX) * self.gridSize) / 2

        val = BOARD_DATA.nextShape.shape
        for x, y in BOARD_DATA.nextShape.getCoords(0, 0, -minY):
            drawSquare(painter, int(x * self.gridSize + dx), y *
                       self.gridSize + dy, val, self.gridSize)


class Board(QFrame):
    msg2Statusbar = pyqtSignal(str)
    speed = 50

    def __init__(self, parent, gridSize):
        super().__init__(parent)
        self.setFixedSize(gridSize * BOARD_DATA.width,
                          gridSize * BOARD_DATA.height)
        self.gridSize = gridSize
        self.initBoard()

    def initBoard(self):
        self.score = 0
        BOARD_DATA.clear()

    def paintEvent(self, event):
        painter = QPainter(self)

        # Draw backboard
        for x in range(BOARD_DATA.width):
            for y in range(BOARD_DATA.height):
                val = BOARD_DATA.getValue(x, y)
                drawSquare(painter, int(x * self.gridSize), y *
                           self.gridSize, val, self.gridSize)

        # Draw current shape
        for x, y in BOARD_DATA.getCurrentShapeCoord():
            val = BOARD_DATA.currentShape.shape
            drawSquare(painter, int(x * self.gridSize), y *
                       self.gridSize, val, self.gridSize)

        # Draw a border
        painter.setPen(QColor(0x777777))
        painter.drawLine(self.width()-1, 0, self.width()-1, self.height())
        painter.setPen(QColor(0xCCCCCC))
        painter.drawLine(self.width(), 0, self.width(), self.height())

    def updateData(self):
        self.msg2Statusbar.emit(str(self.score))
        self.update()


if __name__ == '__main__':
    # random.seed(32)

    # Create the selenium window and wait for the game to start
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get('https://jstris.jezevec10.com/?play=2')
    wait_go()

    # BOARD_DATA is initialised on import - this resets nextShape once the game starts to get the piece properly
    BOARD_DATA.nextShape = Shape(identify_first())

    app = QApplication([])
    tetris = Tetris()

    sys.exit(app.exec_())
