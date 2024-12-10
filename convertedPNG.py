import numpy as np
from PIL import Image

folder = 'images/'
extension = '.png'

img = Image.open( folder+"bomb"+extension ).convert("RGBA")
bomb = np.array( img, dtype='uint8' )
np.save(folder+'bomb.npy', bomb)

img = Image.open( folder+"metal"+extension ).convert("RGBA")
metal = np.array( img, dtype='uint8' )
np.save(folder+'metal.npy', metal)

img = Image.open( folder+"spike"+extension ).convert("RGBA")
spike = np.array( img, dtype='uint8' )
np.save(folder+'spike.npy', spike)