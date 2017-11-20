import maya.cmds as cmds


class CreateJointOnCurveSet:
    
    def __init__( self ):
        
        self._curveShape = ''
        self._minParam   = 0.0
        self._maxParam   = 1.0
        self._infoNum    = 5
        self._numSpans   = 5
        
        
    def setJointNum( self, num ):
        
        self._infoNum = num
        
        
    def setCurve( self, curveShape ):
        
        self._curveShape = curveShape
        self._minParam = cmds.getAttr( self._curveShape+'.minValue' )
        self._maxParam = cmds.getAttr( self._curveShape+'.maxValue' )
        self._numSpans = cmds.getAttr( self._curveShape+'.spans' )
    
    
    def create(self, distanceNode ):
        
        eachParam = ( self._maxParam - self._minParam )/( self._infoNum - 1 )
        
        eachInfos = []
        
        for i in range( self._infoNum ):
            info = cmds.createNode( 'pointOnCurveInfo', n= self._curveShape+'_info%d' % i )
            cmds.connectAttr( self._curveShape+'.local', info+'.inputCurve' )
            cmds.setAttr( info+'.parameter', eachParam*i + self._minParam )
            eachInfos.append( info )
            
        cmds.select( d=1 )
        
        joints = []
        for i in range( self._infoNum ):
            joints.append( cmds.joint(p=[i,0,0]) )
            
        handle, effector = cmds.ikHandle( sj=joints[0], ee=joints[-1], sol='ikSplineSolver', ccv=False, pcv=False, curve=self._curveShape )
        
        distNodes = []
        for i in range( self._infoNum -1 ):
            
            firstInfo = eachInfos[i]
            secondInfo = eachInfos[i+1]
            targetJoint = joints[i+1]
            
            distNode = cmds.createNode( 'distanceBetween' )
            distNodes.append( distNode )
            
            cmds.connectAttr( firstInfo+'.position', distNode+'.point1' )
            cmds.connectAttr( secondInfo+'.position', distNode+'.point2')
            
            if distanceNode:
                cmds.connectAttr( distNode+'.distance', targetJoint+'.tx' )
            else:
                cmds.setAttr( targetJoint+'.tx', cmds.getAttr( distNode+'.distance' ) )
        
        if not distanceNode:
            cmds.delete( distNodes )
        
        return handle, joints
            
            
            
            

def createJointOnCurve( numJoint, distanceNode = True ):
    
    sels = cmds.ls( sl=1 )
    
    curveSetInst = CreateJointOnCurveSet()
    curveSetInst.setJointNum( numJoint )
    
    returnTargets = []
    for sel in sels:
        
        selCurve = cmds.listRelatives( sel, s=1, f=1 )
        
        if not selCurve: continue
        
        selCurve = selCurve[0]
        curveSetInst.setCurve( selCurve )
        joints = curveSetInst.create( distanceNode )
        
        returnTargets.append( joints )
    
    return returnTargets
        
        


def createJointOnCurveByNumSpans( distanceNode = True ):
    
    sels = cmds.ls( sl=1 )
    
    curveSetInst = CreateJointOnCurveSet()
    
    returnTargets = []
    for sel in sels:
        
        selCurve = cmds.listRelatives( sel, s=1 )
        
        if not selCurve: continue
        
        selCurve = selCurve[0]
        curveSetInst.setCurve( selCurve )
        curveSetInst.setJointNum( curveSetInst._numSpans+1 )
        joints = curveSetInst.create( distanceNode )
        
        returnTargets.append( joints )
    
    return returnTargets



def createJointOnCurveByLength( multRate, distNode=True ):
    
    sels = cmds.ls( sl=1 )
    
    curveSetInst = CreateJointOnCurveSet()
    
    curveInfo = cmds.createNode( 'curveInfo' )
    
    returnTargets = []
    for sel in sels:
        
        selCurve = cmds.listRelatives( sel, s=1 )
        
        if not selCurve: continue
        
        selCurve = selCurve[0]
        cmds.connectAttr( selCurve+'.local', curveInfo+'.inputCurve', f=1 )
        length = cmds.getAttr( curveInfo+'.arcLength' )
        curveSetInst.setJointNum( int( length * multRate ) )
        curveSetInst.setCurve( selCurve )
        joints = curveSetInst.create( distNode )
        
        returnTargets.append( joints )

    return returnTargets