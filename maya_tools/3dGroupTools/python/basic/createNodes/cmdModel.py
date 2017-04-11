import maya.cmds as cmds


def mmDecomposeMatrix( *args ):

    cmds.createNode( 'decomposeMatrix' )




def mmShoulderOrient( *args ):
    
    cmds.createNode( 'shoulderOrient' )




def mmFourByFourMatrix( *args ):
    
    cmds.createNode( 'fourByFourMatrix' )
    
    
    
    
def mmMultMatrixDcmp( *args ):
    
    cmds.createNode( 'multMatrixDecompose' )
    
    
    
    
def mmWristAngle( *args ):
    
    cmds.createNode( 'wristAngle' )