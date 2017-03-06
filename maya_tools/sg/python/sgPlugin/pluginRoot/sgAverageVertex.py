
import sys
import copy
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as OpenMayaUI
import maya.OpenMayaMPx as OpenMayaMPx

import maya.OpenMayaUI
from PySide import QtGui, QtCore
import shiboken


class SGAverageVertex( OpenMayaMPx.MPxCommand ): 
    
    commandName = 'sgAverageVertex'

    kWeightFlags  = ['-w', '-weight']
    
    @staticmethod
    def creator():
        return OpenMayaMPx.asMPxPtr(SGAverageVertex())
    
    
    @staticmethod
    def newSyntax():
        syntax = OpenMaya.MSyntax()
        syntax.addFlag(SGAverageVertex.kWeightFlags[0],  SGAverageVertex.kWeightFlags[1], OpenMaya.MSyntax.kDouble )
        return syntax


    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)        
        self.__average = False
        self.__weight  = 1.0
    
    
    def doIt(self, *args):
        
        argData = OpenMaya.MArgDatabase(self.syntax(), *args )
        if argData.isFlagSet( SGAverageVertex.kWeightFlags[0] ):
            self.__weight  = argData.flagArgumentDouble(SGAverageVertex.kWeightFlags[0], 0 )
        
        self.averageVerticesDoit()
        self.redoIt()
    
    
    def averageVerticesDoit(self):
        
        richSelection = OpenMaya.MRichSelection()
        OpenMaya.MGlobal.getRichSelection( richSelection )
        selection = OpenMaya.MSelectionList()
        symetry = OpenMaya.MSelectionList()
        
        richSelection.getSelection( selection )
        richSelection.getSymmetry( symetry )
        
        averageList = []
        for i in range( selection.length() ):
            dagPath = OpenMaya.MDagPath()
            oComponent = OpenMaya.MObject()
            
            selection.getDagPath( i, dagPath, oComponent )
            fnMesh = OpenMaya.MFnMesh( dagPath )
            weights = [ 0 for i in range( fnMesh.numVertices() ) ]
            
            fnComp = OpenMaya.MFnSingleIndexedComponent( oComponent )
            
            for j in range( fnComp.elementCount() ):
                weights[ fnComp.element( j ) ] = fnComp.weight(j).influence()
            averageList.append( [dagPath, weights] )
            

        for i in range( symetry.length() ):
            dagPath = OpenMaya.MDagPath()
            oCompSymmetry = OpenMaya.MObject()
            symetry.getDagPath( i, dagPath, oCompSymmetry )
            fnCompSymmetry = OpenMaya.MFnSingleIndexedComponent( oCompSymmetry )
            
            for j in range( fnCompSymmetry.elementCount() ):
                weights[ fnCompSymmetry.element( j ) ] = fnCompSymmetry.weight(j).influence()
            averageList.append( [dagPath, weights] )
        
        self.dagPaths = []
        self.beforePointList = []
        self.afterPointList = []
        
        for dagPath, weights in averageList:
            itVertex = OpenMaya.MItMeshVertex(dagPath)
        
            fnMesh = OpenMaya.MFnMesh( dagPath )
            meshMatrix = dagPath.inclusiveMatrix()
            meshMatrixInv = dagPath.inclusiveMatrixInverse()
            
            points     = OpenMaya.MPointArray()
            editPoints = OpenMaya.MPointArray()
            fnMesh.getPoints( points )
            fnMesh.getPoints( editPoints )
            
            util = OpenMaya.MScriptUtil()
            util.createFromInt( 0 )
            prevIndex = util.asIntPtr()
            
            resultIndices = OpenMaya.MIntArray()
            
            for i in range( len( weights ) ):
                if not weights[i]: continue
                #print "weight[ %d] : %f" % ( i, weights[i] )
                itVertex.setIndex( i, prevIndex )
                itVertex.getConnectedVertices( resultIndices )
                
                sumPoints = OpenMaya.MVector( 0,0,0 )
                for j in range( resultIndices.length() ):
                    sumPoints += OpenMaya.MVector( (points[resultIndices[j]] * meshMatrix) )
                sumPoints /= resultIndices.length()
                movedPoint = OpenMaya.MVector( sumPoints )
                origPoint = OpenMaya.MVector( points[i] * meshMatrix )
                weightedPoint = OpenMaya.MPoint((movedPoint-origPoint)*weights[i]*self.__weight + origPoint) * meshMatrixInv
                
                editPoints.set( weightedPoint, i )
            
            #fnMesh.setPoints( editPoints )
            self.dagPaths.append( dagPath )
            self.beforePointList.append( points )
            self.afterPointList.append( editPoints )


    def averageVerticesRedo(self):
        
        for i in range( len( self.dagPaths ) ):
            fnMesh = OpenMaya.MFnMesh(self.dagPaths[i] )
            fnMesh.setPoints( self.afterPointList[i] )


    def averageVerticesUndo(self):
        
        for i in range( len( self.dagPaths ) ):
            fnMesh = OpenMaya.MFnMesh(self.dagPaths[i] )
            fnMesh.setPoints( self.beforePointList[i] )
        


    def redoIt(self):
        self.averageVerticesRedo()

    
    def undoIt(self):
        self.averageVerticesUndo()
        
    
    def isUndoable(self):
        return True

    
    




# initialize the script plug-in
def initializePlugin(mobject):
    
    mplugin = OpenMayaMPx.MFnPlugin(mobject, "Autodesk", "1.0", "Any")
    mplugin.registerCommand( SGAverageVertex.commandName, SGAverageVertex.creator, SGAverageVertex.newSyntax )


# Uninitialize the script plug-in
def uninitializePlugin(mobject):
    
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    mplugin.deregisterCommand( SGAverageVertex.commandName )

