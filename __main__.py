import os
import pygame
import math
from multiprocessing import Process
import time

# Initialises Pygame graphics library and hides debugging output
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
os.environ['SDL_VIDEO_CENTERED'] = '0'
pygame.display.init()


# Config Options
# Increasing these will produce a more accurate graph. but will exponentially impact calculation time

w = 850
h = 850
precision = 100

x_Zoom = 0
y_Zoom = 0

x_Offset = 0
y_Offset = 0

# END Config Options

def mod(z):
	# calculates the modulus of a complex number
	return (math.sqrt((z.real**2) + (z.imag**2)))

def calcMandelbrotPoint(x,y):
	previous_Result = 0 + 0j
	current_Result = 0 + 0j
	times_Looped = 0

	while mod(current_Result) <= 2 and times_Looped < precision:
		current_Result = (previous_Result**2) + (x + y*1j)
		previous_Result = current_Result
		times_Looped += 1

	if times_Looped != precision:
		if times_Looped < 15:
			return pygame.Color(255 - times_Looped,0,100 + times_Looped*2)
		elif times_Looped < 150:
			return pygame.Color(255 - times_Looped,0,times_Looped)
		else:
			return pygame.Color(255,255,255)
	else:
		return pygame.Color(0,0,0)

def calculate_Quad1(render_Array):
	# Loops through the points within the first quadrant of the argand diagram
	for y in range(0,int(h/2)):
		for x in range(int(w/2),w):
			render_Array[x, y] = calcMandelbrotPoint(((x - (w/2))/w) * 3,((y - (h/2))/h) * 3)

def calculate_Quad2(render_Array):
	for y in range(0,int(h/2)):
		for x in range(0,int(w/2)):
			render_Array[x, y] = calcMandelbrotPoint(((x - (w/2))/w) * 3,((y - (h/2))/h) * 3)

def calculate_Quad3(render_Array):
	for y in range(int(h/2),h):
		for x in range(0,int(w/2)):
			render_Array[x, y] = calcMandelbrotPoint(((x - (w/2))/w) * 3,((y - (h/2))/h) * 3)

def calculate_Quad4(render_Array):
	for y in range(int(h/2),h):
		for x in range(int(w/2),w):
			render_Array[x, y] = calcMandelbrotPoint(((x - (w/2))/w) * 3,((y - (h/2))/h) * 3)

def render_MandelbrotSet():
	# create a 2D array each representing a single pixel on the screen
	render_Array = pygame.PixelArray(screen)

	# gets the current time to be used for the calculation of the time to compute the Mandelbrot set
	time_Start = time.perf_counter()

	# Sets the function to calculate each quadrant of the graph to a different CPU Core
	# This allow for simultaneous multiprocessing of the data (can reduce the time to update by 60% or more)
	core1_Process = Process(target=calculate_Quad1, args=(render_Array,))
	core2_Process = Process(target=calculate_Quad2, args=(render_Array,))
	core3_Process = Process(target=calculate_Quad3, args=(render_Array,))
	core4_Process = Process(target=calculate_Quad4, args=(render_Array,))

	# Starts each process
	core1_Process.start()
	core2_Process.start()
	core3_Process.start()
	core4_Process.start()

	# ends waits for the end of each process
	core1_Process.join()
	core2_Process.join()
	core3_Process.join()
	core4_Process.join()

	# renders the final array to the screen surface
	render_Array.make_surface()

	# prints to the console the time taken to compute
	print("Computational Time: %5.1f secs" % (time.perf_counter() - time_Start))

	# Updates the screen with the new result
	pygame.display.update()

def __main__():
	global screen
	screen = pygame.display.set_mode((w,h),pygame.RESIZABLE)

	# Sets the application window title
	pygame.display.set_caption("Mandelbrot Set")

	render_MandelbrotSet()

	while True:
		# Keeps application running until the user closes it
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				pygame.quit()

__main__()
