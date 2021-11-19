# Kaih White
# 4/12/2021
# Pong

import math
import sys
import random as ra
import pygame as pg
import time


class Paddle():
    def __init__(self, startpos, speed, col, leng, wid, screen, up, down):
        super().__init__()
        self.color = col
        self.screen = screen
        self.rect = pg.Rect(startpos[0], startpos[1], wid, leng)
        self.speed = speed
        self.up = up
        self.down = down
        self.vel = 0

    def update(self):
        if pg.key.get_pressed()[self.up] and pg.key.get_pressed()[self.down]:
            self.vel = 0
        elif pg.key.get_pressed()[self.up]:
            if self.rect.top > 0:
                self.vel = -self.speed
            else:
                self.vel = 0
        elif pg.key.get_pressed()[self.down]:
            if self.rect.bottom < self.screen.get_height():
                self.vel = self.speed
            else:
                self.vel = 0
        else:
            self.vel = 0

        self.rect = self.rect.move(0, self.vel)

    def draw(self):
        pg.draw.rect(self.screen, self.color, self.rect)

    def collision(self):
        return self.rect


class Ball():
    def __init__(self, startpos, vel, col, rad, ang, screen):
        super().__init__()
        self.color = col
        self.screen = screen
        self.vel = vel
        self.rad = rad
        size = rad * 2
        self.rect = pg.Rect(startpos[0], startpos[1], size, size)
        self.ang = math.radians(ang)
        self.pos = self.rect.center
        self.score = [0, 0]

    def update(self, player1, player2):
        dx = self.vel * math.cos(self.ang)
        dy = self.vel * math.sin(self.ang)
        self.pos = (self.pos[0] + dx, self.pos[1] + dy)
        self.rect.center = round(self.pos[0]), round(self.pos[1])

        if self.rect.top > self.screen.get_height() or self.rect.bottom < 0:
            self.ang = -self.ang

        if player1.top <= self.rect.center[1] <= player1.bottom:
            if self.rect.center[0] < player1.right:
                ra.seed(((player1.top+player1.bottom)/2)-self.rect.center[1])
                self.ang = (math.pi-self.ang)-ra.randint(0, round(math.pi/4))
        if player2.top <= self.rect.center[1] <= player2.bottom:
            if self.rect.center[0] > player2.left:
                ra.seed(((player2.top+player2.bottom)/2)-self.rect.center[1])
                self.ang = (math.pi-self.ang)-ra.randint(0, round(math.pi/4))

        if self.rect.right < -50:
            self.score[1] = self.score[1]+1
            self.pos = [self.screen.get_width()/2, self.screen.get_height()/2]
            self.ang = math.pi
        if self.rect.left > self.screen.get_width()+50:
            self.score[0] = self.score[0]+1
            self.pos = [self.screen.get_width()/2, self.screen.get_height()/2]
            self.ang = 0

    def draw(self):
        pg.draw.circle(self.screen, self.color, self.rect.center, self.rad)


def main():
    white = (255, 255, 255)
    red = (255, 0, 0)
    blue = (0, 0, 255)
    green = (0, 255, 0)
    ballspeed = 0
    paddlespeed = 0
    paddlelength = 0
    ballrad = 0
    winscore = 0

    while 1:
        print("\nHello! Welcome to Kaih's Pong!\n")
        change = input("Would you like to use default settings or edit colors, sizes and speeds? Input 1 to edit: ")
        if change == "1":

            userinput = input("\nBall color: 1 - white | 2 - red | 3 - blue | 4 - green\n")
            if userinput == "2":
                ballcolor = red
                print("\nYou chose red\n")
            elif userinput == "3":
                ballcolor = blue
                print("\nYou chose blue\n")
            elif userinput == "4":
                ballcolor = green
                print("\nYou chose green\n")
            else:
                ballcolor = white
                print("\nYou chose white\n")

            userinput = input("Paddle color: 1 - white | 2 - red | 3 - blue | 4 - green\n")
            if userinput == "2":
                paddlecolor = red
                print("\nYou chose red\n")
            elif userinput == "3":
                paddlecolor = blue
                print("\nYou chose blue\n")
            elif userinput == "4":
                paddlecolor = green
                print("\nYou chose green\n")
            else:
                paddlecolor = white
                print("\nYou chose white\n")

            userinput = input("\nEnter a speed for the ball that is greater than 0 (1 is already fast): ")
            for item in userinput:
                if "0" <= item <= "9":
                    pass
                else:
                    ballspeed = 1
                    print("\nThat was either not an integer or less than 0\n")
                    break
            if ballspeed != 1:
                ballspeed = int(userinput)

            userinput = input("\nEnter a speed for the paddles that is greater than 0 (1 is already fast): ")
            for item in userinput:
                if "0" <= item <= "9":
                    pass
                else:
                    paddlespeed = 1
                    print("\nThat was either not an integer or less than 1\n")
                    break
            if paddlespeed != 1:
                paddlespeed = int(userinput)

            userinput = input("\nEnter paddle length greater than 0 and less than 200: ")
            for item in userinput:
                if "0" <= item <= "9":
                    pass
                else:
                    paddlelength = 50
                    print("\nThat was either not an integer or less than 1\n")
                    break
            if paddlelength != 50:
                paddlelength = int(userinput)
                if paddlelength > 200 or paddlelength < 1:
                    paddlelength = 50
                    print("\nNice try. You get default now.\n")

            userinput = input("\nEnter ball radius greater than 0 and less than 50: ")
            for item in userinput:
                if "0" <= item <= "9":
                    pass
                else:
                    ballrad = 9
                    print("\nThat was either not an integer or less than 1\n")
                    break
            if ballrad != 9:
                ballrad = int(userinput)
                if ballrad > 50 or ballrad < 1:
                    ballrad = 9
                    print("\nNice try. You get default now.\n")

            userinput = input("\nEnter the number of points to win from 1 to 10: ")
            for item in userinput:
                if "0" <= item <= "9":
                    pass
                else:
                    winscore = 2
                    print("\nThat was either not an integer or less than 1\n")
                    break
            if winscore != 2:
                winscore = int(userinput) - 1
                if winscore > 10 or winscore < 0:
                    winscore = 2
                    print("\nNice try. You get default now.\n")

        else:
            print("\nYou selected default\n")
            ballspeed = 1
            paddlespeed = 1
            paddlelength = 50
            ballrad = 9
            ballcolor = white
            paddlecolor = white
            winscore = 2

        print("\nGet ready, the window will open but it will not push to front, you will need to click on the window.")
        print("Player 1 (left) uses the up and down arrow keys. Player 2 (right) uses w and s keys.")
        print("Keep clicking on the window. I made it wait 3 seconds to start so that you would have time to react.")


        pg.init()
        size = width, height = 1280, 720
        screen = pg.display.set_mode(size)
        player1 = Paddle((1, height/2), paddlespeed, paddlecolor, paddlelength, 10, screen, pg.K_UP, pg.K_DOWN)
        player2 = Paddle((width - 11, height/2), paddlespeed, paddlecolor, paddlelength, 10, screen, pg.K_w, pg.K_s)
        ball = Ball((width/2, height/2), ballspeed * -1, ballcolor, ballrad, 0, screen)

        time.sleep(3)

        while 1:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()

            player1.update()
            player2.update()
            ball.update(player1.collision(), player2.collision())

            screen.fill((0, 0, 0))
            player1.draw()
            player2.draw()
            ball.draw()
            pg.display.flip()
            score = ball.score

            if score[0] > winscore:
                print("\nPlayer 1 Won!\n")
                pg.display.quit()
                break
            elif score[1] > winscore:
                print("\nPlayer 2 Won!\n")
                pg.display.quit()
                break
        again = input("\nDo you want to play again? 1 for yes, anything else to quit: ")
        if again == "1":
            continue
        pg.display.quit()
        pg.quit()
        sys.exit(0)


if __name__ == '__main__':
    main()
