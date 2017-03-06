import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import math, sys
from maya import cmds

kPluginCmdName="sgCmdSkinClustser"

kDefaultFlag = "-d"
kDefaultFlag_long = "-setDefault"

# command
class SGCmdSkinCluster(OpenMayaMPx.MPxCommand):
    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)
        self.__setDefault = 0
        self.__sList = OpenMaya.MSelectionList()


    def doIt(self, args):
        argData = OpenMaya.MArgDatabase(self.syntax(), args)
        if argData.isFlagSet(kDefaultFlag):
            self.__setDefault = argData.flagArgumentInt(kDefaultFlag, 0)
        argData.getObjects( self.__sList )
        self.redoIt()


    def redoIt(self):
        
        picked = OpenMaya.MObjectArray()
        dependNode = OpenMaya.MObject()     # Selected dependency node

        # Create a selection list iterator
        
        OpenMaya.MGlobal.getActiveSelectionList(self.__sList)
        iter = OpenMaya.MItSelectionList(self.__sList)

        # Iterate over all selected dependency nodes
        # and save them in a list
        while not iter.isDone():
            # Get the selected dependency node
            iter.getDependNode(dependNode)
            picked.append(dependNode)
            iter.next()
        
        self.__undoSetList = []
        self.__skinNodes = []
        
        cmds.undoInfo( swf=0 )
        
        for i in range( picked.length() ):
            fnPicked = OpenMaya.MFnDependencyNode( picked[i] )
            hists = cmds.listHistory( fnPicked.name() )
            
            skinNode = None
            for hist in hists:
                if cmds.nodeType( hist ) == 'skinCluster':
                    skinNode = hist
                    break
            
            fnSkinNode = OpenMaya.MFnDependencyNode( self.__getMObject( skinNode ) )
            
            plugMatrix = fnSkinNode.findPlug( 'matrix' )
            plugBindPre = fnSkinNode.findPlug( 'bindPreMatrix' )
            
            for i in range( plugMatrix.numElements() ):
                loIndex = plugMatrix[i].logicalIndex()
                srcJoints = cmds.listConnections( plugMatrix[i].name(), s=1, d=0 )
                if not srcJoints: continue
                undoSet = [plugBindPre.elementByLogicalIndex( loIndex ).name(), cmds.getAttr( plugBindPre.elementByLogicalIndex( loIndex ).name() )]
                cmds.setAttr( plugBindPre.elementByLogicalIndex( loIndex ).name(), cmds.getAttr( srcJoints[0] +'.wim' ), type='matrix' )
                self.__undoSetList.append( undoSet )
            cmds.dgdirty( fnSkinNode.name() )
            self.__skinNodes.append( fnSkinNode.name() )
        cmds.undoInfo( swf=1 )
    
    
    def undoIt(self):
        
        cmds.undoInfo( swf=0 )
        for attr, data in self.__undoSetList:
            cmds.setAttr( attr, data, type='matrix' )
        for skinNode in self.__skinNodes:
            cmds.dgdirty( skinNode )
        cmds.undoInfo( swf=1 )
    
    
    
    def isUndoable(self):
        return True
    
    
    
    def __getMObject( self, target ):
        mObject = OpenMaya.MObject()
        selList = OpenMaya.MSelectionList()
        selList.add( target )
        selList.getDependNode( 0, mObject )
        return mObject
        
        
        

# Creator
def cmdCreator():
    return OpenMayaMPx.asMPxPtr( SGCmdSkinCluster() )


# Syntax creator
def syntaxCreator():
    syntax = OpenMaya.MSyntax()
    syntax.addFlag(kDefaultFlag, kDefaultFlag_long, OpenMaya.MSyntax.kLong)
    syntax.useSelectionAsDefault(True);
    syntax.setObjectType( syntax.kSelectionList, 0 );
    return syntax


# Initialize the script plug-in
def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject, "Autodesk", "1.0", "Any")
    try:mplugin.registerCommand(kPluginCmdName, cmdCreator, syntaxCreator)
    except:sys.stderr.write("Failed to register command: %s\n" % kPluginCmdName);raise


# Uninitialize the script plug-in
def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:mplugin.deregisterCommand(kPluginCmdName)
    except:sys.stderr.write("Failed to unregister command: %s\n" % kPluginCmdName);raise


