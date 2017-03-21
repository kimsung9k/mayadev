#pragma once

#include <maya/MPxNode.h>
#include <maya/MMatrix.h>
#include <maya/MMatrixArray.h>
#include <maya/MDoubleArray.h>

class SGControlledCurve00 : public MPxNode
{
public:
	SGControlledCurve00();
	virtual ~SGControlledCurve00();

	static void* creator();
	static MStatus initialize();

	virtual MStatus compute(const MPlug& targetPlug, MDataBlock& datablock);
	virtual MStatus setDependentsDirty(const MPlug& targetPlug, MPlugArray& plugArr);

	void computDetail();

private:
	static MObject aInputCurve;
	static MObject aControls;
		static MObject aParameter;
		static MObject aBindPreMatrix;
		static MObject aMatrix;
	static MObject aSmoothRate;
	static MObject aOutputCurve;

	static MString strInputCurve;
	static MString strControls;
		static MString strParameter;
		static MString strBindPreMatrix;
		static MString strMatrix;
	static MString strSmoothRate;
	static MString strOutputCurve;

public:
	static  MString     typeName;
	static	MTypeId		id;


private:
	MObject      m_oInputCurve;
	MDoubleArray m_parameters;
	MMatrixArray m_bindPreMatrices;
	MMatrixArray m_matrices;
	double       m_smoothValue;
	MObject      m_oOutputCurve;
};