#include "sgFootPrintMesh.h"
#include "sgPrintf.h"


MTypeId sgFootPrintMesh::id( unsigned int(0x20171207000) );
MString sgFootPrintMesh::deformerName = "sgFootPrintMesh";

MObject sgFootPrintMesh::aInputs;
	MObject sgFootPrintMesh::aMesh;
	MObject sgFootPrintMesh::aMatrix;

MString sgFootPrintMesh::nameInputs = "inputs";
	MString sgFootPrintMesh::nameMesh = "mesh";
	MString sgFootPrintMesh::nameMatrix = "matrix";


sgFootPrintMesh::sgFootPrintMesh()
{
	MFnMeshData meshData;
	mem_modifiedMesh = meshData.create();
}



sgFootPrintMesh::~sgFootPrintMesh()
{
}



void* sgFootPrintMesh::creator()
{
	return new sgFootPrintMesh();
}



MStatus sgFootPrintMesh::initialize()
{
	MStatus status;

	MFnCompoundAttribute cAttr;
	MFnTypedAttribute tAttr;
	MFnMatrixAttribute mAttr;

	aInputs = cAttr.create(nameInputs, nameInputs);

	aMesh = tAttr.create(nameMesh, nameMesh, MFnData::kMesh);
	tAttr.setCached( true );
	tAttr.setStorable( false );

	aMatrix = mAttr.create( nameMatrix, nameMatrix );
	mAttr.setStorable( false );

	cAttr.addChild( aMesh );
	cAttr.addChild( aMatrix );
	cAttr.setArray( true );

	addAttribute( aInputs );
	attributeAffects(aInputs, outputGeom );

	return MS::kSuccess;
}



MStatus sgFootPrintMesh::setDependentsDirty(const MPlug& plug, MPlugArray& plugArr)
{
	//sgPrintf("dirty plug name : %s", plug.name().asChar());

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


void sgFootPrintMesh::restoreElementList()
{
	//sgPrintf("restore element");
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



void sgFootPrintMesh::restoreMeshs(unsigned int index )
{
	//sgPrintf("restore mesh[%d]", index);
	MStatus status;
	MFnDependencyNode fnThisNode(thisMObject());
	MPlug plugInputs = fnThisNode.findPlug(aInputs);

	MPlug plugMesh = plugInputs[index].child(aMesh);
	MPlugArray connections;

	plugMesh.connectedTo(connections, true, false);
	if (!connections.length()) return;

	MFnMesh fnMesh(connections[0].node(), &status );
	if (!status) return;

	mem_inputMeshInfos[index].setMesh(connections[0].node());
}


void sgFootPrintMesh::restoreMatrices(unsigned int index)
{
	//sgPrintf("restore matrix[%d]", index);
	MFnDependencyNode fnThisNode(thisMObject());
	MPlug plugInputs = fnThisNode.findPlug(aInputs);

	MPlug plugMatrix = plugInputs[index].child(aMatrix);
	mem_inputMeshInfos[index].setMatrix(plugMatrix.asMObject());
}



void sgFootPrintMesh::setDirty(unsigned int logicalIndex )
{
	mem_dirtyList[logicalIndex] = true;
}



void sgFootPrintMesh::finalize()
{
	for (unsigned int i = 0; i < mem_dirtyList.size(); i++)
	{
		mem_dirtyList[i] = false;
	}
}



MObject sgFootPrintMesh::getThisGeometryObject()
{
	MPlug plugOutputGeom = MFnDependencyNode(thisMObject()).findPlug( outputGeom );
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




MStatus sgFootPrintMesh::deform(MDataBlock& data,
	MItGeometry& itGeo,
	const MMatrix& localToWorldMatrix,
	unsigned int geomIndex)
{
	MStatus status;

	MPointArray origPositions;
	itGeo.allPositions(origPositions);

	MArrayDataHandle hArrInputs = data.inputArrayValue(aInputs);
	for (unsigned int i = 0; i < hArrInputs.elementCount(); i++, hArrInputs.next() )
	{
		MDataHandle hInput = hArrInputs.inputValue();
		MDataHandle hMatrix = hInput.child(aMatrix);
		MDataHandle hMesh = hInput.child(aMesh);

		hMatrix.asMatrix();
		hMesh.asMesh();
	}

	for( unsigned int i = 0; i < mem_dirtyList.size(); i++ )
	{
		if (!mem_dirtyList[i]) continue;
		deformEach( mem_inputMeshInfos[i], origPositions, localToWorldMatrix );
	}

	itGeo.setAllPositions(origPositions);

	return MS::kSuccess;
}


void sgFootPrintMesh::deformEach(const sgMeshInfo& meshInfo, MPointArray& points, MMatrix deformerMatrix )
{
	MMatrix multPointMtx = deformerMatrix * meshInfo.matrix().inverse();

	for (unsigned int i = 0; i < points.length(); i++)
	{
		MPoint resultPoint = meshInfo.getClosestPoint( points[i] * multPointMtx );
		points[i] = resultPoint * multPointMtx.inverse();
	}
}