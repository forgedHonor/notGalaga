# for the music that plays in background
#License: BipCot NoGov http://bipcot.org or CC-BY 3.0 https://creativecommons.org/licenses/by/3.0/
# lasers and explosions sounds from  bfxr.net
# ships from Skorpio at opengameart.org
# explosion animation from WrathGames Studio [http://wrathgames.com/blog]


import time
import pygame										# idea from kidscancode/pygame/tutorials
import random
from os import path

imgdir = path.join(path.dirname(__file__),'images')					# imgdir is the directory that contains the images, contains several images many unused for now
sounddir = path.join(path.dirname(__file__),'thenoise')

WIDTH = 600										# DIMENSIONS OF THE GAME
HEIGHT = 800
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
pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))		# invisible cursor

fonttype = pygame.font.match_font('aerial')
def show_hud(psurf, text, size, x, y):
	font = pygame.font.Font(fonttype, size)
	surface = font.render(text, True, GREEN)
	fontrect = surface.get_rect()
	fontrect.midtop = (x,y)
	psurf.blit(surface,fontrect)

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
		self.image = pygame.transform.scale(misslepic,(40,40))
		self.image = pygame.transform.rotate(misslepic,0)
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
		self.speedx = 0					# can adjust delay with upgrades, smaller delay faster weapon shoots
		self.delay = 250
		self.last_shot = pygame.time.get_ticks()

	def fire(self):
		now = pygame.time.get_ticks()
		if now - self.last_shot > self.delay:
			self.last_shot = now
			missle = Missle(self.rect.centerx, self.rect.top) 			# center bullet over pilot put on top of pilot
			all_sprites.add(missle)
			missles.add(missle)
			bulletsnd1.play()

	def update(self):
		self.speedx = 0								# lateral speeds
		self.speedy = 0
		keystate = pygame.key.get_pressed()					# can only used key presses
		if keystate[pygame.K_LEFT] or keystate[pygame.K_a] or keystate[pygame.K_KP4]:
			self.speedx = -5
		if keystate[pygame.K_RIGHT] or keystate[pygame.K_d] or keystate[pygame.K_KP6]:
			self.speedx = 5
		if keystate[pygame.K_UP] or keystate[pygame.K_w] or keystate[pygame.K_KP8]:
			self.speedy = -5
		if keystate[pygame.K_DOWN] or keystate[pygame.K_s] or keystate[pygame.K_KP5]:
			self.speedy = 5
		if keystate[pygame.K_SPACE]:
			self.fire()
		self.rect.x += self.speedx
		self.rect.y += self.speedy
		if  self.rect.right > WIDTH:
			self.rect.right = WIDTH
		if self.rect.left < 0:
			self.rect.left = 0
		if self.rect.bottom > 800:
			self.rect.bottom = 800
		if self.rect.top < 0:
			self.rect.top = 0

class enemy(pygame.sprite.Sprite):							# basic enemy ship class
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(enemypic, (30,30))
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()							# half of image width
		self.radius = int(self.rect.width * .85 / 2)
		self.rect.x = random.randrange(WIDTH - self.rect.width)
		self.rect.y = random.randrange(-100,-40)
		self.speedy = random.randrange(1,10)
		self.speedx = random.randrange(-5,5)
	def update(self):								# update on each frame
		self.rect.x += self.speedx
		self.rect.y += self.speedy
		if self.rect.top > HEIGHT + 10 or self.rect.left < -30 or self.rect.right > WIDTH + 30:
			self.rect.x = random.randrange(WIDTH - self.rect.width)
			self.rect.y = random.randrange(-100,-40)
			self.speedy = random.randrange(1,10)

										# images
background = pygame.image.load(path.join(imgdir, "space.png")).convert()
background_rect = background.get_rect()
pilotpic = pygame.image.load(path.join(imgdir, "alienship.png")).convert()
enemypic = pygame.image.load(path.join(imgdir, "enemy2.png")).convert()
misslepic = pygame.image.load(path.join(imgdir, "rocket3.png")).convert()

explosions = {}
explosions['big'] = []				# can be used for bigger enemies
explosions['small'] = []			# used for smaller enemies
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
											# these should probably become instance variables of the pilot class
lives = 3										# create get and set functions for these instance variables later
score = 0										#MAIN LOOP FOR THE GAME
run = True
pygame.mixer.music.play(loops = -1)
pygame.mixer.music.set_volume(10.0)
while run:
	clock.tick(FPS)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	all_sprites.update()											# update all the sprites

	collisions = pygame.sprite.groupcollide(enemies,missles, True, True) 	# first true to delete enemy second true to delete missle as it has exploded
	for col in collisions:
		explsnd1.play()
		explshow = explosion(col.rect.center, 'big')											# did a missle hit an enemy
		all_sprites.add(explshow)											# could have multiple of these functions for each enemy
		score += 100
		e = enemy()
		all_sprites.add(e)
		enemies.add(e)

	collisions = pygame.sprite.spritecollide(pilot1, enemies, True, pygame.sprite.collide_circle)		# see if enemy ran into the pilot
	for col in collisions:
		explshow = explosion(col.rect.center, 'big')
		all_sprites.add(explshow)
		explsnd1.play()
		e = enemy()
		all_sprites.add(e)
		enemies.add(e)

		#time.sleep(1)
		#run = False

	screen.fill(BLACK)
	screen.blit(background, background_rect)
	all_sprites.draw(screen)
	show_hud(screen, "SCORE: " + str(score) + "    LIVES: " + str(lives), 28, WIDTH/4, 8 )										# blits all sprites onto screen
	pygame.display.flip()

pygame.quit													# exit game and window
