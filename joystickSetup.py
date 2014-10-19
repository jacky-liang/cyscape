import viz
viz.go()

# Load DirectInput plug-in 
dinput = viz.add('DirectInput.dle')

# Add first available joystick
joy = dinput.addJoystick()

#Left Bumper = Button 4
#Right Bumper = Button 5

def onSensorDown(e):
	if e.button == 4:
		print 'Psychic action'
	if e.button == 5:
		print 'Physical action'
		
viz.callback(viz.SENSOR_DOWN_EVENT, onSensorDown)