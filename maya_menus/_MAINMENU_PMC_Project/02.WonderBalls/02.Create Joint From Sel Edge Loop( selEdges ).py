from sgProject import wonderBalls
import pymel.core
sels = pymel.core.ls( sl=1, fl=1 )
wonderBalls.buildJointFromEdgeLineVertices( sels )