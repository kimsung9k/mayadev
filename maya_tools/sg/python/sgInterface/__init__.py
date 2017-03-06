import maya.cmds as cmds
from sgInterface import mainMenu
from sgInterface import popup_default
from sgInterface import popup_modeling
from sgInterface import popup_rigging
from sgInterface import popup_animation
import os



class Popup_Global:
    
    name = 'SGMTool_popupMenu'
    infoPath = cmds.about(pd=True) + "/sg_toolInfo/popupMode.txt"
    
    if not os.path.exists( infoPath ):
        file.makeFile( infoPath )
    
    popupMode = "popup_default"
    
    @staticmethod
    def saveInfo():
        pass
    
    @staticmethod
    def loadInfo():
        pass



def show(*args):
    
    cmds.popupMenu( Popup_Global.name, e=1, deleteAllItems=1 )
    
    sels = cmds.ls( sl=1 )
    if sels:
        popup_rigging.create( Popup_Global.name )
    else:
        popup_default.create( Popup_Global.name )
    
    
    
if __name__ == "sgRig":
    if cmds.popupMenu( Popup_Global.name, ex=1 ):
        cmds.deleteUI( Popup_Global.name )
    cmds.popupMenu( Popup_Global.name, alt=1, ctl=1, mm=1, p="viewPanes", pmc=show )
    
    targetPath =  os.path.dirname(__file__) + '/menus'
    for root, dirs, names in os.walk( targetPath ):
        for directory in dirs:
            mainMenu.showMayaWindow( directory, root+'/'+directory )
        break