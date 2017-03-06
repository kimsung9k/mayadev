#ifndef _keepRoundDeformer_h
#define _keepRoundDeformer_h


#include <maya/MPxDeformerNode.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MTypeId.h>
#include <maya/MItGeometry.h>
#include <maya/MPlug.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>

#include <maya/MVector.h>
#include <maya/MPointArray.h>
#include <maya/MDoubleArray.h>
#include <maya/MFnMesh.h>
#include <maya/MMatrix.h>

#include <maya/MGlobal.h>


class keepRoundDeformer : public MPxDeformerNode
{
public:
						keepRoundDeformer();
	virtual				~keepRoundDeformer();
	
	virtual MStatus     deform( MDataBlock& data, MItGeometry& iter, const MMatrix& mat, unsigned int index );
	virtual MStatus     setDependentsDirty( const MPlug& plug, MPlugArray& plugArr );

	MStatus editPointsWidthMatrix( const MDoubleArray& distsPoint, const MPointArray& editPointArr,
		                           MPointArray& outPointArr, MMatrix& InputMatrix, float envValue ); 

	static  void*		creator();
	static  MStatus		initialize();

public:
	static  MObject     aBaseMesh;
	static  MObject		aInputMatrix;
	static	MTypeId		id;
	
public:
	bool    m_isOrigGeomDirty;
	bool    m_isBaseGeomDirty;
	bool    m_isMatrixDirty;

	MMatrix      m_matrix;
	MDoubleArray m_distsPoint;
	MPointArray  m_pointsOrig;
	MPointArray  m_outputPoints;
};


#endif