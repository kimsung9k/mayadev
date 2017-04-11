import maya.cmds as cmds
import baseFunctions


class ConnectWidthMainBlendShape:


    def __init__(self, controler, targetObj ):
    
        targetObjShape = cmds.listRelatives( targetObj, s=1 )[0]
        
        mainBlendShape = cmds.listConnections( targetObjShape+'.inMesh', type='blendShape' )[0]
    
        self.checkHelpTextExists( controler )
        
        self.connectToBlendShape( controler, mainBlendShape )
                
                
                
    def checkHelpTextExists( self, controler ):
        
        if not cmds.attributeQuery( '____', node=controler, ex=1 ):
            baseFunctions.addHelpTx( controler, 'Blend Shape' )
            
            
            
    def connectToBlendShape(self, controler, mainBlendShape ):
        
        lastIndex = baseFunctions.getLastIndex( mainBlendShape+'.w' )
        
        for i in range( lastIndex+1 ):
            currentAttr = mainBlendShape+'.w[%d]' % i 
            
            cons = cmds.listConnections( currentAttr )
            
            if not cons:
                realAttrName = baseFunctions.getAttrRealName( currentAttr ).split( '.' )[1]
                
                if not cmds.attributeQuery( realAttrName, node=controler, ex=1 ):
                    cmds.addAttr( controler, ln=realAttrName, min=0, max=1 )
                    cmds.setAttr( controler+'.'+realAttrName, e=1, k=1 )
                    
                    cmds.connectAttr( controler+'.'+realAttrName, currentAttr )