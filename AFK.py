'''
AFK.py [version v2022.12.15]

Requirements:
	pyautogui module (terminal > "pip install pyautogui")
'''

import os; os.system('cls' if os.name == 'nt' else 'clear')
import math
import pyautogui
import time
import threading

class AFK(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		drawCircle()

class Style():
	BLACK = '\033[30m'
	RED = '\033[31m'
	GREEN = '\033[32m'
	YELLOW = '\033[33m'
	BLUE = '\033[34m'
	MAGENTA = '\033[35m'
	CYAN = '\033[36m'
	WHITE = '\033[37m'
	UNDERLINE = '\033[4m'
	RESET = '\033[0m'
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKCYAN = '\033[96m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

	def apply(text, colour): return (getattr(Style(), colour.upper()) + text + Style.RESET)

'''
Draws circles with the cursor in clockwise direction, slowing down near the bottom of the circle, speeding up near the top
	- makes a click when at the bottom of the circle

Params:
	radius (int): Circle radius, in pixels
	w (positive number): Angular velocity (aka omega, frequency) of the circle which the cursor draws, in rad/s
		- the frequency of the cursor wont match this value exactly, because of the little delays caused by processing time
	t_step (positive number): Time step. this controls how often cursor movements are calculated and made
		- it controls the 'smoothness' of the circle, and the resolution of the path drawn by the cursor
		- a value loosely around the refresh period of your display makes sense
		- a value which is a fraction of 1 is recommended
'''
def drawCircle(radius=50, w=32, t_step=1/240):
	class pixelBuffer: # acts as a buffer which holds mouse movements, since the cursor cant move by a fraction of a pixel.
		def __init__(self, buffer=[0, 0]): # buffer[0] is the buffer for x axis, buffer[1] for y axis
			self.buffer = buffer

		def add(self, increment): # add to the buffer. if the buffer increases past a whole number (a full pixel), then it unloads; the whole number is returned
			res = [None, None]
			for i in range(len(self.buffer)):
				self.buffer[i] += increment[i]

				res[i] = round(self.buffer[i]) # this makes the cursor move to the pixel closest to where its *supposed* to be, by rounding pixels to the nearest integer.
				self.buffer[i] -= round(self.buffer[i]) # the rounding difference (whether positive or negative) is saved for the next time step

			return res

		def clear(self): self.buffer = [0, 0]

	def moveRel_matrix(matrix=list(), duration=0): pyautogui.moveRel(matrix[0], matrix[1], duration) # move the cursor, relative to current position

	# Circle should start from the bottom, and progress leftwards to the top.
		# the horizontal component of the cursor path can be modelled by a -sin(wt) func. Its derivative is -cos(wt)*w.
		# since the vertical scale is flipped, the vertical component of the cursor path is modelled by a +cos(wt) func. Its derivative is -sin(w)*w
	def dx_path(t): return (-math.cos(w*t) * w * radius) # derivative of horiztonal component of cursor path
	def dy_path(t): return (-math.sin(w*t) * w * radius) # derivative of vertical componento of cursor path

	# Movement should gradually accelerate as the cursor reaches the top of the circle, and decelerate as it comes back towards the bottom, where it stops briefly
	loopRatio = 16
	def t_stretch(t): return (-(loopRatio/w) * math.sin((w/loopRatio)*t) + t) # we want the cursor to slow down at each period, and speed up mid period. this function acts as a oscillating time function (compare it graphically with f(t) = t to really understand
	def dt_stretch(t): return (1 - math.cos((w/loopRatio)*t)) # the derivative of the t_stretch(t) function, which is used when calculating the derivative of the dx_path_timeStretch(t) and dy_path_timeStretch(t) functions

	def dx_path_timeStretch(t): return (dx_path(t_stretch(t)) * dt_stretch(t)) # derivative of x_path(t_stretch(t)) using chain rule
	def dy_path_timeStretch(t): return (dy_path(t_stretch(t)) * dt_stretch(t)) # derivative of y_path(t_stretch(t)) using chain rule

	my_pixelBuffer = pixelBuffer()

	switch_x, switch_y = 0, 0
	switch_x = 1
	switch_y = 1

	period = 2*math.pi / (w/loopRatio)
	t = 0
	while True:
		moveRel_matrix(my_pixelBuffer.add([dx_path_timeStretch(t)*t_step*switch_x, dy_path_timeStretch(t)*t_step*switch_y]))
		time.sleep(t_step)

		if t >= period:
			pyautogui.click() # click the mouse
			t -= period # reset t so that it doesnt grow to enormous values
			if not threading.main_thread().is_alive(): break # if the main thread died for whatever reason, quit

		t += t_step

		if threadLock.acquire(blocking=0) == 1:
			threadLock.release()
			break

# MAIN ======================================

pyautogui.PAUSE = 1/1000 # the pause time (s) after each mouse movement
pyautogui.MINIMUM_DURATION = 1/1000
pyautogui.MINIMUM_SLEEP = 1/1000

print("5 second prep time...")
time.sleep(5)

threadLock = threading.Lock()
threadLock.acquire(blocking=1)

print("Drawing circles and clicking..")
thread_1 = AFK()
thread_1.start()
input(Style.apply("Press <ENTER> to stop", "WARNING"))
threadLock.release()
thread_1.join()