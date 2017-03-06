#include "precompile.h"

#include "SGCommand.h"
#include <maya/MPlug.h>
#include <maya/MPlugArray.h>
#include <maya/MFnComponentListData.h>
#include <maya/MFnSingleIndexedComponent.h>
#include "SGNodeControl.h"
#include "SGTimeCheck.h"
#include <maya/MItSelectionList.h>


void SGCommand::mergeVertex()
{
	MString command = "polyMergeVertex  -d 0.00001 -am 1 -ch 1 ";
	MFnMesh fnMesh = m_dagPathMesh;
	MString meshName = fnMesh.partialPathName();
	char vtxName[128];
	for (unsigned int i = 0; i < m_vmMergeIndices.length(); i++) {
		sprintf(vtxName, "%s.vtx[%d] ", meshName.asChar(), m_vmMergeIndices[i]);
		command += vtxName;
	}
	MGlobal::executeCommand(command, false, true);
}

#include <SGPrintf.h>
void SGCommand::polySplit(const vector<MIntArray>& indices, const vector<MFloatArray>& params, 
	const vector<MPointArray>& points)
{
	MString nodeName = "polySplit";
	MString nodeInputName = "inputPolymesh";
	MString nodeOutputName = "output";

	MObjectArray oArr;
	for (int i = 0; i < indices.size(); i++) {
		MObject node = SGNodeControl::addNewNodeOnMesh(m_dagPathMesh, nodeName, nodeInputName, nodeOutputName);
		oArr.append(node);
	}
	
	for (int i = 0; i < indices.size(); i++) {
		MFnDependencyNode fnNode = oArr[i];
		MPlug plugEdge = fnNode.findPlug("edge");
		MPlug plugDesc = fnNode.findPlug("desc");
		MPlug plugVertices = fnNode.findPlug("vertices");

		for (unsigned int j = 0; j < indices[i].length(); j++) {
			MPlug plugEdgeElement = plugEdge.elementByLogicalIndex(j);
			MPlug plugDescElement = plugDesc.elementByLogicalIndex(j);
			plugEdgeElement.setFloat(params[i][j]);
			plugDescElement.setInt(indices[i][j]);

			if (indices[i][j] >= 0) {
				MPlug plugVerticesElement = plugVertices.elementByLogicalIndex(indices[i][j]);
				plugVerticesElement.child(0).setDouble(points[i][indices[i][j]].x);
				plugVerticesElement.child(1).setDouble(points[i][indices[i][j]].y);
				plugVerticesElement.child(2).setDouble(points[i][indices[i][j]].z);
			}
			else if (i == 1 && indices[i][j] == indices[0][j] && params[i][j] != 0) {
				plugEdgeElement.setFloat(1);
			}
		}
	}
}



void SGCommand::polySplitRing(int rootEdge, float rootWeight, MIntArray& indicesEdge)
{
	MString nodeName = "polySplitRing";
	MString nodeInputName = "inputPolymesh";
	MString nodeOutputName = "output";
	MObject node = SGNodeControl::addNewNodeOnMesh(m_dagPathMesh, nodeName, nodeInputName, nodeOutputName);

	MFnComponentListData fnComponentList; MObject componentList = fnComponentList.create();
	MFnSingleIndexedComponent singleComp; MObject component = singleComp.create(MFn::kMeshEdgeComponent);
	singleComp.addElements(indicesEdge); fnComponentList.add(component);

	MFnDependencyNode fnNode = node;
	MPlug plugComponent = fnNode.findPlug("inputComponents");
	plugComponent.setValue(componentList);
	MPlug plugRootEdge = fnNode.findPlug("rootEdge");
	plugRootEdge.setInt(rootEdge);
	MPlug plugWeight = fnNode.findPlug("weight");
	plugWeight.setFloat(rootWeight);
}

#include <maya/MFnComponentListData.h>
#include <maya/MFnSingleIndexedComponent.h>

void SGCommand::deleteComponent(MDagPath dagPath, MIntArray edgeIndices, MIntArray polyIndices)
{
	if (polyIndices.length()) {
		MString nodeName = "deleteComponent";
		MString nodeInputName = "inputGeometry";
		MString nodeOutputName = "outputGeometry";
		MObject node = SGNodeControl::addNewNodeOnMesh(m_dagPathMesh, nodeName, nodeInputName, nodeOutputName);

		MPlug plugComponents = MFnDependencyNode(node).findPlug("deleteComponents");
		
		
		MFnComponentListData compListData;
		MFnSingleIndexedComponent singleComp;

		MObject oSingleComp = singleComp.create( MFn::kMeshPolygonComponent);
		MObject oCompListData = compListData.create();

		singleComp.addElements(polyIndices);
		compListData.add(oSingleComp);
		plugComponents.setMObject(oCompListData);
	}
	else if (edgeIndices.length()) {
		MFnMesh fnMesh = dagPath;
		MString delEdgeCommand = "polyDelEdge -cv true -ch 1 ";
		for (unsigned int i = 0; i < edgeIndices.length(); i++) {
			MString addString = fnMesh.partialPathName();
			char buffer[128];
			sprintf(buffer, ".e[%d] ", edgeIndices[i]);
			addString += buffer;
			delEdgeCommand += addString;
		}
		MGlobal::executeCommand(delEdgeCommand, false, false);
	}
}


bool SGCommand::checkMeshIsSelected()
{
	MStatus status;
	MSelectionList selectionList;
	MGlobal::getActiveSelectionList(selectionList);
	if (!selectionList.length()) return false;

	MItSelectionList itList(selectionList);
	MDagPath pathNode;
	unsigned int numShapes;

	bool pathExists = false;
	for (; !itList.isDone(); itList.next())
	{
		status = itList.getDagPath(pathNode);
		if (pathNode.node().hasFn(MFn::kMesh))
		{
			MFnDagNode fnDag(pathNode);
			if (!fnDag.isIntermediateObject())
			{
				pathExists = true;
			}
		}
		if (pathExists) break;
		CHECK_MSTATUS_AND_RETURN_IT(status);
		numShapes = pathNode.childCount();
		for (unsigned int i = 0; i < numShapes; ++i)
		{
			status = pathNode.push(pathNode.child(i));
			CHECK_MSTATUS_AND_RETURN_IT(status);

			if (pathNode.node().hasFn(MFn::kMesh))
			{
				MFnDagNode fnDag(pathNode);
				if (!fnDag.isIntermediateObject())
				{
					pathExists = true;
					break;
				}
			}
			pathNode.pop();
		}
		if (pathExists) break;
	}

	if (pathExists) return true;

	return false;
}