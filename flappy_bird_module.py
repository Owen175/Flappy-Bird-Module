# import pygame as py
import time
from bird import Bird
from pipe import Pipe
import random
from config import *


class Game:
    def __init__(self, bgScroll, bseScroll, highScore, AllTimeHS, pipeInterval, pointWhenPassed, startPos, numBirds):
        self.bgScroll, self.bseScroll, self.highScore, self.AllTimeHS, self.pipeInterval, self.pointWhenPassed, self.startPos = \
            bgScroll, bseScroll, highScore, AllTimeHS, pipeInterval, pointWhenPassed, startPos
        self.bseHeight = bse.get_height()
        self.bgHeight = bg.get_height()
        self.initialVelocity = 0
        self.speed = speed
        self.anSpeed = anSpeed
        self.skipTime = 0
        self.pos = self.startPos
        self.t = time.time()
        self.pipeList = []
        self.pipeTime = time.time()
        self.birdList = []
        for i in range(numBirds):
            self.birdList.append(Bird(image=bd, gravity=gravity, pos=startPos, mass=30, initVeloc=initialVelocity, an1=an1, an2=an2))
        self.newPipe()
        self.drawPipe(self.pipeList[0])
        self.lastTime = time.time()
        self.deltaTime = 0.00001

        self.endGame = False
        self.intScore = 0
        self.cumulativeSkipTime = 0
        self.skipTime = 0

    def checkKeys(self):
        oldt = self.t
        for evt in py.event.get():
            if evt.type == py.QUIT:
                quit()
            if evt.type == py.KEYDOWN:
                if evt.key == py.K_SPACE:
                    for i in range(len(self.birdList)):
                        if self.birdList[i].dead:
                            pass
                        else:
                            self.birdList[i].flap()
                            self.birdList[i].anTime = 1
                    # for playing note.wav file
                            if wingSounds:
                                py.mixer.Sound.play(wings)
                if evt.key == py.K_q:
                    quit()
                if evt.key == py.K_p:
                    paused = True
                    py.mixer.music.pause()
                    while paused:
                        for e in py.event.get():
                            if evt.type == py.QUIT:
                                quit()
                            if e.type == py.KEYDOWN:
                                if e.key == py.K_p:
                                    paused = False
                                    py.mixer.music.unpause()
                                    self.skipTime = time.time() - oldt
                                if e.key == py.K_q:
                                    quit()
                        py.display.update()



    def scrollIm(self, img, scroll, y, tls):
        i = 0
        while i < tls:
            screen.blit(img, (img.get_width() * i + scroll, y))
            i += 1


    def birdPosSet(self, pos, img):
        screen.blit(img, (pos[0], pos[1]))


    def cont(self):
        deadLst = []
        for i in range(len(self.birdList)):
            if not(self.birdList[i].pos[1] >= self.bseHeight + self.birdList[i].image.get_height()):
                self.birdList[i].dead = True
            deadLst.append(self.birdList[i].dead)
        return (False in deadLst) and (not self.endGame)


    def newPipe(self):
        pipeGap = random.randint(100, 250)
        bottomPipeStart = random.randint(400 - pipeGap, FrameHeight - bseHeight - 20)
        topPipeStart = bottomPipeStart - pipeGap - pipetop.get_height()
        self.pipeList.append(Pipe((FrameWidth, topPipeStart), pipetop.get_width(), pipetop.get_height(), pipetop))
        self.pipeList.append(Pipe((FrameWidth, bottomPipeStart), pipebottom.get_width(), pipebottom.get_height(), pipebottom))


    def drawPipe(self, pipe):
        screen.blit(pipe.img, (pipe.pipeStartPos, pipe.pipeTop))


    def shiftPipe(self, scroll):
        for i in range(len(self.pipeList)):
            self.pipeList[i].nextFrame(scroll)


    def removeOffScreen(self):
        pPair = []

        for i, p in enumerate(self.pipeList):
            if i % 2 == 0:
                pPair.append([p])
            else:
                pPair[(i - 1) // 2].append(p)

        finList = []

        for pr in pPair:
            if pr[0].pipeEndPos >= 0:
                finList.extend(pr)
        self.pipeList = finList


    def displayScore(self, coords=[30, 20], count=3):
        if self.intScore == 999:
            print('You won with a score of 999. Well done.')
            self.endGame = True
        score = str(self.intScore)
        for _ in range(count - len(score)):
            score = '0' + score

        digitList = []
        for char in score:
            match int(char):
                case 0:
                    digitList.append(zero)
                case 1:
                    digitList.append(one)
                case 2:
                    digitList.append(two)
                case 3:
                    digitList.append(three)
                case 4:
                    digitList.append(four)
                case 5:
                    digitList.append(five)
                case 6:
                    digitList.append(six)
                case 7:
                    digitList.append(seven)
                case 8:
                    digitList.append(eight)
                case 9:
                    digitList.append(nine)

        for i, dg in enumerate(digitList):
            screen.blit(dg, (scoreDist * i + coords[0], coords[1]))



    def run(self, highScore, AllTimeHS):
        while self.cont():
            self.checkKeys()
            self.lastTime = self.t
            self.t = time.time()
            self.deltaTime = self.t - self.lastTime - self.skipTime
            for i in range(len(self.birdList)):
                self.birdList[i].anTime -= self.deltaTime * self.anSpeed
            self.cumulativeSkipTime += self.skipTime
            for id, bird in enumerate(self.birdList):
                if bird.anTime > 0.5:
                    self.birdList[id].anFrame = an1
                elif bird.anTime > 0:
                    self.birdList[id].anFrame = an2
                elif bird.anTime > -0.5:
                    self.birdList[id].anFrame = an1
                else:
                    self.birdList[id].anFrame = bd

            self.scrollIm(bg, self.bgScroll, 0, tiles)

            self.pipeScroll = -self.speed * self.deltaTime
            self.bgScroll -= self.speed * self.deltaTime  # keeps the movement speed constant despite FPS changes
            self.bseScroll -= self.speed * self.deltaTime
            if abs(self.bgScroll) > bg.get_width():
                self.bgScroll = 0
            if abs(self.bseScroll) > bse.get_width():
                self.bseScroll = 0
            if regularPipeIntervals:
                if self.pipeTime + self.cumulativeSkipTime + minPipeInterval < time.time():
                    self.pipeTime = self.t
                    self.newPipe()
            else:
                if time.time() > self.pipeInterval + self.cumulativeSkipTime + self.pipeTime:
                    self.newPipe()
                    self.pipeTime = time.time()
                    self.pipeInterval = minPipeInterval / max(math.sqrt(random.random()), 0.5)

            self.shiftPipe(self.pipeScroll)
            self.removeOffScreen()
            for p in self.pipeList:
                self.drawPipe(p)
            self.birdPosList = []
            for i in range(len(self.birdList)):
                pos = self.birdList[i].frameChange(self.deltaTime * timeMultiplier)
                self.birdPosList.append((pos[0],FrameHeight-pos[1]))
                if self.birdList[i].dead:
                    self.birdPosList[i] = (-100, 0)
                self.birdPosSet(self.birdPosList[i], self.birdList[i].anFrame)
            pipePairs = []
            for i, p in enumerate(self.pipeList):
                if i % 2 == 0:
                    pipePairs.append([p])
                else:
                    pipePairs[(i - 1) // 2].append(p)

            for pair in pipePairs:
                for id, bird in enumerate(self.birdList):
                    additionToScore = pair[0].checkForScore(bird.pos[0], pointWhenPassed)
                    self.intScore += additionToScore
                    if additionToScore == 1 and soundOnPoint:
                        py.mixer.Sound.play(point)

                p1y = pair[0].pipeTop + pipetop.get_height()
                p2y = pair[1].pipeTop

                for id, bird in enumerate(self.birdList):
                    for row in [bird.shape[0], bird.shape[2], bird.shape[4], bird.shape[6], bird.shape[12], bird.shape[14],
                                bird.shape[16], bird.shape[20], bird.shape[23]]:
                        start = row[0]
                        start = [start[0] + bird.pos[0], start[1] + FrameHeight - bird.pos[1]]

                        flapRealPosy = start[1]  # FrameHeight-start[1]
                        if not (p1y < flapRealPosy < p2y):
                            end = row[1]
                            end = end[0] + bird.pos[0]

                            if end > pair[0].pipeStartPos and start[0] < pair[0].pipeEndPos:
                                self.birdList[id].dead = True

            self.scrollIm(bse, self.bseScroll, FrameHeight - bse.get_height(), tilesBse)
            self.displayScore()
            clock.tick(FPS)  # Limits the FPS to the num
            py.display.update()
            skipTime = 0

        screen.blit(gm_over, (FrameWidth // 2 - gm_over.get_width() // 2, FrameHeight // 2 - gm_over.get_height() // 2))
        py.mixer.Sound.play(die)

        if self.intScore > self.highScore:
            self.highScore = self.intScore
        if self.highScore > self.AllTimeHS:
            with open('highScore.txt', 'w') as f:
                f.write(str(self.highScore))
            AllTimeHS = self.highScore
            print(f'Congratulations, you beat the all time high score. It is now {highScore}')
        print(f'Current Session High score is {highScore}')
        while True:
            py.display.update()
            for event in py.event.get():
                if event.type == py.QUIT:
                    print(f'Session High Score was {highScore}')
                    quit()
                if event.type == py.KEYDOWN:
                    if event.key == py.K_r:
                        return highScore, AllTimeHS
                    if event.key == py.K_q:
                        print(f'Session High Score was {highScore}')
                        quit()



py.init( )
if __name__ == '__main__':
    # PYGAME FRAME WINDOW
    py.display.set_caption("Flappy Bird V2")
    py.display.set_icon(icon)
    screen = py.display.set_mode((FrameWidth, FrameHeight))

    t = time.time()
    clock.tick(33)

    if toggleMusic:
        py.mixer.music.play(-1)  # Repeats

    while True:
        game1 = Game(bgScroll, bseScroll, highScore, AllTimeHS, pipeInterval, pointWhenPassed, startPos, 1)
        print('Press Space to play.')
        highScore, AllTimeHS = game1.run(highScore, AllTimeHS)

