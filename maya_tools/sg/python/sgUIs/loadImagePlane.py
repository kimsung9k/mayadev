import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
from __qtImprot import *


class Window_global:
    
    name = "SGMTool_loadImagePlane"
    title = "SGMTool Load Image Plane"
    wh = [400,100]
    el_height = 25
    marginTop = 10
    marginSide = 10
    
    txf_imagePath = ""
    intf_imageWidth = ""
    intf_imageHeight = ""
    floatf_planeWidth = ""
    floatf_planeHeight = ""
    check_linkWh = ""
    radio_dir = ""
    
    imgWidth = 1
    imgHeight = 1
    
    
    


class UI_commands:
    
    @staticmethod
    def loadImage( *args ):
        filePaths = cmds.fileDialog2( fm=1, ds=2 )
        if not filePaths: return None
        cmds.textField( Window_global.txf_imagePath, e=1, tx=filePaths[0] )
        UI_commands.setInfo()
    
    
    @staticmethod
    def setInfo( *args ):
        filePath = cmds.textField( Window_global.txf_imagePath, q=1, tx=1 )
        pixmap = QPixmap(filePath)
        
        Window_global.imgWidth = pixmap.width()
        Window_global.imgHeight = pixmap.height()
        cmds.intField( Window_global.intf_imageWidth, e=1, v=Window_global.imgWidth )
        cmds.intField( Window_global.intf_imageHeight, e=1, v=Window_global.imgHeight )
        
        planeWidth = cmds.floatField( Window_global.floatf_planeWidth, q=1, v=1 )
        planeHeight = planeWidth * float(Window_global.imgWidth) / float(Window_global.imgHeight)

        cmds.floatField( Window_global.floatf_planeHeight, e=1, v= planeHeight )
    
    @staticmethod
    def editWidth( *args ):
        if not cmds.checkBox( Window_global.check_linkWh, q=1, v=1 ): return None
        
        aspectRatio = float( Window_global.imgWidth ) / float( Window_global.imgHeight )
        width = cmds.floatField( Window_global.floatf_planeWidth, q=1, v=1 )
        height = width * aspectRatio
        cmds.floatField( Window_global.floatf_planeHeight, e=1, v=height )
        
    
    
    @staticmethod
    def editHeight( *args ):
        if not cmds.checkBox( Window_global.check_linkWh, q=1, v=1 ): return None
        
        aspectRatio = float( Window_global.imgWidth ) / float( Window_global.imgHeight )
        height = cmds.floatField( Window_global.floatf_planeHeight, q=1, v=1 )
        width = height / aspectRatio
        cmds.floatField( Window_global.floatf_planeWidth, e=1, v=width )


    @staticmethod
    def createPlane( *args ):
        import math
        path   = cmds.textField( Window_global.txf_imagePath, q=1, tx=1 )
        width  = cmds.floatField( Window_global.floatf_planeWidth, q=1, v=1 )
        height = cmds.floatField( Window_global.floatf_planeHeight, q=1, v=1 )
        plane = cmds.polyPlane( w=height, h=width, cuv=1, sw=1, sh=1 )
        
        radioSelObject = cmds.radioCollection( Window_global.radio_dir, q=1, sl=1 ).split( '|' )[-1]
        items = cmds.radioCollection( Window_global.radio_dir, q=1, cia=1 )
        items = map( lambda x : x.split( "|" )[-1], items )
        selIndex = items.index( radioSelObject )
        
        directions = [(90,90,0), (0,0,0), (90,0,0), (90,-90,0), (180,0,0), (90,180,0)]
        
        rotValue = directions[selIndex]
        cmds.rotate( rotValue[0], rotValue[1], rotValue[2], plane )
        
        lambert = cmds.shadingNode( 'lambert', asShader=1)
        shadingGrp = cmds.sets( name="%sSG" % lambert, renderable=1, noSurfaceShader=1, empty=1 );
        cmds.connectAttr( lambert + ".outColor", shadingGrp +".surfaceShader", f=1 )
        cmds.sets( plane, e=1, forceElement=shadingGrp  )
        fileNode = cmds.shadingNode( 'file', asTexture=1 )
        cmds.connectAttr( fileNode + ".outColor", lambert + ".color", f=1 )
        cmds.setAttr( fileNode +".fileTextureName", path, type="string" )




class UI_imagePath:
    
    def __init__(self):
        
        self.height = 25
        self.marginSide = 10
    
    
    def create(self):
        
        form = cmds.formLayout()
        text = cmds.text( l="Image Path : ", w=100, al="right", h=self.height )
        txf  = cmds.textField( h=self.height, cc= UI_commands.setInfo )
        button = cmds.button( l="Load Image", h=self.height, c= UI_commands.loadImage )
        cmds.setParent('..')

        cmds.formLayout( form, e=1, 
                         af = [ (button, "top", 0), (button, "left", 0), (button, "right", 0),
                                (text,"left",0), (txf,"right",0) ],
                         ac = [(text, "top", Window_global.marginTop, button), (txf, "top", Window_global.marginTop, button),
                               (txf, "left", 0, text)] )
        
        self.form = form
        Window_global.txf_imagePath = txf





class UI_imageInfo:
    
    def __init__(self):
        
        self.height = 25
        self.marginSide = 10

    
    def create(self):
        
        form  = cmds.formLayout()
        text1   = cmds.text( l="Image Size : ", w=100, al="right", h=self.height )
        intf1   = cmds.intField( h=self.height, en=0, w=50 )
        text2   = cmds.text( l="X", w=20, al="center", h=self.height )
        intf2   = cmds.intField( h=self.height, en=0, w=50 )
        cmds.setParent('..')

        cmds.formLayout( form, e=1, 
                         af = [ (text1,"top",0), (intf1,"top",0),(text2,"top",0),(intf2,"top",0),
                                (text1,"left",0) ],
                         ac = [(intf1, "left", 0, text1), (text2, "left", 0, intf1), (intf2, "left", 0, text2)] )
        
        self.form = form
        Window_global.intf_imageWidth  = intf1
        Window_global.intf_imageHeight = intf2





class UI_planeInfo:
    
    def __init__(self):
        
        self.height = 25
    
    def create(self):
        
        form  = cmds.formLayout()
        text1   = cmds.text( l="Plane Size : ", w=100, al="right", h=self.height )
        floatf1   = cmds.floatField( h=self.height, w=50, v=1, pre=3, cc= UI_commands.editWidth, ec= UI_commands.editWidth )
        text2   = cmds.text( l="X", w=20, al="center", h=self.height )
        floatf2   = cmds.floatField( h=self.height, w=50, v=1, pre=3, cc= UI_commands.editHeight, ec= UI_commands.editHeight )
        check = cmds.checkBox( l="Link", v=1, h=self.height  )
        cmds.setParent( '..' )

        cmds.formLayout( form, e=1, 
                         af = [ (text1,"top",0), (floatf1,"top",0),(text2,"top",0),(floatf2,"top",0), ( check, "top", 0 ),
                                (text1,"left",0) ],
                         ac = [(floatf1, "left", 0, text1), (text2, "left", 0, floatf1), (floatf2, "left", 0, text2), (check, "left", 5, floatf2)] )
        
        self.form = form
        Window_global.floatf_planeWidth = floatf1
        Window_global.floatf_planeHeight = floatf2
        Window_global.check_linkWh = check




class UI_planeDirection:
    
    def __init__(self):
        
        self.height = 25
    
    def create(self):
        
        form  = cmds.formLayout()
        text    = cmds.text( l="Plane Direction : ", w=100, al="right", h=self.height )
        radio = cmds.radioCollection()
        rbx = cmds.radioButton( l="X", h=self.height )
        rby = cmds.radioButton( l="Y", h=self.height )
        rbz = cmds.radioButton( l="Z", h=self.height )
        rbmx = cmds.radioButton( l="-X", h=self.height )
        rbmy = cmds.radioButton( l="-Y", h=self.height )
        rbmz = cmds.radioButton( l="-Z", h=self.height )
        cmds.setParent( '..' )

        cmds.radioCollection( radio, edit=True, select=rbx )
        
        cmds.formLayout( form, e=1, 
                         af = [ (text,"top",0), (text,"left",0), (rbx,"top",0),(rby,"top",0),(rbz,"top",0) ],
                         ac = [ (rbx, "left", 0, text), (rby, "left", 0, rbx), (rbz, "left", 0, rby),
                                (rbmx, "left", 0, text), (rbmy, "left", 0, rbmx), (rbmz, "left", 0, rbmy),
                                (rbmx, "top", 0, text), (rbmy, "top", 0, text), (rbmz, "top", 0, text)] )
        
        self.form = form
        
        Window_global.radio_dir = radio




class Window:
    
    def __init__(self):
        
        self.ui_imagePath = UI_imagePath()
        self.ui_imageInfo = UI_imageInfo()
        self.ui_planeInfo = UI_planeInfo()
        self.ui_planeDir  = UI_planeDirection()
    
    
    def show(self, evt=0 ):
        
        if cmds.window( Window_global.name, ex=1 ):
            cmds.deleteUI( Window_global.name, wnd=1 )
        cmds.window( Window_global.name, title=Window_global.title )
        
        form = cmds.formLayout()
        self.ui_imagePath.create()
        self.ui_imageInfo.create()
        self.ui_planeInfo.create()
        self.ui_planeDir.create()
        sep = cmds.separator()
        button = cmds.button( l="Create Plane", c=UI_commands.createPlane )
        cmds.setParent('..')
        
        cmds.formLayout( form, e=1,
                         af = [(self.ui_imagePath.form,"top",Window_global.marginTop), 
                               (self.ui_imagePath.form,"left",Window_global.marginSide), 
                               (self.ui_imagePath.form,"right",Window_global.marginSide),
                               (self.ui_imageInfo.form,"left",Window_global.marginSide),
                               (self.ui_imageInfo.form,"right",Window_global.marginSide),
                               (self.ui_planeInfo.form,"left",Window_global.marginSide),
                               (self.ui_planeInfo.form,"right",Window_global.marginSide),
                               (self.ui_planeDir.form,"left",Window_global.marginSide),
                               (self.ui_planeDir.form,"right",Window_global.marginSide),
                               (sep,"left",Window_global.marginSide),
                               (sep,"right",Window_global.marginSide),
                               (button,"left",Window_global.marginSide),
                               (button,"right",Window_global.marginSide),
                               (button,"bottom",Window_global.marginTop) ],
                         ac = [(self.ui_imageInfo.form,"top",Window_global.marginTop,self.ui_imagePath.form),
                               (sep,"top",Window_global.marginTop,self.ui_imageInfo.form),
                               (self.ui_planeInfo.form,"top",Window_global.marginTop,sep),
                               (self.ui_planeDir.form,"top",Window_global.marginTop,self.ui_planeInfo.form),
                               (button,"top",Window_global.marginTop,self.ui_planeDir.form)])
        
        cmds.window( Window_global.name, e=1, wh= Window_global.wh, rtf=1 )
        cmds.showWindow( Window_global.name )


def show():
    Window().show()
    