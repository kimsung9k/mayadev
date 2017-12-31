#include "sgBulgeDeformer.h"
#include "sgPrintf.h"
#include  "sgMeshInfo.h"


MTypeId sgBulgeDeformer::id( unsigned int(0x2017121900) );
MString sgBulgeDeformer::nodeName = "sgBulgeDeformer";


MObject sgBulgeDeformer::aBulgeWeight;
MObject sgBulgeDeformer::aBulgeRadius;
MObject sgBulgeDeformer::aBulgeInputs;
	MObject sgBulgeDeformer::aMatrix;
	MObject sgBulgeDeformer::aMesh;


MString sgBulgeDeformer::nameBulgeWeight = "bulgeWeight";
MString sgBulgeDeformer::nameBulgeRadius = "bulgeRadius";
MString sgBulgeDeformer::nameBulgeInputs = "bulgeInputs";
	MString sgBulgeDeformer::nameMatrix = "matrix";
	MString sgBulgeDeformer::nameMesh   = "mesh";


sgBulgeDeformer::sgBulgeDeformer()
{
	mem_maxLogicalIndex = 0;
	mem_resetElements = false;
	mem_meshInfosInner.clear();
	mem_meshInfosOuter.clear();
}


sgBulgeDeformer::~sgBulgeDeformer()
{
	mem_meshInfosInner.clear();
	mem_meshInfosOuter.clear();
}


MStatus sgBulgeDeformer::initialize()
{
	MStatus status;

	MFnNumericAttribute nAttr;
	MFnTypedAttribute tAttr;
	MFnMatrixAttribute mAttr;
	MFnCompoundAttribute cAttr;

	aBulgeWeight = nAttr.create(nameBulgeWeight, nameBulgeWeight, MFnNumericData::kFloat, 1.0);
	nAttr.setStorable(false);
	nAttr.setKeyable(true);
	addAttribute(aBulgeWeight);

	aBulgeRadius = nAttr.create(nameBulgeRadius, nameBulgeRadius, MFnNumericData::kDouble, 0);
	nAttr.setMin(0);
	nAttr.setStorable(false);
	nAttr.setKeyable(true);
	addAttribute(aBulgeRadius);

	aBulgeInputs = cAttr.create(nameBulgeInputs, nameBulgeInputs);
	aMatrix = mAttr.create(nameMatrix, nameMatrix);
	aMesh = tAttr.create(nameMesh, nameMesh, MFnData::kMesh );
	cAttr.addChild(aMatrix);
	cAttr.addChild(aMesh);
	cAttr.setArray(true);
	addAttribute(aBulgeInputs);

	attributeAffects(aBulgeWeight, outputGeom);
	attributeAffects(aBulgeRadius, outputGeom);
	attributeAffects(aBulgeInputs, outputGeom);

	return status;
}


void* sgBulgeDeformer::creator()
{
	return new sgBulgeDeformer;
}



MStatus sgBulgeDeformer::setDependentsDirty(const MPlug& plug, MPlugArray& plugs)
{
	MStatus status;

	if( plug == aMesh || plug == aMatrix )
	{
		unsigned int logicalIndex = plug.parent().logicalIndex();
		if (logicalIndex > mem_maxLogicalIndex)
		{
			mem_maxLogicalIndex = logicalIndex;
			mem_resetElements   = true;
		}
	}

	return status;
}



MStatus sgBulgeDeformer::deform(MDataBlock& dataBlock, MItGeometry& iter, const MMatrix& mtx, unsigned int index)
{
	MStatus status;

	float bulgeWeight = dataBlock.inputValue(aBulgeWeight).asFloat();
	double bulgeRadius = dataBlock.inputValue(aBulgeRadius).asDouble();

	MArrayDataHandle hArrInputs = dataBlock.inputArrayValue(aBulgeInputs);

	MPointArray allPositions;
	iter.allPositions(allPositions);

	if (mem_resetElements)
	{
		unsigned int elementCount = hArrInputs.elementCount();
		mem_meshInfosInner.resize(mem_maxLogicalIndex);
		mem_meshInfosOuter.resize(mem_maxLogicalIndex);

		for (unsigned int i = 0; i < elementCount; i++, hArrInputs.next())
		{
			MDataHandle hInput = hArrInputs.inputValue();
			MDataHandle hMatrix = hInput.child(aMatrix);
			MDataHandle hMesh   = hInput.child(aMesh);

			MMatrix mtxMesh = hMatrix.asMatrix();
			MObject oMesh   = hMesh.asMesh();

			MFnMeshData meshDataInner, meshDataOuter;
			MObject oMeshInner = meshDataInner.create();
			MObject oMeshOuter = meshDataOuter.create();
			MFnMesh fnMesh;
			fnMesh.copy(oMesh, oMeshInner);
			fnMesh.copy(oMesh, oMeshOuter);

			sgMeshInfo* newMeshInfoInner = new sgMeshInfo(oMeshInner, hMatrix.asMatrix());
			sgMeshInfo* newMeshInfoOuter = new sgMeshInfo(oMeshOuter, hMatrix.asMatrix());

			mem_meshInfosInner[hArrInputs.elementIndex()] = newMeshInfoInner;
			mem_meshInfosOuter[hArrInputs.elementIndex()] = newMeshInfoOuter;
		}
	}
	
	for (unsigned int i = 0; i < elementCount; i++)
	{
		mem_meshInfosInner[i]->setBulge(bulgeWeight, MSpace::kWorld );
	}
	
	MFloatArray weightList;
	weightList.setLength(allPositions.length());
	for (unsigned int i = 0; i < weightList.length(); i++)
		weightList[i] = 0.0f;
	MMatrixArray inputMeshMatrixInverses;
	inputMeshMatrixInverses.setLength(elementCount);
	for (unsigned int i = 0; i < elementCount; i++)
	{
		inputMeshMatrixInverses[i] = mem_meshInfosInner[i]->matrix();
	}

	for (unsigned int i = 0; i < allPositions.length(); i++)
	{
		float resultWeight = 0;
		for (unsigned int infoIndex = 0; infoIndex < elementCount; infoIndex++)
		{
			MPoint localPoint = allPositions[i] * mtx* inputMeshMatrixInverses[infoIndex];
			MPoint innerPoint = mem_meshInfosInner[infoIndex]->getClosestPoint(localPoint);
			MPoint outerPoint = mem_meshInfosOuter[infoIndex]->getClosestPoint(localPoint);
			MVector innerVector = innerPoint - localPoint;
			MVector outerVector = outerPoint - localPoint;

			if (innerVector * outerVector < 0)
			{
				double innerLength = innerVector.length();
				double outerLength = outerVector.length();
				double allLength = innerLength + outerLength;

				float numerator = float( innerLength * outerLength );
				float denominator = float( pow(allLength / 2.0, 2) );

				resultWeight = numerator / denominator;
			}
		}
		weightList[i] = resultWeight;
	}

	for (unsigned int i = 0; i < allPositions.length(); i++)
	{
		allPositions[i] += weightList[i] * MVector(0, 1, 0);
	}
	
	iter.setAllPositions(allPositions);

	return MS::kSuccess;
}