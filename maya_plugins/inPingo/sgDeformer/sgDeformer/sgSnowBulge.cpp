#include "sgSnowBulge.h"
#include "sgPrintf.h"


MTypeId sgSnowBulge::id(0x2017121800);
MString sgSnowBulge::nodeName = "sgSnowBulge";


MObject sgSnowBulge::aReset;
MObject sgSnowBulge::aBulgeWeight;
MObject sgSnowBulge::aBulgeRadius;
MObject sgSnowBulge::aInputOriginalMesh;
MObject sgSnowBulge::aInputModifedMesh;
MObject sgSnowBulge::aOutputMesh;

MString sgSnowBulge::nameReset = "reset";
MString sgSnowBulge::nameBulgeWeight = "bulgeWeight";
MString sgSnowBulge::nameBulgeRadius = "bulgeRadius";
MString sgSnowBulge::nameInputOriginalMesh = "inputOrigMesh";
MString sgSnowBulge::nameInputModifiedMesh = "inputModifiedMesh";
MString sgSnowBulge::nameOutputMesh = "outputMesh";


sgSnowBulge::sgSnowBulge()
{
	MFnMeshData dataModifiedKeep, dataResult;
	mem_oMeshModifiedKeep = dataModifiedKeep.create();
	mem_oMeshResult = dataResult.create();
}


sgSnowBulge::~sgSnowBulge()
{
}


MStatus sgSnowBulge::initialize()
{
	MStatus status;

	MFnNumericAttribute nAttr;
	MFnTypedAttribute tAttr;

	aReset = nAttr.create(nameReset, nameReset, MFnNumericData::kBoolean, false);
	nAttr.setStorable(false);
	nAttr.setKeyable(true);
	addAttribute(aReset);

	aBulgeWeight = nAttr.create(nameBulgeWeight, nameBulgeWeight, MFnNumericData::kFloat, 1.0);
	nAttr.setStorable(false);
	nAttr.setKeyable(true);
	addAttribute(aBulgeWeight);

	aBulgeRadius = nAttr.create(nameBulgeRadius, nameBulgeRadius, MFnNumericData::kDouble, 0 );
	nAttr.setMin(0);
	nAttr.setStorable(false);
	nAttr.setKeyable(true);
	addAttribute(aBulgeRadius);

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

	attributeAffects(aReset, aOutputMesh);
	attributeAffects(aBulgeWeight, aOutputMesh);
	attributeAffects(aBulgeRadius, aOutputMesh);
	attributeAffects(aInputOriginalMesh, aOutputMesh);
	attributeAffects(aInputModifedMesh, aOutputMesh);

	return status;
}


void* sgSnowBulge::creator()
{
	return new sgSnowBulge;
}



void sgSnowBulge::getModifiedPoints( MPointArray &resultPoints, 
	const MPointArray& pointsModified, const MPointArray& pointsOriginal,
	MIntArray* ptrModifiedIndicesMap)
{
	for (unsigned int i = 0; i < pointsModified.length(); i++)
	{
		MVector deltaDefault  = resultPoints[i] - pointsOriginal[i];
		MVector deltaModified = pointsModified[i] - pointsOriginal[i];

		if (fabs(deltaModified.x) > fabs(deltaDefault.x))
			deltaDefault.x = deltaModified.x;
		if (fabs(deltaModified.y) > fabs(deltaDefault.y))
			deltaDefault.y = deltaModified.y;
		if (fabs(deltaModified.z) > fabs(deltaDefault.z))
			deltaDefault.z = deltaModified.z;

		MPoint tempResult = deltaDefault + pointsOriginal[i];

		if (ptrModifiedIndicesMap != NULL && tempResult != resultPoints[i])
			(*ptrModifiedIndicesMap)[i] = 1;

		resultPoints[i] = tempResult;
	}
}



void getRadiusParameterMapFromEachComponent(int baseIndex, int connectedIndex, MFloatArray& radiusParameterMap, float maxRadius,
	const MPointArray& samplePoints, const MIntArray& sampleModifiedMap,
	const MFloatVectorArray& normalsOrig, const MFloatVectorArray& normalsModified,
	MItMeshVertex& itVtx, MIntArray numCheckedMap)
{
	if (sampleModifiedMap[baseIndex]) return;
	if (connectedIndex == -1)
		connectedIndex = baseIndex;
	if (sampleModifiedMap[connectedIndex]) return;

	const MPoint& basePoint      = samplePoints[baseIndex];
	const MPoint& connectedPoint = samplePoints[connectedIndex];
	double dist = basePoint.distanceTo(connectedPoint);
	if (dist > maxRadius) return;
	if (maxRadius == 0) return;

	radiusParameterMap[connectedIndex] = 1.0 - dist / maxRadius;

	int prevIndex;
	itVtx.setIndex(connectedIndex, prevIndex);
	MIntArray connectedIndices;
	itVtx.getConnectedVertices(connectedIndices);

	if (numCheckedMap[connectedIndex] >= connectedIndices.length()) return;
	numCheckedMap[connectedIndex] += 1;

	float editedMaxRadius = maxRadius - dist;

	for ( unsigned int i = 0; i < connectedIndices.length(); i++ )
	{
		getRadiusParameterMapFromEachComponent(baseIndex, connectedIndices[i], radiusParameterMap, editedMaxRadius,
			samplePoints, sampleModifiedMap, normalsOrig, normalsModified,
			itVtx, numCheckedMap);
	}
}


void getRadiusParameterMap( MFloatArray& radiusMap, float maxRadius,
	const MPointArray& samplePoints, const MIntArray& sampleModifiedMap,
	const MFloatVectorArray& normalsOrig, const MFloatVectorArray& normalsModified,
	MItMeshVertex& itVtx )
{
	MIntArray numCheckedMap;
	numCheckedMap.setLength(samplePoints.length());
	for (unsigned int i = 0; i < numCheckedMap.length(); i++)
		numCheckedMap[i] = 0;

	for ( unsigned int i = 0; i < sampleModifiedMap.length(); i++ )
	{
		if( sampleModifiedMap[i] ) continue;
		if (normalsOrig[i] == normalsModified[i]) continue;
		getRadiusParameterMapFromEachComponent(i, -1, radiusMap, maxRadius, samplePoints, sampleModifiedMap, normalsOrig, normalsModified, itVtx, numCheckedMap);
	}
}


void sgSnowBulge::getBulgePoints(MPointArray &bulgePoints,
	const MFloatVectorArray& normalOrig, const MFloatVectorArray& normalModified,
	const MIntArray& mapModified, MItMeshVertex& itVtx,
	float weightBulge, float radiusBulge)
{
	unsigned int numPoints = mapModified.length();
	if (normalOrig.length() != numPoints || normalModified.length() != numPoints) return;
	unsigned int modifiedNormalLength = 0;

	int privIndex;

	MVectorArray bulgeDeltas;
	bulgeDeltas.setLength(numPoints);

	for (unsigned int i = 0; i < bulgeDeltas.length(); i++) {
		bulgeDeltas[i] = normalModified[i];
	}

	MFloatArray radiusParameterMap;
	radiusParameterMap.setLength(numPoints);
	for (unsigned int i = 0; i < radiusParameterMap.length(); i++)
		radiusParameterMap[i] = 0;

	getRadiusParameterMap( radiusParameterMap, radiusBulge, bulgePoints, mapModified, normalOrig, normalModified, itVtx );

	for (unsigned int i = 0; i < bulgeDeltas.length(); i++)
	{
		bulgePoints[i] += ( bulgeDeltas[i] * weightBulge * radiusParameterMap[i]);
	}
}



MStatus sgSnowBulge::compute(const MPlug& plug, MDataBlock& dataBlock)
{
	MStatus status;

	//-------------------------get FnMesh ( original, modified )--------------------------------
	MDataHandle hInputOriginalMesh = dataBlock.inputValue(aInputOriginalMesh);
	MDataHandle hInputModifiedMesh = dataBlock.inputValue(aInputModifedMesh);

	MObject oInputOrigMesh = hInputOriginalMesh.asMesh();
	MObject oInputModifyMesh = hInputModifiedMesh.asMesh();
	
	MFnMesh fnOrig(oInputOrigMesh);
	MFnMesh fnModified(oInputModifyMesh);
	//------------------------------------------------------------------------------------------

	//------------------ Check origMesh and modifiedMesh has same vertices ---------------------
	if (!fnOrig.numVertices() || fnOrig.numVertices() != fnModified.numVertices()) {
		mem_pointsOrig.clear();
		mem_pointsModifiedKeep.clear();
		MGlobal::displayError("Orignal has no same num vertices with modified");
		return MS::kFailure;
	}
	//------------------------------------------------------------------------------------------

	//---------------Check Reset And Reset------------------------------
	MDataHandle hInputReset = dataBlock.inputValue(aReset);
	if (hInputReset.asBool())
	{
		mem_pointsOrig.clear();
		mem_pointsModifiedKeep.clear();
		MFnDependencyNode fnThisNode(thisMObject());
		fnThisNode.findPlug(aReset).setBool(false);
	}
	//---------------------------------------------------------------

	//---------------- Initialize mem_points( orig, modifiedKeep ) and mem_oMeshs( orig, modifiedKeep ) -------------------------
	//---------------- and mem_modifiedKeepIndicesMap----------------------------------------------------------------------------
	if (!mem_pointsModifiedKeep.length())
	{
		fnOrig.getPoints(mem_pointsOrig);
		fnOrig.getPoints(mem_pointsModifiedKeep);
		fnOrig.copy( oInputOrigMesh, mem_oMeshModifiedKeep);
		fnOrig.copy( oInputOrigMesh, mem_oMeshResult );
		mem_modifiedKeepIndicesMap.setLength(mem_pointsModifiedKeep.length() );
		for (unsigned int i = 0; i < mem_modifiedKeepIndicesMap.length(); i++)
			mem_modifiedKeepIndicesMap[i] = 0;
	}
	//---------------------------------------------------------------------------------------------------------------------------

	//-----------------Get Modified Points and Set ModifiedKeep---------------------
	MPointArray pointsModified;
	fnModified.getPoints(pointsModified);

	getModifiedPoints(mem_pointsModifiedKeep, pointsModified, mem_pointsOrig, &mem_modifiedKeepIndicesMap );
	//------------------------------------------------------------------------------
	
	//---------------¤ÑGet Bolge Points------------------------------

	float bulgeWeight = dataBlock.inputValue(aBulgeWeight).asFloat();
	double bulgeRadius = dataBlock.inputValue(aBulgeRadius).asDouble();

	MFnMesh fnMeshModifiedKeep( mem_oMeshModifiedKeep );
	fnMeshModifiedKeep.setPoints( mem_pointsModifiedKeep );

	MPointArray bulgePoints;
	MFloatVectorArray normalsOrig;
	MFloatVectorArray normalsModifiedKeep;
	MItMeshVertex itVtx(mem_oMeshModifiedKeep);

	fnMeshModifiedKeep.getPoints(bulgePoints);
	fnOrig.getVertexNormals( false, normalsOrig );
	fnMeshModifiedKeep.getVertexNormals(false, normalsModifiedKeep );

	getBulgePoints( bulgePoints, normalsOrig, normalsModifiedKeep, mem_modifiedKeepIndicesMap, itVtx, bulgeWeight, bulgeRadius);

	//---------------------------------------------------------------

	//-----------------Set Points to Result--------------------------
	MFnMesh fnMeshOutput(mem_oMeshResult);
	fnMeshOutput.setPoints(bulgePoints);
	//---------------------------------------------------------------

	//-----------------Set Data to Result----------------------------
	MDataHandle hOutputMesh = dataBlock.outputValue(aOutputMesh);
	hOutputMesh.set(mem_oMeshResult);
	hOutputMesh.setClean();
	//---------------------------------------------------------------

	return MS::kSuccess;
}