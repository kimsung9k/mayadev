import maya.cmds as cmds




def shaderAndSet( nodeName, **options ):
    
    options.update( {'asShader':1})
    shader = cmds.shadingNode( nodeName, **options )
    shadingGrp = cmds.sets( renderable=1, noSurfaceShader=1, empty=1, name=nodeName+"SG" )
    for attrName in ['outColor','outMaterial']:
        try:
            cmds.connectAttr( shader+'.' + attrName, shadingGrp + '.surfaceShader', f=1 )
        except:pass
        try:
            cmds.connectAttr( shader + '.' + attrName, shadingGrp + '.ifmMdl', f=1 )
        except:pass
    return shader, shadingGrp



def deleteSources( mainNode, doNotDeleteList = [] ):
    
    nodes = cmds.listConnections( mainNode, s=1, d=0 )
    if nodes:
        for node in nodes:
            if not cmds.objExists( node ): continue
            deleteSources( node )
            if cmds.objExists( node ) and not node in doNotDeleteList:
                try:cmds.delete( node )
                except: pass
    

