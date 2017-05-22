import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
sels = cmds.ls( sl=1 )

from sgModules import sgcommands

first = sels[0]
second = sels[1]

upObj = cmds.listRelatives( cmds.listRelatives( first, p=1, f=1 )[0], p=1, f=1 )[0]

pos = OpenMaya.MPoint( *cmds.xform( first, q=1, ws=1, t=1 )[:3] )
upObjMtx = sgcommands.listToMatrix( cmds.getAttr( upObj + '.wm' ) )
directionIndex = sgcommands.getDirectionIndex( pos * upObjMtx.inverse() )

directionList = [ [1,0,0], [0,1,0], [0,0,1],
                  [-1,0,0], [0,-1,0], [0,0,-1]]

aimDirection = directionList[ directionIndex ]
upVector = directionList[ (directionIndex+2) % 3 ]

cmds.aimConstraint( first, second, aim=aimDirection, u=upVector, wu=upVector, wut='objectrotation', wuo=upObj )