#include "sgprintf.h"

#include "SGControlledCurve00.h"

#include <maya/MFnCompoundAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnNurbsCurve.h>
#include <maya/MPointArray.h>
#include <maya/MDagPath.h>
#include <maya/MFnNurbsCurveData.h>
#include <vector>


MString SGControlledCurve00::typeName = "SGControlledCurve00";
MTypeId SGControlledCurve00::id( 0xda + 0x133c651 + 0 );

MObject SGControlledCurve00::aInputCurve;
MObject SGControlledCurve00::aControls;
	MObject SGControlledCurve00::aParameter;
	MObject SGControlledCurve00::aBindPreMatrix;
	MObject SGControlledCurve00::aMatrix;
MObject SGControlledCurve00::aSmoothRate;
MObject SGControlledCurve00::aOutputCurve;


MString SGControlledCurve00::strInputCurve = "inputCurve";
MString SGControlledCurve00::strControls = "controls";
	MString SGControlledCurve00::strParameter = "parameter";
	MString SGControlledCurve00::strBindPreMatrix = "bindPreMatrix";
	MString SGControlledCurve00::strMatrix = "matrix";
MString SGControlledCurve00::strSmoothRate = "smoothRate";
MString SGControlledCurve00::strOutputCurve = "outputCurve";


SGControlledCurve00::SGControlledCurve00()
{
}


SGControlledCurve00::~SGControlledCurve00()
{
}


void* SGControlledCurve00::creator()
{
	return new SGControlledCurve00();
}



MStatus SGControlledCurve00::initialize()
{
	MFnCompoundAttribute cAttr;
	MFnMatrixAttribute   mAttr;
	MFnTypedAttribute    tAttr;
	MFnNumericAttribute  nAttr;

	aOutputCurve = tAttr.create( strOutputCurve , strOutputCurve, MFnData::kNurbsCurve );
	tAttr.setStorable(false);
	addAttribute(aOutputCurve);

	aInputCurve = tAttr.create(strInputCurve, strInputCurve, MFnData::kNurbsCurve);
	tAttr.setStorable(true);
	addAttribute(aInputCurve);
	attributeAffects(aInputCurve, aOutputCurve);

	aControls = cAttr.create(strControls, strControls);
	aParameter = nAttr.create(strParameter, strParameter, MFnNumericData::kDouble);
	aBindPreMatrix = mAttr.create(strBindPreMatrix, strBindPreMatrix);
	aMatrix = mAttr.create(strMatrix, strMatrix);
	cAttr.addChild(aParameter);
	cAttr.addChild(aBindPreMatrix);
	cAttr.addChild(aMatrix);
	cAttr.setStorable(true);
	cAttr.setArray(true);
	addAttribute(aControls);
	attributeAffects(aControls, aOutputCurve);

	aSmoothRate = nAttr.create(strSmoothRate, strSmoothRate, MFnNumericData::kDouble);
	nAttr.setMin(0);
	nAttr.setStorable(true);
	addAttribute(aSmoothRate);
	attributeAffects(aSmoothRate, aOutputCurve);

	return MS::kSuccess;
}



MStatus SGControlledCurve00::compute(const MPlug& targetPlug, MDataBlock& datablock)
{
	if (targetPlug != aOutputCurve)
		return MS::kSuccess;

	MStatus status;

	if (m_oInputCurve.isNull())
	{
		MDataHandle hInputCurve = datablock.inputValue(aInputCurve, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);
		m_oInputCurve = hInputCurve.asNurbsCurve();
		MFnNurbsCurve fnInputCurve(m_oInputCurve);
		MFnNurbsCurveData curveData;
		m_oOutputCurve = curveData.create();
		fnInputCurve.copy(m_oInputCurve, m_oOutputCurve );
	}
	MArrayDataHandle hArrControls = datablock.inputArrayValue(aControls, &status);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	int elementCount = hArrControls.elementCount();
	if (m_parameters.length() != elementCount)
		m_parameters.setLength(elementCount);
	if (m_matrices.length() != elementCount)
		m_matrices.setLength(elementCount);
	if (m_bindPreMatrices.length() != elementCount)
		m_bindPreMatrices.setLength(elementCount);
	for ( unsigned int i = 0; i < hArrControls.elementCount(); i++, hArrControls.next() )
	{
		MDataHandle hControls = hArrControls.inputValue(&status);
		m_parameters[i]       = hControls.child(aParameter).asDouble();
		m_matrices[i]         = hControls.child(aMatrix).asMatrix();
		m_bindPreMatrices[i]  = hControls.child(aBindPreMatrix).asMatrix();
	}
	m_smoothValue = datablock.inputValue(aSmoothRate).asDouble();

	computDetail();

	datablock.outputValue(aOutputCurve).set( m_oOutputCurve );

	return MS::kSuccess;
}



void SGControlledCurve00::computDetail()
{
	MFnNurbsCurve fnCurve(m_oInputCurve);
	
	MDagPath dpCurve = MDagPath::getAPathTo(m_oInputCurve);

	MPointArray cvPoints;
	fnCurve.getCVs(cvPoints, MSpace::kTransform);
	
	int numCVs = cvPoints.length();
	int numControl = m_parameters.length();

	MDoubleArray cvParams;
	cvParams.setLength(cvPoints.length());
	for (unsigned int i = 0; i < cvPoints.length(); i++)
	{
		double param;
		fnCurve.closestPoint(cvPoints[i], &param );
		cvParams[i] = param;
	}
	
	std::vector< MDoubleArray > eachControlWeightList;
	eachControlWeightList.resize(numControl);
	for (int i = 0; i < numControl; i++)
		eachControlWeightList[i].setLength(cvParams.length());

	for ( int i = 0; i < numControl-1; i++)
	{
		for ( unsigned int j = 0; j < eachControlWeightList[i].length(); j++)
		{
			if (cvParams[j] <= m_parameters[i]) {
				eachControlWeightList[i][j] = 1.0;
				eachControlWeightList[i + 1][j] = 0.0;
			}
			else if (cvParams[j] <= m_parameters[i + 1]) {
				double paramRange = m_parameters[i + 1] - m_parameters[i];
				double paramValue = cvParams[j] - m_parameters[i];
				double weightValue = paramValue / paramRange;
				eachControlWeightList[i][j] = 1.0-weightValue;
				eachControlWeightList[i + 1][j] = weightValue;
			}
			else {
				eachControlWeightList[i][j] = 0.0;
				eachControlWeightList[i + 1][j] = 1.0;
			}
		}
	}

	MPointArray weightedPoints;
	weightedPoints.setLength(cvPoints.length());

	for (unsigned int i = 0; i < weightedPoints.length(); i++)
	{
		MMatrix weightedMatrix;
		weightedMatrix *= 0;
		double allWeights = 0;
		for (int j = 0; j < numControl; j++)
		{
			weightedMatrix += m_bindPreMatrices[j] * m_matrices[j] * eachControlWeightList[j][i];
			allWeights += eachControlWeightList[j][i];
		}

		if (allWeights == 0) weightedMatrix = MMatrix();
		else { weightedMatrix *= (1.0 / allWeights); }
		weightedPoints[i] = cvPoints[i] * weightedMatrix;
	}

	MFnNurbsCurve fnCurveOutput(m_oOutputCurve);
	fnCurveOutput.setCVs(weightedPoints);
}



MStatus SGControlledCurve00::setDependentsDirty(const MPlug& targetPlug, MPlugArray& plugArr)
{
	if (targetPlug == aInputCurve)
		m_oInputCurve = MObject();

	return MS::kSuccess;
}