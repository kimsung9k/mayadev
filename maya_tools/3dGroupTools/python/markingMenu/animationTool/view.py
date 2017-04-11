import animation.cmdModel as animmation
import model

import maya.cmds as cmds

class Create:
    
    def __init__(self, parentMenu, *args ):
        
        self._parentMenu = parentMenu
        
        cmds.popupMenu( self._parentMenu, e=1, deleteAllItems=1 )
        self.defaultMenu()
        
        
    def divider(self):
        
        cmds.setParent( self._parentMenu, menu=1 )
        cmds.menuItem( d=1 )
    
    
    def defaultMenu(self, rp=None ):
        
        cmds.setParent( self._parentMenu, menu=1 )
        cmds.menuItem( l='Rot Scale Key Copy', rp='NE', c=animmation.mmRotScaleKeyCopy )
        cmds.menuItem( l='Key Copy', rp='N', c=animmation.mmKeyCopy )
        cmds.menuItem( l='Trans Key Copy', rp='NW', c=animmation.mmTransKeyCopy )