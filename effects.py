import gizeh
from defines import *

class effect: 
    def __init__(self, x, y, currentTime, type = "none", inputString = ""):
        self.type = type
        self.string = inputString
        self.x = x
        self.y = y
        self.dead = False
        self.time = currentTime
    def draw(self, surface):
        if self.type == "bomb":
            ball = gizeh.circle(r=1, fill=(1,0,0)).scale(20).translate((self.x,self.y))
            ball.draw(surface)

effects = []

def addEffect(x, y, currentTime, type = "none", inputString = ""):
    effects.append(effect(x, y, currentTime, type, inputString))

def handleEffects(surface, time):
    global effects
    new_effect_array = []
    for i, obj in enumerate(effects):
        # effect updating
        obj.draw(surface)
        # effect filtering
        if time - obj.time >= 1:
            pass
        else:
            new_effect_array.append(obj)
    effects = new_effect_array