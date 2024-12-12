FPS = 15
W,H = 1280,720 # width, height, in pixels
DURATION = 60 # duration of the clip, in seconds
CONST_MAXMARBLES = 200

# Spawn time constants
RED_SPAWN_MIN = 0.25
RED_SPAWN_MAX = 1
BLUE_SPAWN_MIN = 0.25
BLUE_SPAWN_MAX = 1

center = [W/2, H/2]

winScreenTime = 1

def getDeltaTime(): # Adjust movement based on fps
    return 1/FPS