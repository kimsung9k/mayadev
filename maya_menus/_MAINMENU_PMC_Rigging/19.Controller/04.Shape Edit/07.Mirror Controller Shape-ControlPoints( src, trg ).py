import pymel.core
sels = pymel.core.ls( sl=1 )

first = sels[0].getShape()
second = sels[1].getShape()

for i in range( first.numCVs() ):
    second.controlPoints[i].set( -first.controlPoints[i].get() )