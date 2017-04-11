import maya.cmds as cmds
import dataModel
import ui.view
import copy


class CreateController:
    
    def __init__(self, target, numCtl ):
        
        self._colorIndiecesBase = [ 4,24,22,23,15 ]
        self._colorIndieces     = []
        
        self._mainName = target
        
        size  = self.getSize( target )*0.5
        bbc  = self.getBBC(target)
        
        self.sizeRate = self.getSizeX( self._mainName )/self.getSize( self._mainName )
        
        ctlPs, inits = self.buildInitAndControllerSet( numCtl )
        self.connectInitsToCtlPs(ctlPs, inits)
        main, mainP = self.createMainController()
        cmds.parent( inits, ctlPs[-1], main )
        cmds.setAttr( mainP+'.t', *bbc )
        cmds.setAttr( mainP+'.s', size, size, size )

        target, targetP = self.setTarget( target )
        youngestCtl = cmds.listRelatives( ctlPs[0], c=1 )[0]
        targetP = cmds.parent( targetP, youngestCtl )[0]
        
        self.targetConnect( targetP, inits, main )
        self._target = target
    


    def createController( self, name, position ):
        
        ctl = cmds.curve( p=dataModel.SphereShapeInfo.pointList, n='%s_%s_Ctl' %( self._mainName, name ), d=1 )
        cmds.setAttr( ctl+'.v', e=1, lock=1, k=0 )
        cmds.setAttr( ctl+'.shearXY', e=1, k=1 )
        cmds.setAttr( ctl+'.shearXZ', e=1, k=1 )
        cmds.setAttr( ctl+'.shearYZ', e=1, k=1 )
        ctlP = cmds.group( ctl, n=ctl+'_P' )
        cmds.setAttr( ctlP+'.t', *position )
        
        self.setCtlShape( ctl )
        
        return ctlP
        


    def createInit( self, name, position ):
        
        init = cmds.createNode( 'transform', n= '%s_%s_Init' %( self._mainName, name ) )
        cmds.setAttr( init+'.t', *position )
        cmds.setAttr( init+'.dh', 1 )
        return init
    
    
    def buildInitAndControllerSet( self, num ):
        
        if num == 0: return [], []
        
        namePosList = []
        
        if num == 1:
            namePosList = [['Num00', [ 0,-1, 0] ]]
        else:
            rate = (self.sizeRate*2)/(num-1.0)
            for i in range( num ):
                namePosList.append( ['Num%d' % i, [ -self.sizeRate + rate*i,-1, 0] ] )
        
        ctlPs = []
        inits = []
        for name, pos in namePosList:
            ctlP = self.createController( name, pos )
            init = self.createInit( name, pos )
            ctlPs.append( ctlP )
            inits.append( init )
        
        return ctlPs, inits
    

    def connectInitsToCtlPs( self, ctlPs, inits ):
        
        if not ctlPs: return None
        for i in range( len( ctlPs )-1 ):
            mmdc = cmds.createNode( 'multMatrixDecompose', n=ctlPs[i]+'_LocalDc' )
            cmds.connectAttr( inits[i]+'.wm', mmdc+'.i[0]' )
            cmds.connectAttr( inits[i+1]+'.wim', mmdc+'.i[1]' )
            cmds.connectAttr( mmdc+'.ot', ctlPs[i]+'.t' )
            cmds.connectAttr( mmdc+'.or', ctlPs[i]+'.r' )
            nextCtlPChild = cmds.listRelatives( ctlPs[i+1], c=1 )[0]
            cmds.parent( ctlPs[i], nextCtlPChild )
        
        mmdc = cmds.createNode( 'multMatrixDecompose', n=ctlPs[-1]+'_worldDc' )
        cmds.connectAttr( inits[-1]+'.wm',    mmdc+'.i[0]' )
        cmds.connectAttr( ctlPs[-1]+'.pim',  mmdc+'.i[1]' )
        cmds.connectAttr( mmdc+'.ot', ctlPs[-1]+'.t' )
        cmds.connectAttr( mmdc+'.or', ctlPs[-1]+'.r' )
        
        
        
    def getBBC( self, target):
        
        bbmin = cmds.getAttr( target + '.boundingBoxMin' )[0]
        bbmax = cmds.getAttr( target + '.boundingBoxMax' )[0]
        
        xCenter = ( bbmin[0] + bbmax[0] )*0.5
        yCenter = ( bbmin[1] + bbmax[1] )*0.5
        zCenter = ( bbmin[2] + bbmax[2] )*0.5
        
        return [xCenter, yCenter, zCenter]
    
    
    def getSizeX(self, target ):
        
        bbmin = cmds.getAttr( target + '.boundingBoxMin' )[0]
        bbmax = cmds.getAttr( target + '.boundingBoxMax' )[0]
        
        return bbmax[0] - bbmin[0]
    
    

    def getSize( self, target ):
        
        bbmin = cmds.getAttr( target + '.boundingBoxMin' )[0]
        bbmax = cmds.getAttr( target + '.boundingBoxMax' )[0]
        
        return bbmax[1] - bbmin[1]
    


    def createMainController(self):
        
        ctl = cmds.curve( p=dataModel.RectShapeInfo.pointList, n='%s_Main_CTL' % self._mainName, d=1 )
        cmds.addAttr( ctl, ln='TextVis', min=0, max=1, dv=1, at='long' )
        cmds.setAttr( ctl+'.TextVis', e=1, k=1 )
        cmds.connectAttr( ctl+'.TextVis', self._mainName+'.v' )
        cmds.setAttr( ctl+'.v', e=1, lock=1, k=0 )
        cmds.setAttr( ctl+'.shearXY', e=1, k=1 )
        cmds.setAttr( ctl+'.shearXZ', e=1, k=1 )
        cmds.setAttr( ctl+'.shearYZ', e=1, k=1 )
        cmds.setAttr( ctl+'.s', self.sizeRate, 1,1 )
        cmds.makeIdentity( ctl, apply=1, t=0, r=0, s=1 )
        ctlP = cmds.group( ctl, n=ctl+'_P' )
        
        self.setCtlShape( ctl )
        
        return ctl, ctlP
    
    
    def setTarget(self, target ):
        
        bbc = self.getBBC( target )
        cmds.setAttr( target+'.v', e=1, k=0 )
        grp = cmds.createNode( 'transform', n=target+'_P' )
        
        cmds.setAttr( grp+'.t', bbc[0], bbc[1], bbc[2] )
        target = cmds.parent( target, grp )[0]
        
        cmds.setAttr( target+'.shearXY', e=1, k=1 )
        cmds.setAttr( target+'.shearXZ', e=1, k=1 )
        cmds.setAttr( target+'.shearYZ', e=1, k=1 )
        
        cmds.makeIdentity( target, apply=1, t=1, r=1, s=1 )
        cmds.xform( target, ws=1, piv=bbc )
        
        return target, grp
    
    
    def targetConnect(self, targetP, inits, main ):
        
        mmdc = cmds.createNode( 'multMatrixDecompose', n=targetP+'_worldDc' )
        cmds.connectAttr( main+'.wm',    mmdc+'.i[0]' )
        cmds.connectAttr( inits[0]+'.wim',  mmdc+'.i[1]' )
        cmds.connectAttr( mmdc+'.ot', targetP+'.t' )
        cmds.connectAttr( mmdc+'.or', targetP+'.r' )
        
        
    def setCtlShape(self, target ):
        if not self._colorIndieces:
            self._colorIndieces = copy.copy( self._colorIndiecesBase )
        targetShape = cmds.listRelatives( target, s=1 )[0]
        targetShape = cmds.rename( targetShape, target+'Shape' )
        cmds.setAttr( targetShape+'.overrideEnabled', 1 )
        cmds.setAttr( targetShape+'.overrideColor', self._colorIndieces.pop(0) );

        
        

def copyController( first, second ):
    
    def getInits( target ):
        inits = []
        
        targetP = cmds.listRelatives( target, p=1, f=1 )[0]
        
        mmdc = cmds.listConnections( targetP, s=1, d=0, type='multMatrixDecompose' )[0]
        mainCtl = cmds.listConnections( mmdc+'.i[0]' )[0]
        mainCtlCs = cmds.listRelatives( mainCtl, c=1, f=1 )

        for mainCtlC in mainCtlCs:
            if mainCtlC.find( '_Init' ) != -1:
                inits.append( mainCtlC )
        return inits
    
    fInits = getInits( first )
    
    inst = CreateController( second, len(fInits) )
    second = inst._target
    
    sInits = getInits( second )
    
    for i in range( len( fInits ) ):
        mtx = cmds.getAttr( fInits[i]+'.m' )
        cmds.xform( sInits[i], matrix=mtx )        




def mmCreateController( *args ):
    
    sels = cmds.ls( sl=1 )
    
    for sel in sels:
        CreateController( sel )
        
        
def mmCopyController( *args ):
    
    sels = cmds.ls( sl=1 )
    
    first = sels[0]
    
    for sel in sels[1:]:
        copyController( first, sel )
        
        
def mmOpenKeyControlUI( *args ):
    
    ui.view.KeyControlUI().create()
    
    
def uiCmd_CopyController( *args ):
    
    sels = cmds.ls( sl=1 )
    
    first = sels[0]
    
    for sel in sels[1:]:
        copyController( first, sel )