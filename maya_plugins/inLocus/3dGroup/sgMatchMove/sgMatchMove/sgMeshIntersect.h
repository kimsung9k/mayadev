#ifndef _sgMeshIntersectNode
#define _sgMeshIntersectNode


#include <maya/MPxNode.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MTypeId.h> 
#include <maya/MFnMesh.h>
#include <maya/MMatrix.h>
#include <maya/MPoint.h>
#include <maya/MVector.h>
#include <maya/MPointArray.h>

#include <maya/MFnTypedAttribute.h>
#include <maya/MFnMatrixAttribute.h>


struct sgMeshIntersectTesk
{
	MPointArray pointsSrc;
	MPointArray pointsDest;
};



class sgMeshIntersect : public MPxNode
{
public:
						sgMeshIntersect();
	virtual				~sgMeshIntersect(); 

	virtual MStatus		compute( const MPlug& plug, MDataBlock& data );
	virtual MStatus     setDependentsDirty( const MPlug& plug, MPlugArray& plugArr );

	static  void*		creator();
	static  MStatus		initialize();

public:
	static  MObject		aPointSource;
		static  MObject		aPointSourceZ;
		static  MObject		aPointSourceY;
		static  MObject		aPointSourceX;
	static  MObject		aPointDest;
		static  MObject		aPointDestX;
		static  MObject		aPointDestY;
		static  MObject		aPointDestZ;
	static  MObject     aInputMesh;
	static  MObject     aInputMeshMatrix;
	static  MObject     aParentInverseMatrix;
	static  MObject     aOutPoint;
		static  MObject     aOutPointX;
		static  MObject     aOutPointY;
		static  MObject     aOutPointZ;

	static	MTypeId		id;

	static unsigned int m_nodeNumber;
	static MIntArray m_existingNodeNumbers;
	static MIntArray m_existingNodeNumbersMap;

private:
	MFnMesh     m_fnMesh;
	MMatrix     m_mtxMesh;
	MMatrix     m_mtxInvMesh;
	MMatrix     m_mtxParentInverse;
	MPoint      m_pointSource;
	MPoint      m_pointDest;
	MVector     m_rayDirection;
	MPointArray m_pointsIntersect;

	bool m_isDirtyPointSrc;
	bool m_isDirtyPointDest;
	bool m_isDirtyMesh;
	bool m_isDirtyMeshMatrix;

	unsigned int m_thisNodeNumber;
};

#endif
