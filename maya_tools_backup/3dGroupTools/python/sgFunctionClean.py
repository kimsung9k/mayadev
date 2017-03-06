import maya.cmds as cmds


def deleteUnused():
    import maya.mel as mel
    mel.eval( 'hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes")' )



def removeUnknown():
    
    unknownNodes = cmds.ls( type='unknown' )
    
    for node in unknownNodes:
        try:
            cmds.lockNode( node, lock=0 )
            cmds.delete( node )
            print "%s node is deleted" % node
        except:pass


def deleteSgNodes():
    
    sgNodeTypeList = ['keepRoundDeformer', 'slidingDeformer_before',
              'slidingDeformer', 'blendCurve', 'getLowerestValue',
              'aimObjectMatrix', 'meshRivet', 'collisionJoint',
              'sgLockAngleMatrix', 
              'psdJointBase',
              'volumeCurvesOnSurface', 'clusterControledSurface',
              'splineMatrix', 'matrixFromPolygon', 'simulatedCurveControledSurface',
              'sgWobbleCurve', 'sgWobbleCurve2',
              'ikSmoothStretch', 'meshSnap',
              'sgEpCurveNode', 'sgEpBindNode',
              'wristAngle', 'shoulderOrient', 'squash', 'blendTwoMatrix',
              'blendTwoAngle', 'matrixToThreeByThree', 'matrixToFourByFour',
              'followMatrix', 'followDouble',
              'smartOrient', 'ikStretch', 'twoSideSlidingDistance',
              'multMatrixDecompose','blendTwoMatrixDecompose','verticalVector',
              'splineCurveInfo', 'distanceSeparator', 'controlerShape', 'footControl',
              'angleDriver',
              'blendAndFixedShape', 'inverseSkinCluster', 'vectorWeight',
              'dgTransform', 'retargetBlender', 'retargetOrientNode', 'retargetTransNode',
              'editMatrixByCurve', 'transRotateCombineMatrix', 'retargetLocator', 'meshShapeLocator',
              'timeControl',
              'sgMeshIntersect','sgBlendTwoMatrix','sgFollowMatrix','sgMatrixToThreeByThree',
              'sgMultMatrixDecompose']

    for sgNodeType in sgNodeTypeList:
        
        sgNodes = cmds.ls( type=sgNodeType )
        if sgNodes: cmds.delete( sgNodes )



mc_deleteUnused ="""import maya.mel as mel
mel.eval( 'hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes")' )"""


mc_deleteUnknown = """import sgFunctionClean
sgFunctionClean.removeUnknown()"""

mc_deleteSgNodes = """import sgFunctionClean
sgFunctionClean.deleteSgNodes()"""