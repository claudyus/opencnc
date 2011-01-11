# This file is released under the term of GPLv2.
#
# 2010 (R) - Claudio Mignanti  <c.mignanti@gmail.com>
#
# $Id$

import fox
from threading import Thread

class axis(Thread):
	stepper		 = 0 # class
	miss_step	 = 0 # int
	act_position = 0 # mm
	unit = 0 		# 0= mm 1= inches
	max_step = 0	# int
	step_per_mm = 0	# int

	position_to_go = 0
	home	= 0		# mm
	end_dir	= 0


	def __init__ (self, stepper_class, step_max, step_per_mm=315, unit=1):
		""" This method is a shell of stepper one. Mainly it is used to manage the axis limit and threading the operation!"""
		Thread.__init__(self)
		self.stepper	 = stepper_class
		self.max_step	 = step_max
		self.step_per_mm = step_per_mm
		self.unit = unit
		return None

#axis diagram
#    limit
#		|
#		V
#		L-------------------act_position-----------------L
#
#		<---------				max_step			----->
#			<---- dir0					dir1---->

	def run (self):
		#calcolate steps and direction from position
		diff = self.position_to_go - self.act_position
		if (diff < 0):
			direction = 0
			diff = diff * -1
		else:
			direction = 1

		if ( unit == 1):
			num_step = diff * ( step_per_mm * 2.54 )
		else:
			num_step = diff * step_per_mm

		#check if we can move in the opposide direction
		if (self.is_at_end == 1):
			if (direction == self.end_dir ):
				#yet at the end here on this direction
				return 1

		self.stepper.dir(direction)
		self.stepper.enable()
		self.miss_step = self.stepper.step(num_step, 0, 7)
		if (miss_step != 0):
			# we are at the end of axis
			self.is_at_end 	= 1
			self.end_dir 	= direction

		#calculate the effective position
		if (unit == 1):
			self.act_position = position - ( miss_step * ( step_per_mm * 2.54 ))
		else:
			self.act_position = position - ( miss_step * step_per_mm)
		return 0

	#run Thread cannot get 2 parameters
	def set_position(self, position):
		self.position_to_go = position

	def unit(self, string):
		if (string == "mm" or string == "metric" or string == "millimeters"):
			self.unit = 0
		else:
			self.unit = 1

	def set_home(self):
		self.home = self.position

	def get_home(self):
		return self.home


class cnc_3A0T():
	""" This method can be used to manage a complete 3 axes cnc without tool.\n
You should add 3 existing axes to it to operate."""

	if_error = 0

	x_axis = None
	y_axis = None
	z_axis = None

	x_list = []

	def __init__ (self, x_ax, y_ax, z_ax):
		self.x_axis = x_ax
		self.y_axis = y_ax
		self.z_axis = z_ax
		self.x_list.append(self.x_axis)
		self.x_list.append(self.y_axis)
		self.x_list.append(self.z_axis)

	def wait_axis(self):
		for ax in self.x_list:
			ax.join()

	def reset(self):
		self.z_axis.start(-99999)
		self.z_axis.join()
		self.x_axis.start(-99999)
		self.y_axis.start(-99999)
		self.x_axis.join()
		self.y_axis.join

	def command(self, cmd):
		
		return 0

