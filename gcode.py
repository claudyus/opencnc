class gcode_interpreter:

	def __init__(self):
		status = 0			#I implement the gcode interpreter like 
		#	a status machine. each command is a state

	#list of basic commands from arduino firmware for reprap
		l = cmd.partition("GTM");

		if (l[0] == "G00"): #rapid motion
			x.set_position(l[1])
			x.start()
			y.set_position(l[2])
			y.start()


		if (l[0] ==  "G01"): #coordinated motion
			pass
		if (l[0] == "G02"): #arc, clockwise
			pass
		if (l[0] == "G03"): #arc counter clockwise
			pass
		if (l[0] == "G04"): #dwell
			pass

		if (l[0] == "G20"): #inches as units
			for ax in self.x_list:
				ax.unit("inches")

		if (l[0] == "G21"): #millimeters as units
			for ax in self.x_list:
				ax.unit("mm")

		if (l[0] == "G28"): #go home
			for ax in self.x_list:
				ax.go_home()
			wait_axis()

		if (l[0] == "G30"): #go home via intermediate point
			pass

		if (l[0] == "G91"): #incremental positioning
			pass

		if (l[0] == "G92"): #set current as home
			for ax in self.x_list:
				ax.set_home()


