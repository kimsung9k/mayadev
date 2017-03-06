#ifndef _CollisionJointNode
#define _CollisionJointNode


#include <maya/MPxNode.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnEnumAttribute.h>
#include <maya/MTypeId.h> 

#include <maya/MMatrix.h>
#include <maya/MMatrixArray.h>

#include <maya/MFnMesh.h>

 
class CollisionJoint : public MPxNode
{
public:
						CollisionJoint();
	virtual				~CollisionJoint(); 

	virtual MStatus		compute( const MPlug& plug, MDataBlock& data );
	virtual MStatus     setDependentsDirty( const MPlug& plug, MPlugArray& plugArr );

	static  void*		creator();
	static  MStatus		initialize();

	MStatus clearMatrix( MDataBlock& data );
	MStatus clearMeshMatrix( MDataBlock& data );
	MStatus clearMesh( MDataBlock& data );
	MStatus clearAxis( MDataBlock& data );
	MStatus clearLockRate( MDataBlock& data );

	MStatus defaultOutputCaculate();

public:

	static  MObject		aInputMatrix;
	static  MObject		aMesh;
	static  MObject     aMeshMatrix;
	static  MObject     aAimAxis;
	static  MObject     aUpAxis;
	static  MObject     aAngleLockRate;
	static  MObject     aOutputMatrix;

	static	MTypeId		id;

public:
	bool    m_dirtyMatrix;
	bool    m_dirtyMesh;
	bool    m_dirtyMeshMatrix;
	bool    m_dirtyAxis;
	bool    m_dirtyAngleLockRate;

	MMatrixArray  m_mtxArrWorld;
	MMatrixArray  m_mtxArrLocal;
	MMatrix       m_mtxMesh;
	MFnMesh       m_mesh;
	unsigned char m_aimIndex;
	unsigned char m_upIndex;
	float         m_angleRate;
	MMatrixArray  m_mtxArrDefaultOutput;
	MMatrixArray  m_mtxArrAxisOutput;
};

#endif
