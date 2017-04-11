import maya.cmds as cmds
import ui.view

def transformKeyCopy( first, second, tr=True, rot=True, scale=True ):
    
    animCurves = cmds.listConnections( first, s=1, d=0, p=1, c=1, type='animCurve' )
    
    outputs = animCurves[1::2]
    inputs  = animCurves[::2]
    
    firstOriginName = first.find( '|' ) == -1
    secondOriginName = second.find( '|' ) == -1
    isOriginName = firstOriginName and secondOriginName
    
    trAttrList = ['translateX', 'translateY', 'translateZ' ]
    roAttrList = ['rotateX', 'rotateY', 'rotateZ' ]
    scaleAttrList = ['scaleX', 'scaleY', 'scaleZ' ]
    
    checkAttrList = []
    
    if tr:
        checkAttrList += trAttrList
    if rot:
        checkAttrList += roAttrList
    if scale:
        checkAttrList += scaleAttrList
    
    for i in range( len( outputs ) ):
        
        animNode, attr = outputs[i].split( '.' )
        firstAttr = inputs[i].split( '.' )[1]
        if not firstAttr in checkAttrList: continue
        
        duAnim = cmds.duplicate( animNode )[0]
        
        if isOriginName:
            duAnim = cmds.rename( duAnim, duAnim.replace( first, second ) ) 
        
        cmds.connectAttr( duAnim+'.'+attr, second+'.'+firstAttr )
        
        
        
def keyCopy( first, second ):
    
    animCurves = cmds.listConnections( first, s=1, d=0, p=1, c=1, type='animCurve' )
    
    outputs = animCurves[1::2]
    inputs  = animCurves[::2]
    
    firstOriginName = first.find( '|' ) == -1
    secondOriginName = second.find( '|' ) == -1
    isOriginName = firstOriginName and secondOriginName
    
    for i in range( len( outputs ) ):
        
        animNode, attr = outputs[i].split( '.' )
        firstAttr = inputs[i].split( '.' )[1]
        
        duAnim = cmds.duplicate( animNode )[0]
        
        if isOriginName:
            duAnim = cmds.rename( duAnim, duAnim.replace( first, second ) ) 
        
        cmds.connectAttr( duAnim+'.'+attr, second+'.'+firstAttr )
            
            
            

def mmKeyCopy( *args ):
    
    sels = cmds.ls( sl=1 )
    
    first = sels[0]
    others = sels[1:]
    
    for other in others:
        keyCopy( first, other )
        
        
def mmTransKeyCopy( *args ):
    
    sels = cmds.ls( sl=1 )
    
    first = sels[0]
    others = sels[1:]
    
    for other in others:
        transformKeyCopy( first, other, tr=True, rot=False, scale=False )
        
        
def mmRotKeyCopy( *args ):
    
    sels = cmds.ls( sl=1 )
    
    first = sels[0]
    others = sels[1:]
    
    for other in others:
        transformKeyCopy( first, other, tr=False, rot=True, scale=False )
        
        
def mmScaleKeyCopy( *args ):
    
    sels = cmds.ls( sl=1 )
    
    first = sels[0]
    others = sels[1:]
    
    for other in others:
        transformKeyCopy( first, other, tr=False, rot=False, scale=True )
        

def mmRotScaleKeyCopy( *args ):
    
    sels = cmds.ls( sl=1 )
    
    first = sels[0]
    others = sels[1:]
    
    for other in others:
        transformKeyCopy( first, other, tr=False, rot=True, scale=True )



def mmCreateCaptureUI( *args ):
    
    captureUI = ui.view.CaptureViewUI()
    captureUI.create()



uiCmd_OpenVirtualAdTool ="""import animation.virtualAd.view
animation.virtualAd.view.Window().create()
"""
    
    
uiCmd_OpenModelPanel = """import animation.modelPanel.view
modelPanelWindow = animation.modelPanel.view.Window()
modelPanelWindow.create()
"""
