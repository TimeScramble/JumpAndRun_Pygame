import sys, pygame
from Field import Block, Movement_Unit
from Person import *
from time import *
from pygame.locals import *
pygame.init()
pygame.key.set_repeat(10, 10)
clock = pygame.time.Clock()

size = width, height = 1000, 700
to_show = []
people = []
speed = [5, 9]
black = 0, 0, 0
screen = pygame.display.set_mode(size, FULLSCREEN)
background = pygame.image.load("background.png").convert_alpha()

#Define Length and Height of Movement_Units
Length_Move = 0.5
Height_Move = 0.5
#Define Length and Height of Blocks
LENGTH = 42
HEIGHT = 42
assert(int(LENGTH/Length_Move)== LENGTH/Length_Move)
assert(int(HEIGHT/Height_Move)== HEIGHT/Height_Move)
assert(int(width/Length_Move)== width/Length_Move)
assert(int(height/Height_Move)== height/Height_Move)


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
	return lines


def create_wall(x, y, plan):
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

def spider(MovementArray, MovementUnit, screen, MovementX, MovementY, background):
	spider = Enemy(MovementArray, MovementUnit, screen, MovementX, MovementY, background, "Spider")
	return spider


def init_block(twoD_Array):
	#Create two_dimensional Array for all Movement_Units
	pygame.font.init()
	myfont = pygame.font.SysFont('Comic Sans MS', 40)
	completed = 0
	to_be_completed = len(twoD_Array)*HEIGHT/Height_Move*len(twoD_Array[0])*LENGTH/Length_Move
	plan = []
	for y in range(int(len(twoD_Array)*HEIGHT/Height_Move)):
		layer = []
		for x in range(int(len(twoD_Array[0])*LENGTH/Length_Move)):
			unit = Movement_Unit(x*Length_Move, y*Height_Move)
			layer.append(unit)
			completed += 1
		plan.append(layer)
		#textsurface = myfont.render(str(int(completed/to_be_completed*100))+"%", False, (100,100,255))
		print(str(int((completed/to_be_completed)*100))+"%")
		#screen.blit(textsurface, (0,0))
		#pygame.display.flip()
	#Iterate through input
	for y in range(len(twoD_Array)):
		for x in range(len(twoD_Array[y])):
			#Create Dungeon_Wall for input "_"
			if twoD_Array[y][x] == "_":
				create_wall(x, y, plan)
	#MovementArray, MovementUnit, screen, MovementX, MovementY, background, designfolder
	for y in range(len(twoD_Array)):
		for x in range(len(twoD_Array[y])):
			"""if twoD_Array[y][x] == "s":
				movementUnit = plan[int((y-3)*HEIGHT/Height_Move)][int((x+2)*LENGTH/Length_Move)]
				enemy = spider(plan, movementUnit, screen, x * Length_Move, y * Height_Move, background)
				people.append(enemy)"""

	return plan

plan = init_block(load_level("Levels/1.1.txt"))

player = Player(plan, plan[20][int(LENGTH/Length_Move)-1], screen,int( LENGTH/Length_Move-1), 20, background)
to_show.append(player)

current_key = None

while True:
	should_move = 0
	clock.tick(10)
	screen.blit(background, (0, 0))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
	keys = pygame.key.get_pressed()
	if keys[pygame.K_a]:
		pygame.display.set_mode(size)
	if keys[pygame.K_RIGHT]:
		should_move = player.move("right")
	elif keys[pygame.K_LEFT]:
		should_move = player.move("left")
	if keys[pygame.K_UP] or keys[pygame.K_SPACE]:
		player.jump()
	for item in to_show:
		try:
			item.x += -should_move
		except:
			None
		item.show()
	for person in people:
		person.walk()
	pygame.display.flip()
	sleep(0.01)
