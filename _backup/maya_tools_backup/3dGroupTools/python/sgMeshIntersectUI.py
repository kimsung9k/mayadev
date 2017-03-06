import maya.cmds as cmds
import sgModelUI
import sgModelFileAndPath
import sgRigMesh


class Window:
    
    def __init__(self):
        
        sgModelFileAndPath.autoLoadPlugin( 'sgMatrix' )
        sgModelFileAndPath.autoLoadPlugin( 'sgMatchMove' )
        
        self.uiname = 'sgMeshIntersectUi'
        self.title  = 'SG Mesh Intersect UI'
        self.width = 300
        self.height = 50
        
        self.sourceField = sgModelUI.PopupFieldUI( 'Source Locator : ', 'Load Selected', 40 )
        self.destField   = sgModelUI.PopupFieldUI( 'Dest Locator : ', 'Load Selected', 40 )
        self.meshField   = sgModelUI.PopupFieldUI( 'Target Mesh : ', 'Load Selected', 40 )
    
    
    def cmdSet(self, *args ):
        
        sourcePointObject = self.sourceField.getFieldText()
        destPointObjects  = self.destField.getFieldTexts()
        mesh              = self.meshField.getFieldText()
        
        trObjs = []
        crvs = []
        for destPointObject in destPointObjects:
            trObj, crv = sgRigMesh.createMeshInstersectPointObject( sourcePointObject, destPointObject, mesh )
            trObjs.append( trObj )
            crvs.append( crv )
        
        cmds.group( trObjs )
        cmds.group( crvs )



    def cmdClose(self, *args ):
        
        cmds.deleteUI( self.uiname, wnd=1 )

    
    def create(self):
        
        self.fields = []
        
        if cmds.window( self.uiname, ex=1 ):
            cmds.deleteUI( self.uiname, wnd=1 )
        
        cmds.window( self.uiname, title= self.title )
        
        cmds.columnLayout()
        
        columnWidth = self.width - 2
        firstWidth = ( columnWidth -2 ) / 2
        secondWidth = ( columnWidth -2 ) - firstWidth
        
        cmds.rowColumnLayout( nc=1, cw=[(1,columnWidth)] )
        self.sourceField.create()
        self.destField.create()
        self.meshField.create()
        cmds.setParent( '..' )
        
        cmds.rowColumnLayout( nc=2, cw=[(1,firstWidth),(2,secondWidth)])
        cmds.button( l='Create', c= self.cmdSet )
        cmds.button( l='Close', c= self.cmdClose )
        
        cmds.window( self.uiname, e=1, width= self.width, height = self.height )
        cmds.showWindow( self.uiname )



def showWindow( *args ):
    
    Window().create()