import sys, pygame
class Player():
	
	def __init__(self, MovementArray, MovementUnit, screen, MovementX, MovementY, background):
		self.design = pygame.image.load("standing.png").convert_alpha()
		self.look = "standing"
		self.movementArray = MovementArray
		self.movementUnit = MovementUnit
		self.movementX = MovementX
		self.movementY = MovementY
		self.rect = self.design.get_rect()
		self.rect.right = 0
		self.rect.bottom = 0
		self.rect = self.rect.move(self.movementUnit.x, self.movementUnit.y)
		self.screen = screen
		self.velocity = 0
		self.speed = 0
		self.background = background
		self.in_jump = True
		self.in_move = False
	
	def show(self):
		if self.in_move != True:
			self.look = "standing"
			self.design = pygame.image.load("standing.png")
		oldx = self.rect.right
		oldy = self.rect.bottom
		self.physics()
		self.rect.right = 0
		self.rect.bottom = 0
		self.rect = self.rect.move(self.movementUnit.x, self.movementUnit.y)
		self.screen.blit(self.design, self.rect)
		self.in_move = False
									   
	def physics(self):
		try:
			assert(self.movementArray[self.movementY+1][self.movementX].movable == True or (self.in_jump == True and self.velocity < -1))
			if self.velocity == 0:
				self.velocity += 5
			self.velocity = self.velocity + 20
			self.movementY += self.velocity
			while True:
				try:
					self.movementUnit = self.movementArray[self.movementY][self.movementX]
					assert(self.movementUnit.movable == True)
					break
				except:
					if self.velocity > -1:
						self.movementY +=  -1
					elif self.velocity < 0:
						self.movementY += 1
		except:
			self.in_jump = False
			self.velocity = 0
				
	def move(self, direction):
		self.in_move = True
		#set values for speed depending on direction
		SPEED = 40
		if self.in_jump:
			SPEED += -10
		if direction == "right":
			self.speed = SPEED
		elif direction == "left":
			self.speed = -SPEED
		elif direction == None:
			self.speed = 0
		#add spedd to x_coordinate
		self.movementX += self.speed
		#load running design
		if self.in_jump != True:
			if self.look == "running1":
				self.look = "running2"
				if self.speed > 0:
					self.design = pygame.image.load("running2right.png")
				else:
					self.design = pygame.image.load("running2leftq.png")
			else:
				self.look = "running1"
				if self.speed > 0:
					self.design = pygame.image.load("running1right.png")
				else:
					self.design = pygame.image.load("running1left.png")
		#check if move is allowed (if movable == True)
		try:
			self.movementUnit = self.movementArray[self.movementY][self.movementX]
			assert(self.movementUnit.movable == True)
		except:
			#if not, make player go back
			self.movementX += -self.speed
			self.movementUnit = self.movementArray[self.movementY][self.movementX]
			
	def jump(self):
		if self.in_jump == False:
			self.velocity = -140
			self.in_jump = True
			self.look = "standing"
			self.design = pygame.image.load("standing.png")
			


			
		
	
	

