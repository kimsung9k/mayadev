from sgMaya import sgAnim
import pymel.core
sels = pymel.core.ls( sl=1 )
for sel in sels:
    try:sgAnim.ParentedMove.reset( sel )
    except:continue