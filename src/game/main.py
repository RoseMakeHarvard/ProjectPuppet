# KidsCanCode - Game Development with Pygame video series
# Jumpy! (a platform game) - Part 4
# Video link: https://youtu.be/G8pYfkIajE8
# Jumping

import pygame as pg
import random
from settings import *
from game_objects import *
import numpy as np
import cv2
import pipeline
import itertools
from threading import Thread

PLATFORM_LIST = [(0, HEIGHT - 40, WIDTH, 40)]

class Game:
    def __init__(self):
        # initialize game window, etc
        self.frameSeen = 0
        self.platsSeen = 0
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT),pg.FULLSCREEN)
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.g = pipeline.GripPipeline()
        self.cap = cv2.VideoCapture('http://10.253.64.129:8080/video')
        self.detPlats = []
        self.detFrame = []


    def new(self):
        # start a new game
        self.platforms = pg.sprite.Group()
        self.players = pg.sprite.Group()
        for plat in PLATFORM_LIST:
            p = Platform(*plat)
            self.platforms.add(p)
            self.players.add(Player(self))
        # self.gameThread.start()
        # self.imageThread.start()
        # Thread(target=self.run, args=()).start()
        Thread(target=self.imageProcess, args=()).start()
        self.run()

    def update_platforms(self, rel_plat_coords=[]):
        self.platforms = pg.sprite.Group()
        self.platforms.add(Platform(*BASE_PLATFORM))
        for coord in rel_plat_coords:
            if coord[0] <= 1 and coord[1] <=1 and coord[2] <=1 and coord[3] <=1:
                p = Platform(coord[0] * WIDTH,
                             coord[1] * HEIGHT,
                             coord[2] * WIDTH,
                             coord[3] * HEIGHT)
                self.platforms.add(p)
        self.platforms.update()

    def update_players(self):
        self.players.update()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def imageProcess(self):
        self.playing = True
        while(self.playing):
            ret, frame = self.cap.read()
            self.g.process(frame)

            self.detPlats = []
            # if not self.platsSeen >=18:
            for i in range(len(self.g.find_contours_0_output)):
                self.platsSeen += 1
                self.detPlats.append(cv2.boundingRect(self.g.find_contours_0_output[i]))
                # self.platX[i], self.platY[i], self.platW[i], self.platH += cv2.boundingRect(self.g.find_contours_0_output[i])
            if self.frameSeen < 100:
                self.detFrame = []
                for i in range(len(self.g.find_contours_1_output)):
                    self.frameSeen += 1
                    self.detFrame.append(cv2.boundingRect(self.g.find_contours_1_output[i]))
                    # self.frameX[i], self.frameY[i], self.frameW[i], self.frameH[i] = cv2.boundingRect(self.g.find_contours_1_output[i])

    def update(self):
        # Game Loop - Update
        platform_coords = []
        if(len(self.detFrame) > 0):
            # print(self.detFrame)
            fx = min(self.detFrame, key = lambda i : i[0])[0]
            fy = min(self.detFrame, key = lambda i : i[1])[1]
            fw = max(self.detFrame, key = lambda i : i[2])[2]
            fh = max(self.detFrame, key = lambda i : i[3])[3]
            # print(str(fx) + ' ' + str(fy) + ' ' + str(fw) + ' ' + str(fh))
            for i, (x, y, w, h) in enumerate(self.detPlats):
                platform_coords.append([(x - fx)/fw, (y - fy)/fh, w/fw, h/fw])

        # print(platform_coords)
        self.update_platforms(platform_coords)
        self.update_players()

        # check if player hits a platform - only if falling
        player = self.players.sprites()[0]
        hits = pg.sprite.spritecollide(player, self.platforms, False)
        dx = player.pos.x
        dy = player.pos.y

        if player.vel.y > 0:
            if hits:
                player.pos.y = hits[0].rect.top
                player.vel.y = 0

        if player.vel.y < 0:
            if hits:
                player.pos.y += 5
                player.vel.y = player.vel.y * -0.2;
                player.vel.x = player.vel.x * -1;



    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.players.sprites()[0].jump()

    def draw(self):
        # Game Loop - draw
        self.screen.fill(BLACK)
        self.players.draw(self.screen)
        self.platforms.draw(self.screen)
        # *after* drawing everything, flip the display

        # draw borders
        pg.draw.rect(self.screen, BORDER_COLOR, (0, 0, WIDTH, BORDER_THICKNESS)) # top border
        pg.draw.rect(self.screen, BORDER_COLOR, (0, HEIGHT - BORDER_THICKNESS, WIDTH, BORDER_THICKNESS)) # bottom border
        pg.draw.rect(self.screen, BORDER_COLOR, (0, 0, BORDER_THICKNESS, HEIGHT)) # left
        pg.draw.rect(self.screen, BORDER_COLOR, (WIDTH - BORDER_THICKNESS, 0, BORDER_THICKNESS, HEIGHT))
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        pass

    def show_go_screen(self):
        # game over/continue
        pass

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
