import maya.cmds as cmds
from model import *


def constraint( first, second ):
    
    mmdc = cmds.createNode( 'multMatrixDecompose', n=second + '_mmdc' )
    cmds.connectAttr( first  + '.wm',  mmdc+'.i[0]' )
    cmds.connectAttr( second + '.pim', mmdc+'.i[1]' )
    cmds.connectAttr( mmdc + '.ot', second + '.t' )
    cmds.connectAttr( mmdc + '.or', second + '.r' )
    


def constraintPoint( first, second ):
    
    mmdc = cmds.createNode( 'multMatrixDecompose', n=second + '_mmdc' )
    cmds.connectAttr( first  + '.wm',  mmdc+'.i[0]' )
    cmds.connectAttr( second + '.pim', mmdc+'.i[1]' )
    cmds.connectAttr( mmdc + '.ot', second + '.t' )



def constraintOrient( first, second ):
    
    mmdc = cmds.createNode( 'multMatrixDecompose', n=second + '_mmdcOri' )
    cmds.connectAttr( first + '.wm', mmdc+'.i[0]' )
    cmds.connectAttr( second + '.pim', mmdc+'.i[1]' )
    cmds.connectAttr( mmdc + '.or', second + '.r' )

    
    
def localMatrixConnect( first, second ):
    
    dcmp = cmds.createNode( 'decomposeMatrix', n=second+'_localConnect' )
    cmds.connectAttr( first + '.m', dcmp+'.inputMatrix' )
    cmds.connectAttr( dcmp+'.ot', second+'.t', f=1 )
    cmds.connectAttr( dcmp+'.or', second+'.r', f=1 )
    



def connectTranslate( first, second ):
    
    cmds.connectAttr( first + '.t', second + '.t' )
    
    

def connectRotate( first, second ):
    
    cmds.connectAttr( first + '.r', second + '.r' )
    
    
def connectScale( first, second ):
    
    cmds.connectAttr( first + '.s', second + '.s' )
    
    
def connectShear( first, second ):
    
    cmds.connectAttr( first + '.sh', second + '.sh' )
    
    
    
def aimObjectConnect( targets ):
    
    for i in range( len( targets ) -1 ):
        
        first  = targets[i]
        second = targets[i+1]
        
        grp = cmds.createNode( 'transform', n=second+'_aimObj_GRP' )
        trg = cmds.createNode( 'transform', n=second+'_aimObj' )
        cmds.parent( trg, grp )
        constraint( first, grp )
        
        localMtx = cmds.createNode( 'multMatrixDecompose', n=second+'_localMtx' )
        fbfMtx   = cmds.createNode( 'fourByFourMatrix',    n=second+'_fbfMtx' )
        shdOrt   = cmds.createNode( 'shoulderOrient',      n=second+'_shdOrt' )
        
        cmds.connectAttr( second+'.wm', localMtx+'.i[0]' )
        cmds.connectAttr( first+'.wim', localMtx+'.i[1]' )
        cmds.connectAttr( localMtx+'.otx', fbfMtx+'.i00' )
        cmds.connectAttr( localMtx+'.oty', fbfMtx+'.i01' )
        cmds.connectAttr( localMtx+'.otz', fbfMtx+'.i02' )
        cmds.connectAttr( fbfMtx+'.output', shdOrt+'.inputMatrix' )
        cmds.connectAttr( shdOrt+'.outAngleX', trg+'.rx' )
        cmds.connectAttr( shdOrt+'.outAngleY', trg+'.ry' )
        cmds.connectAttr( shdOrt+'.outAngleZ', trg+'.rz' )
    



def localBlendMatrixConnect( first, second, third ):
    
    blendNode = cmds.createNode( 'blendTwoMatrixDecompose', n=second+'_fkikBlend' )
    cmds.connectAttr( first+'.m', blendNode+'.inMatrix1' )
    cmds.connectAttr( second+'.m', blendNode+'.inMatrix2' )
    #cmds.connectAttr( blendNode+'.ot', third+'.t' )
    
    if not cmds.attributeQuery( 'blend', node=third, ex=1 ):
        cmds.addAttr( third, ln='blend', min=0, max=1, dv=0.5 )
        cmds.setAttr( third+'.blend', e=1, k=1 )
    
    cmds.connectAttr( third+'.blend', blendNode+'.attributeBlender' )
    cmds.connectAttr( blendNode+'.or', third+'.r' )
    return blendNode




def replaceConnection( first, second ):
    
    fSrcCons = cmds.listConnections( first, s=1, d=0, p=1, c=1 )
    
    if fSrcCons:
        outputs = fSrcCons[1::2]
        inputs  = fSrcCons[::2]
        
        for i in range( len( outputs ) ):
            try:
                cmds.connectAttr( outputs[i], inputs[i].replace( first, second ), f=1 )
                cmds.disconnectAttr( outputs[i], inputs[i] )
            except: pass
    
    fDesCons = cmds.listConnections( first, s=0, d=1, p=1, c=1 )
    
    if fDesCons:
        outputs = fDesCons[::2]
        inputs  = fDesCons[1::2]
        
        for i in range( len( outputs ) ):
            try:
                cmds.connectAttr( outputs[i].replace( first, second ), inputs[i], f=1 )
                cmds.disconnectAttr( outputs[i], inputs[i] )
            except:pass

    


class MmConnectEach:
    
    def __init__(self ):
        
        self._parentMode = ConnectionInfo._parentMode
    
    
    def updateSelections(self):
        sels = cmds.ls( sl=1 )
        self._sels = sels
        
        self._firsts = sels[::2]
        self._seconds = sels[1::2]
        
        self._len = len( self._seconds )
        
        if self._parentMode:
            for i in range( self._len ):
                self._seconds[i] = cmds.listRelatives( self._seconds[i], p=1, f=1 )[0]

    
    def translate(self, *args ):
        self.updateSelections()
        for i in range( self._len ):
            connectTranslate( self._firsts[i], self._seconds[i] )
        cmds.select( self._sels )
            
    def rotate(self, *args ):
        self.updateSelections()
        for i in range( self._len ):
            connectRotate( self._firsts[i], self._seconds[i] )
        cmds.select( self._sels )
            
    def scale(self, *args ):
        self.updateSelections()
        for i in range( self._len ):
            connectScale( self._firsts[i], self._seconds[i] )
        cmds.select( self._sels )
        
    def shear(self, *args ):
        self.updateSelections()
        for i in range( self._len ):
            connectShear( self._firsts[i], self._seconds[i] )
        cmds.select( self._sels )    
        
    def localTransform( self, *args ):
        self.updateSelections()
        for i in range( self._len ):
            localMatrixConnect( self._firsts[i], self._seconds[i] )
        cmds.select( self._sels )    
            
    def constraint(self, *args ):
        self.updateSelections()
        for i in range( self._len ):
            constraint( self._firsts[i], self._seconds[i] )
        cmds.select( self._sels )
        
    def constraintOrient(self, *args ):
        self.updateSelections()
        for i in range( self._len ):
            constraintOrient( self._firsts[i], self._seconds[i] )
        cmds.select( self._sels )



def mmSetParentModeTrue( *args ):
    
    ConnectionInfo._parentMode = True
    
    
    
def mmSetParentModeFalse( *args ):
    
    ConnectionInfo._parentMode = False



class MmConnectAll:
    
    def __init__(self ):
        
        self._parentMode = ConnectionInfo._parentMode

    
    def updateSelections(self):
        sels = cmds.ls( sl=1 )
        self._sels = sels
        
        self._first = sels[0]
        self._others = sels[1:]
        
        self._len = len( self._others )
        
        if self._parentMode:
            for i in range( self._len ):
                self._others[i] = cmds.listRelatives( self._others[i], p=1, f=1 )[0]

    
    def translate(self, *args ):
        self.updateSelections()
        for i in range( self._len ):
            connectTranslate( self._first, self._others[i] )
        cmds.select( self._sels )
            
    def rotate(self, *args ):
        self.updateSelections()
        for i in range( self._len ):
            connectRotate( self._first, self._others[i] )
        cmds.select( self._sels )
            
    def scale(self, *args ):
        self.updateSelections()
        for i in range( self._len ):
            connectScale( self._first, self._others[i] )
        cmds.select( self._sels )
            
    def shear(self, *args ):
        self.updateSelections()
        for i in range( self._len ):
            connectShear( self._first, self._others[i] )
        cmds.select( self._sels )
            
    def localTransform( self, *args ):
        self.updateSelections()
        for i in range( self._len ):
            localMatrixConnect( self._first, self._others[i] )
        cmds.select( self._sels )
            
    def constraint(self, *args ):
        self.updateSelections()
        for i in range( self._len ):
            constraint( self._first, self._others[i] )
        cmds.select( self._sels )
            
    def constraintOrient(self, *args ):
        self.updateSelections()
        for i in range( self._len ):
            constraintOrient( self._firsts[i], self._seconds[i] )
        cmds.select( self._sels )
    



def mmAimObjectConnect( *args ):
    
    aimObjectConnect( cmds.ls( sl=1 ) )
    
    


def mmLocalBlendMatrixConnect( *args ):
    
    sels = cmds.ls( sl=1 )
    
    first  = sels[0]
    second = sels[1]
    thirds  = sels[2:]
    
    nodes = []
    for i in range( len( thirds ) ):
        node = localBlendMatrixConnect( first, second, thirds[i] )
        nodes.append( node )
        
    cmds.select( sels )
    



def mmSwitchVisConnection( *args ):
    
    sels = cmds.ls( sl=1 )
    
    switch = sels[0]
    
    selectAttr = cmds.channelBox( 'mainChannelBox', q=1, sma=1 )[0]
    
    condition1 = cmds.createNode( 'condition', n=switch+'_'+selectAttr+'_f' )
    condition2 = cmds.createNode( 'condition', n=switch+'_'+selectAttr+'_s' )
    cmds.setAttr( condition1+'.secondTerm', 1 )
    cmds.setAttr( condition2+'.secondTerm', 0 )
    cmds.connectAttr( switch+'.'+selectAttr, condition1+'.firstTerm' )
    cmds.connectAttr( switch+'.'+selectAttr, condition2+'.firstTerm' )
    
    
    
    
def mmGetChildDecompose( *args ):
    
    sels = cmds.ls( sl=1 )
    
    child = sels[0]
    parent = sels[1]
    
    mmdc = cmds.createNode( 'multMatrixDecompose', n=child+'_mmdc' )
    cmds.connectAttr( child+'.wm', mmdc+'.i[0]' )
    cmds.connectAttr( parent + '.wim', mmdc+'.i[1]' )
    
    cmds.select( mmdc )
    
    
def mmGetChildMatrix( *args ):
    
    sels = cmds.ls( sl=1 )
    
    child = sels[0]
    parent = sels[1]
    
    mmdc = cmds.createNode( 'multMatrix', n=child+'_mmtx' )
    cmds.connectAttr( child+'.wm', mmdc+'.i[0]' )
    cmds.connectAttr( parent + '.wim', mmdc+'.i[1]' )
    
    cmds.select( mmdc )
    
    
    
def mmReplaceByTarget( *args ):
    
    sels = cmds.ls( sl=1 )
    
    first = sels[0]
    second = sels[1]
    target = sels[2]
    
    cons = cmds.listConnections( first, d=1, s=0, p=1, c=1 )
    
    outputs = cons[::2]
    inputs  = cons[1::2]
    
    for i in range( len( outputs ) ):
        if inputs[i].find( target ) != -1:
            cmds.connectAttr( outputs[i].replace( first, second ), inputs[i], f=1 )
            
            
def mmReplaceConnections( *args ):
    
    sels = cmds.ls( sl=1 )
    
    firsts = sels[::2]
    seconds= sels[1::2]
    
    for i in range( len( seconds ) ):
        replaceConnection( firsts[i], seconds[i] )