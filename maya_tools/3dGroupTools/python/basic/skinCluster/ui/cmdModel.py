from uiModel import *
import maya.mel as mel
import maya.cmds as cmds
import maya.OpenMaya as om
import functions.autoLoadPlugin



def getMObject( target ):
    
    selList = om.MSelectionList()
    selList.add( target )
    mObj = om.MObject()
    selList.getDependNode( 0, mObj )
    return mObj
    


def copyWeight( first, second ):
    
    hists = cmds.listHistory( first, pdo=1 )
    
    skinNode = None
    for hist in hists:
        
        if cmds.nodeType( hist ) == 'skinCluster':
            skinNode = hist
            
    if not skinNode: return None
    
    targetSkinNode = None
    targetHists = cmds.listHistory( second, pdo=1 )
    if targetHists:
        for hist in targetHists:
            if cmds.nodeType( hist ) == 'skinCluster':
                targetSkinNode = hist

    if not targetSkinNode:
        bindObjs = cmds.listConnections( skinNode+'.matrix', s=1, d=0, type='joint' )
        bindObjs.append( second )
        print bindObjs
        cmds.skinCluster( bindObjs, tsb=1 )
    
    cmds.copySkinWeights( first, second, noMirror=True, surfaceAssociation='closestPoint', influenceAssociation ='oneToOne' )


class CmdLock:
    
    @classmethod
    def lockAll( cls, *args ):
        
        for jnt in cmds.ls( type='joint' ):
            if not cmds.attributeQuery( 'lockInfluenceWeights', node=jnt, ex=1 ): continue
            cmds.setAttr( jnt+'.lockInfluenceWeights', 1 )

    @classmethod
    def unlockAll( cls, *args ):
        
        for jnt in cmds.ls( type='joint' ):
            if not cmds.attributeQuery( 'lockInfluenceWeights', node=jnt, ex=1 ): continue
            cmds.setAttr( jnt+'.lockInfluenceWeights', 0 )
            
    @classmethod
    def lockSel( cls, *args ):
        
        for jnt in cmds.ls( sl=1, type='joint' ):
            if not cmds.attributeQuery( 'lockInfluenceWeights', node=jnt, ex=1 ): continue
            cmds.setAttr( jnt+'.lockInfluenceWeights', 1 )
            
    @classmethod
    def unlockSel( cls, *args ):
        
        for jnt in cmds.ls( sl=1, type='joint' ):
            if not cmds.attributeQuery( 'lockInfluenceWeights', node=jnt, ex=1 ): continue
            cmds.setAttr( jnt+'.lockInfluenceWeights', 0 )
            
    @classmethod
    def lockOSel( cls, *args ):
        
        for jnt in cmds.ls( type='joint' ):
            if not cmds.attributeQuery( 'lockInfluenceWeights', node=jnt, ex=1 ): continue
            cmds.setAttr( jnt+'.lockInfluenceWeights', 0 )
        for jnt in cmds.ls( type='joint', sl=1 ):
            if not cmds.attributeQuery( 'lockInfluenceWeights', node=jnt, ex=1 ): continue
            cmds.setAttr( jnt+'.lockInfluenceWeights', 1 )
        
    @classmethod
    def unlockOSel( cls, *args ):
        
        for jnt in cmds.ls( type='joint' ):
            if not cmds.attributeQuery( 'lockInfluenceWeights', node=jnt, ex=1 ): continue
            cmds.setAttr( jnt+'.lockInfluenceWeights', 1 )
        for jnt in cmds.ls( type='joint', sl=1 ):
            if not cmds.attributeQuery( 'lockInfluenceWeights', node=jnt, ex=1 ): continue
            cmds.setAttr( jnt+'.lockInfluenceWeights', 0 )




class CmdWeight:
    
    @staticmethod
    def copyVtxW( *args ):
        
        mel.eval( 'artAttrSkinWeightCopy()' )
    
    @staticmethod  
    def pastVtxW( *args ):
        
        mel.eval( 'artAttrSkinWeightPaste()' )
        
        
    @staticmethod
    def weightHammer( *args ):
        
        mel.eval( 'weightHammerVerts' )



class CmdMirrorWeight:
    
    @staticmethod
    def weightToR( *args ):
        
        sels = cmds.ls( sl=1 )
        targetObj = sels[0]
        
        hists = cmds.listHistory( targetObj )
        
        skinNode = ''
        for hist in hists:
            if cmds.nodeType( hist ) == 'skinCluster':
                skinNode = hist
                break
                
        if not skinNode: return None

        cmds.copySkinWeights( ss=skinNode, ds=skinNode, mirrorMode = 'YZ',
                              surfaceAssociation = 'closestPoint', influenceAssociation = ['oneToOne','closestJoint'] )
    
    @staticmethod
    def weightToL( *args ):
        
        sels = cmds.ls( sl=1 )
        targetObj = sels[0]
        
        hists = cmds.listHistory( targetObj )
        
        skinNode = ''
        for hist in hists:
            if cmds.nodeType( hist ) == 'skinCluster':
                skinNode = hist
                break
                
        if not skinNode: return None
        
        cmds.copySkinWeights( ss=skinNode, ds=skinNode, mirrorMode = 'YZ', mirrorInverse=True,
                              surfaceAssociation = 'closestPoint', influenceAssociation = ['oneToOne','closestJoint'] )
        
        
class CmdHammerBrush:
    
    _cmdStr =  """global string $tf_skinSmoothPatin_selection[];
    
    global proc tf_smoothBrush( string $context )     
    {       
     artUserPaintCtx -e -ic "tf_init_smoothBrush"
     -svc "tf_set_smoothBrushValue"
     -fc "" -gvc "" -gsc "" -gac "" -tcc "" $context;
    }
    
    global proc tf_init_smoothBrush( string $name )
    {
        string $sel[] = `ls -sl -fl`;
        string $obj[] = `ls -sl -o`;
        
        sgSmoothWeightCommand $obj;
    }
    
    global proc tf_set_smoothBrushValue( int $slot, int $index, float $val )             
    {         
        sgSmoothWeightCommand -i $index -w $val;
    }
    
    ScriptPaintTool;     
    artUserPaintCtx -e -tsc "tf_smoothBrush" `currentCtx`;"""
    
    @staticmethod
    def doCmd( *args ):
        
        import functions
        functions.autoLoadPlugin.AutoLoadPlugin().load( 'sgSmoothWeightCommand' )
        mel.eval( CmdHammerBrush._cmdStr )




class CmdHardBrush:
    
    _cmdStr =  """global string $tf_skinHardPatin_selection[];
    
    global proc tf_hardBrush( string $context )     
    {       
     artUserPaintCtx -e -ic "tf_init_hardBrush"
     -svc "tf_set_hardBrushValue"
     -fc "" -gvc "" -gsc "" -gac "" -tcc "" $context;
    }
    
    global proc tf_init_hardBrush( string $name )
    {
        string $sel[] = `ls -sl -fl`;
        string $obj[] = `ls -sl -o`;
        
        sgSmoothWeightCommand $obj;
    }
    
    global proc tf_set_hardBrushValue( int $slot, int $index, float $val )             
    {
        sgSmoothWeightCommand -h 1 -i $index -w $val;
    }
    
    ScriptPaintTool;     
    artUserPaintCtx -e -tsc "tf_hardBrush" `currentCtx`;"""
    
    @staticmethod
    def doCmd( *args ):
        
        import functions
        functions.autoLoadPlugin.AutoLoadPlugin().load( 'sgSmoothWeightCommand' )
        mel.eval( CmdHardBrush._cmdStr )
        
        
        
        
class cmdSmoothBind:
    
    def __init__(self):
        
        pass
    
    @staticmethod
    def smoothBind( *args ):
        
        sels = cmds.ls( sl=1 )
        cmds.skinCluster( sels )
    
    @staticmethod
    def setJointSelectInfluence( *args ):
        
        mel.eval( 'ArtPaintSkinWeightsTool_select_joint' )
        
        
    @staticmethod
    def ArtPaintSkinWeightsTool( *args ):
        
        mel.eval( 'ArtPaintSkinWeightsTool' )
        
        
    @staticmethod
    def setSkinMatrixDefault( *args ):
        
        sels = cmds.ls( sl=1 )
    
        for sel in sels:
            hists = cmds.listHistory( sel )
            
            skinNode = None
            for hist in hists:
                if cmds.nodeType( hist ) == 'skinCluster':
                    skinNode = hist
                    break
            
            fnSkinNode = om.MFnDependencyNode( getMObject( skinNode ) )
            
            plugMatrix = fnSkinNode.findPlug( 'matrix' )
            plugBindPre = fnSkinNode.findPlug( 'bindPreMatrix' )
            
            for i in range( plugMatrix.numElements() ):
                loIndex = plugMatrix[i].logicalIndex()
                oMtx = plugMatrix[i].asMObject()
                mtxData = om.MFnMatrixData( oMtx )
                mtx = mtxData.matrix()
                invData = om.MFnMatrixData()
                oInv = invData.create( mtx.inverse() )
                plugBindPre.elementByLogicalIndex( loIndex ).setMObject( oInv )
    
    
        


class CmdExportImport:
    
    def __init__(self):
        
        pass
    
    @staticmethod
    def export( *args ):
        
        import functions
        functions.autoLoadPlugin.AutoLoadPlugin().load( 'sgSkinWeightExportImport' )
        
        pathName = cmds.fileDialog2(fileMode=0, ff='*.weight', caption="Export Weight")
        cmds.file( pathName[0], f=1, options="v=0", typ="weight", pr=1, es=1 )


    @staticmethod
    def cmdImport( *args ):
        
        import functions
        functions.autoLoadPlugin.AutoLoadPlugin().load( 'sgSkinWeightExportImport' )
        
        pathName = cmds.fileDialog2(fileMode=1, ff='*.weight', caption="Import Weight")
        cmds.file( pathName[0], i=1, options="v=0", typ="weight", pr=1 )
        
    @staticmethod
    def cmdCopyWeight( *args ):
        
        sels = cmds.ls( sl=1 )
        copyWeight( sels[0], sels[1] );
        
        
class CmdInfluence:
    
    def __init__(self):
        
        pass
    
    @staticmethod
    def removeUnused( *args ):
        
        mel.eval( 'removeUnusedInfluences' )
        
    @staticmethod
    def removeInfluence( *args ):
        
        mel.eval( 'RemoveInfluence' )


    @staticmethod
    def addInfluence( *args ):
        
        mel.eval( 'skinClusterInfluence 1 "-ug -dr 4 -ps 0 -ns 10 -lw true -wt 0";' )
        
    @staticmethod
    def removeCrossWeightInfluence( *args ):
        
        import functions
        functions.autoLoadPlugin.AutoLoadPlugin().load( 'sgSkinClusterWeightEditCommand' )
        cmds.sgRemoveCrossWeights()