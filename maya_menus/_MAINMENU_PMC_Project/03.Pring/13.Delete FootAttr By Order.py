from maya import cmds
import pymel.core
sels = pymel.core.ls( 'Ctl_FootIkFootPiv_*_' )

attrs = ['liftToe','liftHill','liftBall','bank','hillTwist','ballTwist','toeTwist','toeRot']
attrs.reverse()

for sel in sels:
    for attr in attrs:
        pymel.core.deleteAttr( sel.attr( attr ) )