import pymel.core
sels = pymel.core.ls( sl=1 )
srcSel = sels[0]
dstSel = sels[1]

srcShape = srcSel.getShape()
dstShape = dstSel.getShape()

srcShape.local >> dstShape.create