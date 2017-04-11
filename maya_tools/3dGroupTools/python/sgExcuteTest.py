import maya.OpenMaya as om
import maya.OpenMayaAnim as omAnim
import sgModelDag
import maya.mel as mel
import maya.cmds as cmds

def doTest( first, second ):
    oNodeFirst = sgModelDag.getMObject( first )
    oNodeSecond = sgModelDag.getMObject( second )
    
    fnNodeFirst = om.MFnDependencyNode( oNodeFirst )
    fnNodeSecond = om.MFnDependencyNode( oNodeSecond )
    
    attrCountFirst = fnNodeFirst.attributeCount();
    
    for i in range( attrCountFirst ):
        oAttr = fnNodeFirst.attribute( i )
        fnAttr = om.MFnAttribute( oAttr )
        
        
def doTest2():
    
    minTime = om.MTime()
    maxTime = om.MTime()
    currentTime = om.MTime()
    
    minTime = omAnim.MAnimControl().minTime()
    maxTime = omAnim.MAnimControl().maxTime()
    currentTime = omAnim.MAnimControl().currentTime()
    
    print minTime.value()
    print maxTime.value()
    print currentTime.asUnits( 8 )


def doTest3():
    
    oNode = om.MObject()
    selList = om.MSelectionList()
    selList.add( 'pSphere2' )
    selList.getDependNode( 0, oNode )
    
    fnNode = om.MFnDependencyNode( oNode )
    txPlug = fnNode.findPlug( 'tx' )
    
    fnAnimCurve = omAnim.MFnAnimCurve()
    oAnimCurve = fnAnimCurve.create( txPlug )
    
    fnAnimCurve.setObject( oAnimCurve )
    
    time1 = om.MTime( 0 )
    time2 = om.MTime( 1 )
    fnAnimCurve.addKeyframe( time1, 1 )
    fnAnimCurve.addKeyframe( time2, 2 )