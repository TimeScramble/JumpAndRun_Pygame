import sys, pygame
from Field import Block, Movement_Unit
from Player import Player
from time import *
pygame.init()
pygame.key.set_repeat(10, 10)
clock = pygame.time.Clock()

size = width, height = 1000, 700
to_show = []
to_move = []
speed = [5, 9]
black = 0, 0, 0
screen = pygame.display.set_mode(size)
background = pygame.image.load("background.png").convert_alpha()

#Define Length and Height of Movement_Units
Length_Move = 0.4
Height_Move = 0.4
#Define Length and Height of Blocks
LENGTH = 84
HEIGHT = 84


def load_level(level):
	level = open(level)
	lines = []
	for line in level:
		text = line.rstrip()
		lines.append(list(line))
	lines.append([])
	max_length = 0
	for line in lines:
		if len(line) > max_length:
			max_length = len(line)
	for i in range(max_length):
		for line in lines:
			if len(line) < max_length:
				line.append(None)
	print(lines)
	return lines



def init_block(twoD_Array):
	#Create two_dimensional Array for all Movement_Units
	plan = []
	for y in range(int(len(twoD_Array)*HEIGHT/Height_Move)):
		layer = []
		for x in range(int(len(twoD_Array[0])*LENGTH/Length_Move)):
			unit = Movement_Unit(x*Length_Move, y*Height_Move)
			layer.append(unit)
			to_move.append(unit)
		plan.append(layer)
	#Iterate through input
	for y in range(len(twoD_Array)):
		for x in range(len(twoD_Array[y])):
			#Create Dungeon_Wall for input "_"
			if twoD_Array[y][x] == "_":
				block = Block(screen, x * LENGTH, y * HEIGHT)
				to_show.append(block)
				#Set Movement_Status to False, if Dungeon_Wall is created
				try:
					for q in range(int((x*LENGTH)/Length_Move),int(((x+2)*LENGTH)/Length_Move)):
						for i in range(int((y*HEIGHT)/Height_Move),int(((y+2)*HEIGHT)/Height_Move)):
							plan[i][q].setMovementStatus(False)
				except:
					for q in range(int((x*LENGTH)/Length_Move),int(((x+1)*LENGTH)/Length_Move)):
						for i in range(int((y*HEIGHT)/Height_Move),int(((y+1)*HEIGHT)/Height_Move)):
							plan[i][q].setMovementStatus(False)

	return plan

plan = init_block(load_level("Levels/1.1.txt"))

player = Player(plan, plan[20][int(LENGTH/Length_Move)-1], screen,int( LENGTH/Length_Move-1), 20, background)
to_show.append(player)

current_key = None

while True:
	should_move = 0
	clock.tick(60)
	screen.blit(background, (0, 0))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYUP:
			player.look = "standing"
			player.deign = pygame.image.load("standing.png")
	keys = pygame.key.get_pressed()
	if keys[pygame.K_RIGHT]:
		should_move = player.move("right", to_move)
	elif keys[pygame.K_LEFT]:
		should_move = player.move("left", to_move)
	if keys[pygame.K_UP] or keys[pygame.K_SPACE]:
		player.jump()
	for item in to_show:
		try:
			item.x += -should_move
		except:
			None
		item.show()
	pygame.display.flip()
