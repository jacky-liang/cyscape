"""
This module was generated by Vizconnect.
Version: 1.01
Generated on: 2014-08-07 13:32:33.816000
"""

import viz
import vizconnect

#################################
# Parent configuration, if any
#################################

def getParentConfiguration():
	#VC: set the parent configuration
	_parent = ''
	
	#VC: return the parent configuration
	return _parent



#################################
# Pre viz.go() Code
#################################

def preVizGo():
	return True


#################################
# Pre-initialization Code
#################################

def preInit():
	"""Add any code here which should be called after viz.go but before any initializations happen.
	Returned values can be obtained by calling getPreInitResult for this file's vizconnect.Configuration instance."""
	return None


#################################
# Group Code
#################################

def initGroups(initFlag=vizconnect.INIT_INDEPENDENT, initList=None):
	#VC: place any general initialization code here
	rawGroup = vizconnect.getRawGroupDict()
	
	#VC: return values can be modified here
	return None


#################################
# Display Code
#################################

def initDisplays(initFlag=vizconnect.INIT_INDEPENDENT, initList=None):
	#VC: place any general initialization code here
	rawDisplay = vizconnect.getRawDisplayDict()

	#VC: initialize a new display
	_name = 'rift'
	if vizconnect.isPendingInit('display', _name, initFlag, initList):
		#VC: init the raw object
		if initFlag&vizconnect.INIT_RAW:
			#VC: set the window for the display
			_window = viz.MainWindow
			
			#VC: create the raw object
			import oculus
			_window.displayNode = oculus.Rift(window=_window, autoDetectMonitor=True)
			viz.window.setFullscreen(True)
			rawDisplay[_name] = _window
	
		#VC: init the wrapper (DO NOT EDIT)
		if initFlag&vizconnect.INIT_WRAPPERS:
			vizconnect.addDisplay(rawDisplay[_name], _name, make='Oculus VR', model='Rift')
	
		#VC: set the parent of the node
		if initFlag&vizconnect.INIT_PARENTS:
			vizconnect.getDisplay(_name).setParent(vizconnect.getAvatar('female').getAttachmentPoint('head'))

	#VC: return values can be modified here
	return None


#################################
# Tracker Code
#################################

def initTrackers(initFlag=vizconnect.INIT_INDEPENDENT, initList=None):
	#VC: place any general initialization code here
	rawTracker = vizconnect.getRawTrackerDict()

	#VC: initialize a new tracker
	_name = 'rift_orientation_tracker'
	if vizconnect.isPendingInit('tracker', _name, initFlag, initList):
		#VC: init the raw object
		if initFlag&vizconnect.INIT_RAW:
			#VC: create the raw object
			import oculus
			index=0
			sensorList = oculus.getSensors()
			if index < len(sensorList):
				orientationTracker = sensorList[index]
			else:
				viz.logWarn("** WARNING: Oculus VR Rift Orientation Tracker not present.")
				orientationTracker = viz.addGroup()
				orientationTracker.invalidTracker = True
			rawTracker[_name] = orientationTracker
	
		#VC: init the wrapper (DO NOT EDIT)
		if initFlag&vizconnect.INIT_WRAPPERS:
			vizconnect.addTracker(rawTracker[_name], _name, make='Oculus VR', model='Rift Orientation Tracker')
	
		#VC: init the offsets
		if initFlag&vizconnect.INIT_OFFSETS:
			_link = vizconnect.getTracker(_name).getLink()
			#VC: clear link offsets
			_link.reset(viz.RESET_OPERATORS)
			
			#VC: reset orientation
			_link.preEuler([0, 0, 0], target=viz.LINK_ORI_OP, priority=-20)
			
			#VC: apply offsets
			_link.postTrans([0, 1.6, 0])

	#VC: return values can be modified here
	return None


#################################
# Input Code
#################################

def initInputs(initFlag=vizconnect.INIT_INDEPENDENT, initList=None):
	#VC: place any general initialization code here
	rawInput = vizconnect.getRawInputDict()

	#VC: initialize a new input
	_name = 'joystick'
	if vizconnect.isPendingInit('input', _name, initFlag, initList):
		#VC: init the raw object
		if initFlag&vizconnect.INIT_RAW:
			#VC: create the raw object
			import vizjoy
			rawInput[_name] = vizjoy.add()
	
		#VC: init the wrapper (DO NOT EDIT)
		if initFlag&vizconnect.INIT_WRAPPERS:
			vizconnect.addInput(rawInput[_name], _name, make='Generic', model='Joystick')

	#VC: set the name of the default
	vizconnect.setDefault('input', 'joystick')

	#VC: return values can be modified here
	return None


#################################
# Event Code
#################################

def initEvents(initFlag=vizconnect.INIT_INDEPENDENT, initList=None):
	#VC: place any general initialization code here
	rawEvent = vizconnect.getRawEventDict()

	#VC: return values can be modified here
	return None


#################################
# Transport Code
#################################

def initTransports(initFlag=vizconnect.INIT_INDEPENDENT, initList=None):
	#VC: place any general initialization code here
	rawTransport = vizconnect.getRawTransportDict()

	#VC: initialize a new transport
	_name = 'walking'
	if vizconnect.isPendingInit('transport', _name, initFlag, initList):
		#VC: init the raw object
		if initFlag&vizconnect.INIT_RAW:
			#VC: set some parameters
			height = 0
			acceleration = 4
			maxSpeed = 10.44
			rotationAcceleration = 90
			maxRotationSpeed = 120
			autoBreakingDragCoef = 0.1
			dragCoef = 0.0001
			rotationAutoBreakingDragCoef = 0.2
			rotationDragCoef = 0.0001
			transportationGroup = None
			
			#VC: create the raw object
			from transportation import walking
			rawTransport[_name] = walking.Walking(	node=transportationGroup,
									height=height,
									acceleration=acceleration,
									maxSpeed=maxSpeed,
									rotationAcceleration=rotationAcceleration,
									maxRotationSpeed=maxRotationSpeed,
									autoBreakingDragCoef=autoBreakingDragCoef,
									dragCoef=dragCoef,
									rotationAutoBreakingDragCoef=rotationAutoBreakingDragCoef,
									rotationDragCoef=rotationDragCoef)
	
		#VC: init the mappings for the raw object
		if initFlag&vizconnect.INIT_MAPPINGS:
			#VC: per frame mappings
			if initFlag&vizconnect.INIT_MAPPINGS_PER_FRAME:
				#VC: get the raw input dict so we have access to signals
				import vizact
				rawInput = vizconnect.getConfiguration().getRawDict('input')
				#VC: set the update function which checks for input signals
				def update(transport):
					if rawInput['joystick'].getPosition()[1] < -0.05:# make=Generic, model=Joystick, name=joystick, signal=Analog Up
						transport.moveForward(mag=abs(rawInput['joystick'].getPosition()[1]))
					if rawInput['joystick'].getPosition()[1] > 0.05:# make=Generic, model=Joystick, name=joystick, signal=Analog Down
						transport.moveBackward(mag=abs(rawInput['joystick'].getPosition()[1]))
					if rawInput['joystick'].getPosition()[0] < -0.05:# make=Generic, model=Joystick, name=joystick, signal=Analog Left
						transport.moveLeft(mag=abs(rawInput['joystick'].getPosition()[0]))
					if rawInput['joystick'].getPosition()[0] > 0.05:# make=Generic, model=Joystick, name=joystick, signal=Analog Right
						transport.moveRight(mag=abs(rawInput['joystick'].getPosition()[0]))
					if rawInput['joystick'].getRotation()[0] < -0.05:# make=Generic, model=Joystick, name=joystick, signal=Rotate X Left
						transport.turnLeft(mag=abs(rawInput['joystick'].getRotation()[0]))
					if rawInput['joystick'].getRotation()[0] > 0.05:# make=Generic, model=Joystick, name=joystick, signal=Rotate X Right
						transport.turnRight(mag=abs(rawInput['joystick'].getRotation()[0]))
				rawTransport[_name].setUpdateFunction(update)
	
		#VC: init the wrapper (DO NOT EDIT)
		if initFlag&vizconnect.INIT_WRAPPERS:
			vizconnect.addTransport(rawTransport[_name], _name, make='Virtual', model='Walking')
	
		#VC: set the parent of the node
		if initFlag&vizconnect.INIT_PARENTS:
			vizconnect.getTransport(_name).setParent(vizconnect.getRoot())

	#VC: set the name of the default
	vizconnect.setDefault('transport', 'wandmagicccarpet')

	#VC: return values can be modified here
	return None


#################################
# Tool Code
#################################

def initTools(initFlag=vizconnect.INIT_INDEPENDENT, initList=None):
	#VC: place any general initialization code here
	rawTool = vizconnect.getRawToolDict()
	
	#VC: return values can be modified here
	return None


#################################
# Avatar Code
#################################

def initAvatars(initFlag=vizconnect.INIT_INDEPENDENT, initList=None):
	#VC: place any general initialization code here
	rawAvatar = vizconnect.getRawAvatarDict()

	#VC: initialize a new avatar
	_name = 'female'
	if vizconnect.isPendingInit('avatar', _name, initFlag, initList):
		#VC: init the raw object
		if initFlag&vizconnect.INIT_RAW:
			#VC: create the raw object
			avatar = viz.add('vcc_female.cfg')
			avatar._bodyPartDict = {}
			avatar._handModelDict = {}
			rawAvatar[_name] = avatar
	
		#VC: init the wrapper (DO NOT EDIT)
		if initFlag&vizconnect.INIT_WRAPPERS:
			vizconnect.addAvatar(rawAvatar[_name], _name, make='Complete Characters', model='Female')
	
		#VC: init the animator
		if initFlag&vizconnect.INIT_ANIMATOR:
			# need to get the raw tracker dict for animating the avatars
			from vizconnect.util.avatar import animator
			from vizconnect.util.avatar import skeleton
			
			# get the skeleton from the avatar
			_skeleton = skeleton.CompleteCharacters(rawAvatar[_name])
			
			#VC: set which trackers animate which body part
			# format is: bone: (tracker, parent, degrees of freedom used)
			_trackerAssignmentDict = {
				vizconnect.AVATAR_HEAD:(vizconnect.getTracker('rift_orientation_tracker').getNode3d(), None, vizconnect.DOF_ORI),
			}
			
			#VC: create the raw object
			_rawAnimator = animator.InverseKinematics(rawAvatar[_name], _skeleton, _trackerAssignmentDict)
			
			#VC: set animator in wrapper (DO NOT EDIT)
			vizconnect.getAvatar(_name).setAnimator(_rawAnimator, make='WorldViz', model='Inverse Kinematics')
	
		#VC: init the mappings for the wrapper
		if initFlag&vizconnect.INIT_WRAPPER_MAPPINGS:
			#VC: on-state mappings
			if initFlag&vizconnect.INIT_MAPPINGS_ON_STATE:
				vizconnect.getAvatar(_name).setOnStateEventList([
						vizconnect.onstate(lambda rawInput: rawInput['joystick'].isButtonDown(3), vizconnect.getAvatar(_name).setVisible),# make=Generic, model=Joystick, name=joystick, signal=Button 3
				])
	
		#VC: set the parent of the node
		if initFlag&vizconnect.INIT_PARENTS:
			vizconnect.getAvatar(_name).setParent(vizconnect.getTransport('walking'))

	#VC: return values can be modified here
	return None


#################################
# Application Settings
#################################

def initSettings():
	#VC: apply general application settings
	viz.mouse.setTrap(False)
	viz.mouse.setVisible(viz.MOUSE_AUTO_HIDE)
	vizconnect.setMouseTrapToggleKey('')
	
	#VC: return values can be modified here
	return None


#################################
# Post-initialization Code
#################################

def postInit():
	"""Add any code here which should be called after all of the initialization of this configuration is complete.
	Returned values can be obtained by calling getPostInitResult for this file's vizconnect.Configuration instance."""
	viz.phys.setGravity(0,0,0)
	import vizact
	collideBox = vizconnect.getRawTransport().getPhysicsNode().collideNone()
	collideBox = vizconnect.getRawTransport().getPhysicsNode().collideBox(1,2,1)
	collideBox.setBounce(.0001)
	collideBox.setFriction(.00)
	
	vizconnect.getRawTransport().getPhysicsLink().reset( viz.RESET_OPERATORS )
	vizconnect.getRawTransport().getPhysicsLink().preTrans([0,-.9,0])
	vizconnect.getRawTransport().getPhysicsNode().setPosition(0,1,0)
	
	
	return None


#################################
# Stand alone configuration
#################################

def initInterface():
	#VC: start the interface
	vizconnect.interface.go(__file__,
							live=True,
							openBrowserWindow=True,
							openChromiumWindow=False,
							startingInterface=vizconnect.interface.INTERFACE_ADVANCED)

	#VC: return values can be modified here
	return None


###############################################

if __name__ == "__main__":
	initInterface()
	gal = viz.add('gallery.osgb')
#	gal.collideMesh()
#	viz.phys.enable()
	
	
viz.stereo( viz.STEREO_3DTV_SIDE_BY_SIDE )