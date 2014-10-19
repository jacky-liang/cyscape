import math
import random
import viz
import vizact
from expression.boneExpression import *
from datetime import datetime

class Affect(object):
	
	def __init__(self, values):
		self.nr_of_factors=len(values);
		self.factor= [0.0]*self.nr_of_factors
		self.target= [0.0]*self.nr_of_factors
		self.neutral= [0.0]*self.nr_of_factors	#init at 0,0,0 neutral point
		self.onsetSteps= [0.0]*self.nr_of_factors	#init at 0 updates
		self.decaySteps= [0.0]*self.nr_of_factors	#init at 0 updates
		for i in range(len(values)):
			self.factor[i]=values[i]
		self.mood=None
		self.onsetDelay=1
		self.hold=1
		self.decayDelay=1
		self.update=False
			
	def set(self, values):
		for i in range(self.nr_of_factors):
			self.target[i]=values[i]
		if (self.mood):
			self.mood.influence(self.target)
		self.clip()
		self.startUpdate()
		
			
	def add(self, values):
		for i in range(self.nr_of_factors):
			self.target[i]=self.factor[i]+values[i]
		if (self.mood):
			self.mood.influence(self.target)
		self.clip()
		self.startUpdate()

	def setTiming(self, onset, hold, decay):
		self.onsetDelay=onset
		self.hold=hold
		self.decayDelay=decay
	
	def setNeutral(self, values):
		for i in range(self.nr_of_factors):
			self.neutral[i]=min(1, max(-1, values[i]))
	
	def startUpdate(self):
		self.changedLast=datetime.now()
		self.changedStart=datetime.now()
		
		#set the update steps to the correct increment per second towards the target emotion
		for i in range(self.nr_of_factors):
			self.onsetSteps[i]=(self.target[i]-self.factor[i])/self.onsetDelay
		
		#set the decay steps to the correct increment per second 
		for i in range(self.nr_of_factors):
			self.decaySteps[i]=(self.neutral[i]-self.target[i])/self.decayDelay
		
		self.update=True
		
	def doUpdate(self):
		#updates the current state towards neutral in self.delay seconds using 
		#self.steps increments per second
		if (self.update==True):
			#now we have a triggered emotion, we go to the emotion dynamics
			if (self.updatePeriod()<self.onsetDelay):
				for i in range(self.nr_of_factors):
					self.factor[i]+=self.elapsed()*self.onsetSteps[i]
				self.changedLast=datetime.now()
			elif (self.updatePeriod()>=self.onsetDelay and self.updatePeriod()<self.onsetDelay+self.hold):
				self.changedLast=datetime.now()
			elif (self.updatePeriod()<self.onsetDelay+self.hold+self.decayDelay):
				for i in range(self.nr_of_factors):
					self.factor[i]+=self.elapsed()*self.decaySteps[i]
				self.changedLast=datetime.now()
			else:
				for i in range(self.nr_of_factors):
					self.factor[i]=self.neutral[i]
				self.update=False
		else:
			#now we don't, so we keep setting our current state to our neutral state (which is the mood, if we have one).
			if (self.mood):
				for i in range(self.nr_of_factors):
					self.factor[i]=self.neutral[i]
	
	def linkToMood(self, mood):
		self.neutral=mood.factor
		self.mood=mood
		
	def clip(self):
		for i in range(self.nr_of_factors):
			self.factor[i]=min(1, max(-1, self.factor[i]))
		
	def reset(self):
		self.factor=[0.0]*self.nr_of_factors
		self.update=False;
		if (self.mood):
			self.mood.add(self.factor)
	
	def get(self):
		return self.factor
		
	def write(self):
		print self.factor
	
	def elapsed(self):
		return (datetime.now()-self.changedLast).seconds+(datetime.now()-self.changedLast).microseconds/1000000.0
		
	def updatePeriod(self):
		return (datetime.now()-self.changedStart).seconds+(datetime.now()-self.changedStart).microseconds/1000000.0
	
	def express(self, expressionModel, expressionOn=True, mixed=False, intensityBooster=1):
		self.expressionOn=expressionOn
		self.expressionModel=expressionModel
		self.mixed=mixed
		self.intensityBooster=intensityBooster
		
	def doExpress(self):
		None
		
class Emotion(Affect):
	def __init__(self, name, values, isEmotion=True):
		Affect.__init__(self, values)
		self.emotion= [0.0]*self.nr_of_factors
		for i in range(len(values)):
			self.emotion[i]=values[i]
		self.reset()
		self.name=name
		self.affect=None
		self.isEmotion=isEmotion
		
	def trigger(self, intensity=1):
		tempFactor=[]
		for i in range(self.nr_of_factors):
			tempFactor.append((self.emotion[i]*intensity))
		if (self.affect):
			#if this emotion is linked to an affective state (Affect object),
			# a trigger should be relayed to that object
			self.affect.set(tempFactor)
		else:
			self.set(tempFactor)
	
	def linkTo(self, affect):
		#links this state to the state of the underlying affect object
		self.factor=affect.factor
		self.affect=affect
	
	def updateReady(self):
		if (self.affect):
			return not self.affect.update
		else:
			return not self.update
			
	def doUpdate(self):
		if (self.affect):
			return self.affect.doUpdate()
		else:
			return super(Emotion, self).doUpdate()
		
	def intensity(self):
		sum=0
		total=0
		for i in range(self.nr_of_factors):
			sum+=math.pow(self.factor[i]-self.emotion[i], 2)
			total+=math.pow(self.emotion[i], 2)
		return max(0, 1.0-(math.sqrt(sum)/math.sqrt(total)))
	
	def doExpress(self):
		if (self.expressionOn):
			if (updateReady()):
				#express mood
				self.expressionModel.express([self.name], [self.intensity()], False, self.intensityBooster, True)
			else:
				#express emotion
				self.expressionModel.express([self.name], [self.intensity()], False, self.intensityBooster)

class Mood(Affect):
	def __init__(self, values, dampening=0.1):
		self.dampening=dampening
		Affect.__init__(self, values)
		self.dampening=dampening
		
	def influence(self, target):
		#updates the mood towards the target 
		#introduces a dampening factor
		for i in range(self.nr_of_factors):
			self.factor[i]+=((target[i]-self.factor[i])*self.dampening)
		self.clip()
		print str(self.factor[0]) +","+str(self.factor[1]) +","+str(self.factor[2])
	def set(self, values):
		for i in range(self.nr_of_factors):
			self.factor[i]=values[i]
		
		self.clip()	
			
class Categoricals(object):
	def __init__(self):
		self.emotions=[]
		self.emotionLookup=dict()
		self.names=[]
		self.intensities=[]
		self.expressionOn=False
		self.mixed=False
		self.expressionModel=None
		
	def add(self, emotion):
		self.emotions.append((0.0, emotion.name, emotion))
		self.names.append(emotion.name)
		self.intensities.append(0.0)
		self.emotionLookup[emotion.name]=emotion
		
	def trigger(self, name, intensity=1):
		if (isinstance(name,(list,tuple))):
			for i in range(len(name)):
				if (isinstance(intensity, (list,tuple))):
					self.emotionLookup[name[i]].trigger(intensity[i])
				else:
					self.emotionLookup[name[i]].trigger(intensity)
		else:
			self.emotionLookup[name].trigger(intensity)
		
	def getEmotionObject(self, name):
		return self.emotionLookup[name];
		
	def setTiming(self, onset, hold, decay):
		for i in range(len(self.emotions)):
			intensity, name, emotion = self.emotions[i]
			emotion.setTiming(onset, hold, decay)
			
	def doUpdate(self):
		for i in range(len(self.emotions)):
			intensity, name, emotion = self.emotions[i]
			emotion.doUpdate()
	
	def updateReady(self):
		for i in range(len(self.emotions)):
			intensity, name, emotion = self.emotions[i]
			if (emotion.isEmotion ==True and emotion.updateReady() == False):
				return False
		return True
		
	def linkTo(self, affect):
		for i in range(len(self.emotions)):
			intensity, name, emotion = self.emotions[i]
			emotion.linkTo(affect)
			
	def linkToMood(self, mood):
		for i in range(len(self.emotions)):
			intensity, name, emotion = self.emotions[i]
			emotion.linkToMood(mood)
			
	def getIntensities(self):
		#returns the emotion intensities
		for i in range(len(self.emotions)):
			intensity, name, emotion = self.emotions[i]
			self.emotions[i]=(emotion.intensity(), name, emotion)
			self.names[i]=name
			self.intensities[i]=emotion.intensity()
			
		return self.intensities
		
	def express(self, expressionModel, expressionOn=True, mixed=False, intensityBooster=1):
		self.expressionOn=expressionOn
		self.expressionModel=expressionModel
		self.mixed=mixed
		self.intensityBooster=intensityBooster
		
	def doExpress(self):
		if (self.expressionOn):
			self.getIntensities()
			if (self.updateReady()):
				#express mood
				self.expressionModel.express(self.names, self.intensities, self.mixed, self.intensityBooster, True)
			else:
				self.expressionModel.express(self.names, self.intensities, self.mixed, self.intensityBooster)
	
	
class AffectManager(object):
	#This class has to be instantiated for EACH VIRTUAL CHARACTER!
	#It handles the emotion update and expression updates and provides basic emotional system creation
	
	def __init__(self, ticksPerSecond):
		self.affectList=[]
		self.ticksPerSecond=ticksPerSecond
		self.timer = vizact.ontimer2(1.0/ticksPerSecond,viz.FOREVER,self.update)
		self.blinkOn=False
		self.blink=False
		
	def addAffect(self, affect):
		self.affectList.append(affect)
		
	def update(self):
		for affect in self.affectList:
			affect.doUpdate()
			affect.doExpress()
			if (self.blinkOn and random.random()<(.05/(self.ticksPerSecond/10))):
				select=random.random()
				if (select<.50):
					self.blink.trigger()
				elif (select<.75):
					self.lookLeft.trigger()
				else:
					self.lookRight.trigger()
		
	def setExpressionBooster(self, booster):
		self.emotions.express(self.expressionModel, True, True, booster)
		
	def setAnimation(self, blink):
		if (self.emotions):
			if (self.blink==False):
				self.blink=Emotion("blink", [1,1,1], False)
				self.blink.setTiming(.1,0,.1)
				self.emotions.add(self.blink)
				self.lookLeft=Emotion("lookLeft", [1,1,1], False)
				self.lookLeft.setTiming(.3,1,.3)
				self.emotions.add(self.lookLeft)
				self.lookRight=Emotion("lookRight", [1,1,1], False)
				self.lookRight.setTiming(.3,1,.3)
				self.emotions.add(self.lookRight)
				
			self.blinkOn=blink
		else:
			print "warning: blinking only available with expression model already in place"
		
		
	def createBasicPADWithoutExpression(self):
		#creates a bare minimum emotional state and returns the created affect object to manipulate (i.e., an affect object)
		self.affect=Affect([0,0,0])
		self.affect.setTiming(.4,0.3,0.3)
		self.addAffect(self.affect)

		return self.affect
		
	def createPAdWithMoodWithoutExpression(self):
		#creates a bare minimum emotional state with slowly changing mood and returns the created affect object to manipulate (i.e., an affect object)
		self.affect=Affect([0,0,0])
		self.affect.setTiming(.4,0.3,0.3)
		self.mood=Mood([0,0,0], 0.2)
		self.affect.linkToMood(self.mood)
		self.addAffect(self.affect)
		self.addAffect(self.mood)

		return self.affect
	
	def createBasicEkmanWithExpression(self, vizardCharacter):
		#creates 6 basic emotions, that are not linked to each other, accessable through the returned a Categorical object		#it also inititaies 6 emotion expressions based on the bone model from Broekens and Chao
		#This system allows for easy emotion prototyping, and allows for mixed expressions, because 
		#triggering one emotion wil not influence the other (the emotions do not share an underlying affective state)
		self.emotions=Categoricals()
		
		self.emotions.add(Emotion("happy", [1,1,1]))
		self.emotions.add(Emotion("sad", [-1,-1,-1]))
		self.emotions.add(Emotion("angry", [-1,1,1]))
		self.emotions.add(Emotion("fear", [-1,1,-1]))
		self.emotions.add(Emotion("surprise", [0,1,0]))
		self.emotions.add(Emotion("disgust", [-1,0.2,0.5]))
		
		self.addAffect(self.emotions)
		self.emotions.setTiming(.4,0.3,0.3)
		#timing based on Schmid and Cohn 2001, Smidth et al 2003
		#onset = .5, peak =.2 offset = .3, but as onset takes a bit from peak in a linear setting to correct for slow speed, onset became .4
		#Initialize categorical bone-based emotion expression
		self.expressionModel = CategoricalBoneExpression(vizardCharacter)
		#and tell the categorical emotions to use the just created expresison model
		#for expression
		self.emotions.express(self.expressionModel, True, True, 1)
		
		return self.emotions
	
	def createBasicEkmanWithMoodExpression(self, vizardCharacter):
		#creates 6 basic emotions, that are not linked to each other, accessable through the returned a Categorical object		#it also inititaies 6 emotion expressions based on the bone model from Broekens and Chao
		#This system allows for easy emotion prototyping, and allows for mixed expressions, because 
		#triggering one emotion wil not influence the other (the emotions do not share an underlying affective state)
		self.emotions=Categoricals()
		
		self.emotions.add(Emotion("happy", [1,1,1]))
		self.emotions.add(Emotion("sad", [-1,-1,-1]))
		self.emotions.add(Emotion("angry", [-1,1,1]))
		self.emotions.add(Emotion("fear", [-1,1,-1]))
		self.emotions.add(Emotion("surprise", [0,1,0]))
		self.emotions.add(Emotion("disgust", [-1,0.2,0.5]))
		
		self.addAffect(self.emotions)
		self.emotions.setTiming(.4,0.3,0.3)
		
		self.mood=Mood([0,0,0], 0.2)
		self.addAffect(self.mood)
		self.emotions.getEmotionObject("happy").linkToMood(self.mood)
		self.emotions.getEmotionObject("sad").linkToMood(self.mood)
		self.emotions.getEmotionObject("angry").linkToMood(self.mood)
		self.emotions.getEmotionObject("fear").linkToMood(self.mood)
		self.emotions.getEmotionObject("surprise").linkToMood(self.mood)
		self.emotions.getEmotionObject("disgust").linkToMood(self.mood)
		
		#timing based on Schmid and Cohn 2001, Smidth et al 2003
		#onset = .5, peak =.2 offset = .3, but as onset takes a bit from peak in a linear setting to correct for slow speed, onset became .4
		#Initialize categorical bone-based emotion expression
		self.expressionModel = CategoricalBoneExpression(vizardCharacter)
		#and tell the categorical emotions to use the just created expresison model
		#for expression
		self.emotions.express(self.expressionModel, True, True, 1)
		
		return self.emotions
	
	def createPADEkmanWithExpression(self, vizardCharacter):
		#creates 6 basic emotions, linked to each other with an underlying PAD Affective state.
		#It means that triggering one emotion in fact changes the underlying state, hence also influence the others emotions
		#The Method returns the Categoricals object, but the affect object is available thourgh <affectManager>.affect
		#This allows the user to change the state and see the effect on the categories e.g. by:
		#<affectManager>.affect.add([.5,.5,.5]  resulting in a movement of the actual affetcive state in the direction .5.5.5
		#it also inititaies 6 emotion expressions based on the bone model from Broekens and Chao
		#Please note that as the emotions share an underlying affective state, it is not possible to mix emotions 
		#by using the emotion.trigger() method, as this in fact changes the underlying affective state each time.
		#i.e., the character has only 1 affective state, that is kept consistent.
		#mixing is possible, but should be done by directly manipulating the affect object (affective state)
		#if this is not desired, use createBasicEkmanWithExpression()
		self.affect=Affect([0,0,0])
		self.affect.setTiming(.4,0.3,0.3)
		
		self.emotions=Categoricals()
		
		self.emotions.add(Emotion("happy", [1,1,1]))
		self.emotions.add(Emotion("sad", [-1,-1,-1]))
		self.emotions.add(Emotion("angry", [-1,1,1]))
		self.emotions.add(Emotion("fear", [-1,1,-1]))
		self.emotions.add(Emotion("surprise", [0,1,0]))
		self.emotions.add(Emotion("disgust", [-1,0.2,0.5]))
		
		self.emotions.linkTo(self.affect)
		
		self.addAffect(self.emotions)
		self.addAffect(self.affect)
		
		#Initialize categorical bone-based emotion expression
		self.expressionModel = CategoricalBoneExpression(vizardCharacter)
		#and tell the categorical emotions to use the just created expresison model
		#for expression
		self.emotions.express(self.expressionModel, True, True, 1)
		
		return self.emotions
	
	def createPADEkmanWithMoodWithExpression(self, vizardCharacter):
		#creates 6 basic emotions, linked to each other with an underlying PAD Affective state with MOOD.
		#It means that triggering one emotion in fact changes the underlying state, hence also influence the others emotions
		#The Method returns the Categoricals object, but the affect object is available thourgh <affectManager>.affect
		#This allows the user to change the state and see the effect on the categories e.g. by:
		#<affectManager>.affect.add([.5,.5,.5]  resulting in a movement of the actual affetcive state in the direction .5.5.5
		#it also inititaies 6 emotion expressions based on the bone model from Broekens and Chao
		#Please note that as the emotions share an underlying affective state, it is not possible to mix emotions 
		#by using the emotion.trigger() method, as this in fact changes the underlying affective state each time.
		#i.e., the character has only 1 affective state, that is kept consistent.
		#mixing is possible, but should be done by directly manipulating the affect object (affective state)
		#if this is not desired, use createBasicEkmanWithExpression()self.affect=Affect([0,0,0])
		#mood can be set by <affectManager>.mood.set([1,1,1])
		self.affect=Affect([0,0,0])
		self.affect.setTiming(.4,0.3,0.3)
		
		self.mood=Mood([0,0,0], 0.2)
		self.affect.linkToMood(self.mood)
		
		self.emotions=Categoricals()
		
		self.emotions.add(Emotion("happy", [1,1,1]))
		self.emotions.add(Emotion("sad", [-1,-1,-1]))
		self.emotions.add(Emotion("angry", [-1,1,1]))
		self.emotions.add(Emotion("fear", [-1,1,-1]))
		self.emotions.add(Emotion("surprise", [0,1,0]))
		self.emotions.add(Emotion("disgust", [-1,0.2,0.5]))

		self.emotions.linkTo(self.affect)
		
		self.addAffect(self.affect)
		self.addAffect(self.emotions)
		self.addAffect(self.mood)
		
		#Initialize categorical bone-based emotion expression
		self.expressionModel = CategoricalBoneExpression(vizardCharacter)
		#and tell the categorical emotions to use the just created expresison model
		#for expression
		self.emotions.express(self.expressionModel, True, True, 1)
		
		return self.emotions