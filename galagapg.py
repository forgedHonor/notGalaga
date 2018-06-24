import pygame		# idea from kidscancode/pygametutorials
import random
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


background = pygame.image.load(path.join(imgdir, "space.png")).convert()
background_rect = background.get_rect()
pilotpic = pygame.image.load(path.join(imgdir, "alienship.png")).convert()
enemypic = pygame.image.load(path.join(imgdir, "enemy2.png")).convert()
misslepic = pygame.image.load(path.join(imgdir, "rocket3.png")).convert()


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
while run:
	clock.tick(FPS)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				pilot1.fire()

	all_sprites.update()				# update all the sprites

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

pygame.quit					# exit game and window
