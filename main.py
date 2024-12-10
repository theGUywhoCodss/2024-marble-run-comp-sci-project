import gizeh
import moviepy.editor as mpy
import math
import random
from defines import *
from marbleClass import *
from effects import *

marbles = [] # Marbles array

blueSpawnTime = random.uniform(BLUE_SPAWN_MIN,BLUE_SPAWN_MAX)
blueLastSpawn = 0
blueLastAmount = 0
blueLastType = "None"
bluePoints = 0
redSpawnTime = random.uniform(RED_SPAWN_MIN,RED_SPAWN_MAX)
redLastSpawn = 0
redLastAmount = 0
redPoints = 0
redLastType = "None"
print(winScreenTime)

def make_frame(t):
    global redPoints
    global bluePoints
    global marbles
    surface = gizeh.Surface(W,H)
    gizeh_draw_text(surface,str(getDeltaTime()*t),20,(1,1,1),(W/2,10))
    if DURATION-t > winScreenTime:
        # main simulation
        background = gizeh.rectangle(lx=W, ly=H,fill=(0,1,0),xy=center)
        background.draw(surface)
        # marble collision
        marble_collision(t)
        handleEffects(surface, t)
        # marble spawning
        gizeh_draw_text(surface,str(redLastAmount),50,(1,0.25,0),(50,50))
        gizeh_draw_text(surface,str(blueLastAmount),50,(0,0.25,1),(W-50,50))
        # death amount
        gizeh_draw_text(surface,str(redPoints),25,(1,0.25,0),(50,75))
        gizeh_draw_text(surface,str(bluePoints),25,(0,0.25,1),(W-50,75))
        spawn_marble(t)

        new_marble_list = []
        for obj in marbles:
            # marble modification
            obj.update(marbles)
            obj.draw(surface)
            # array modification
            if obj.health <= 0:
                # win modifier
                if obj.team == 1:
                    redPoints+=1
                else:
                    bluePoints+=1
            else:
                new_marble_list.append(obj)
        marbles = new_marble_list
    else:
        # point count
        gizeh_draw_text(surface,str(redPoints),25,(1,0.25,0),(50,75))
        gizeh_draw_text(surface,str(bluePoints),25,(0,0.25,1),(W-50,75))
        # winner text
        if bluePoints>redPoints:
            gizeh_draw_text(surface,"Blue wins!",50,(0,0.25,1),(W/2,75))
        elif redPoints>bluePoints:
            gizeh_draw_text(surface,"Red wins!",50,(0,0.25,1),(W/2,75))
        else:
            gizeh_draw_text(surface,"Tie!",50,(0,0.25,1),(W/2,75))


    return surface.get_npimage()

def gizeh_draw_text(surface, text, fontsize, fill, xy):
    text = gizeh.text(text, fontsize=fontsize, fontfamily="Impact", 
           fill=fill, 
           xy=xy)
    text.draw(surface)

def spawn_marble(t):
    global redSpawnTime
    global redLastSpawn
    global redLastAmount
    global blueSpawnTime
    global blueLastSpawn
    global blueLastAmount
    # Red team.
    spawnAmount = random.randint(1,6)
    if(t-redLastSpawn>=redSpawnTime and len(marbles)<CONST_MAXMARBLES+spawnAmount):  
        # red marble spawning
        for i in range(0,spawnAmount): 
            marbles.append(marble(x = 16, 
                y = random.randint(0,H),radius = 16, 
                angle = random.randint(1,180)-90,team = 1,type = random.randint(1,3)))
        # red team modification
        redLastSpawn = t
        redSpawnTime = random.uniform(RED_SPAWN_MIN, RED_SPAWN_MAX)
        redLastAmount = spawnAmount
    # Blue team.
    spawnAmount = random.randint(1,6)
    marbleType = random.randint(1,100)
    if(t-blueLastSpawn>=blueSpawnTime and len(marbles)<CONST_MAXMARBLES+spawnAmount):  
        # blue marble spawning
        for i in range(0,spawnAmount): 
            marbles.append(marble(x = W-16, 
                y = random.randint(0,H),radius = 16, 
                angle = random.randint(90,270),team = 2,type = random.randint(1,3)))
        # blue team modifcation
        blueLastSpawn = t
        blueSpawnTime = random.uniform(BLUE_SPAWN_MIN, BLUE_SPAWN_MAX)
        blueLastAmount = spawnAmount

def marble_collision(t):
    '''Loop through marbles and get the velocity ->
    Check other marbles in relation to that marble ->
    Adjust marble and the other marble based on relationship.'''
    for obj in marbles:
        velocity = obj.getVelocity()
        for obj2 in marbles:
            if (not obj.colided and not obj2.colided and 
                obj.checkCollision(obj2.x,obj2.y,obj2.radius) 
                and obj != obj2):
                objVelocity = obj2.getVelocity()
                normalAngle = math.atan2(obj2.y-obj.y,obj2.x-obj.x)
                # Unstuck the marbles
                obj.x = obj2.x-(obj2.radius+obj.radius)*math.cos(normalAngle)
                obj.y = obj2.y-(obj2.radius+obj.radius)*math.sin(normalAngle)
                obj2.x = obj.x+(obj2.radius+obj.radius)*math.cos(normalAngle)
                obj2.y = obj.y+(obj2.radius+obj.radius)*math.sin(normalAngle)
                # The marbles bounce off eachother based on the normal.
                obj.update_angle(normalAngle-math.pi)
                obj2.update_angle(normalAngle)
                obj.colided = True
                obj2.colided = True
                # Apply damage for both marbles if not same team.
                if obj.team != obj2.team:
                    # 1 is bomb. 2 is metal. 3 is spike.
                    # Bomb wins over spike.
                    if obj.type == 1 and obj2.type == 3:
                        obj2.health -= 10
                        addEffect(obj2.x, obj2.y, t, "bomb", "boom")
                    if obj2.type == 1 and obj.type == 3:
                        obj.health -= 10
                        addEffect(obj.x, obj.y, t, "bomb", "boom")
                    # Spike wins over metal.
                    if obj.type == 3 and obj2.type == 2:
                        obj2.health -= 10
                    if obj2.type == 3 and obj.type == 2:
                        obj.health -= 10
                    # Metal wins over bomb.
                    if obj.type == 2 and obj2.type == 1:
                        obj2.health -= 10
                    if obj2.type == 2 and obj.type == 1:
                        obj.health -= 10
                    # Tie.
                    if obj.type == obj2.type:
                        obj.health -= 10
                        obj2.health -= 10

            if obj.x + obj.radius > W:
                obj.update_angle(math.atan2(velocity[1],-velocity[0]))
                obj.x = W-obj.radius
            elif obj.x-obj.radius < 0:
                obj.update_angle(math.atan2(velocity[1],-velocity[0]))
                obj.x = obj.radius
            if obj.y + obj.radius > H:
                obj.update_angle(math.atan2(-velocity[1],velocity[0]))
                obj.y = H-obj.radius
            elif obj.y-obj.radius < 0:
                obj.update_angle(math.atan2(-velocity[1],velocity[0]))
                obj.y = obj.radius

clip = mpy.VideoClip(make_frame, duration=DURATION) # Make video
clip.write_videofile("input.mp4", fps=FPS, codec='libx264', preset="ultrafast")
print(len(marbles))