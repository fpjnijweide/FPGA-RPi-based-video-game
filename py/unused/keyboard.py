"""

















DEPRECATED... 
Replaced by main.py, objects.py, constants.py, keyBindings.py



















"""
import pygame
import sys

class Ball(pygame.sprite.Sprite):
	#This class represents a Ball. It derives from the "Sprite" class in Pygame.
	
	def __init__(self, color, radius):
		# Call the parent class (Sprite) constructor
		super().__init__()
		
		# Pass in the color of the Ball, and its x and y position, width and height.
		# Set the background color and set it to be transparent
		self.image = pygame.Surface([radius*2, radius*2])
		#self.image.fill(WHITE)
		#self.image.set_colorkey(WHITE)
 
		# Draw the Ball (a circle)
		pygame.draw.circle(self.image, color, [radius,radius], radius)

		# Fetch the rectangle object that has the dimensions of the screen.
		self.rect = self.image.get_rect()

		#set initial speed
		self.xspeed=0
		self.yspeed=0


# --- constants --- (UPPER_CASE names)


#define colors and screen size
WHITE = (255,255,255)
BLACK  = (0,0,0)

SCREEN_WIDTH=800
SCREEN_HEIGHT=600

# -- INIT ---
pygame.init()


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #set up screen
pygame.display.set_caption("Sensor Pong") #set title of screen


all_sprites_list = pygame.sprite.Group() #get list of sprites

ballradius=5 #define the ball as being in the centre of the screen, with color WHITE
playerBall = Ball(WHITE, ballradius)
playerBall.rect.x = SCREEN_WIDTH//2
playerBall.rect.y = SCREEN_HEIGHT//2

all_sprites_list.add(playerBall) #add this ball to the list of sprites
clock=pygame.time.Clock() #create game clock

#execute game
carryOn = True


while carryOn:
	keys = pygame.key.get_pressed() #get key presses, set ball speed according to keys pressed
	if keys[pygame.K_UP]:
		playerBall.yspeed -= 0.1
	if keys[pygame.K_DOWN]:
		playerBall.yspeed += 0.1
	if keys[pygame.K_LEFT]:
		playerBall.xspeed -= 0.1  
	if keys[pygame.K_RIGHT]:
		playerBall.xspeed += 0.1


		#we use this for terminal output and terminating game
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			carryOn=False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				print("K_UP pressed")
				
			if event.key == pygame.K_DOWN:
				print("K_DOWN pressed")
				
			if event.key == pygame.K_LEFT:
				print("K_LEFT pressed")
				              	
			if event.key == pygame.K_RIGHT:
				print("K_RIGHT pressed")
				
			if event.key == pygame.K_ESCAPE:
				pygame.quit();               
			if event.key == pygame.K_RETURN:
				print("K_RETURN pressed")                
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_UP:
				print("K_UP released")
			if event.key == pygame.K_DOWN:
				print("K_DOWN released")
			if event.key == pygame.K_LEFT:
				print("K_LEFT released")                	
			if event.key == pygame.K_RIGHT:
				print("K_RIGHT released")
			if event.key == pygame.K_ESCAPE:
				print("K_ESCAPE released")                
			if event.key == pygame.K_RETURN:
				print("K_RETURN released") 


	##########game logic################3

	screen.fill(BLACK)
	#maybe draw orhter stuff
	#pygame.draw.rect(screen, WHITE, [40,0, 200,300])
	#pygame.draw.line(screen, WHITE, [140,0],[140,300],5)

	all_sprites_list.update() #update list of sprites

	#-- if ball is at edge, reverse speed to make it bounce
	if playerBall.rect.x > SCREEN_WIDTH - ballradius:
		playerBall.xspeed = -playerBall.xspeed
	if playerBall.rect.y > SCREEN_HEIGHT - ballradius:
		playerBall.yspeed = -playerBall.yspeed
	if playerBall.rect.x < 0:
		playerBall.xspeed = -playerBall.xspeed
	if playerBall.rect.y < 0:
		playerBall.yspeed = -playerBall.yspeed

	#increase position according to speed
	playerBall.rect.x += playerBall.xspeed
	playerBall.rect.y += playerBall.yspeed

	#draw sprites
	all_sprites_list.draw(screen)

	#Refresh Screen
	pygame.display.flip()

	#Number of frames per secong e.g. 60
	clock.tick(60)	

pygame.quit()







#code stolen from stackoverflow which is useful

# --- classes --- (CamelCase names)

# class LBuild(pygame.sprite.Sprite):

# 	def __init__(self, color, width, height, x, y):
# 		super().__init__()

# 		self.image = pygame.Surface([width, height])
# 		self.image.fill(WHITE)
# 		self.image.set_colorkey(WHITE)

# 		# Draw the Ball (a rectangle!)
# 		pygame.draw.rect(self.image, color, [0, 0, width, height])

# 		# Fetch the rectangle object that has the dimensions of the image.
# 		self.rect = self.image.get_rect()
# 		self.rect.x = x
# 		self.rect.y = y

# --- functions --- (lower_case names)

# def level_1(screen, all_sprites_list, movblock):

# 	x = 0

# 	for _ in range(50):
# 		all_sprites_list.add(LBuild(GREY, 20, 20, x, 680))
# 		x += 20

# 	y = 660
# 	x2 = 40

# 	for _ in range(2):
# 		all_sprites_list.add(LBuild(BLACK, 60, 20, x2, y))
# 		y -= 20

# 	mblk = LBuild(RED, 100, 20, 120, 600)
# 	movblock.add(mblk)

# 	spd = 5

# 	# - mainloop -

# 	clock = pygame.time.Clock()

# 	#current_time = pygame.time.get_ticks()
# 	# change something after 2s
# 	#change_time = current_time + 2000 # 2000ms = 2s

# 	while True:

# 		# - events -

# 		for event in pygame.event.get():
# 			if event.type == pygame.QUIT:
# 				# False = exit game
# 				return False
# 			if event.type == pygame.KEYDOWN:
# 				if event.key == pygame.K_ESCAPE:
# 					# True = go to next level
# 					return True

# 		# - updates (without draws) -

# 		#current_time = pygame.time.get_ticks()

# 		#if current_time >= change_time:
# 		#    # change something again after 2s
# 		#    change_time = current_time + 2000

# 		all_sprites_list.update()

# 		if mblk.rect.x > 200:
# 			spd = -spd

# 		if mblk.rect.x < 100:
# 			spd = -spd

# 		mblk.rect.x += spd

# 		# - draws (without updates) -

# 		screen.fill(WHITE)

# 		all_sprites_list.draw(screen)
# 		movblock.draw(screen)

# 		pygame.display.flip()

# 		# - FPS -

# 		clock.tick(60)

