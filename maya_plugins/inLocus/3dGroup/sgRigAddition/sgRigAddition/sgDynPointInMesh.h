#ifndef _sgDynPointInMesh_h
#define _sgDynPointInMesh_h


#include <maya/MPxNode.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnUnitAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MTypeId.h>

#include <maya/MFnMesh.h>

#include <maya/MPointArray.h>

#include <maya/MMatrix.h>
#include <maya/MMatrixArray.h>
#include <maya/MVector.h>
#include <maya/MFloatPoint.h>
#include <maya/MMeshIntersector.h>

#include <maya/MTime.h>

#include <maya/MPlugArray.h>

#include <maya/MObjectArray.h>

#include <maya/MFnTransform.h>

#include <maya/MDagModifier.h>

#include <maya/MGlobal.h>

class sgDynPointInMesh : public MPxNode
{
public:
						sgDynPointInMesh();
	virtual				~sgDynPointInMesh();

	virtual MStatus		compute( const MPlug& plug, MDataBlock& data );
	virtual MStatus     setDependentsDirty( const MPlug& plug, MPlugArray& plugArr );

	static  void*		creator();
	static  MStatus		initialize();

public:
	static  MObject     aDynamicOn;

	static  MObject     aStartTime;
	static  MObject     aCurrentTime;

	static  MObject     aAttachPercent;
	static  MObject     aDecreasePercent;
	static  MObject     aBounceRate;
	static  MObject     aLockDistance;

	static  MObject     aTimeScale;
	static  MObject     aSpaceScale;

	static  MObject     aInputPoint;
		static  MObject     aInputPointX;
		static  MObject     aInputPointY;
		static  MObject     aInputPointZ;
	static  MObject     aLocalMesh;
	static  MObject     aMeshMatrix;
	static  MObject		aOutputPoint;
		static  MObject		aOutputPointX;
		static  MObject		aOutputPointY;
		static  MObject		aOutputPointZ;

	static  MObject     aFrames;
	static  MObject     aValues;

	static	MTypeId		id;

private:
	bool m_meshChanged;
	MObject m_oMesh;
	MFnMesh m_fnMesh;

	MPoint  m_beforePoint;
	MMatrix m_beforeMatrix;
	MTime   m_beforeTime;

	MVector  m_beforeVelocity;

	MVector m_meshSpeed;

	MFnDependencyNode m_fnNode;

	MObjectArray m_oTrs;

	bool m_attrModified;
};

#endif