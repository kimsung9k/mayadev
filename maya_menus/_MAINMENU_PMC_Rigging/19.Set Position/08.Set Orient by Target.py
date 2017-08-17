import pymel.core

sels = pymel.core.ls( sl=1 )

rotValue = sels[-1].getRotation( ws=1 )

for sel in sels[:-1]:
    sel.setRotation( rotValue, ws=1 )