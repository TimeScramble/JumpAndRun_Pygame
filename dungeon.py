import sys, pygame
from Field import Block, Movement_Unit
from Player import Player
pygame.init()
pygame.key.set_repeat(10, 10)
clock = pygame.time.Clock()

size = width, height = 1000, 700
to_show = []
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


test = [[None,None,None,None,None,None,None,None,None], [None,None,None,None,None,None,None,None,None], [None,None,None,None,None,None,None,None,None],  [None,None,None,None,None,None,None,None,None], [None,None,None,"_","_","_",None,None,None], [None,"_",None,None,None,None,None,None,None], ["_",None,None,None,None,None,None,None,"_"], ["_","_","_","_","_","_","_","_","_"]]

def init_block(twoD_Array):
	#Create two_dimensional Array for all Movement_Units
	plan = []
	for y in range(int(len(twoD_Array)*HEIGHT/Height_Move)):
		layer = []
		for x in range(int(len(twoD_Array[0])*LENGTH/Length_Move)):
			layer.append(Movement_Unit(x*Length_Move, y*Height_Move))
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
	
plan = init_block(test)

player = Player(plan, plan[20][int(LENGTH/Length_Move)-1], screen,int( LENGTH/Length_Move-1), 20, background)
to_show.append(player)
	
current_key = None
			
while True:
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
		player.move("right")
	elif keys[pygame.K_LEFT]:
		player.move("left")
	if keys[pygame.K_UP] or keys[pygame.K_SPACE]:
		player.jump()
	for item in to_show:
		item.show()
	pygame.display.flip()