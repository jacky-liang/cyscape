#Vizworld Imports
import viz
import vizconnect
import vizjoy
import vizact
import viz
import vizact

#Custom modules
import joystickSetup
from emotion.emotion import *

vizconnect.go('vizconnect_config2.py')

#Init Game
room = viz.add('room.osgb')
scientist = viz.add('./avatars/male/avatar 003.cfg')
scientist.setPosition([-7.64, 0, 7.91])
scientist.setEuler(120,0,0)
scientist.state(1)

#Emotions for Scientist
affectManager=AffectManager(24)
scientist_expression=affectManager.createBasicEkmanWithExpression(scientist)

head = vizconnect.getTracker('rift_orientation_tracker').getNode3d()

joystick = vizconnect.getInput('joystick')
transport = vizconnect.getTransport('wandmagiccarpet')

avatarNova = viz.add('./avatars/female/avatar 001.cfg')
avatarNova.state(1)
avatarNova.setParent(transport.getNode3d())


##Joystick##
# Load DirectInput plug-in 
dinput = viz.add('DirectInput.dle')
# Add first available joystick
joy = dinput.addJoystick()

#Left Bumper = Button 4
#Right Bumper = Button 5
leftArm = avatarNova.getBone('Bip01 L UpperArm')
leftHand = avatarNova.getBone('Bip01 L Forearm')
	

def onSensorDown(e):
	if e.button == 4:
		print 'Psychic action'
		avatarNova.execute(6)
		avatarNova.setAnimationTime(6,1)
		scientist_expression.trigger('surprise',1.0)
	if e.button == 5:
		print 'Physical action'	
		avatarNova.execute(6)
		avatarNova.setAnimationTime(6,2)
viz.callback(viz.SENSOR_DOWN_EVENT, onSensorDown)

#Scientist Eye Tracking
scientist_le = scientist.getChild('avatar 003 mesh03.CMF')
scientist_re = scientist.getChild('avatar 003 mesh02.CMF')
def updateEyes():
    pos = avatarNova.getPosition()
    scientist_re.lookAt(pos,mode=viz.ABS_GLOBAL)
    scientist_le.lookAt(pos,mode=viz.ABS_GLOBAL)
vizact.ontimer(0, updateEyes)

#Door animation
def slideDoor():
	doors = room.getChild('Door')
	doors.visible(viz.OFF)
	print 'slide Door'
	
vizact.onkeydown('d', slideDoor)

#Clear an existing action
def clearActions():
	avatarNova.stopAction(6)
	avatarNova.state(1)

vizact.ontimer(2, clearActions)