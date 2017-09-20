from sgCmds import *
import pymel.core


class NetControlRig:
    
    groupAttrName = 'netControlGroup'
    rowAttrName   = 'netControlRow'
    columnAttrName = 'netControlColumn'
    bigControlAttrName = 'netControlBigTarget'


    def __init__(self, netGroupName ):
        
        self.baseName = netGroupName
        self.numRows = 0
        self.numColumns = 0
        self.targets = []


    def setRows( self, *inputOrderedTargets ):
        
        orderedTargets = [ pymel.core.ls( inputOrderedTarget )[0] for inputOrderedTarget in inputOrderedTargets ]
        for i in range( len( orderedTargets ) ):
            orderedTargets[i].rename( self.baseName + '_%02d' % i )
            addAttr( orderedTargets[i], ln=NetControlRig.groupAttrName, dt='string' )
            orderedTargets[i].attr( NetControlRig.groupAttrName ).set( self.baseName )
            addAttr( orderedTargets[i], ln=NetControlRig.rowAttrName, at='long' )
            orderedTargets[i].attr( NetControlRig.rowAttrName ).set( i )
            self.numRows += 1
            self.targets.append( orderedTargets[i] )


    def setBigConnect( self, *inputBigTargets ):
        
        bigTargets = [ pymel.core.ls( inputBigControl )[0] for inputBigControl in inputBigTargets ]
        
        for i in range( len( bigTargets ) ):
            closeTarget = getClosestTransform( bigTargets[i], self.targets )
            addAttr( closeTarget, ln=NetControlRig.bigControlAttrName, at='message' )
            bigTargets[i].message >> closeTarget.attr( NetControlRig.bigControlAttrName )
    
    
    def setParentContraint(self, circle=False, toParent=False ):
        
        def getBigControl( target ):
            return target.attr( NetControlRig.bigControlAttrName ).listConnections( s=1, d=0 )[0]
        
        if not self.numColumns:
            bigControlIndices = []
            
            for i in range( len( self.targets ) ):
                if not pymel.core.attributeQuery( NetControlRig.bigControlAttrName,
                                                  node = self.targets[i], ex=1 ):
                    continue
                bigControlIndices.append( i )

            for i in range( len( self.targets ) ):
                if toParent:
                    parentTarget = self.targets[i].getParent()
                else:
                    parentTarget = self.targets[i]

                if i in bigControlIndices:
                    bigControl = getBigControl(self.targets[i])
                    pymel.core.parentConstraint( bigControl, parentTarget, mo=1 )
                else:
                    twoSideBigControlsIndices = [None, None]
                    for j in range( len( bigControlIndices ) ):
                        if i < bigControlIndices[j]:
                            if j == 0:
                                if circle:
                                    twoSideBigControlsIndices = [ bigControlIndices[0], bigControlIndices[-1]]
                                else:
                                    twoSideBigControlsIndices = [ bigControlIndices[0], bigControlIndices[0]]
                            else:
                                twoSideBigControlsIndices = [bigControlIndices[j-1],bigControlIndices[j]]
                            break
                    
                    if twoSideBigControlsIndices[0] == None:
                        if circle:
                            twoSideBigControlsIndices = [bigControlIndices[-1], bigControlIndices[0]]
                        else:
                            twoSideBigControlsIndices = [bigControlIndices[-1], bigControlIndices[-1]]
                    
                    twoSideControls = [ getBigControl( self.targets[k] ) for k in twoSideBigControlsIndices ]
                    
                    first  = getMVector( twoSideControls[0] )
                    second = getMVector( twoSideControls[1] )
                    target = getMVector( self.targets[i] )
                    
                    baseVector = second - first
                    targetVector = target - first
                    
                    if baseVector.length() < 0.00001:
                        pymel.core.parentConstraint( twoSideControls[0], parentTarget, mo=1 )
                        continue
                    
                    projTargetToBase = baseVector * ( ( targetVector * baseVector )/baseVector.length()**2 )
                    
                    secondWeight = projTargetToBase.length() / baseVector.length()
                    if secondWeight > 1:
                        secondWeight = 1
                    firstWeight = 1.0 - secondWeight
                    
                    print firstWeight, secondWeight
                    
                    if firstWeight == 0:
                        constraint = pymel.core.parentConstraint( twoSideControls[1], parentTarget, mo=1 )
                    elif secondWeight == 0:
                        constraint = pymel.core.parentConstraint( twoSideControls[0], parentTarget, mo=1 )
                    else:
                        constraint = pymel.core.parentConstraint( twoSideControls[0], twoSideControls[1], parentTarget, mo=1 )
                        constraint.w0.set( firstWeight )
                        constraint.w1.set( secondWeight )
                    
                    
                    
                    
                    
            
            
            
                    