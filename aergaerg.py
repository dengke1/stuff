import os, sys, random
import pygame
from pygame.locals import *

w = 40
h = 10
blocksize = 10
gmap = [[0 for x in range(w)] for y in range(h)]
blue = Color(0, 0, 255)
black = Color(0, 0, 0)

class pc(pygame.sprite.Sprite):
	xpos = 0
	ypos = 0
	isalive = True
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		gmap[self.xpos][self.ypos] = 1
		self.isalive = True
		self.rect = pygame.Rect(self.xpos, self.ypos, blocksize, blocksize)

		# screen = pygame.display.get_surface()
		# self.area = screen.get_rect()

	def getPos(self):
		return (xpos, ypos)

	def north(self):
		if self.ypos > 0:
			self.ypos-=1
			self.rect = self.rect.move(0, -blocksize)

	def south(self):
		if self.ypos < h - 1:
			self.ypos+=1
			self.rect = self.rect.move(0, blocksize)

	def west(self):
		if self.xpos > 0:
			self.xpos-=1
			self.rect = self.rect.move(-blocksize, 0)

	def east(self):
		if self.xpos < w - 1:
			self.xpos+=1
			self.rect = self.rect.move(blocksize, 0)

	def move(self, d):
		gmap[self.xpos][self.ypos] = 0

		if d == 8:
			self.north()
		elif d == 4:
			self.west()
		elif d == 5:
			self.south()
		elif d == 6:
			self.east()

		gmap[self.xpos][self.ypos] = 1

		if gmap[self.xpos][self.ypos] == 8:
		 	self.isalive = False


class snake(pygame.sprite.Sprite):
	'''
	2 = snake
	'''
	hposx = w-1
	hposy = h-1

	length = 1
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		gmap[self.hposx][self.hposy] = 2
		self.rect = pygame.Rect(self.hposx*blocksize-1, self.hposy*blocksize-1, blocksize-2, blocksize-2)

	def grow(self):
		self.length+=1

	def north(self):
		if self.hposy > 0:
			self.hposy-=1
			self.rect = self.rect.move(0, -blocksize)

	def south(self):
		if self.hposy < h - 1:
			self.hposy+=1
			self.rect = self.rect.move(0, blocksize)

	def west(self):
		if self.hposx > 0:
			self.hposx-=1
			self.rect = self.rect.move(-blocksize, 0)

	def east(self):
		if self.hposx < w - 1:
			self.hposx+=1
			self.rect = self.rect.move(blocksize, 0)

	def chase(self, x, y):
		xdif = abs(x - self.hposx)
		ydif = abs(y - self.hposy)

		# have snake move straight depending on max(x/y dif) and difference on x/y dif



def main():
	pygame.init()
	screen = pygame.display.set_mode((w*blocksize, h*blocksize), 0, 32)
	player = pc()

	pygame.draw.rect(screen, blue, player.rect)
	pygame.key.set_repeat(20, 20)
	keystate = pygame.key.get_pressed()

	# main loop
	while player.isalive:
		pygame.draw.rect(screen, blue, player.rect)
		for event in pygame.event.get():
			if event.type==QUIT or (event.type==KEYDOWN and keystate[K_q]):
				pygame.quit()
				sys.exit()
			if event.type==KEYDOWN:
				pygame.draw.rect(screen, black, player.rect)
				if keystate[K_UP]:
					player.move(8)
				elif keystate[K_DOWN]:
					player.move(5)
				elif keystate[K_LEFT]:
					player.move(4)
				elif keystate[K_RIGHT]:
					player.move(6)
				elif keystate[K_m]:
					for i in gmap:
						print(i, "/n")
				elif keystate[K_g]:
					print("mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm")
		keystate = pygame.key.get_pressed()

		pygame.display.update()




if __name__ == '__main__':
    main()