from sgMaya import sgCmds
from sgProject import wonderBalls
import pymel.core

sels = pymel.core.ls( sl=1 )
wonderBalls.treeBendingLookAtConnect( sels[0], sels[1] )