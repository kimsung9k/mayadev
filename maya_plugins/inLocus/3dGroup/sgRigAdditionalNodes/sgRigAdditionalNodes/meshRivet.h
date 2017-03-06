#ifndef _meshRivet_h
#define _meshRivet_h


#include <maya/MPxNode.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnUnitAttribute.h>
#include <maya/MFnEnumAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MTypeId.h>
#include <maya/MPlug.h>
#include <maya/MDataBlock.h>

#include <maya/MTransformationMatrix.h>
#include <maya/MEulerRotation.h>

#include <maya/MBoundingBox.h>

#include <maya/MVector.h>
#include <maya/MPoint.h>
#include <maya/MMatrix.h>
#include <maya/MPointArray.h>
#include <maya/MFnMesh.h>

#include <maya/MFnNurbsCurve.h>

#include <maya/MFnDependencyNode.h>
#include <maya/MPlugArray.h>
#include <maya/MDagPath.h>

#include <maya/MGlobal.h>


class meshRivet : public MPxNode
{
public:
						meshRivet();
	virtual				~meshRivet();

	virtual MStatus     compute( const MPlug& plug, MDataBlock& data );
	virtual MStatus setDependentsDirty( const MPlug& plug, MPlugArray& plugArr );

	static  void*		creator();
	static  MStatus		initialize();

	MStatus setResult( const MPlug& plug, MDataBlock& data );
	void    getMeshInfomation( MDataBlock& data );
	void    getMeshMatrix( MDataBlock& data );
	void    getParentInverseMatrix( MDataBlock& data );
	void    getCenterIndices( MDataBlock& data );
	void    getAimIndices( MDataBlock& data );
	void    getUpIndices( MDataBlock& data );

public:
	static  MObject  aInputMesh;
	static  MObject  aMeshMatrix;

	static  MObject  aCenterIndices;
	static  MObject  aAimPivIndices;
	static  MObject  aAimIndices;
	static  MObject  aUpPivIndices;
	static  MObject  aUpIndices;
	static  MObject  aAimAxis;
	static  MObject  aUpAxis;
	static  MObject  aInverseCross;

	static  MObject  aParentInverseMatrix;

	static  MObject  aResult;
	static  MObject  aOutMatrix;
	static  MObject  aOutTranslate;
		static  MObject  aOutTranslateX;
		static  MObject  aOutTranslateY;
		static  MObject  aOutTranslateZ;
	static  MObject  aOutRotate;
		static  MObject  aOutRotateX;
		static  MObject  aOutRotateY;
		static  MObject  aOutRotateZ;

	static  MTypeId  id;

public:
	bool m_dirty;
	bool m_meshDirty;
	bool m_matrixDirty;
	bool m_parentInverseDirty;
	bool m_indicesCenterDirty;
	bool m_indicesAimDirty;
	bool m_indicesUpDirty;

	unsigned char  m_aimAxis;
	unsigned char  m_upAxis;

	MPointArray m_pointArr;
	MMatrix     m_mtxMesh;
	MMatrix     m_mtxParentInverse;
	MMatrix     m_mtxMult;

	MIntArray m_indicesCenter;
	MIntArray m_indicesAimPiv;
	MIntArray m_indicesAim;
	MIntArray m_indicesUpPiv;
	MIntArray m_indicesUp;

	MPoint  m_localCenter;
	MVector m_localAim;
	MVector m_localUp;

	MPoint  m_outputCenter;
	MVector m_outputAim;
	MVector m_outputUp;

	MMatrix m_mtxResult;
	MVector m_rotResult;
};


#endif