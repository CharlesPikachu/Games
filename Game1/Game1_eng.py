# coding: utf-8
# Author: Charles
# Public name: Charles的皮卡丘
# Import Pygame Library, which allows you to use the functionality provided by the library
import pygame
from pygame.locals import *
import math   # Because of calculating the angle of rotation.
import random # Because of using random functions.

# InItIalIze Pygame, set up a display window
pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
# Keys used to record keys : WASD (correspondence)
keys = [False, False, False, False]
# playerpos表示玩家位置
playerpos = [100, 100]
# Trace the player's precision variables, recording the arrow numbers and the number of badgers.
# Then we'll use these information to calculate accuracy.。
acc = [0, 0]
# Tracking arrow variable
arrows = []
# Define a timer so that the game will be built after a period of time.
badtimer = 100
badtimer1 = 0
badguys = [[640, 100]]
healthvalue = 194
# Play Acoustic InItIatIon
pygame.mixer.init()

# Loading picture
rabbit_img = pygame.image.load("resources/images/dude.png")
# Add some more scenery.
grass_img = pygame.image.load("resources/images/grass.png")
castle_img = pygame.image.load("resources/images/castle.png")
# Loading arrow
arrow_img = pygame.image.load('resources/images/bullet.png')
# Badger
badguy_img1 = pygame.image.load("resources/images/badguy.png")
badguy_img = badguy_img1
# Loaded castle healthy picture
healthbar_img = pygame.image.load("resources/images/healthbar.png")
health_img = pygame.image.load("resources/images/health.png")
# Loading Victory and Failure Picture
gameover_img = pygame.image.load("resources/images/gameover.png")
youwin_img = pygame.image.load("resources/images/youwin.png")
# Load the voice files and configure the volume
hit = pygame.mixer.Sound("resources/audio/explode.wav")
enemy = pygame.mixer.Sound("resources/audio/enemy.wav")
shoot = pygame.mixer.Sound("resources/audio/shoot.wav")
hit.set_volume(0.05)
enemy.set_volume(0.05)
shoot.set_volume(0.05)
# Play the game background music and keep the background music on。
pygame.mixer.music.load('resources/audio/moonlight.wav')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)

# CIrcumstantIally execute the next part.
# The running variable checks whether the game is finished or not,
# exiThe exitcode variable checks whether the player wins or not.
running = True
exitcode = False
while running:
	# Fill the screen window with black before running
	screen.fill(0)
	# The added landscape also needs to be painted on the screen.
	for x in range(width//grass_img.get_width()+1):
		for y in range(height//grass_img.get_height()+1):
			screen.blit(grass_img, (x*100, y*100))
	screen.blit(castle_img, (0, 30))
	screen.blit(castle_img, (0, 135))
	screen.blit(castle_img, (0, 240))
	screen.blit(castle_img, (0, 345))
	# First, obtain the mouse and the player's position. Then you get the angle and the radIans from the ATAN 2 functions.。
	# When the rabbit is rotating, its position will change
	# So you need to calculate the rabbit's new location and then display it on the screen.
	position = pygame.mouse.get_pos()
	angle = math.atan2(position[1]-(playerpos[1]+32), position[0]-(playerpos[0]+26))
	playerrot = pygame.transform.rotate(rabbit_img, 360-angle*57.29)
	playerpos1 = (playerpos[0]-playerrot.get_rect().width/2, playerpos[1]-playerrot.get_rect().height/2)
	screen.blit(playerrot, playerpos1)
	# Draw an arrow on the screen
	# The values of Vely and Velx are calculated according to trigonometric theorem.。
	# 10 is the speed of an arrow. 'If' is an arrow is beyond the scope of the screen,
	# If it's outside, delete this arrow.。
	# The second 'for' rotates the arrow to its rotation.
	for bullet in arrows:
		index = 0
		velx = math.cos(bullet[0])*10
		vely = math.sin(bullet[0])*10
		bullet[1] += velx
		bullet[2] += vely
		if bullet[1]<-64 or bullet[1]>640 or bullet[2]<-64 or bullet[2]>480:
			arrows.pop(index)
		index += 1
		for projectile in arrows:
			arrow1 = pygame.transform.rotate(arrow_img, 360-projectile[0]*57.29)
			screen.blit(arrow1, (projectile[1], projectile[2]))
	# Update and display these bad guys
	# Check whether BadtImer is 0, creating a baddImer if 0, creating a baddImer.
	# The first cycle updates on the Badger is to check whether the badger is exceeded beyond the screen,
	# and if it extends beyond the scope of the screen, the badger is removed.
	# The second round is to draw all the baddIes.
	if badtimer == 0:
		badguys.append([640, random.randint(50, 430)])
		badtimer = 100 -(badtimer1*2)
		if badtimer1 >= 35:
			badtimer1 = 35
		else:
			badtimer1 += 5
	index_badguy = 0
	for badguy in badguys:
		if badguy[0] < -64:
			badguys.pop(index_badguy)
		badguy[0] -= 7
		# Badgers can blow up the castle.
		# This paragraph is quite simple. If the x x coordinates are less than 64,
		# DesIgnatIng the Bad and reducing the health value of the game,
		# reducing the size of the game to a random number of 20 - 20 miles.。
		# Of course, the baddIes come and go when they run into the castle.
		badrect = pygame.Rect(badguy_img.get_rect())
		badrect.top = badguy[1]
		badrect.left = badguy[0]
		if badrect.left < 64:
			hit.play()
			healthvalue -= random.randint(5, 20)
			badguys.pop(index_badguy)
		# Check all the bad bugs and all the arrows to check whether there is a collision.
		# If the collision occurs, remove the badger,
		# remove the arrows, and exact the exact value of the variable.
		# Use Pygame built-in function to check the two rectangle if they cross the intersection.
		index_arrow = 0
		for bullet in arrows:
			bulletrect = pygame.Rect(arrow_img.get_rect())
			bulletrect.left = bullet[1]
			bulletrect.top = bullet[2]
			if badrect.colliderect(bulletrect):
				enemy.play()
				acc[0] += 1
				badguys.pop(index_badguy)
				arrows.pop(index_arrow)
			index_arrow += 1
		index_badguy += 1
	for badguy in badguys:
		screen.blit(badguy_img, badguy)
	# Add a timer
	# Use the PyGame Default 24 font size to display time information.
	font = pygame.font.Font(None, 24)
	survivedtext = font.render(str((90000-pygame.time.get_ticks())//60000)+":"+
							   str((90000-pygame.time.get_ticks())//1000%60).zfill(2), True, (0,0,0))
	textRect = survivedtext.get_rect()
	textRect.topright=[635,5]
	screen.blit(survivedtext, textRect)
	# Draw out the castle health value.
	# First, paint a whole red life bar. Then add green light to the life of the castle.
	screen.blit(healthbar_img, (5, 5))
	for health1 in range(healthvalue):
		screen.blit(health_img, (health1+8, 8))
	# Update screen
	pygame.display.flip()
	# Check some new events. If you have any exit orders, abort the program.
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		# Press buttons to update the key record array
		if event.type == pygame.KEYDOWN:
			if event.key == K_w:
				keys[0] = True
			elif event.key == K_a:
				keys[1] = True
			elif event.key == K_s:
				keys[2] = True
			elif event.key == K_d:
				keys[3] = True
		if event.type == pygame.KEYUP:
			if event.key == K_w:
				keys[0] = False
			elif event.key == K_a:
				keys[1] = False
			elif event.key == K_s:
				keys[2] = False
			elif event.key == K_d:
				keys[3] = False
		# When a player clicks on a mouse, he's gon na shoot an arrow.
		# This code will check if the mouse clicks on.，
		# It gets the mouse position and the position of the arrow based on the player and the cursor.。
		# The value of rotation is stored in the array of arrowworks.
		if event.type == pygame.MOUSEBUTTONDOWN:
			shoot.play()
			position = pygame.mouse.get_pos()
			acc[1] += 1
			arrows.append([math.atan2(position[1]-(playerpos1[1]+32), position[0]-(playerpos1[0]+26)),
						   playerpos1[0]+32, playerpos1[1]+26])
	# 移动玩家
	if keys[0]:
		playerpos[1] -= 5
	elif keys[2]:
		playerpos[1] += 5
	if keys[1]:
		playerpos[0] -= 5
	elif keys[3]:
		playerpos[0] += 5
	badtimer -= 1
	# Here are the basic conditions of victory / failure :
	# If the time is up (90 s) : Then stop running games, set up the game.;
	# If the castle is destroyed, then stop playing games and set up the game
	# Accuracy is always needed.
	# The first 'if' is whether it is time for inspection.
	# The second 'if' examines whether the castle is destroyed.
	# Third 'if' , count your accuracy.。
	# After that, last 'if' is checked, you win or lose, then show the appropriate picture。
	if pygame.time.get_ticks() >= 90000:
		running = False
		exitcode = True
	if healthvalue <= 0:
		running = False
		exitcode = False
	if acc[1] != 0:
		accuracy = acc[0]*1.0/acc[1]*100
		accuracy = ("%.2f" % accuracy)
	else:
		accuracy = 0
if exitcode == False:
	pygame.font.init()
	font = pygame.font.Font(None, 24)
	text = font.render("Accuracy: "+str(accuracy)+"%", True, (255,0,0))
	textRect = text.get_rect()
	textRect.centerx = screen.get_rect().centerx
	textRect.centery = screen.get_rect().centery+24
	screen.blit(gameover_img, (0, 0))
	screen.blit(text, textRect)
else:
	pygame.font.init()
	font = pygame.font.Font(None, 24)
	text = font.render("Accuracy: "+accuracy+"%", True, (0,255,0))
	textRect = text.get_rect()
	textRect.centerx = screen.get_rect().centerx
	textRect.centery = screen.get_rect().centery+24
	screen.blit(youwin_img, (0,0))
	screen.blit(text, textRect)
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
	pygame.display.flip()
