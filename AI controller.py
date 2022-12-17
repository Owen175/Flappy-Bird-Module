import pygame as py
from flappy import flappy_bird_module as fbm
from flappy import config as cf
import time

py.init()
if __name__ == '__main__':
    # PYGAME FRAME WINDOW
    py.display.set_caption("Flappy Bird V2")
    screen = py.display.set_mode((cf.FrameWidth, cf.FrameHeight))

    t = time.time()
    cf.clock.tick(33)

    if cf.toggleMusic:
        py.mixer.music.play(-1)  # Repeats

    while True:
        game1 = fbm.Game(cf.bgScroll, cf.bseScroll, highScore, AllTimeHS, cf.pipeInterval, cf.pointWhenPassed, cf.startPos, 1)
        print('Press Space to play.')
        highScore, AllTimeHS = game1.run(highScore, AllTimeHS)