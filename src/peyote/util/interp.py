"""processing will let you specify your coordinates as the centerpoint of a shape.  
shiftPosToCenter will translate your point by half of the width/height of your shape."""

__all__ = ['shiftPosToCenter',
           'norm',
           'lerp',
           'remap']

def shiftPosToCenter(value, distance):
    return value - (distance/2)

def norm(value, rangeMin, rangeMax):
    rangeSize = rangeMax - rangeMin
    return (value - rangeMin) / rangeSize

def lerp(pos1, pos2, intermediatePos):
    return pos1 + intermediatePos * (pos2 - pos1)

def remap(value, dataMin, dataMax, outputMin, outputMax):
    return lerp(outputMin, outputMax, norm(value, dataMin, dataMax))

