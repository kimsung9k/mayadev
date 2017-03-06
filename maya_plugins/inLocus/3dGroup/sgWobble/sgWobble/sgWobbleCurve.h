#ifndef _sgWobbleCurve
#define _sgWobbleCurve


#include <maya/MPxNode.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnEnumAttribute.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MFnUnitAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MRampAttribute.h>
#include <maya/MTypeId.h> 
#include <maya/MFnDependencyNode.h>

#include <maya/MPlugArray.h>

#include <maya/MPointArray.h>
#include <maya/MDoubleArray.h>

#include <maya/MTime.h>
#include <maya/MMatrix.h>
#include <maya/MVector.h>
#include <maya/MMatrixArray.h>

#include <maya/MFnNurbsCurve.h>
#include <maya/MFnNurbsCurveData.h>

#include <math.h>

class sgWobbleCurve : public MPxNode
{
public:
						sgWobbleCurve();
	virtual				~sgWobbleCurve();

	virtual MStatus		compute( const MPlug& plug, MDataBlock& data );
	virtual MStatus     setDependentsDirty( const MPlug& plug, MPlugArray& plugArr );

	static  void*		creator();
	static  MStatus		initialize();

	MStatus clearCurveDirty( MDataBlock& data );
	MStatus clearAimMatrix( MDataBlock& data );
	MStatus clearCurveMatrix( MDataBlock& data );
	MStatus clearAimIndex( MDataBlock& data );
	MStatus clearWaves( MDataBlock& data );
	MStatus clearEndRate( MDataBlock& data );

	MStatus getEachPointMatrix();
	MStatus getEachAngleMatrix();
	MStatus multEachPoints();
	MStatus editPoints();
	MStatus editPointsByMatrixMult();

	MStatus setResult( MDataBlock& data );

	MMatrix getAimVectorMatrix( MMatrix mtxBase, MVector vAim, MPoint pointStart, unsigned int indexAxis );
	MMatrix getAngledMatrix( double angle1, double angle2, unsigned int indexAxis );

public:
	static MObject  aAimMatrix;
	static MObject  aAimIndex;
	static MObject  aInputCurveMatrix;
	static MObject  aInputCurve;

	static  MObject aWaves;
		static  MObject aRate1;
		static  MObject aRate2;
	static  MObject aWaveOptions;
		static  MObject aOffset;
		static  MObject aWaveLength;
		static  MObject aTimeMult;
	static  MObject  aPinEndRate;

	static  MObject aFallOff;

	static  MObject  aTime;
	static  MObject  aEnvelope;
	static  MObject  aMatrixMult;

	static  MObject  aOutputCurve;
	static  MObject  aOutMatrix;

	static  MObject aApplyCurveLength;

	static	MTypeId		id;

public:
	bool m_isCurveDirty;
	bool m_isAimMatrixDirty;
	bool m_isCurveMatrixDirty;
	bool m_isAimIndexDirty;
	bool m_isWaveDirty;
	bool m_isTimeDirty;
	bool m_isFalloffDirty;
	bool m_isEndRateDirty;

	MPointArray m_pointsInputCurve;
	MObject m_outputCurve;
	double m_curveLength;
	int m_indexAxis;

	float m_endRate;
	float m_envelope;
	bool  m_matrixMult;

	MMatrix m_mtxCurve;
	MMatrix m_mtxAim;
	MMatrix m_mtxLocalAim;

	MMatrixArray m_mtxArrEachPoint;
	MMatrixArray m_mtxArrEachAngle;
	MPointArray  m_pointsResult;

	MDoubleArray m_dArrRate1;
	MDoubleArray m_dArrRate2;

	int m_numCVs;
	int m_degrees;
};

#endif