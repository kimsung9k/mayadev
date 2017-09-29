from sgMaya import sgAnim
import pymel.core
sels = pymel.core.ls( sl=1 )
sgAnim.ParentedMove.set( sels[0], sels[1] )
sgAnim.ParentedMove.createExpression()