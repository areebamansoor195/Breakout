import pygame

import sys #parameters and functions
from pygame.locals import *     #copys all names in pygame.locals i
from pyparsing import col  #tool for extracting information from structured textual data


class BreakColors:
    black = pygame.Color(0, 0, 0)
    white = pygame.Color(255, 255, 255)
    pink = pygame.Color(255,20,147)   
    blue = pygame.Color(0,191,255)
    red = pygame.Color(255,0,0)
    firebrick=pygame.Color(178,34,34)
    orange=pygame.Color(255,140,0)
    purple=pygame.Color(148,0,211)
class Paddle:
    def __init__(self): #constructor #self for methods and attributes
        self.rect = pygame.Rect(0, 480-20, 160, 16) #paddle in top bottom left right

class Ball:
    def __init__(self, pos):
        self.reset(pos)

    def update(self):
        self.rect.x += self.dx #ball on x-axis 
        self.rect.y += self.dy #ball on y-axis

    def reverseY(self):
        self.dy = -self.dy  #updown back on y axis

    def reverseX(self):
        self.dx = -self.dx  #updown back on x axis

    def reset(self, pos):
        self.rect = pygame.Rect(pos, 480-32, 16, 16)     #starts with paddle up-width down-width
        self.dx = 5 #ball speed
        self.dy = -5 

class Block:
    def __init__(self, rect):
        self.rect = rect


class BreakoutGame:
    def __init__(self):
        self.running = False
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()
        self.clock = pygame.time.Clock() #paddle ball movement #create an object to help track time

        self.screenSize = self.screenWidth, self.screenHeight = (640, 480)
        pygame.display.set_caption("Breakout!!")
        pygame.mouse.set_visible(False)
        self.screen = pygame.display.set_mode(self.screenSize) #display of screen

        self.font = pygame.font.Font("fonts\PressStart2P.ttf", 16) #fonts 

        self.paddle = Paddle()
        self.ball = Ball(320)

        self.topEdge = pygame.Rect(0, 0, self.screenWidth, 16) 
        self.leftEdge = pygame.Rect(0, 0, 16, self.screenHeight)
        self.rightEdge = pygame.Rect(self.screenWidth-16, 0, 16, self.screenHeight)

        self.boopSound = pygame.mixer.Sound('sounds/boop.wav')
        self.bloopSound = pygame.mixer.Sound('sounds/bloop.wav')
        self.explosionSound = pygame.mixer.Sound('sounds/explosion.wav')

        self.lives = 2 #lives are 2
        self.score = 0

        self.blocks = [pygame.Rect(20 + self.screenWidth / 6 * x, 32 + self.screenHeight / 8 * y, 64, 16) for x in range(6) for y in range(4)]

    def run(self): #key settings
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.event.post(pygame.event.Event(QUIT))
                if event.type == MOUSEMOTION:
                    # Update the paddle position to mouse position
                    self.mousePosition = event.pos[0]
                    self.paddle.rect.x = self.mousePosition
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            self.tick()
            self.render()
            pygame.display.update()
            self.clock.tick(60)

    def tick(self):
        # Update the ball position
        self.ball.update()

        # Check for collisions with edges
        if self.ball.rect.left <= self.leftEdge.right:
            self.boopSound.play()
            self.ball.reverseX()
        elif self.ball.rect.right >= self.rightEdge.left:
            self.boopSound.play()
            self.ball.reverseX()
        if self.ball.rect.top <= self.topEdge.bottom:
            self.boopSound.play()
            self.ball.reverseY()

        # Check for collision with paddle
        if self.ball.rect.bottom >= self.paddle.rect.top and self.ball.rect.bottom <= self.screenHeight and self.ball.rect.centerx < self.paddle.rect.right and self.ball.rect.centerx > self.paddle.rect.left:
            self.bloopSound.play()
            self.ball.reverseY()

        # Check for collision with blocks
        collisionIndex = self.ball.rect.collidelist(self.blocks)
        if collisionIndex != -1:
            self.ball.reverseY()
            self.blocks.pop(collisionIndex)
            self.explosionSound.play()
            self.score += 100

        # Check for out
        if self.ball.rect.top >= self.screenHeight:
            self.lives -= 1
            self.ball.reset(self.mousePosition + 80)

        # Check if dead
        if self.lives <= 0:
            self.gameOver()

        # Check if won
        if len(self.blocks) <= 0:
            self.win()


    def render(self):
        # Clear the screen
        self.screen.fill(BreakColors.white)

        # Draw edges
        # top
        pygame.draw.rect(self.screen, BreakColors.black, self.topEdge)
        # left
        pygame.draw.rect(self.screen, BreakColors.black, self.leftEdge)
        # right
        pygame.draw.rect(self.screen, BreakColors.black, self.rightEdge)

        # Draw the paddle
        pygame.draw.rect(self.screen, BreakColors.blue, self.paddle.rect)

        # Draw the ball
        pygame.draw.rect(self.screen, BreakColors.purple, self.ball.rect)

        # draw blocks
        for block in self.blocks:
            pygame.draw.rect(self.screen, BreakColors.pink, block)

        # Draw scoreboard
        scoreSurface = self.font.render("Lives: %i Score: %i" % (self.lives, self.score), False, BreakColors.firebrick)
        self.screen.blit(scoreSurface, (16 , 16)) #score written on top

    def gameOver(self):
        messageSurface = self.font.render("You died, game over! :(", False, BreakColors.red) #text on new surface
        self.screen.blit(messageSurface, ((self.screenWidth - messageSurface.get_width())/2,240)) #game over text position
        pygame.display.update()
        pygame.time.wait(2000)	#pause the program for an amount of time
        self.resetGame()

    def win(self):
        messageSurface = self.font.render("You won, congratulations!", False, BreakColors.orange)
        self.screen.blit(messageSurface, ((self.screenWidth - messageSurface.get_width())/2,240))
        pygame.display.update()
        pygame.time.wait(2000)
        self.resetGame()

    def resetGame(self):
        self.lives = 10
        self.score = 0
        self.blocks = [pygame.Rect(32 + self.screenWidth / 6 * x, 32 + self.screenWidth / 8 * y, 64, 16) for x in range(6) for y in range(4)]


game = BreakoutGame()
game.run()
