import os, sys
import pygame
import math
from multiprocessing import Process
import time

import cppyy
cppyy.include("program.h")
cppyy.load_library("cppCalc")
from cppyy.gbl import Calc

cpp = Calc()

# Initialises Pygame graphics library and hides debugging output
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
os.environ['SDL_VIDEO_CENTERED'] = '0'
pygame.display.init()

# Config Options
# Increasing these will produce a more accurate graph. but will exponentially impact calculation time

window_Width = 1300
window_Height = 850

graph_Width = 850
graph_Height = 850
precision = 100

zoom = 2

x_Offset = 0
y_Offset = 0
# END Config Options

def calcMandelbrotPoint(x,y):
	times_Looped = cpp.calcMandelbrotPoint(x,y,precision)
	if times_Looped != precision:
		if times_Looped < int(precision/5):
			return pygame.Color(0,0,255)
		else:
			return pygame.Color(255,0,0)
	else:
		return pygame.Color(0,0,0)

def calculateSector(render_Array,sectorMap,sector_X,sector_Y):
	for y in range(sectorMap[1][sector_Y][0],sectorMap[1][sector_Y][1]):
		if (sector_X == 1 and sector_Y == 2):
			pygame.display.update()
		for x in range(sectorMap[0][sector_X][0],sectorMap[0][sector_X][1]):
			render_Array[x][y] = calcMandelbrotPoint(((x - (graph_Width/2))/graph_Width) * 3,((y - (graph_Height/2))/graph_Height) * 3)

def render_MandelbrotSet():
	# create a 2D array each representing a single pixel on the screen
	render_Array = pygame.PixelArray(screen)

	# gets the current time to be used for the calculation of the time to compute the Mandelbrot set
	time_Start = time.perf_counter()

	# Sets the function to calculate each quadrant of the graph to a different CPU Core
	# This allow for simultaneous multiprocessing of the data (can reduce the time to update by 60% or more)
	sectorMap =  [
					[[0,int(graph_Width/4)],[int(graph_Width/4),int(graph_Width/2)],[int(graph_Width/2),int((graph_Width/4)*3)],[int((graph_Width/4)*3),graph_Width]],
					[[0,int(graph_Height/4)],[int(graph_Height/4),int(graph_Height/2)],[int(graph_Height/2),int((graph_Height/4)*3)],[int((graph_Height/4)*3),graph_Height]]
				];

	core_Processes = []
	for y in range(4):
		for x in range(4):
			core_Processes.append(Process(target=calculateSector, args=(render_Array,sectorMap,x,y,)))

	for process in core_Processes:
		process.start()

	for process in core_Processes:
		process.join()

	# renders the final array to the screen surface
	render_Array.make_surface()
	# prints to the console the time taken to compute
	print("Computational Time: %5.1f secs" % (time.perf_counter() - time_Start))

def __main__():
	global screen
	screen = pygame.display.set_mode((window_Width,window_Height))
	screen.fill((46, 48, 58))
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
