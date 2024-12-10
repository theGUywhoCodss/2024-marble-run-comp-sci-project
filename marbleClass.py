import math
import random
import gizeh
from defines import *
from convertedPNG import bomb,metal,spike

bombImg = gizeh.ImagePattern(image=bomb, pixel_zero=[16, 16], filter="best", extend="none")
metalImg = gizeh.ImagePattern(image=metal, pixel_zero=[16, 16], filter="best", extend="none")
spikeImg = gizeh.ImagePattern(image=spike, pixel_zero=[16, 16], filter="best", extend="none")

# Special marbles include spike, metal, bomb. Bomb counters spike. Metal counters bomb. Spike counters metal.
# Bomb1 -> Spike3 -> Metal2

class marble: # Marble class for marbling
    def __init__(self, x, y, radius, angle = 0, team=0, type = 0):
        self.x = float(x)
        self.y = float(y)
        self.lastx = self.x
        self.lasty = self.y
        self.speed = 200
        self.angle = angle
        self.radius = radius
        self.team = team
        self.health = 10
        self.colided = False

        self.type = type
        
        colorinfo = (random.randint(0,100)/100,
            random.randint(0,100)/100,random.randint(0,100)/100)
        if(team == 1):
            colorinfo = (1,0,0)
        elif team == 2:
            colorinfo = (0,0,1)
        self.gradient = gizeh.ColorGradient(type="radial",
                stops_colors = [(0,colorinfo),(1,(0.1,0,0))],
                xy1=[0.3,-0.3], xy2=[0,0], xy3 = [0,1.4])
    
    def update_angle(self,value): # Update the angle based on value.
        if(self.angle<=0):
            self.angle = 2*math.pi
        elif(self.angle>2*math.pi):
            self.angle -= 2*math.pi
        self.angle = value

    def checkCollision(self, otherx, othery, otherRadius): # Check if collides with other marble.
        distence = math.sqrt((otherx-self.x)**2+(othery-self.y)**2)
        return distence <= self.radius+otherRadius

    def getVelocity(self):
        return (self.speed*math.cos(self.angle)*getDeltaTime(),self.speed*math.sin(self.angle)*getDeltaTime())

    def update(self, marbles):
        velocity = self.getVelocity()
        self.lastx = self.x
        self.lasty = self.y
        self.x += velocity[0]
        self.y += velocity[1]
        self.colided = False
        
    def draw(self,surface):
        #https://github.com/Zulko/gizeh/issues/24
        ball = gizeh.circle(r=1, fill=self.gradient).scale(self.radius).translate((self.x,self.y))
        ball.draw(surface)
        if self.type == 1:
            circ = gizeh.rectangle(lx=32, ly=32, fill=bombImg, xy=(self.x,self.y))
            circ.draw(surface)
        if self.type == 2:
            circ = gizeh.rectangle(lx=32, ly=32, fill=metalImg, xy=(self.x,self.y))
            circ.draw(surface)
        if self.type == 3:
            circ = gizeh.rectangle(lx=32, ly=32, fill=spikeImg, xy=(self.x,self.y))
            circ.draw(surface)