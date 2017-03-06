import maya.cmds as cmds


def exportControllerShapeInfo():
    
    import json, os
    
    sels = cmds.ls( 'Ctl_*', type='transform' )
    
    ctlInfos = {}
    for sel in sels:
        selShapes = cmds.listRelatives( sel, s=1, f=1 )
        if not selShapes: continue
        
        pointAttrs = cmds.ls( selShapes[0] + '.controlPoints[*]', fl=1 )
        points = [cmds.getAttr( selShapes[0] + '.overrideColor' )]
        for i in range( len( pointAttrs ) ):
            points.append( cmds.xform( pointAttrs[i], q=1, os=1, t=1 ) )
        
        ctlInfos.update( {'%s' % sel : points} )
    
    filePath = os.path.dirname( __file__ ) + '/ctlShapeInfo.txt'
    
    f = open( filePath, 'w' )
    json.dump( ctlInfos, f, indent=2 )
    f.close()



import get
import os
import popupMenu
import mainMenu


class Popup_Global:
    
    name = 'SGAutoRig_popupMenu'




def popupShow(*args):
    
    cmds.popupMenu( Popup_Global.name, e=1, deleteAllItems=1 )

    sels = cmds.ls( sl=1 )
    popupMenu.create( Popup_Global.name )


if __name__ == "sgHumanRig":
    if cmds.popupMenu( Popup_Global.name, ex=1 ):
        cmds.deleteUI( Popup_Global.name )
    cmds.popupMenu( Popup_Global.name, alt=1, sh=1, mm=1, p="viewPanes", pmc=popupShow )
    
    menuPath =  os.path.dirname(__file__) + '/menus'
    mainMenu.showMayaWindow('Human_Rig', menuPath)
