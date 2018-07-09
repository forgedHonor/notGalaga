import pygame		# idea from kidscancode/pygametutorials
import random
import time
from os import path

imgdir = path.join(path.dirname(__file__),'images')

WIDTH = 480		# DIMENSIONS OF THE GAME
HEIGHT = 600
FPS = 60		# CHANGE BETWEEN 30 AND 60

# colors are...
BLUE = (0,0,255)
GREEN = (0,255,0)
RED = (255,0,0)
BLACK = (0,0,0)
WHITE = (255,255,255)

# USUAL PYGAME COMMANDS TO START THE WINDOW AND GAME
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("THIS IS NOT GALAGA")
clock = pygame.time.Clock()

class Missle(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(misslepic,(40,40))
		self.image = pygame.transform.rotate(misslepic,0)
		self.image.set_colorkey(BLACK)
		#self.image.fill(BLUE)
		self.rect = self.image.get_rect()
		self.rect.bottom = y
		self.rect.centerx = x
		self.speedy = -20
	def update(self):
		self.rect.y += self.speedy
		if self.rect.bottom < 0:
			self.kill()

class pilot(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(pilotpic,(50,45))
		self.image.set_colorkey(BLACK)
		#self.image.fill(GREEN)
		self.rect = self.image.get_rect()
		self.rect.centerx = WIDTH / 2
		self.rect.bottom = HEIGHT - 10
		self.speedx = 0

	def fire(self):
		missle = Missle(self.rect.centerx, self.rect.top) # center bullet over pilot put on top of pilot
		all_sprites.add(missle)
		missles.add(missle)

	def update(self):
		self.speedx = 0				# instance var self.
		self.speedy = 0
		keystate = pygame.key.get_pressed()	# can only used key presses
		if keystate[pygame.K_LEFT]:
			self.speedx = -5
		if keystate[pygame.K_RIGHT]:
			self.speedx = 5
		if keystate[pygame.K_UP]:
			self.speedy = -5
		if keystate[pygame.K_DOWN]:
			self.speedy = 5
		self.rect.x += self.speedx
		self.rect.y += self.speedy
		if  self.rect.right > WIDTH:
			self.rect.right = WIDTH
		if self.rect.left < 0:
			self.rect.left = 0
		if self.rect.bottom > 600:
			self.rect.bottom = 600
		if self.rect.top < 0:
			self.rect.top = 0

class enemy(pygame.sprite.Sprite):		# enemy ship class
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(enemypic, (30,30))
		self.image.set_colorkey(BLACK)
		#self.image.fill(RED)
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(WIDTH - self.rect.width)
		self.rect.y = random.randrange(-100,-40)
		self.speedy = random.randrange(1,10)
		self.speedx = random.randrange(-5,5)
	def update(self):
		self.rect.x += self.speedx
		self.rect.y += self.speedy
		if self.rect.top > HEIGHT + 10 or self.rect.left < -30 or self.rect.right > WIDTH + 30:
			self.rect.x = random.randrange(WIDTH - self.rect.width)
			self.rect.y = random.randrange(-100,-40)
			self.speedy = random.randrange(1,10)

#class for the selector in menus(IN ALL MENUS MAKE SURE TO RUN UPDATE TO ENSURE THE SELECTOR RESPONDS TO ARROW KEYS)
class selector(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(selectorPic, (20,20))
		#self.image.set_colorkey(WHITE)########come back to this, can't get background to go away
		self.rect = self.image.get_rect()
		self.rect.x = pause_rec.x + pause_rec.width/4
		self.rect.y = pause_rec.y + pause_rec.height/4 #initialize over the resume
	def draw(self):	#draw the selector
		screen.blit(self.image,self.rect)		
		


background = pygame.image.load(path.join(imgdir, "space.png")).convert()
background_rect = background.get_rect()
pilotpic = pygame.image.load(path.join(imgdir, "alienship.png")).convert()
enemypic = pygame.image.load(path.join(imgdir, "enemy2.png")).convert()
misslepic = pygame.image.load(path.join(imgdir, "rocket3.png")).convert()
pausePic = pygame.image.load(path.join(imgdir, "pauseMenu.png")).convert()
#pause rec details
pause_rec = pausePic.get_rect()#gets a rectangle to draw pause menu onto based off of size of pic
pause_rec.x = background_rect.x + (WIDTH/2 - pause_rec.width/2)
pause_rec.y = background_rect.y + (HEIGHT/2 - pause_rec.height/2)

homePic = pygame.image.load(path.join(imgdir, "homePage.png")).convert()
selectorPic = pygame.image.load(path.join(imgdir, "selector.png")).convert()
#selector details
selectorPauseImage = pygame.transform.scale(selectorPic, (20,20))
#self.image.set_colorkey(WHITE)########come back to this, can't get background to go away
selectrect = selectorPauseImage.get_rect()
selectrect.x = pause_rec.x + pause_rec.width/4
selectrect.y = pause_rec.y + pause_rec.height/2 #initialize over the resume
#selector for main menu
selectorMainImage = pygame.transform.scale(selectorPic, (30, 30))
selectorMainImage.fill(GREEN)
selectMainRect = selectorMainImage.get_rect()
#init main selector next to commence                                         # go back and change these to relative coordiantes
selectMainRect.x = selectMainRect.x + 275 
selectMainRect.y = selectMainRect.y + 125

#positions on main menu


all_sprites = pygame.sprite.Group()
missles = pygame.sprite.Group()
enemies = pygame.sprite.Group()		# group of enemies
pilot1 = pilot()
all_sprites.add(pilot1)

for i in range(5):			# adding random blocks for enemies
	e = enemy()
	all_sprites.add(e)
	enemies.add(e)

#MAIN LOOP FOR THE GAME
run = True
gameState = "play"
while run:
	clock.tick(FPS)
	if(gameState=="play"):#game state is play-----------------------------
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					pilot1.fire()
				elif event.key == pygame.K_p:#checks for pause button to be pressed
					gameState = "pause"
		all_sprites.update()				# update all the sprites
		#seperate path for paused gamestate	
	#	elif(gameState == "play"):
		collisions = pygame.sprite.groupcollide(enemies,missles, True, True) # first true to delete enemy second true to delete missle as it has exploded
		for col in collisions:
			e = enemy()
			all_sprites.add(e)
			enemies.add(e)
		collisions = pygame.sprite.spritecollide(pilot1, enemies, False)	# see if pilot hit an enemy
		if collisions:
			run = False
		screen.fill(BLACK)
		screen.blit(background, background_rect)
		all_sprites.draw(screen)		# blits all sprites onto screen
		pygame.display.flip()
	elif(gameState=="pause"):
		#check for events
		#positions
		resumePos = pause_rec.y + pause_rec.height/2
		quitPos = pause_rec.y + pause_rec.height/2 + pause_rec.height/7
		#########################
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_p:##if game is set back to play remove the selector sprite
					gameState = "play"
				elif event.key ==pygame.K_UP:# and selectrect.y > (pause_rec.y + pause_rec.height/2):#is below it's initial pos
					selectrect.y = resumePos
				elif event.key == pygame.K_DOWN:# and selectrect.y < (pause_rec.y + pause_rec.height/2 - pause_rec.height/8):
					selectrect.y = quitPos
				elif event.key == pygame.K_RETURN:
					if(selectrect.y == quitPos):
						run = False
					elif(selectrect.y == resumePos):
						gameState = "play"			
		#draw menu 
		screen.fill(BLACK)
                screen.blit(background, background_rect)
		##########################
                all_sprites.draw(screen) 
		#draw the selector and pause menu
		screen.blit(pausePic, pause_rec)
		#now for selector
                screen.blit(selectorPauseImage,selectrect)
		pygame.display.flip()
	elif(gameState=="Main Menu"):
		#change screen size
		mainRect = homePic.get_rect()
		if(screen.get_rect().width != mainRect.width):
			screen = pygame.display.set_mode((mainRect.width, mainRect.height))
		#positions for selector
		commencePos = selectMainRect.y + 125
		upgradesPos = selectMainRect.y + 150
		settingsPos = selectMainRect.y + 175	
		for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                print("Quiting...")
				run = False
			elif event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_UP:# 
                                        if(selectMainRect.y == upgradesPos):
						selectMainRect.y = commencePos
					elif(selectMainRect.y == settingsPos):
						selectMainRect.y = upgradesPos
                                elif event.key == pygame.K_DOWN:#
					if(selectMainRect.y == commencePos):
						selectMainRect.y = upgrades.pos
		#Selector for main menu
		
		#draw the menu
		screen.fill(BLACK)
		screen.blit(homePic, mainRect)
		#now draw mainSelect
		screen.blit(selectorMainImage,selectMainRect)
		pygame.display.flip()	
		
pygame.quit					# exit game and window

#function to draw the pause menu
#maybe add
	
