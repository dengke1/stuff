import os, sys, random
import pygame
from pygame.locals import *

w = 50
h = 40
blocksize = 10
gmap = [[0 for x in range(w)] for y in range(h)]
blue = Color(0, 0, 255)
black = Color(0, 0, 0)
red = Color(255, 0, 0)
sMaxSpeed = 0.0315
sMinSpeed = 0.06
playerSpeed = 0.03


class pc(pygame.sprite.Sprite):
	'''
	square representing player
	'''
	xpos = 0
	ypos = 0
	isalive = True
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		gmap[self.ypos][self.xpos] = 1
		self.isalive = True
		self.rect = pygame.Rect(self.xpos, self.ypos, blocksize, blocksize)

		# screen = pygame.display.get_surface()
		# self.area = screen.get_rect()

	def getPos(self):
		return (self.xpos, self.ypos)

	def north(self):
		if self.ypos > 0:
			self.ypos-=1
			self.rect = self.rect.move(0, -blocksize)
			self.checkCollision(self.xpos, self.ypos)

	def south(self):
		if self.ypos < h - 1:
			self.ypos+=1
			self.rect = self.rect.move(0, blocksize)
			self.checkCollision(self.xpos, self.ypos)

	def west(self):
		if self.xpos > 0:
			self.xpos-=1
			self.rect = self.rect.move(-blocksize, 0)
			self.checkCollision(self.xpos, self.ypos)

	def east(self):
		if self.xpos < w - 1:
			self.xpos+=1
			self.rect = self.rect.move(blocksize, 0)
			self.checkCollision(self.xpos, self.ypos)

	def checkCollision(self, x, y):
		if gmap[y][x] == 8:
		 	self.isalive = False

	def move(self, d):
		gmap[self.ypos][self.xpos] = 0

		if d == 8:
			self.north()
		elif d == 4:
			self.west()
		elif d == 5:
			self.south()
		elif d == 6:
			self.east()

		gmap[self.ypos][self.xpos] = 1



class segment(pygame.sprite.Sprite):
	xpos = None
	ypos = None
	next = None
	prev = None
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.xpos = x
		self.ypos = y
		gmap[self.ypos][self.xpos] = 8
		self.rect = pygame.Rect(self.xpos*blocksize+1, self.ypos*blocksize+1, blocksize-2, blocksize-2)

	def getPos(self):
		return [self.xpos, self.ypos]

	def setNext(self, seg):
		self.next = seg

	def setPrev(self, seg):
		self.prev = seg

	def getNext(self):
		return self.next

	def getPrev(self):
		return self.prev

	def move(self):
		'''
		Moves segment to location where previous segment was, updates map values
		'''
		if self.getNext() is None:
			gmap[self.ypos][self.xpos] = 0
		prev = self.getPrev()
		prevc = prev.getPos()
		self.xpos = prevc[0]
		self.ypos = prevc[1]
		self.rect = prev.rect
		gmap[self.ypos][self.xpos] = 8


class snake(pygame.sprite.Sprite):
	'''
	a snake object consisting of a number of segments
	'''
	hx = w-4
	hy = h-1
	direction = 'w'

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.head = segment(self.hx, self.hy)
		one = segment(self.hx + 1, self.hy)
		two = segment(self.hx + 2, self.hy)
		three = segment(self.hx + 3, self.hy)

		self.head.setNext(one)
		one.setNext(two)
		two.setNext(three)

		one.setPrev(self.head)
		two.setPrev(one)
		three.setPrev(two)
		self.tail = three


	def onwards(self):
		if self.direction == 'n':
			self.head.ypos-=1
			self.head.rect = self.head.rect.move(0, -blocksize)
		elif self.direction == 's':
			self.head.ypos+=1
			self.head.rect = self.head.rect.move(0, blocksize)
		elif self.direction == 'w':
			self.head.xpos-=1
			self.head.rect = self.head.rect.move(-blocksize, 0)
		elif self.direction == 'e':
			self.head.xpos+=1
			self.head.rect = self.head.rect.move(blocksize, 0)

		if gmap[self.head.ypos][self.head.xpos] == 1:
			return True
		else:
			gmap[self.head.ypos][self.head.xpos] = 8
			return False

	def chase(self, x, y, grow):
		'''
		changes direction of snake and chases pc, also grows occasionally
		'''
		xdif = abs(x - self.head.xpos)
		ydif = abs(y - self.head.ypos)

		# move head and rest of body from tail up
		temp = self.tail
		gpos = temp.getPos()
		gmap[temp.ypos][temp.xpos] = 0
		while temp != self.head:
			prev = temp.getPrev()
			cprev = prev.getPos()

			temp.xpos = cprev[0]
			temp.ypos = cprev[1]

			temp.rect = prev.rect
			temp = prev
		if grow:
			newTail = segment(gpos[0], gpos[1])
			self.tail.setNext(newTail)
			newTail.setPrev(self.tail)
			self.tail = newTail

		ret = self.onwards()


		# Change directions based on location
		if xdif <= 1:
			if y > self.head.ypos:
				self.direction = 's'
			else:
				self.direction = 'n'

		if ydif <= 1:
			if x > self.head.xpos:
				self.direction = 'e'
			else:
				self.direction = 'w'
		return ret

def drawSnake(seg, dis, color):
	while seg is not None:
		pygame.draw.rect(dis, color, seg.rect)
		seg = seg.getNext()

def drawSnake2(seg, dis):
	r = 255
	g = 0
	b = 0
	while seg is not None:
		if r >= 250 and b <= 245:
			b+=5
		elif b >= 250 and r >= 5:
			b = 255
			r-=5
		elif r <= 5 and g <= 245:
			r = 0
			g +=10
		elif g >= 245 and b >= 5:
			g = 255
			b -= 5
		elif b <= 5 and r <= 250:
			b = 0
			r += 5
		pygame.draw.rect(dis, Color(r, g, b), seg.rect)
		seg = seg.getNext()


def game():
	count = 10
	doGrow = False

	pygame.init()
	screen = pygame.display.set_mode((w*blocksize, h*blocksize), 0, 32)
	player = pc()
	enemy = snake()

	pygame.draw.rect(screen, blue, player.rect)
	
	drawSnake(enemy.head, screen, red)

	pygame.key.set_repeat(1, 1)
	keystate = pygame.key.get_pressed()

	clock = pygame.time.Clock()

	pcWalkCD = 0
	pcDelay = playerSpeed

	sWalkCD = 0
	sDelay = sMinSpeed
	# main loop
	while player.isalive:

		delta = clock.tick() / 1000.0
		pcWalkCD -= delta
		sWalkCD -= delta

		pygame.draw.rect(screen, blue, player.rect)

		pos = player.getPos()

		drawSnake2(enemy.head, screen)

		for event in pygame.event.get():
			if event.type==QUIT or (event.type==KEYDOWN and keystate[K_q]):
				pygame.quit()
				sys.exit()
			if pcWalkCD <= 0:
				if event.type==KEYDOWN:
					pygame.draw.rect(screen, black, player.rect)

					if keystate[K_UP]:
						player.move(8)
						pcWalkCD = pcDelay
					elif keystate[K_DOWN]:
						player.move(5)
						pcWalkCD = pcDelay
					elif keystate[K_LEFT]:
						player.move(4)
						pcWalkCD = pcDelay
					elif keystate[K_RIGHT]:
						player.move(6)
						pcWalkCD = pcDelay
					elif keystate[K_m]:
						print("#####################################################")
						for i in gmap:
							for m in i:
								print(m, " ", end="")
							print()
					
		keystate = pygame.key.get_pressed()

		# move snake, update counter to increase speed and length
		if sWalkCD <= 0:
			drawSnake(enemy.head, screen, black)
			count -= 1
			if enemy.chase(pos[0], pos[1], doGrow):
				player.isalive = False
			doGrow = False
			if count == 0: 
				count = 10
				doGrow = True
				if sDelay > sMaxSpeed:
					sDelay -= 0.0005
			sWalkCD = sDelay
		pygame.display.update()
	return 1

def end():
	screen = pygame.display.set_mode((w*blocksize, h*blocksize), 0, 32)


if __name__ == '__main__':
	while 1:
		gmap = [[0 for x in range(w)] for y in range(h)]
		game()

