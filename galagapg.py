# for the music that plays in background
# License: BipCot NoGov http://bipcot.org or CC-BY 3.0 https://creativecommons.org/licenses/by/3.0/
# lasers and explosions sounds from  bfxr.net
# ships from Skorpio at opengameart.org
# explosion animation from WrathGames Studio [http://wrathgames.com/blog]

import sys
import time
import pygame										# idea from kidscancode/pygame/tutorials
import random
import time
from os import path

imgdir = path.join(path.dirname(__file__),'images')					# imgdir is the directory that contains the images, contains several images many unused for now
sounddir = path.join(path.dirname(__file__),'thenoise')

WIDTH = 800										# DIMENSIONS OF THE GAME
HEIGHT = 700										# needs to fit on my laptop had to shrink it
FPS = 60										# CHANGE BETWEEN 30 AND 60

											# colors are...
BLUE = (0,0,255)
GREEN = (0,255,0)
RED = (255,0,0)
BLACK = (0,0,0)
WHITE = (255,255,255)

pygame.mixer.pre_init(22100, -16, 1, 4)											# USUAL PYGAME COMMANDS TO START THE WINDOW AND GAME
pygame.mixer.init(22100,-16,1,4)
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("THIS IS NOT GALAGA")
clock = pygame.time.Clock()

fireratelevel = 1						#THIS HAD TO BE MOVED TO THE TOP AWAY FROM THE OTHER VARIABLES THAT CAN BE UPGRADED
gamelevel = 1							# overall level of the game

def showshield(surf, x, y, amount):
	if amount < 0:
		amount = 0
	rectlen = 200
	rectheight = 10
	shellrec = pygame.Rect(x,y,rectlen, rectheight)		# encapsulates the actual shield bar
	barrec = pygame.Rect(x,y, amount, rectheight)		# the actual shield bar that changes based on shields that are left
	pygame.draw.rect(surf, GREEN, barrec)
	pygame.draw.rect(surf, BLUE, shellrec, 2)


fonttype = pygame.font.match_font('aerial')
def show_hud(psurf, text, size, x, y):
	font = pygame.font.Font(fonttype, size)
	surface = font.render(text, True, RED)
	fontrect = surface.get_rect()
	fontrect.midtop = (x,y)
	psurf.blit(surface,fontrect)


def showupgrade():
		screen.blit(background, background_rect)
		show_hud(screen, "SELECT AN UPGRADE", 64, WIDTH / 2, HEIGHT /4)
		show_hud(screen, "Current Cash:  " + str(score), 64, WIDTH / 2, 250)
		show_hud(screen, "LVL 2 FIRE RATE(a)", 32, WIDTH / 6, HEIGHT / 2)
		show_hud(screen, "LVL 3 FIRE RATE(b)", 32, WIDTH / 6, HEIGHT / 1.8)
		show_hud(screen, "LVL 2 Missles(c)", 32, WIDTH / 6, HEIGHT - 200)
		show_hud(screen, "LVL 3 Missles(d)", 32, WIDTH / 6, HEIGHT - 170)
		show_hud(screen, "LVL 2 MOVE SPEED(e)", 32, WIDTH -150, HEIGHT - 200)
		show_hud(screen, "LVL 3 MOVE SPEED(f)", 32, WIDTH -150, HEIGHT - 170)
		show_hud(screen, "LVL 2 SHIELDS(g)", 32, WIDTH -150, HEIGHT / 2)
		show_hud(screen, "LVL 3 SHIELDS(h)", 32, WIDTH - 150, HEIGHT / 1.8)
		show_hud(screen, "Press Enter Key to PLAY!", 58 , WIDTH / 2, HEIGHT * 5/6)
		pygame.display.flip()

class explosion(pygame.sprite.Sprite):
	def __init__(self,center,size):
		pygame.sprite.Sprite.__init__(self)
		self.size = size
		self.image = explosions[self.size][0]
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.frame = 0
		self.lastupdate = pygame.time.get_ticks()
		self.framerate = 50

	def update(self):
		now = pygame.time.get_ticks()
		if now - self.lastupdate > self.framerate:
			self.lastupdate = now
			self.frame += 1
			if self.frame == len(explosions[self.size]):
				self.kill()
			else:
				center = self.rect.center
				self.image = explosions[self.size][self.frame]
				self.rect = self.image.get_rect()
				self.rect.center = center

class Missle(pygame.sprite.Sprite):							# base class for pilots weapon
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)

		if misslelevel == 1:
			self.image = pygame.transform.scale(misslepic,(40,40))
			self.image = pygame.transform.rotate(misslepic,0)

		if misslelevel == 2:
			self.image = pygame.transform.scale(misslepic2,(40,40))
			self.image = pygame.transform.rotate(misslepic2,0)

		if misslelevel == 3:
			self.image = pygame.transform.scale(misslepic3,(30,30))
			self.image = pygame.transform.rotate(misslepic3,0)

		if misslelevel == 4:
			self.image = pygame.transform.scale(misslepic4,(40,40))
			self.image = pygame.transform.rotate(misslepic4,0)

		self.image.set_colorkey(BLACK)						# clearing the background of the image
		self.rect = self.image.get_rect()
		self.rect.bottom = y
		self.rect.centerx = x
		self.speedy = -20							# image speed used on update negative is up on screen
	def update(self):								# how the missle gets updated on every frame
		self.rect.y += self.speedy
		if self.rect.bottom < 0:
			self.kill()

class pilot(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(pilotpic,(50,45))
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.radius = 25							# half of the image width
		self.rect.centerx = WIDTH / 2
		self.rect.bottom = HEIGHT - 10
		#self.speedx = 0					# can adjust delay with upgrades, smaller delay THE faster weapon shoots
		if fireratelevel == 1:					# FIRERATE LEVEL WAS TESTED AND IT WORKS FINE
			self.delay = 500
		if fireratelevel == 2:
			self.delay = 300
		if fireratelevel == 3:
			self.delay = 150
		self.last_shot = pygame.time.get_ticks()
		self.shield = 200

	def fire(self):
		now = pygame.time.get_ticks()
		if now - self.last_shot > self.delay:
			self.last_shot = now

			if misslelevel == 1:								# MISSLE LEVEL WAS TESTED AND IT WORKS FINE
				missle = Missle(self.rect.centerx, self.rect.top) 			# center bullet over pilot put on top of pilot
				all_sprites.add(missle)
				missles.add(missle)
													# creating two buttlets for lvl 2 upgrade
			if misslelevel == 2:								# add another parameter to the fire function for the level of upgrade the pilot has purchased
				missle2a = Missle(self.rect.centerx - 10, self.rect.top)
				missle2b = Missle(self.rect.centerx + 10, self.rect.top)
				all_sprites.add(missle2a)
				all_sprites.add(missle2b)
				missles.add(missle2a)
				missles.add(missle2b)

			if misslelevel == 3:								# creating three bullets for lvl 3 upgrade
				missle3a = Missle(self.rect.centerx - 20, self.rect.top)
				missle3b = Missle(self.rect.centerx, self.rect.top)
				missle3c = Missle(self.rect.centerx + 20, self.rect.top)
				all_sprites.add(missle3a)
				all_sprites.add(missle3b)
				all_sprites.add(missle3c)
				missles.add(missle3a)
				missles.add(missle3b)
				missles.add(missle3c)

			bulletsnd1.play()

	def update(self):
		self.speedx = 0								# lateral speeds
		self.speedy = 0
		keystate = pygame.key.get_pressed()					# can only used key presses
		if keystate[pygame.K_LEFT] or keystate[pygame.K_a] or keystate[pygame.K_KP4]:
			if speedlevel == 1:						# SPEED LEVEL WAS TESTED AND IT WORKS FINE
				self.speedx = -5
			if speedlevel == 2:
				self.speedx = -10
			if speedlevel == 3:
				self.speedx = -15
		if keystate[pygame.K_RIGHT] or keystate[pygame.K_d] or keystate[pygame.K_KP6]:
			if speedlevel == 1:
				self.speedx = 5
			if speedlevel == 2:
				self.speedx = 10
			if speedlevel == 3:
				self.speedx = 15
		if keystate[pygame.K_UP] or keystate[pygame.K_w] or keystate[pygame.K_KP8]:
			if speedlevel == 1:
				self.speedy = -5
			if speedlevel == 2:
				self.speedy = -10
			if speedlevel == 3:
				self.speedy = -15
		if keystate[pygame.K_DOWN] or keystate[pygame.K_s] or keystate[pygame.K_KP5]:
			if speedlevel == 1:
				self.speedy = 5
			if speedlevel == 2:
				self.speedy = 10
			if speedlevel == 3:
				self.speedy = 15
		if keystate[pygame.K_SPACE]:
			self.fire()
		self.rect.x += self.speedx
		self.rect.y += self.speedy
		if  self.rect.right > WIDTH:
			self.rect.right = WIDTH
		if self.rect.left < 0:
			self.rect.left = 0
		if self.rect.bottom > HEIGHT:
			self.rect.bottom = HEIGHT
		if self.rect.top < 0:
			self.rect.top = 0

class enemy(pygame.sprite.Sprite):							# basic enemy ship class
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

		if gamelevel == 1:
			self.image = pygame.transform.scale(enemypic,(50,50))
			self.image.set_colorkey(BLACK)

		if gamelevel == 2:
			self.image = pygame.transform.scale(enemypic2,(60,60))
			self.image.set_colorkey(BLACK)

		if gamelevel == 3:
			self.image = pygame.transform.scale(enemypic3,(70,70))
			self.image.set_colorkey(BLACK)

		if gamelevel == 4:
			self.image = pygame.transform.scale(enemypic4,(80,80))
			self.image.set_colorkey(BLACK)

		if gamelevel == 5:
			self.image = pygame.transform.scale(enemypic5,(90,90))
			self.image.set_colorkey(BLACK)

		self.rect = self.image.get_rect()							# half of image width
		self.radius = int(self.rect.width * .85 / 2)
		self.rect.x = random.randrange(0 + self.rect.width  , WIDTH - self.rect.width )
		self.rect.y = random.randrange(-100,-40)
		self.speedy = random.randrange(10,20)
		self.speedx = random.randrange(-1,1)
	def update(self):								# update on each frame
		self.rect.x += self.speedx
		self.rect.y += self.speedy
		if self.rect.top > HEIGHT + 10 or self.rect.left < -30 or self.rect.right > WIDTH + 30:
			self.rect.x = random.randrange(0 + self.rect.width * 2 , WIDTH - self.rect.width * 2)
			self.rect.y = random.randrange(-100,-40)
			self.speedy = random.randrange(10,20)

										# images
										#class for the selector in menus(IN ALL MENUS MAKE SURE TO RUN UPDATE TO ENSURE THE SELECTOR RESPONDS TO ARROW KEYS)
class selector(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(selectorPic, (20,20))
		#self.image.set_colorkey(WHITE)########come back to this, can't get background to go away
		self.rect = self.image.get_rect()
		self.rect.x = pause_rec.x + pause_rec.width/4
		self.rect.y = pause_rec.y + pause_rec.height/4 		#initialize over the resume
	def draw(self):							#draw the selector
		screen.blit(self.image,self.rect)


background = pygame.image.load(path.join(imgdir, "space.png")).convert()
background_rect = background.get_rect()

pilotpic = pygame.image.load(path.join(imgdir, "alienship.png")).convert()

enemypic = pygame.image.load(path.join(imgdir, "enemy2.png")).convert()
enemypic2 = pygame.image.load(path.join(imgdir, "lvl2enemy.png")).convert()
enemypic3 = pygame.image.load(path.join(imgdir, "lvl3enemy.png")).convert()
enemypic4 = pygame.image.load(path.join(imgdir, "lvl4enemy.png")).convert()
enemypic5 = pygame.image.load(path.join(imgdir, "lvl5enemy.png")).convert()

misslepic = pygame.image.load(path.join(imgdir, "rocket3.png")).convert()
misslepic2 = pygame.image.load(path.join(imgdir, "lvl2missle.png")).convert()
misslepic3 = pygame.image.load(path.join(imgdir, "lvl3missle.png")).convert()
misslepic4 = pygame.image.load(path.join(imgdir, "lvl4missle.png")).convert()

pausePic = pygame.image.load(path.join(imgdir, "pauseMenu.png")).convert()
														#pause rec details
pause_rec = pausePic.get_rect()						#gets a rectangle to draw pause menu onto based off of size of pic
pause_rec.x = background_rect.x + (WIDTH/2 - pause_rec.width/2)
pause_rec.y = background_rect.y + (HEIGHT/2 - pause_rec.height/2)

homePic = pygame.image.load(path.join(imgdir, "homePage.png")).convert()
selectorPic = pygame.image.load(path.join(imgdir, "selector.png")).convert()
										#selector details
selectorPauseImage = pygame.transform.scale(selectorPic, (20,20))
										#self.image.set_colorkey(WHITE)########come back to this, can't get background to go away
selectrect = selectorPauseImage.get_rect()
selectrect.x = pause_rec.x + pause_rec.width/4
selectrect.y = pause_rec.y + pause_rec.height/2					#initialize over the resume
										#selector for main menu	##??
#selector for main menu
selectorMainImage = pygame.transform.scale(selectorPic, (30, 30))
selectorMainImage.fill(GREEN)
selectMainRect = selectorMainImage.get_rect()
#init main selector next to commence    go back and change these to relative coordiantes
selectMainRect.x = 275
selectMainRect.y = 125

#positions on main menu

explosions = {}
explosions['big'] = []				# can be used for bigger enemies
explosions['small'] = []
for x in range (1,91):
	explfile = 'explosion1_{}.png'.format(x)
	explimg = pygame.image.load(path.join(imgdir,explfile)).convert()
	explimg.set_colorkey(BLACK)
	bigexplimg = pygame.transform.scale(explimg,(75,75))
	explosions['big'].append(bigexplimg)
	smallexplimg = pygame.transform.scale(explimg,(40,40))
	explosions['small'].append(smallexplimg)
										#sounds
bulletsnd1 = pygame.mixer.Sound(path.join(sounddir,"Laser_Shoot.wav"))
explsnd1 = pygame.mixer.Sound(path.join(sounddir,"Explosion8.wav"))
pygame.mixer.music.load(path.join(sounddir,"09 - Overdrive Sex Machine v0_5.mp3"))	# dont mind the name

all_sprites = pygame.sprite.Group()
missles = pygame.sprite.Group()
enemies = pygame.sprite.Group()							# group of enemies
pilot1 = pilot()
all_sprites.add(pilot1)

for i in range(5):								# adding random blocks for enemies
	e = enemy()
	all_sprites.add(e)
	enemies.add(e)


#fireratelevel = 1					moved to top of file could not be seen by pilot constructor.  determines how quickly the pilot can fire used in pilot class, all of these variables manipulate values in pilot class
misslelevel = 1						# level of missle upgrades one is base level determines number of rockets to shoot
shieldlevel = 1						# level of shield upgrades 1 are base shields, as we upgrade we take less dmg from hits as handled below in COLLISIONS SECTION
speedlevel = 1						# these should probably become instance variables of the pilot class, base level for speed of pilot
lives = 3						# create get and set functions for these instance variables later
							# maybe amount of money the character has to buy upgrades
score = 0						# for MAIN LOOP FOR THE GAME
run = True


posChecker = 1
pygame.mixer.music.play(loops = -1)
pygame.mixer.music.set_volume(10.0)
gameState = "upgrade"
while run:
	clock.tick(FPS)
	if (gameState == "upgrade"):
		showupgrade()
		pygame.display.flip()
		waiting = True
		while waiting:								# do keys for purchase here
			clock.tick(FPS)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
				if event.type == pygame.KEYDOWN:
					keystate = pygame.key.get_pressed()
					if keystate[pygame.K_RETURN]:
						gameState = "play"
						waiting = False
					if keystate[pygame.K_ESCAPE]:
						gameState = "play"
						waiting = False
					if keystate[pygame.K_a] and fireratelevel == 1 and score >= 1000:	# only let them get better equipment
						fireratelevel = 2
						score = score - 1000
						showupgrade()
					if keystate[pygame.K_b] and fireratelevel == 2 and score >= 3000:
						fireratelevel = 3
						score = score - 3000
						showupgrade()
					if keystate[pygame.K_c] and misslelevel == 1 and score >= 1000:
						misslelevel = 2
						score = score - 1000
						showupgrade()
					if keystate[pygame.K_d] and misslelevel == 2 and score >= 3000:		# and score above the necessary level
						misslelevel = 3
						score = score - 3000
						showupgrade()
					if keystate[pygame.K_e] and speedlevel == 1 and score >= 1000:
						speedlevel = 2
						score = score - 1000
						showupgrade()
					if keystate[pygame.K_f] and speedlevel == 2 and score >= 3000:
						speedlevel = 3
						score = score - 3000
						showupgrade()
					if keystate[pygame.K_g] and shieldlevel == 1 and score >= 1000:
						shieldlevel = 2
						score = score - 1000
						showupgrade()
					if keystate[pygame.K_h] and shieldlevel == 2 and score >= 3000:
						shieldlevel = 3
						score = score - 3000
						showupgrade()
		screen.fill(BLACK)
		screen.blit(background, background_rect)
		all_sprites.draw(screen)
		gameState = "play"

	if (gameState == "over"):

		speedlevel = 1				#resetting the game , ship, score, and cash once the game is over
		misslelevel = 1
		fireratelevel = 1
		gamelevel = 1
		shieldlevel = 1
		score = 0				# moved this down like 10 lines so proper score showed
		lives = 3

		screen.blit(background, background_rect)
		show_hud(screen, "GAME OVER!", 64, WIDTH / 2, HEIGHT /4)
		show_hud(screen, "Score: " + str(score), 64, WIDTH / 2, HEIGHT / 2)
		score = 0
		show_hud(screen, "Press Enter Key to Restart", 58 , WIDTH / 2, HEIGHT * 3/4)
		show_hud(screen,"Press Esc to Exit", 40, WIDTH / 2, HEIGHT * 7/8)
		pygame.display.flip()
		waiting = True
		while waiting:
			clock.tick(FPS)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
				if event.type == pygame.KEYDOWN:
					keystate = pygame.key.get_pressed()
					if keystate[pygame.K_RETURN]:
						all_sprites = pygame.sprite.Group()
						missles = pygame.sprite.Group()
						enemies = pygame.sprite.Group()       # group of enemies
						pilot1 = pilot()
						all_sprites.add(pilot1)

						for i in range(5):
							e = enemy()
							all_sprites.add(e)
							enemies.add(e)
						lives = 3
						score = 0
						waiting = False
					if keystate[pygame.K_ESCAPE]:
						pygame.quit()

		screen.fill(BLACK)
		screen.blit(background, background_rect)
		all_sprites.draw(screen)
		show_hud(screen, "SCORE: " + str(score) + "    LIVES: " + str(lives), 28, WIDTH/4 , 8 )
		pygame.display.flip()
		gameState = "play"

	if(gameState == "play"):
		#print("Game state play")												#game state is play
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			elif event.type == pygame.KEYDOWN:
				#print("key pressed")
				if event.key == pygame.K_p:  										#checks for pause button to be pressed
					gameState = "pause"
				if event.key == pygame.K_u:
					gameState = "upgrade"
		all_sprites.update()													# update all the sprites

		collisions = pygame.sprite.groupcollide(enemies,missles, True, True) 							# first true to delete enemy second true to delete missle as it has exploded
		for col in collisions:
			explsnd1.play()
			explshow = explosion(col.rect.center, 'big')									# did a missle hit an enemy
			all_sprites.add(explshow)											# could have multiple of these functions for each enemy
			#score += 100
			if score >= 1000 and score < 2000:
				gamelevel = 2
			if score >= 2000 and score < 3000:
				gamelevel = 3
			if score >= 3000 and score < 4000:
				gamelevel = 4
			if score >= 4000:
				gamelevel = 5
			if gamelevel == 1:
				score += 100
			if gamelevel == 2:
				score += 200
			if gamelevel == 3:
				score += 300
			if gamelevel == 4:
				score += 400
			if gamelevel == 5:
				score += 500
			e = enemy()
			all_sprites.add(e)
			enemies.add(e)

		collisions = pygame.sprite.spritecollide(pilot1, enemies, True, pygame.sprite.collide_circle)	# see if enemy ran into the pilot
		for col in collisions:
														# this could work if we make bigger enemies for harder levels
			if shieldlevel == 1:
				pilot1.shield -= col.radius * 5	* 1						# reduce the shield, lives will be dependent on this value, 2 hits = 1 live here
			if shieldlevel == 2:
				pilot1.shield -= col.radius * 5 * 0.70						# 3 hits equal 1 live
			if shieldlevel ==3:
				pilot1.shield -= col.radius * 5 * 0.50						# tank 4 hits before live is taken
			if pilot1.shield <= 0:
				lives = lives - 1
				pilot1.shield = 200
			if lives == 0:
				gameState = "over"
			explshow = explosion(col.rect.center, 'big')						# bigger faster enemies = more shield dmg
			all_sprites.add(explshow)
			explsnd1.play()
			e = enemy()
			all_sprites.add(e)
			enemies.add(e)

		screen.fill(BLACK)
		screen.blit(background, background_rect)
		all_sprites.draw(screen)
		show_hud(screen, "SCORE: " + str(score) + "    LIVES: " + str(lives), 28, WIDTH/4, 8 )		# blits all sprites onto screen
		showshield(screen, 380, 10, pilot1.shield)
		pygame.display.flip()

		#screen.fill(BLACK)
		#screen.blit(background, background_rect)
		#all_sprites.draw(screen)									# blits all sprites onto screen
		#pygame.display.flip()
	if(gameState == "pause"):										#check for events and positions
		resumePos = pause_rec.y + pause_rec.height/2
		quitPos = pause_rec.y + pause_rec.height/2 + pause_rec.height/7
		#########################
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_p:			#if game is set back to play remove the selector sprite
					gameState = "play"
				elif event.key == pygame.K_UP:			# and selectrect.y > (pause_rec.y + pause_rec.height/2):	is below it's initial pos
					posChecker = 1
					selectrect.y = resumePos
				elif event.key == pygame.K_DOWN:		# and selectrect.y < (pause_rec.y + pause_rec.height/2 - pause_rec.height/8):
					posChecker = 0
					selectrect.y = quitPos
				elif event.key == pygame.K_RETURN:		# WAS RETURN
					print(posChecker)
					if(posChecker == 0):
						gameState = "Main Menu"
					elif(posChecker == 1):
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
													# exit game and window
	if(gameState == "Main Menu"):
		#change screen size
		mainRect = homePic.get_rect()
		if(screen.get_rect().width != mainRect.width):
			screen = pygame.display.set_mode((mainRect.width, mainRect.height))
		#positions for selector
		commencePos = 125
		upgradesPos = 200
		settingsPos = 275
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				print("Quiting...")
				# FOLLOWING LINES WILL GET YOU TO ACTUAL GAME READJUSTING THE SCREEN SIZE
				#screen = pygame.display.set_mode((WIDTH, HEIGHT))
				#screen.fill(BLACK)
				#screen.blit(background, background_rect)
				#all_sprites.draw(screen)
				#show_hud(screen, str(score), 18, WIDTH / 2, 10)
				#pygame.display.flip()
				#gameState = "play"
				run = False
			elif event.type == pygame.KEYDOWN:
			#	print("Key pressed")
			#	print(commencePos)
			#	print(selectMainRect.y)
				if event.key == pygame.K_UP:
					if(selectMainRect.y == upgradesPos):
						selectMainRect.y = commencePos
					elif(selectMainRect.y == settingsPos):
						selectMainRect.y = upgradesPos
				elif event.key == pygame.K_DOWN:
					#print("Key down pressed..")
					if(selectMainRect.y == commencePos):
						selectMainRect.y = upgradesPos
			#			print("Shoudl be on upgrades")
					elif(selectMainRect.y == upgradesPos):
						selectMainRect.y = settingsPos
				elif event.key == pygame.K_RETURN:
					if(selectMainRect.y == commencePos):
						gameState = "play"
						screen = pygame.display.set_mode((WIDTH, HEIGHT))
						#gameState = "play"
					elif(selectMainRect.y == upgradesPos):
						gameState = "upgrade"
					elif(selectMainRect.y == settingsPos):
						screen = pygame.display.set_mode((WIDTH, HEIGHT))
						gameState = "settings"
		#Selector for main menu
		#draw the menu
		screen.fill(BLACK)
		screen.blit(homePic, mainRect)
		#now draw mainSelect
		screen.blit(selectorMainImage,selectMainRect)
		pygame.display.flip()

	#screen.fill(BLACK)
	#screen.blit(background, background_rect)
	#all_sprites.draw(screen)
	#show_hud(screen, str(score), 18, WIDTH / 2, 10)
	#pygame.display.flip()
pygame.quit()

