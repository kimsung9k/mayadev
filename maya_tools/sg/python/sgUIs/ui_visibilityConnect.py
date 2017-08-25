#coding=utf8

from maya import cmds
import pymel.core
import os, json


class ControlBase:
    
    @staticmethod
    def makeFolder( pathName ):
        pathName = pathName.replace( '\\', '/' )
        splitPaths = pathName.split( '/' )
        cuPath = splitPaths[0]
        folderExist = True
        for i in range( 1, len( splitPaths ) ):
            checkPath = cuPath+'/'+splitPaths[i]
            if not os.path.exists( checkPath ):
                os.chdir( cuPath )
                os.mkdir( splitPaths[i] )
                folderExist = False
            cuPath = checkPath
        if folderExist: return None
        return pathName


    @staticmethod
    def makeFile( filePath ):
        if os.path.exists( filePath ): return None
        filePath = filePath.replace( "\\", "/" )
        splits = filePath.split( '/' )
        folder = '/'.join( splits[:-1] )
        ControlBase.makeFolder( folder )
        f = open( filePath, "w" )
        json.dump( {}, f )
        f.close()
    
    
    @staticmethod
    def addAttr( target, **options ):
    
        items = options.items()
        
        attrName = ''
        channelBox = False
        keyable = False
        for key, value in items:
            if key in ['ln', 'longName']:
                attrName = value
            elif key in ['cb', 'channelBox']:
                channelBox = True
                options.pop( key )
            elif key in ['k', 'keyable']:
                keyable = True 
                options.pop( key )
        
        if pymel.core.attributeQuery( attrName, node=target, ex=1 ): return None
        
        pymel.core.addAttr( target, **options )
        
        if channelBox:
            pymel.core.setAttr( target+'.'+attrName, e=1, cb=1 )
        elif keyable:
            pymel.core.setAttr( target+'.'+attrName, e=1, k=1 )
    
    



class Cmd:

    @staticmethod
    def connect( *args ):
        sels = pymel.core.ls( sl=1 )
        
        ctl = sels[0]
        others = sels[1:]
        attrName = cmds.textField( WinMain.fieldAttrName, q=1, tx=1 )
        
        ControlBase.addAttr( ctl, ln=attrName, min=0, max=1, k=1, at='long' )
        for other in others:
            try:ctl.attr( attrName ) >> other.v
            except:
                cmds.warning( "Connection error : %s --> %s" %( ctl.attr( attrName ).name(), other.v.name() ) )
        pass
    



class WinMain:
    
    title  = "UI - Visibility Connector"
    name = "pingo_ui_visibility_connector"
    width = 300
    height= 100
    infoPath = cmds.about( pd=1 ) + '/pingo/ui_visibility_connector.txt'
    
    fieldAttrName = ''


    def __init__(self):
        
        ControlBase.makeFile( WinMain.infoPath )
    
    
    def create(self):
        
        if cmds.window( WinMain.name, q=1, ex=1 ):
            cmds.deleteUI( WinMain.name )
        
        cmds.window( WinMain.name, title=WinMain.title )
        
        form = cmds.formLayout()
        textExplanation = cmds.text( l='1.컨트롤러 선택 \n2.컨트롤할 타겟들 선택'.decode( 'utf-8' ), al='center', h=50, bgc=[.3,.3,.3], font='fixedWidthFont' )
        textAttr = cmds.text( l='Attribute Name', h=25 )
        fieldAttrName = cmds.textField( tx='show', h=25)
        buttonConnect = cmds.button( l='Connect', h=30, c=Cmd.connect )
        
        cmds.formLayout( form, e=1, 
                         af=[(textExplanation, 'top', 0), (textExplanation, 'left', 0), (textExplanation, 'right', 0),
                             (textAttr, 'left', 5), (fieldAttrName, 'right', 5),
                             (buttonConnect, 'left', 0), (buttonConnect, 'right', 0)],
                         ac=[(textAttr, 'top', 5, textExplanation),
                             (fieldAttrName, 'top', 5, textExplanation),
                             (fieldAttrName, 'left', 5, textAttr),
                             (buttonConnect, 'top', 5, textAttr)] )
        
        cmds.window( WinMain.name, e=1, width=WinMain.width, height=WinMain.height )
        
        WinMain.fieldAttrName = fieldAttrName

    
    
    def show(self):
        
        cmds.showWindow( WinMain.name )



def show():
    
    mainWindow = WinMain()
    mainWindow.create()
    mainWindow.show()

