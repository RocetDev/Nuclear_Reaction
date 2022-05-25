import pygame
import math 
from random import randint
import sys

pygame.init()

# add this lines for adding image and sound for screamer
#boom = pygame.mixer.Sound('boom.mp3')
#image = pygame.image.load('eyes.jpg')

screen = pygame.display.set_mode((1310, 690))
pygame.display.set_caption("Nuclear reaction")

pause = False
neitrons = []
atoms = []
secondAtoms = []

NEITRON = (122, 122, 122)
ATOM = (50, 50, 150)
SECONDTATOM = (50, 100, 50)


def generateAtoms(n=50):
	for i in range(n):
		atoms.append([randint(0, 1310), randint(0, 690), 19])


def move():
	delList = []
	for i in range(len(neitrons)):
		if pause == False:
			neitrons[i][0] += 12*math.cos(neitrons[i][3])*neitrons[i][4][0]
			neitrons[i][1] += 12*math.sin(neitrons[i][3])*neitrons[i][4][1]

			if neitrons[i][0] <= 0 or neitrons[i][0] >= 1310:
				neitrons[i][4][0] *= -1
			elif neitrons[i][1] <= 0 or neitrons[i][1] >= 690:
				neitrons[i][4][1] *= -1

	for i in range(len(secondAtoms)):
		if pause == False: 
			if secondAtoms[i][0] < -20 or secondAtoms[i][1] < -20 or\
					secondAtoms[i][0] > 1330 or secondAtoms[i][1] > 720:
				delList.append(i)

			secondAtoms[i][0] += 10*math.cos(secondAtoms[i][3])
			secondAtoms[i][1] += 10*math.sin(secondAtoms[i][3])

	for i in range(len(delList)):
		try:
			secondAtoms.pop(delList[i])
		except IndexError:
			print("I cant do this 1")
	delList.clear()


def createNeitrons(atom):
		neitrons.append([
						atom[0], # x
						atom[1], # y
						5, 		 # radius
						randint(0, 361), # angle
						[1,1], # vectors
					])


def createSecondAtoms(atom):
	for i in range(2):
		secondAtoms.append([
							atom[0], # x
							atom[1], # y
							13,		 # radius
							randint(0, 361), # angle
					])


def colizian():
	delList = []
	for i in range(len(neitrons)):
		for j in range(len(atoms)):
			if distance(neitrons[i], atoms[j]):
				delList.append((i, j))
				for n in range(randint(2, 3)):
					createNeitrons(atoms[j])
				createSecondAtoms(atoms[j])

	for i in range(len(delList)):
		try:
			neitrons.pop(delList[i][0])
			atoms.pop(delList[i][1])
		except IndexError:
			print("I cant do this 2")

	delList.clear()
			


def drawNeitrons():
	for i in range(len(neitrons)):
		pygame.draw.circle(screen, NEITRON, (neitrons[i][0], neitrons[i][1]), neitrons[i][2])


def drawSecondAtoms():
	for i in range(len(secondAtoms)):
		pygame.draw.circle(screen, SECONDTATOM, (secondAtoms[i][0], secondAtoms[i][1]), secondAtoms[i][2])


def distance(core1, core2):
	return True if math.sqrt((core2[0]-core1[0])**2 + (core2[1]-core1[1])**2) < core1[2]+core1[2] else False


def drawAtoms():
	for i in range(len(atoms)):
		pygame.draw.circle(screen, ATOM, (atoms[i][0], atoms[i][1]), atoms[i][2])


generateAtoms(150)
while True:
	move()
	colizian()
	screen.fill((0,0,0))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_SPACE:
				if pause: pause = False
				else: pause = True
			elif event.key == pygame.K_ESCAPE:
				exit()
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				createNeitrons(pygame.mouse.get_pos())

	drawAtoms()
	drawNeitrons()
	drawSecondAtoms()

	if len(atoms) <= 4: 
		# for screamer
		# boom.play()
		# new_image = pygame.transform.scale(image, (1310, 690))
		# screen.blit(new_image, (0,0))
		# no suprise
		neitrons.clear()
		atoms.clear()
		secondAtoms.clear()
		generateAtoms(150)

	pygame.time.Clock().tick(60)
	pygame.display.flip()
