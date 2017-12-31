#include "sgModifiedmeshKeeper.h"


MTypeId sgModifiedMeshKeeper::id(0x2017121400);
MString sgModifiedMeshKeeper::nodeName = "sgModifiedMeshKeeper";


MObject sgModifiedMeshKeeper::aReset;
MObject sgModifiedMeshKeeper::aInputOriginalMesh;
MObject sgModifiedMeshKeeper::aInputModifedMesh;
MObject sgModifiedMeshKeeper::aOutputMesh;

MString sgModifiedMeshKeeper::nameReset = "reset";
MString sgModifiedMeshKeeper::nameInputOriginalMesh = "inputOrigMesh";
MString sgModifiedMeshKeeper::nameInputModifiedMesh = "inputModifiedMesh";
MString sgModifiedMeshKeeper::nameOutputMesh = "outputMesh";


sgModifiedMeshKeeper::sgModifiedMeshKeeper()
{
	MFnMeshData data;
	mem_oOutputMesh = data.create();
}


sgModifiedMeshKeeper::~sgModifiedMeshKeeper()
{
}


MStatus sgModifiedMeshKeeper::initialize()
{
	MStatus status;

	MFnNumericAttribute nAttr;
	MFnTypedAttribute tAttr;

	aReset = nAttr.create(nameReset, nameReset, MFnNumericData::kBoolean, false);
	nAttr.setStorable(false);
	nAttr.setKeyable(true);
	addAttribute(aReset);

	aInputOriginalMesh = tAttr.create(nameInputOriginalMesh, nameInputOriginalMesh, MFnData::kMesh);
	tAttr.setCached(true);
	tAttr.setStorable(true);
	addAttribute(aInputOriginalMesh);

	aInputModifedMesh = tAttr.create(nameInputModifiedMesh, nameInputModifiedMesh, MFnData::kMesh);
	tAttr.setCached(true);
	tAttr.setStorable(true);
	addAttribute(aInputModifedMesh);

	aOutputMesh = tAttr.create(nameOutputMesh, nameOutputMesh, MFnData::kMesh);
	tAttr.setCached(true);
	tAttr.setStorable(true);
	addAttribute(aOutputMesh);

	attributeAffects(aReset,aOutputMesh);
	attributeAffects(aInputOriginalMesh, aOutputMesh);
	attributeAffects(aInputModifedMesh, aOutputMesh);

	return status;
}


void* sgModifiedMeshKeeper::creator()
{
	return new sgModifiedMeshKeeper;
}


MStatus sgModifiedMeshKeeper::compute(const MPlug& plug, MDataBlock& dataBlock)
{
	MStatus status;

	MDataHandle hInputReset = dataBlock.inputValue(aReset);
	MDataHandle hInputOriginalMesh = dataBlock.inputValue(aInputOriginalMesh);
	MDataHandle hInputModifiedMesh = dataBlock.inputValue(aInputModifedMesh);

	MObject oInputOrigMesh = hInputOriginalMesh.asMesh();
	MObject oInputModifyMesh = hInputModifiedMesh.asMesh();

	MFnMesh fnOrig(oInputOrigMesh);
	MFnMesh fnModified(oInputModifyMesh);

	if ( !fnOrig.numVertices() || fnOrig.numVertices() != fnModified.numVertices()) {
		mem_pointsResult.clear();
		MGlobal::displayError("Orignal has no same num vertices with modified");
		return MS::kFailure;
	}
	
	if( hInputReset.asBool() )
	{
		mem_pointsResult.clear();
		MFnDependencyNode fnThisNode(thisMObject());
		fnThisNode.findPlug(aReset).setBool(false);
	}

	if (!mem_pointsResult.length())
	{
		fnOrig.getPoints(mem_pointsResult);
		fnOrig.copy( oInputOrigMesh, mem_oOutputMesh);
	}

	MPointArray pointsOrig;
	MPointArray pointsModified;
	fnOrig.getPoints(pointsOrig);
	fnModified.getPoints(pointsModified);

	for(unsigned int i = 0; i < mem_pointsResult.length(); i++)
	{
		MVector delta = pointsModified[i] - pointsOrig[i];
		MVector mem_pointDelta = mem_pointsResult[i] - pointsOrig[i];

		if ( fabs(delta.x) > fabs(mem_pointDelta.x))
			mem_pointDelta.x = delta.x;
		if ( fabs(delta.y) > fabs(mem_pointDelta.y) )
			mem_pointDelta.y = delta.y;
		if ( fabs(delta.z) > fabs(mem_pointDelta.z) )
			mem_pointDelta.z = delta.z;

		mem_pointsResult[i] = mem_pointDelta + pointsOrig[i];
	}
	MFnMesh fnMeshOutput(mem_oOutputMesh);
	fnMeshOutput.setPoints(mem_pointsResult);

	MDataHandle hOutputMesh = dataBlock.outputValue(aOutputMesh);
	hOutputMesh.set(mem_oOutputMesh);
	hOutputMesh.setClean();

	return MS::kSuccess;
}