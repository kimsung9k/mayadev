#encoding=utf-8
import maya.cmds as cmds


class SubdivisionTagging():
    def __init__( self ):
        self.windowName = 'SubdivisionTaggingWindow'
        self.tagAttrName = 'smoothOn_mark'

    def getSelectedMesh( self ):
        meshs = []
        selected = cmds.ls( sl = True )
        for select in selected:
            mesh = cmds.listRelatives( select, s = True )[0]
            meshs.append( mesh )

        return meshs
        
    def tagOn( self, *args ):
        meshs = self.getSelectedMesh()
        for mesh in meshs:
            attrExist = cmds.attributeQuery( self.tagAttrName, n = mesh, ex = True )
            if not attrExist:
                cmds.addAttr( mesh, ln = self.tagAttrName, at = 'byte', k = True )
            cmds.setAttr( (mesh + '.'+self.tagAttrName), 0 )

    def tagOff( self, *args ):
        meshs = self.getSelectedMesh()
        for mesh in meshs:
            attrExist = cmds.attributeQuery( self.tagAttrName, n = mesh, ex = True )
            if attrExist:
                cmds.deleteAttr( mesh, at = self.tagAttrName )

            # ????????attr 
            attrExist = cmds.attributeQuery( 'objectName', n = mesh, ex = True )
            if attrExist:
                cmds.deleteAttr( mesh, at = 'objectName' )

    def tagOnSelect( self, *args ):
        select = []
        meshs = cmds.ls( typ = 'mesh' )
        for mesh in meshs:
            attrExist = cmds.attributeQuery( self.tagAttrName, n = mesh, ex = True )
            if attrExist:
                if cmds.getAttr( mesh + '.'+self.tagAttrName ) == 0:
                    select.append( mesh )

        if select:
            cmds.select( select, r = True )

    def tagClear( self, *args ):
        meshs = cmds.ls( typ = 'mesh' )
        for mesh in meshs:
            attrExist = cmds.attributeQuery( self.tagAttrName, n = mesh, ex = True )
            if attrExist:
                cmds.deleteAttr( mesh, at = self.tagAttrName )

            # ????????attr 
            attrExist = cmds.attributeQuery( 'objectName', n = mesh, ex = True )
            if attrExist:
                cmds.deleteAttr( mesh, at = 'objectName' )


    def gui( self ):
        if cmds.window( self.windowName, q = True, ex = True ):
            cmds.deleteUI( self.windowName )

        cmds.window( self.windowName, t = 'Smooth Tagging' )
        cmds.columnLayout()
        cmds.separator( st = 'none', h = 2 )
        cmds.rowLayout( nc = 2, cw2 = (170, 150), cl2 = ('center', 'center') )
        cmds.button( l = 'Tag On Selected',  c = self.tagOn , w = 150, h = 30 )
        cmds.button( l = 'Tag Off Selected', c = self.tagOff, w = 150, h = 30 )
        cmds.setParent( '..' )
        cmds.separator( w = 330, h = 10 )
        cmds.button( l = 'Select Tag On', c = self.tagOnSelect, w = 320, h = 30 )
        cmds.separator( w = 330, h = 10 )
        cmds.button( l = 'Clear Tag All', w = 320, h = 30, c = self.tagClear )

        cmds.showWindow()
        #cmds.window( self.windowName, e = True, wh = (330, 100) )

def showUI():
    tag = SubdivisionTagging()
    tag.gui()
