#ifndef MESHSNAPCOMMAND_H
#define MESHSNAPCOMMAND_H

#include <maya/MArgDataBase.h>
#include <maya/MDagPath.h>
#include <maya/MDGModifier.h>
#include <maya/MFnDagNode.h>
#include <maya/MFnDependencyNode.h>
#include <maya/MFnIntArrayData.h>
#include <maya/MFnMesh.h>
#include <maya/MGlobal.h>
#include <maya/MIntArray.h>
#include <maya/MItDependencyGraph.h>
#include <maya/MMeshIntersector.h>
#include <maya/MObject.h>
#include <maya/MPlug.h>
#include <maya/MPointArray.h>
#include <maya/MPxCommand.h>
#include <maya/MSelectionList.h>
#include <maya/MSyntax.h>

class MeshSnapCommand : public MPxCommand
{
public:
    MeshSnapCommand();
    virtual MStatus doIt( const MArgList& argList );
    virtual MStatus redoIt();
    virtual MStatus undoIt();
    virtual bool isUndoable() const;
    static void* creator();
    static MSyntax newSyntax();

private:
    MStatus getShapeNode( MDagPath& path );
    MStatus calculateVertexMapping();
    MStatus getSnapDeformerFromBaseMesh( MObject& oSnapDeformer );

    MDagPath m_pathBaseMesh;
    MDagPath m_pathSnapMesh;
    MIntArray m_vertexMapping;
    MString m_name;
    MDGModifier m_dgMod;


};


#endif