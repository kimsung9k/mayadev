import pymel.core
sels = pymel.core.ls( sl=1 )
for sel in sels:
    sel.rotatePivot.set( 0,0,0 )
    sel.scalePivot.set( 0,0,0 )
    sel.rotatePivotTranslate.set( 0,0,0 )
    sel.scalePivotTranslate.set( 0,0,0 )