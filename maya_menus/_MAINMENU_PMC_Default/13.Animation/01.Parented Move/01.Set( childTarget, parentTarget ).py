from sgMaya import sgRig
import pymel.core
sels = pymel.core.ls( sl=1 )
sgRig.ParentedMove.set( sels[0], sels[1] )
sgRig.ParentedMove.createExpression()