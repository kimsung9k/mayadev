#include "sgFootPrintDeformer.h"
#include "sgPrintf.h"


MTypeId sgFootPrintDeformer::id( unsigned int(0x20171207000) );
MString sgFootPrintDeformer::deformerName = "sgFootPrintDeformer";

MObject sgFootPrintDeformer::aInputMesh;
MObject sgFootPrintDeformer::aInputMeshMatrix;
MObject sgFootPrintDeformer::aInputs;
	MObject sgFootPrintDeformer::aMesh;
	MObject sgFootPrintDeformer::aMatrix;
MObject sgFootPrintDeformer::aOutputMesh;

MString sgFootPrintDeformer::nameInputMesh = "inputMesh";
MString sgFootPrintDeformer::nameInputMeshMatrix = "inputMeshMatrix";
MString sgFootPrintDeformer::nameInputs = "inputs";
	MString sgFootPrintDeformer::nameMesh = "mesh";
	MString sgFootPrintDeformer::nameMatrix = "matrix";
MString sgFootPrintDeformer::nameOutputMesh = "outputMesh";


sgFootPrintDeformer::sgFootPrintDeformer()
{
}



sgFootPrintDeformer::~sgFootPrintDeformer()
{
}



void* sgFootPrintDeformer::creator()
{
	return new sgFootPrintDeformer();
}



MStatus sgFootPrintDeformer::initialize()
{
	MStatus status;

	MFnCompoundAttribute cAttr;
	MFnTypedAttribute tAttr;
	MFnMatrixAttribute mAttr;

	aInputMesh = tAttr.create( nameInputMesh, nameInputMesh, MFnData::kMesh );
	addAttribute(aInputMesh);

	aInputMeshMatrix = mAttr.create(nameInputMeshMatrix, nameInputMeshMatrix);
	addAttribute(aInputMeshMatrix);

	aInputs = cAttr.create(nameInputs, nameInputs);

	aMesh = tAttr.create(nameMesh, nameMesh, MFnData::kMesh);
	tAttr.setCached( true );
	tAttr.setStorable( false );

	aMatrix = mAttr.create( nameMatrix, nameMatrix );
	mAttr.setStorable( false );

	cAttr.addChild( aMesh );
	cAttr.addChild( aMatrix );
	cAttr.setArray( true );

	aOutputMesh = tAttr.create(nameOutputMesh, nameOutputMesh, MFnData::kMesh);
	addAttribute(aOutputMesh);

	addAttribute( aInputs );

	attributeAffects(aInputMesh, aOutputMesh);
	attributeAffects(aInputMeshMatrix, aOutputMesh);
	attributeAffects(aInputs, aOutputMesh);

	return MS::kSuccess;
}



MStatus sgFootPrintDeformer::setDependentsDirty(const MPlug& plug, MPlugArray& plugArr)
{
	if (plug == aMatrix || plug == aMesh)
	{
		restoreElementList();
		setDirty(plug.parent().logicalIndex());
	}

	if (plug == aMatrix)
	{
		restoreMatrices(plug.parent().logicalIndex());
	}

	if ( plug == aMesh )
	{
		restoreMeshs(plug.parent().logicalIndex());
	}

	return MS::kSuccess;
}



void sgFootPrintDeformer::restoreDeformMesh()
{
	MFnDependencyNode fnThisNode(thisMObject());
	MPlug plugInputGeom = fnThisNode.findPlug( aInputMesh );

	MPlugArray connections;
	plugInputGeom.connectedTo( connections, true, false );

	if (!connections.length()) return;

	MObject oInputGeom = connections[0].asMObject();
	if (mem_modifiedMesh.isNull())
	{
		mem_modifiedMesh = oInputGeom;
	}
	else
	{
		MFnMesh fnInputGeom(oInputGeom);
		MFnMesh fnMemGeom(mem_modifiedMesh);

		if( fnInputGeom.numVertices() != fnMemGeom.numVertices() )
		{
			mem_modifiedMesh = oInputGeom;
		}
	}
}



void sgFootPrintDeformer::restoreElementList()
{
	sgPrintf("restore element");
	MFnDependencyNode fnThisNode(thisMObject());
	MPlug plugInputs = fnThisNode.findPlug(aInputs);

	unsigned int elementSize = plugInputs.numElements();
	unsigned int elementSizeByLogicalIndex = 0;

	for (unsigned int i = 0; i < elementSize; i++)
	{
		elementSizeByLogicalIndex = plugInputs[i].logicalIndex() + 1;
	}

	if (mem_connectedList.size() != elementSizeByLogicalIndex)
	{
		mem_connectedList.resize(elementSizeByLogicalIndex);
		mem_dirtyList.resize(elementSizeByLogicalIndex);
		mem_inputMeshInfos.resize(elementSizeByLogicalIndex);

		for (unsigned int i = 0; i < elementSizeByLogicalIndex; i++)
		{
			MPlug plugInput = plugInputs[i];
			MPlug plugMesh = plugInput.child(aMesh);
			MPlug plugMatrix = plugInput.child(aMatrix);
			mem_inputMeshInfos[i].setMesh(plugMesh.asMObject());
			mem_inputMeshInfos[i].setMatrix(plugMatrix.asMObject());
		}
	}
}



void sgFootPrintDeformer::restoreMeshs(unsigned int index )
{
	sgPrintf("restore mesh[%d]", index);
	MStatus status;
	MFnDependencyNode fnThisNode(thisMObject());
	MPlug plugInputs = fnThisNode.findPlug(aInputs);

	MPlug plugMesh = plugInputs[index].child(aMesh);
	MPlugArray connections;

	plugMesh.connectedTo(connections, true, false);
	if (!connections.length()) return;

	MFnMesh fnMesh(connections[0].node(), &status );
	if (!status) return;

	if (mem_inputMeshInfos[index].numVertice() != fnMesh.numVertices() )
	{
		mem_inputMeshInfos[index].setMesh(connections[0].node());
	}
}


void sgFootPrintDeformer::restoreMatrices(unsigned int index)
{
	sgPrintf("restore matrix[%d]", index);
	MFnDependencyNode fnThisNode(thisMObject());
	MPlug plugInputs = fnThisNode.findPlug(aInputs);

	MPlug plugMatrix = plugInputs[index].child(aMatrix);
	mem_inputMeshInfos[index].setMatrix(plugMatrix.asMObject());
}



void sgFootPrintDeformer::setDirty(unsigned int logicalIndex )
{
	mem_dirtyList[logicalIndex] = true;
}



void sgFootPrintDeformer::finalize()
{
	for (unsigned int i = 0; i < mem_dirtyList.size(); i++)
	{
		mem_dirtyList[i] = false;
	}
}



MObject sgFootPrintDeformer::getThisGeometryObject()
{
	MPlug plugOutputGeom = MFnDependencyNode(thisMObject()).findPlug( aOutputMesh );
	MPlugArray connections;
	plugOutputGeom[0].connectedTo(connections, false, true );

	MPlug targetPlug;
	for (unsigned int i = 0; i < connections.length(); i++)
	{
		targetPlug = connections[i];
		break;
	}
	
	return targetPlug.node();
}




MStatus sgFootPrintDeformer::compute(const MPlug& plug, MDataBlock& data)
{
	MStatus status;

	MDataHandle hInputMesh       = data.inputValue(aInputMesh);
	MDataHandle hInputMeshMatrix = data.inputValue(aInputMeshMatrix);

	if( mem_modifiedMesh.isNull() || MFnMesh(mem_modifiedMesh).numVertices() != MFnMesh(hInputMesh.asMesh()).numVertices() )
	{
		mem_modifiedMesh = hInputMesh.asMesh();
	}

	MPointArray  basePoints;
	MFloatVectorArray baseNormals;

	MFnMesh fnMeshModified(mem_modifiedMesh);
	fnMeshModified.getPoints(basePoints);
	fnMeshModified.getVertexNormals(true, baseNormals);

	MArrayDataHandle hArrInputs = data.inputArrayValue(aInputs);

	for( unsigned int i = 0; i < mem_dirtyList.size(); i++ )
	{
		if (!mem_dirtyList[i]) continue;
	}

	MDataHandle hOutputMesh = data.outputValue(aOutputMesh);
	hOutputMesh.setMObject(mem_modifiedMesh);

	finalize();

	return MS::kSuccess;
}