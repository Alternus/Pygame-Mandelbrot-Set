from multiprocessing import Process
from numba import jit
import os, sys
import math
import time

# Initialises Pygame graphics library and hides debugging output
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
os.environ['SDL_VIDEO_CENTERED'] = '0'

pygame.display.init()
pygame.font.init()
refresh_Rate = pygame.time.Clock()

@jit
def calcMandelbrotPoint(x,y):

	z = 0 + 0*1j
	c = x + y*1j

	if (show_Axis == True):
		# draws a white line for each of the axis if configured
		if x == (0 + x_Offset) or y == (0 - y_Offset):
			return (255,255,255)

	times_Looped = 0;
	for i in range(precision):
		if (z.real ** 2) + (z.imag ** 2) > 4:
			break
		z = (z**2) + c;
		times_Looped += 1

	# Return the color of the point
	if times_Looped != precision:
		return (255 * ((1 - math.cos( 0.5 * times_Looped))/2) ,255 * ((1 - math.cos(0.25 * times_Looped)) / 2),255 * (1 - math.sin( 0 * times_Looped)) /2)
	else:
		return (0,0,0)

def calculateSector(pixel_Array,sectorMap,sector_X,sector_Y):
	# Loops through the given points appending the result of the point to the pixel array
	for y in range(sectorMap[1][sector_Y][0],sectorMap[1][sector_Y][1]):
		if (sector_X == 1 and sector_Y == 2 and y % 2 == 0):
			pygame.display.update()
		for x in range(sectorMap[0][sector_X][0],sectorMap[0][sector_X][1]):
			pixel_Array[x][y] = calcMandelbrotPoint((((x - (window_Width/2))/window_Width) * 3 / zoom) + x_Offset,(((y - (window_Height/2))/window_Height) * 3 / zoom) - y_Offset)

def render_MandelbrotSet():
	# create a 2D array each representing a single pixel on the screen
	pixel_Array = pygame.PixelArray(screen)

	# gets the current time to be used for the calculation of the time to compute the Mandelbrot set
	time_Start = time.perf_counter()

	# Defines the sections of the graph for each computer core to render
	# This allow for simultaneous multiprocessing of the data (can reduce the time to update by 60% or more)
	sectorMap =  [
					[[0,int(window_Width/4)],[int(window_Width/4),int(window_Width/2)],[int(window_Width/2),int((window_Width/4)*3)],[int((window_Width/4)*3),window_Width]],
					[[0,int(window_Height/4)],[int(window_Height/4),int(window_Height/2)],[int(window_Height/2),int((window_Height/4)*3)],[int((window_Height/4)*3),window_Height]]
				];

	core_Processes = []
	# appends each process to the array to allow for dynamic assignment and operations
	for y in range(4):
		for x in range(4):
			core_Processes.append(Process(target=calculateSector, args=(pixel_Array,sectorMap,x,y,)))

	# Starts each of the processes
	for process in core_Processes:
		process.start()

	# Closes each of the process once completed
	for process in core_Processes:
		process.join()

	# renders the final array to the screen surface
	pixel_Array.make_surface()

	# Shows Axis and labels if configured
	if (show_Axis == True):
		del pixel_Array

		font = pygame.font.SysFont('./FiraSans-Regular.ttf', 30)

		# adds the axis labels
		imag_Label = font.render('Imag', True, (255, 255, 255))
		real_Label = font.render('Real', True, (255, 255, 255))

		# Adds point labels to the axis
		center_Label = font.render('('+str(0+x_Offset)+','+str(0+y_Offset)+')', True, (255, 255, 255))
		yPos_Label = font.render('('+str(0+x_Offset)+','+str(-(((0 - (window_Height/2))/window_Height) * 3 / zoom + y_Offset))+')', True, (255, 255, 255))
		xNeg_Label = font.render('('+str((((0 - (window_Width/2))/window_Width) * 3 / zoom + x_Offset))+','+str(0+y_Offset)+')', True, (255, 255, 255))

		zoom_Label = font.render('Zoom '+str(zoom)+'x', True, (255, 255, 255))

		# Renders the text onto the screen
		screen.blit(imag_Label,(int(window_Width/2) + 5,5))
		screen.blit(real_Label,(window_Width - 50,int(window_Width/2) - 25))
		screen.blit(zoom_Label,(5,5))
		screen.blit(center_Label,(int(window_Width/2) + 5,int(window_Width/2) + 5))
		screen.blit(yPos_Label,(int(window_Width/2) - 90,5))
		screen.blit(xNeg_Label,(0,int(window_Width/2) + 5))

	#prints to the console the time taken to compute
	print("Computational Time: %5.1f secs" % (time.perf_counter() - time_Start))

def __init__():
	global window_Width, window_Height, precision, zoom, x_Offset, y_Offset, show_Axis

	window_Width = 1000
	window_Height = 1000
	precision = 10000
	zoom = 10
	x_Offset = -0.5
	y_Offset = 0
	show_Axis = True

	completed_Config = False
	# asks the user if they want to use a custom configuration for the render
	while completed_Config == False:
		default_Mode = input("Use default config options (y/n): ")
		if (default_Mode.lower() == "y" or default_Mode.lower() == "yes"):
			completed_Config = True
		elif (default_Mode.lower() == "n" or default_Mode.lower() == "no"):
			completed_Config = True
		else:
			print("Value was invalid please try again")

	# Manual Configuration Options
	if (default_Mode.lower() == "n" or default_Mode.lower() == "no"):
		completed_Config = False
		while completed_Config == False:
			try:
				precision = int(input("Enter Precision: "))
				completed_Config = True
			except:
				print("Value was invalid please try again")
		completed_Config = False
		while completed_Config == False:
			try:
				zoom = float(input("Enter Zoom level (Must be > 0): "))
				completed_Config = True
			except:
				print("Value was invalid please try again")
		completed_Config = False
		while completed_Config == False:
			try:
				x_Offset = float(input("Enter x_Offset: "))
				completed_Config = True
			except:
				print("Value was invalid please try again")
		completed_Config = False
		while completed_Config == False:
			try:
				y_Offset = float(input("Enter y_Offset: "))
				completed_Config = True
			except:
				print("Value was invalid please try again")
		completed_Config = False
		while completed_Config == False:
				input_Value = input("Show Axis? (true,false): ")
				if (input_Value.lower() == "t" or input_Value.lower() == "true"):
					show_Axis = True
					completed_Config = True
				elif (input_Value.lower() == "f" or input_Value.lower() == "false"):
					show_Axis = False
					completed_Config = True
				else:
					print("Value was invalid please try again")

def __main__():
	global screen
	screen = pygame.display.set_mode((window_Width,window_Height))
	screen.fill((46, 48, 58))
	# Sets the application window title
	pygame.display.set_caption("Mitchell Wills 2020 | Mandelbrot Set")

	render_MandelbrotSet()

	while True:
		# Keeps application running until the user closes it
		events = pygame.event.get()
		refresh_Rate.tick(24)
		for event in events:
			if event.type == pygame.QUIT:
				pygame.quit()

__init__()

__main__()
