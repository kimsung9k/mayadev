import maya.cmds as cmds


defaultMatrix = [ i%5 == 0 for i in range( 16 ) ]

setAniColorNum = 0


orderedVertices = []
orderedObjects  = []

topTransformAndVisValues = []

mirrorRigCheckedTargets = []

def getDefaultMatrix():
    
    return [ i%5 == 0 for i in range( 16 ) ]


class AttrInfo:

    def __init__(self, targetObj, attr ):

        chBox = cmds.attributeQuery( attr, node=targetObj, channelBox=1 )
        key   = cmds.attributeQuery( attr, node=targetObj, keyable=1 )
        atType= cmds.attributeQuery( attr, node=targetObj, attributeType=1 )
        listEnum = cmds.attributeQuery( attr, node=targetObj, listEnum=1 )
        minvalue    = None
        maxValue    = None
        if cmds.attributeQuery( attr, node=targetObj, minExists=1 ):
            minvalue = cmds.attributeQuery( attr, node=targetObj, min=1 )
        if cmds.attributeQuery( attr, node=targetObj, maxExists=1 ):
            maxValue = cmds.attributeQuery( attr, node=targetObj, max=1 )
        shortName = cmds.attributeQuery( attr, node=targetObj, shortName=1 )
        longName  = cmds.attributeQuery( attr, node=targetObj, longName=1 )

        options = { 'sn':shortName, 'ln':longName, 'k':key, 'cb':chBox }

        if listEnum:
            options.update( {'listEnum':listEnum} )
        if minvalue:
            options.update( {'min':minvalue[0]} )
        if maxValue:
            options.update( {'max':maxValue[0]} )
        value = cmds.getAttr( targetObj+'.'+attr )

        self.attr = attr
        self.value = value 
        self.atType = atType
        self.options = options



class ObjectUdAttrInfos:
    
    def __init__(self, targetObj ):
        
        self.attrInfos = []
        
        attrs = cmds.listAttr( targetObj, ud=1 )
        if not attrs: return None
        for attr in attrs:
            self.attrInfos.append( AttrInfo( targetObj, attr ) )



globalColorIndex = 0
