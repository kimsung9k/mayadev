import pymel.core

mouthIn = pymel.core.ls( 'face_base|Mouth_IN' )[0]

sels = pymel.core.ls( sl=1 )

for sel in sels:
    selChildren = [ child.split( '|' )[-1] for child in sel.listRelatives( c=1 ) ]
    if 'Mouth_IN' in selChildren: continue
    duMouthIn = pymel.core.duplicate( mouthIn )[0]
    duMouthIn.setParent( sel )
    duMouthIn.t.set( mouthIn.t.get() )
    duMouthIn.rename( 'Mouth_IN' )