moduleName = "MODULE_NAME"

exec( "import %s.file as SGMPlugMod01_file"   % moduleName )
exec( "import %s.mod as SGMPlugMod01_mod"    % moduleName )
exec( "import %s.format as SGMPlugMod01_format" % moduleName )
exec( "import %s.get as SGMPlugMod01_get" % moduleName )

import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as OpenMaya


class SGMPlugMod01_markingMenuCmd:
    
    import cPickle
    
    mirrorValue = 0

    @staticmethod
    def deleteHistory( evt=0 ):
        cuSels = cmds.ls( sl=1 )
        shapes = SGMPlugMod01_get.shapesOfComponentSelected()
        for shape in shapes:
            SGMPlugMod01_mod.deleteHistory( shape )
        cmds.select( cuSels );
    
    @staticmethod
    def collapseEdge( evt=0 ):
        cmds.polyCollapseEdge()
        cmds.select( cl=1 )
    
    @staticmethod
    def extrudeFace( evt=0 ):
        mel.eval( "SGMPlugMod01Command -upm" )
        cmds.polyExtrudeFacet( ch=1, kft=1, d=1, twist=0, taper=1, off=0, tk=0, sma=30, ltz=0 )
        mel.eval( "SGMPlugMod01Command -upm" )
        pass
    
    @staticmethod
    def averageNormal( evt=0 ):
        mel.eval( "SGMPlugMod01Command -upc" )
        SGMPlugMod01_mod.averageNormal()
        mel.eval( "SGMPlugMod01Command -upc" )
    
    @staticmethod
    def averageVertex( evt=0 ):
        mel.eval( "SGMPlugMod01Command -upc" )
        cmds.polyAverageVertex()
        mel.eval( "SGMPlugMod01Command -upc" )
    
    @staticmethod
    def deleteEdge( evt=0 ):
        cmds.DeleteEdge()
        cmds.select( cl=1 )
        
    @staticmethod
    def fillhole( evt=0 ):
        cmds.FillHole()
        cmds.select( cl=1 )
    
    @staticmethod
    def bevelEdge( evt=0 ):
        mel.eval( "SGMPlugMod01Command -upm" )
        cmds.polyBevel( f =0.5, oaf=1, af=1, sg=1, ws=1, sa=30, fn=1, mv=0, ma=180, at=180 )
        mel.eval( "SGMPlugMod01Command -upm" )
        cmds.select( cl= 1 )
    
    @staticmethod
    def updateData( data ):
        f = open( SGMPlugMod01_markingMenuCmd.modeFilePath, 'r' )
        origData = SGMPlugMod01_markingMenuCmd.cPickle.load( f )
        f.close()
        origData.update( data )
        f = open( SGMPlugMod01_markingMenuCmd.modeFilePath, 'w' )
        SGMPlugMod01_markingMenuCmd.cPickle.dump( origData, f )
        f.close()
    
    @staticmethod
    def getData( key ):
        f = open( SGMPlugMod01_markingMenuCmd.modeFilePath, 'r' )
        origData = SGMPlugMod01_markingMenuCmd.cPickle.load( f )
        f.close()
        return origData[key]
    
    
    @staticmethod
    def setDefaultMode( evt=0 ):
        SGMPlugMod01_markingMenuCmd.updateData( {'mode':0} )
        
        
    @staticmethod
    def setMoveBrushMode( evt=0 ):
        SGMPlugMod01_markingMenuCmd.updateData( {'mode':1} )


    @staticmethod
    def setSculptMode( evt=0 ):
        SGMPlugMod01_markingMenuCmd.updateData( {'mode':2} )
    
    @staticmethod
    def symmetryXOn( evt=0 ):
        if SGMPlugMod01_markingMenuCmd.mirrorValue:
            mel.eval( "SGMPlugMod01Command -sym 0")
            SGMPlugMod01_markingMenuCmd.mirrorValue = 0
        else:
            mel.eval( "SGMPlugMod01Command -sym 1")
            SGMPlugMod01_markingMenuCmd.mirrorValue = 1
        
        modeFilePath = uiInfoPath = cmds.about(pd=True) + "/sg_toolInfo/SGMPlugMod01.txt"
        SGMPlugMod01_file.makeFile( modeFilePath )
        
        data = 'False'
        if SGMPlugMod01_markingMenuCmd.mirrorValue: data = 'True'
        
        f = open( modeFilePath, 'w' )
        f.write( data )
        f.close()
        
    
    @staticmethod
    def duplicateAndAddFace( evt=0 ):
        sels = SGMPlugMod01_get.activeSelectionApi()
        
        mel.eval( "SGMPlugMod01Command -upm" )
        commandName = "select "
        for dagPath, oComp in sels:
            singleComp = OpenMaya.MFnSingleIndexedComponent( oComp )
            compIndices = OpenMaya.MIntArray()
            singleComp.getElements( compIndices )
            sgFormatMesh = SGMPlugMod01_format.Mesh( OpenMaya.MFnDagNode( dagPath ).name() )
            newIndices = sgFormatMesh.duplicateAndAddFace( compIndices )
            meshName = OpenMaya.MFnMesh( dagPath ).partialPathName()
            
            for i in range( len( newIndices ) ):
                commandName += " %s.f[%d]" %( meshName, newIndices[i] )
        mel.eval( "SGMPlugMod01Command -upm" )
        
        mel.eval( commandName )
    
    @staticmethod
    def addDivision( evt=0 ):
        if not cmds.ls( sl=1 ): return None
        mel.eval( "SGMPlugMod01Command -upm" )
        cmds.polySubdivideFacet( dv=1, m=0, ch=1 )
        mel.eval( "SGMPlugMod01Command -upm" )
        


def SGMPlugMod01Command_markingMenu_defaultMenu( parentName ):

    modeFilePath = uiInfoPath = cmds.about(pd=True) + "/sg_toolInfo/SGMPlugMod01.txt"
    SGMPlugMod01_file.makeFile( modeFilePath )
    
    f = open( modeFilePath, 'r' )
    data = f.read()
    f.close()
    
    if not data:
        mel.eval( "SGMPlugMod01Command -sym 0" )
        f = open( modeFilePath, 'w' )
        f.write( 'False' )
        f.close()
        SGMPlugMod01_markingMenuCmd.mirrorValue = 0
    else:
        if data == 'True':
            mel.eval( "SGMPlugMod01Command -sym 1" )
            SGMPlugMod01_markingMenuCmd.mirrorValue = 1
        else:
            mel.eval( "SGMPlugMod01Command -sym 0" )
            SGMPlugMod01_markingMenuCmd.mirrorValue = 0

    cmds.menuItem( "Symmetry X", cb=SGMPlugMod01_markingMenuCmd.mirrorValue, rp="N", c=SGMPlugMod01_markingMenuCmd.symmetryXOn, p=parentName  )
    cmds.menuItem( l="Average", p=parentName, sm=1, rp='NW' )
    cmds.menuItem( l="Average Normal", rp="NW", c = SGMPlugMod01_markingMenuCmd.averageNormal )
    cmds.menuItem( l="Average Vertex", rp="W",  c = SGMPlugMod01_markingMenuCmd.averageVertex )
    cmds.menuItem( l="Delete History", p = parentName, c = SGMPlugMod01_markingMenuCmd.deleteHistory )



def SGMPlugMod01Command_markingMenu_edgeMenu( parentName ):
    SGMPlugMod01Command_markingMenu_defaultMenu( parentName )
    cmds.menuItem( l="Collapse Edge",  p = parentName, rp="NE", c = SGMPlugMod01_markingMenuCmd.collapseEdge )
    cmds.menuItem( l="Bevel Edge", p=parentName, rp="E", c= SGMPlugMod01_markingMenuCmd.bevelEdge )
    cmds.menuItem( l="Delete Edge",  p = parentName, rp="SW", c = SGMPlugMod01_markingMenuCmd.deleteEdge )
    cmds.menuItem( l="Fill Hole", p = parentName, c= SGMPlugMod01_markingMenuCmd.fillhole )
    
    cmds.menuItem( l="Convert Selection", p=parentName, sm=1, rp='W' )
    


def SGMPlugMod01Command_markingMenu_polyMenu( parentName ):
    SGMPlugMod01Command_markingMenu_defaultMenu( parentName )
    cmds.menuItem( l="Extrude Face",  p = parentName, rp="NE", c = SGMPlugMod01_markingMenuCmd.extrudeFace )
    cmds.menuItem( l="Duplicate and Add Face",  p = parentName, rp="E", c = SGMPlugMod01_markingMenuCmd.duplicateAndAddFace )
    cmds.menuItem( l="Add division", p= parentName, rp="SE", c= SGMPlugMod01_markingMenuCmd.addDivision )



def SGMPlugMod01Command_markingMenu_vtxMenu( parentName ):
    SGMPlugMod01Command_markingMenu_defaultMenu( parentName )


