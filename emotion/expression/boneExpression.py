import viz
import vizact
import time
import random

#Use this class to keep track of bone positions as Vizard doesn't seem to be update them correctly
class Bone(object):
	
	def __init__(self, name, vizardCharacter):
		self.name = name
		self.bone=vizardCharacter.getBone(name)
		self.position = [0,0,0]
	
	def setPosition(self, position):
		self.position = position
		
	def moveBone(self,x,y,z):
		#Move the bone absolutely to its current position
		self.bone.lock()
		self.bone.setPosition(x-self.position[0], y-self.position[1], z-self.position[2], viz.REL_LOCAL)
		self.setPosition([x,y,z])
	
		
class BoneExpression(object):
	
	def __init__(self, name, bones, maxPositions):
		self.name=name
		self.maxPos=dict()
		self.talking=False
		for i in range(len(bones)):
			self.maxPos[bones[i]]=maxPositions[i]

class CategoricalBoneExpression(object):
	
	
	def __init__(self, vizardCharacter):
		self.emotionsLookup=dict()
		self.emotions=[]
		self.bones = []
		self.boneLookup = dict();
		self.talking=False;
		#create bone expression model
		#Initialize bones by adding a bonehandler to the avatar
		#this assumes the default FACS bone setup with the bones as can be found in bonehandler (boneExpression.py)
		#students boneArray=['bone_Jaw',		'bone_BrowInnerL',	'bone_BrowInnerR',	'bone_BrowOuterL',	'bone_BrowOuterR',	'bone_LidUpperL',	'bone_LidUpperR',	'bone_LidLowerL',	'bone_LidLowerR',	'bone_LipCornerL',    'bone_LipCornerR',    'bone_LipLowerL',    'bone_LipLowerR',    'bone_LipUpperL',    'bone_LipUpperR',    'bone_CheekL',    'bone_CheekR', 'bone_Nostrils']
		
		boneArray=[	'Bip01 Head',	'bJaw',	'bNostrils',	'bLipLL',	'bLipLR',	'bLipUL',	'bLipUR',	'bLipCL',	'bLipCR',	'bCheekL',	'bCheekR',	'bEyeL',	'bEyeR',	'bLidLL',	'bLidLR',	'bLidUL',	'bLidUR',	'bBrowIL',	'bBrowIR',	'bBrowOL',	'bBrowOR'	]
		self.add(BoneExpression('surprise',boneArray,[	[0.002, 0.005, 0  ],	[  -0.005, 0, 0.01],	[0, 0, 0  ],	[0, -0.001, -0.001],	[0, 0.001, -0.001],	[0, -0.002, -0.001],	[0, 0.002, -0.001],	[0, -0.001, 0],	[0, 0.001, 0],	[0, 0.0, 0.004],	[0, 0.0, 0.004],	[0,0,0],	[0,0,0],	[0, 0, 0.001],	[0, 0, 0.001],	[0, 0, -0.003],	[0, 0, -0.003],	[0, 0, -0.005],	[0, 0, -0.005],	[0, 0, -0.005],	[0, 0, -0.005]	]))
		self.add(BoneExpression('happy',boneArray,[	[0, 0, 0  ],	[0,0,0],	[0, 0, 0  ],	[-0.002, 0.001, 0.001],	[-0.002, -0.001, 0.001],	[-0.001, 0.001, -0.001],	[-0.001, -0.001, -0.001],	[-0.005, 0.009, -0.007],	[-0.005, -0.009, -0.007],	[0, 0, -0.011],	[0, 0, -0.011],	[0,0,0],	[0,0,0],	[0, 0, -0.0017],	[0, 0, -0.0017],	[0, 0, 0.0015],	[0, 0, 0.0015],	[0, 0, 0.0],	[0, 0, 0.0],	[0, 0, 0.0],	[0, 0, 0.0]	]))
		self.add(BoneExpression('sad',boneArray,[	[-0.002, 0, 0],	[  0, 0, 0],	[0, 0, 0  ],	[0, 0.001, 0.001],	[0, -0.001, 0.001],	[0, 0.001, 0.001],	[0, -0.001, 0.001],	[0, 0.002, 0.007],	[0, -0.002, 0.007],	[0, 0, 0],	[0, 0, 0],	[0,0,0],	[0,0,0],	[0, 0, 0],	[0, 0, 0],	[0, 0, 0.001],	[0, 0, 0.001],	[0, 0, -0.005],	[0, 0, -0.005],	[0, 0, 0.006],	[0, 0, 0.006]	]))
		self.add(BoneExpression('angry',boneArray,[	[0.002, 0.005, 0  ],	[  0, 0, 0],	[0, 0, 0  ],	[0, -0.002, 0],	[0, 0.002, 0],	[0, -0.002, -0.002],	[0, 0.002, -0.002],	[0, -0.004,0],	[0, 0.004,0],	[0, 0, 0],	[0, 0, 0],	[0,0,0],	[0,0,0],	[0, 0, 0.001],	[0, 0, 0.001],	[0, 0,0],	[0, 0, 0],	[0, -0.013, 0.012],	[0, 0.013, 0.012],	[0, 0, 0.003],	[0, 0, 0.003]	]))
		self.add(BoneExpression('disgust',boneArray,[	[0, -0.005, 0.003 ],	[  -0.001, 0, 0.001],	[0, 0, -0.008],	[-0.004, 0.002, 0.002],	[-0.004, -0.002, 0.0025],	[-0.002, 0.002, -0.0045],	[-0.002, -0.002, -0.0045],	[0, -0.001, 0],	[0, 0.001, 0],	[0, 0, -0.003],	[0, 0, -0.003],	[0,0,0],	[0,0,0],	[0, 0, -0.0025],	[0, 0, -0.0025],	[0, 0, 0.002],	[0, 0, 0.002],	[0, -0.013, 0.004],	[0, 0.013, 0.004],	[0, -0.002, 0],	[0, 0.002, 0]	]))
		self.add(BoneExpression('fear',boneArray,[	[0, -0.005, 0  ],	[  -0.002, 0, 0.003],	[0, 0, 0  ],	[0, 0, 0.002],	[0, 0, 0.002],	[0, 0, -0.002],	[0, 0, -0.002],	[0, 0.002, 0.003],	[0, -0.002, 0.003],	[0, 0, 0],	[0, 0, 0],	[0,0,0],	[0,0,0],	[0, 0, 0.002],	[0, 0, 0.002],	[0, 0, -0.003],	[0, 0, -0.003],	[0, -0.008, -0.006],	[0, 0.008, -0.006],	[0, 0, 0.004],	[0, 0, 0.004]	]))
		self.add(BoneExpression('blink',boneArray,[	[0, 0, 0  ],	[  0, 0, 0],	[0, 0, 0  ],	[  0, 0, 0],	[  0, 0, 0],	[  0, 0, 0],	[  0, 0, 0],	[  0, 0, 0],	[  0, 0, 0],	[  0, 0, 0],	[  0, 0, 0],	[0,0,0],	[0,0,0],	[  0, 0, 0],	[  0, 0, 0],	[0, 0, 0.008],	[0, 0, 0.008],	[  0, 0, 0],	[  0, 0, 0],	[  0, 0, 0],	[  0, 0, 0]	]))
		self.add(BoneExpression('lookLeft',boneArray,[	[0, 0, -0.001  ],	[  0, 0, 0],	[0, 0, 0  ],	[  0, 0, 0],	[  0, 0, 0],	[  0, 0, 0],	[  0, 0, 0],	[  0, 0, 0],	[  0, 0, 0],	[  0, 0, 0],	[  0, 0, 0],	[0,0.001,0],	[0,0.001,0],	[  0, 0, 0],	[  0, 0, 0],	[  0, 0, 0],	[  0, 0, 0],	[  0, 0, 0],	[  0, 0, 0],	[  0, 0, 0],	[  0, 0, 0]	]))
		self.add(BoneExpression('lookRight',boneArray,[	[0, 0, 0.001],	[  0, 0, 0],	[0, 0, 0  ],	[  0, 0, 0],	[  0, 0, 0],	[  0, 0, 0],	[  0, 0, 0],	[  0, 0, 0],	[  0, 0, 0],	[  0, 0, 0],	[  0, 0, 0],	[0,-0.001,0],	[0,-0.001,0],	[  0, 0, 0],	[  0, 0, 0],	[  0, 0, 0],	[  0, 0, 0],	[  0, 0, 0],	[  0, 0, 0],	[  0, 0, 0],	[  0, 0, 0]	]))
		
		for bone in boneArray:
			newBone=Bone(bone, vizardCharacter)
			self.bones.append(newBone)
			self.boneLookup[bone]=newBone
	
	def add(self, emotion):
		self.emotionsLookup[emotion.name]=emotion
		self.emotions.append(emotion)
	
	def talk(self, speed, duration):
		self.talking=True
		self.lastTimer=time.clock()
		self.endTimer=time.clock()+duration
		self.speed=speed
		self.mouthOpen = 0
		
	def express(self, names, intensities, mixed, intensityBooster, mood=False):
		lookUp=dict()
		largest = -1
		#Find the largest intensity emotion, this is the one expressed if we don't use mixing
		for i in range(len(intensities)):
			lookUp[names[i]]=min(1, max(0, intensities[i]))
			if(largest==-1 or intensities[i] > intensities[largest]):
				largest = i		
		#now calculate for each bone its correct position and update the position
		for bone in self.bones:
			x=0
			y=0
			z=0
			if ((self.talking==False or bone.name!="bJaw") and (mood==False or (bone.name!="bJaw" and bone.name!="bLipLL" and bone.name!="bLipLR" and bone.name!="bLipUL" and bone.name!="bLipUR"))):
				#only if we express an emotion do we change the mouth openness, expresing a mood is always with mouth closed
				for i in range(len(self.emotions)):
					name=self.emotions[i].name
					if name in lookUp:
						#we found the emotion in the to be expressed list
						if (mixed or names[largest]==name):
							x=x+self.emotionsLookup[name].maxPos[bone.name][0]*lookUp[name]*intensityBooster
							y=y+self.emotionsLookup[name].maxPos[bone.name][1]*lookUp[name]*intensityBooster
							z=z+self.emotionsLookup[name].maxPos[bone.name][2]*lookUp[name]*intensityBooster
			elif (self.talking==True and bone.name=="bJaw"):
				#do bone stuff for talking
				elapsed = (time.clock()-self.lastTimer)
				self.lastTimer+=elapsed
				#If spinning for a finite duration, check if time has passed
				if (time.clock() > self.endTimer):
					talking=False
				else:
					inc = self.speed*elapsed
					if ((inc>0 and self.mouthOpen+inc>0.012*random.random()) or (inc<0 and self.mouthOpen+inc<0)):
						self.speed=-self.speed
						inc = self.speed*elapsed
					self.mouthOpen += inc
					z=self.mouthOpen
					
			bone.moveBone(x,y,z)