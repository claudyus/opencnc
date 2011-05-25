# This file is released under the term of GPLv2.
#
# 2010-2011 (R) - Claudio Mignanti  <c.mignanti@gmail.com>
#

from threading import Thread

class axis(Thread):
	stepper		 = 0 # device fd
	miss_step	 = 0 # int
	act_position = 0 # mm
	unit = 0 	 # 0= mm 1= inches
	max_step = 0	 # int
	step_per_mm = 0	 # int

	home	= 0		# mm
	end_dir	= 0


	def __init__ (self, stepper_dev, step_max, step_per_mm=315, unit=0):
		""" This method is a shell of stepper motor. Mainly it is used to manage the axis limit and threading the operation!"""
		Thread.__init__(self)
		self.stepper = open (stepper_dev, "rw")
		self.max_step	 = step_max
		self.step_per_mm = step_per_mm
		self.unit = unit

		self.stepper.ioctl(MOTOR_LOWPWR)
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
		if diff < 0:
			direction = 0
			diff = diff * -1
		else:
			direction = 1

		if ( unit == 1):
			num_step = diff * ( step_per_mm * 2.54 )
		else:
			num_step = diff * step_per_mm

		#check if we can move in the opposide direction
		if self.is_at_end == 1:
			if direction == self.end_dir:
				#yet at the end here on this direction
				return 1

		self.stepper.ioctl(MOTOR_ENABLE)
		self.stepper.ioctl(MOTOR_DIR, direction)

		miss_step = self.stepper.write(str(position_to_go))
		if miss_step != 0:
			print "End of axis, missed step %d" % miss_step
			# we are at the end of axis 
			self.is_at_end 	= 1
			self.end_dir 	= direction

		#calculate the effective position
		if (unit == 1):
			self.act_position = position - ( miss_step * ( step_per_mm * 2.54 ))
		else:
			self.act_position = position - ( miss_step * step_per_mm)

		self.stepper.ioctl(MOTOR_DISABLE)
		return 0

	def pwm_set(self, val)
		self.stepper.ioctl(MOTOR_PWM_SET, val)

	#run of Thread cannot get 2 parameters
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

	def go_home(self):
		self.position_to_go = self.home
		self.start()

	def unit_per_sec(self,val):
		self.pwm_set(1/(step_per_mm * val * 2))

	def __del__ (self):
		stepper.close()


class cnc_3A0T():
	""" This method can be used to manage a complete 3 axes cnc without tool.\n"""

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
		#leave tool in home position before move x/y
		self.z_axis.go_home()
		self.z_axis.join()

		self.x_axis.go_home()
		self.y_axis.go_home()
		self.x_axis.join()
		self.y_axis.join()

	def command(self, cmd):
		

		return 0

	def g_file_execute(self, filename):
		fd = open(filename)

		self.command(fd.readline())

		

