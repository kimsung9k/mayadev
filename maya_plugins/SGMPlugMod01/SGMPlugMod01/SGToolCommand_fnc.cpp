#include "precompile.h"

#include "SGToolCommand.h"
#include <maya/MPlug.h>
#include <maya/MPlugArray.h>
#include <maya/MFnComponentListData.h>
#include <maya/MFnSingleIndexedComponent.h>


void SGToolCommand::mergeVertex()
{
	MString command = "polyMergeVertex  -d 0.00001 -am 1 -ch 1 ";
	MFnMesh fnMesh = m_dagPathMesh;
	MString meshName = fnMesh.fullPathName();
	char vtxName[128];
	for (unsigned int i = 0; i < m_vmMergeIndices.length(); i++) {
		sprintf(vtxName, "%s.vtx[%d] ", meshName.asChar(), m_vmMergeIndices[i]);
		command += vtxName;
	}
	MGlobal::executeCommand(command);
}


bool SGToolCommand::setPntsZero(MPlug plugPnts, MIntArray& indices, MPointArray& pnts)
{
	int numElements = plugPnts.numElements();
	for (int i = 0; i < numElements; i++) {
		MPlug plugPntx = plugPnts[i].child(0);
		MPlug plugPnty = plugPnts[i].child(1);
		MPlug plugPntz = plugPnts[i].child(2);
		MVector point(plugPntx.asDouble(), plugPnty.asDouble(), plugPntz.asDouble());
		plugPntx.setDouble(0);
		plugPnty.setDouble(0);
		plugPntz.setDouble(0);
		if (point.length() == 0) continue;
		indices.append(plugPnts[i].logicalIndex());
		pnts.append(point);
	}
	if (indices.length()) return true;
	return false;
}


MPlug SGToolCommand::getCurrentMeshOutputConnection(MObject oMesh)
{
	MDGModifier dgmode;

	MFnMesh fnMesh = oMesh;
	MObject oParent = fnMesh.parent(0);
	MPlug plugInMesh = fnMesh.findPlug("inMesh");

	MPlugArray connections;
	plugInMesh.connectedTo(connections, true, false);

	MIntArray indices;
	MPointArray pnts;
	MPlug plugPnts = fnMesh.findPlug("pnts");
	bool pntsResult = setPntsZero(plugPnts, indices, pnts);

	if (!connections.length()) {
		MFnMesh copyMesh = fnMesh.copy(oMesh, oParent);
		MPlug outMeshPlug = copyMesh.findPlug("outMesh");
		dgmode.connect(outMeshPlug, plugInMesh);
		dgmode.doIt();

		MPlug plugIo = copyMesh.findPlug("io");
		plugIo.setBool(true);
	}

	plugInMesh.connectedTo(connections, true, false);

	if (pntsResult)
	{
		MObject oTweakNode = dgmode.createNode("polyTweak");
		dgmode.doIt();
		MFnDependencyNode fnTweakNode = oTweakNode;
		MPlug plugTweak = fnTweakNode.findPlug("tweak");

		for (unsigned int i = 0; i < indices.length(); i++)
		{
			//sgPrintf("tweak index : %d", indices[i]);
			MPlug plugTweakElement = plugTweak.elementByLogicalIndex(indices[i]);
			MPlug plugX = plugTweakElement.child(0);
			MPlug plugY = plugTweakElement.child(1);
			MPlug plugZ = plugTweakElement.child(2);
			plugX.setDouble(pnts[i].x);
			plugY.setDouble(pnts[i].y);
			plugZ.setDouble(pnts[i].z);
		}
		MPlug plugInputMesh = fnTweakNode.findPlug("inputPolymesh");
		MPlug plugOutput = fnTweakNode.findPlug("output");
		dgmode.connect(connections[0], plugInputMesh);
		dgmode.doIt();
		dgmode.disconnect(connections[0], plugInMesh);
		dgmode.connect(plugOutput, plugInMesh);
		dgmode.doIt();
		return plugOutput;
	}
	return connections[0];
}



MObject SGToolCommand::addNewNodeOnMesh(MObject oMesh, MString nodeType, MString nodeInputName, MString nodeOutputName)
{
	MFnMesh fnMesh = oMesh;

	MString nodeName = nodeType;
	MDGModifier mode;
	MObject node = mode.createNode(nodeName);
	mode.doIt();

	MFnDependencyNode fnNode = node;

	MPlug plugInMesh = fnMesh.findPlug("inMesh");
	MPlug plugOutput = SGToolCommand::getCurrentMeshOutputConnection(oMesh);

	MPlug plugInputPolyMesh = fnNode.findPlug(nodeInputName);
	mode.connect(plugOutput, plugInputPolyMesh);
	mode.doIt();

	MPlug plugNodeOutput = fnNode.findPlug(nodeOutputName);
	mode.disconnect(plugOutput, plugInMesh);
	mode.connect(plugNodeOutput, plugInMesh);
	mode.doIt();
	return node;
}


void SGToolCommand::polySplit(const MIntArray& edgeIndices, const MFloatArray& edgeParams)
{
	MString nodeName = "polySplit";
	MString nodeInputName = "inputPolymesh";
	MString nodeOutputName = "output";
	MObject node = SGToolCommand::addNewNodeOnMesh(m_dagPathMesh.node(), nodeName, nodeInputName, nodeOutputName);

	MFnDependencyNode fnNode = node;
	MPlug plugEdge = fnNode.findPlug("edge");
	MPlug plugDesc = fnNode.findPlug("desc");
	for (int j = 0; j < 2; j++)
	{
		MPlug plugEdgeElement = plugEdge.elementByLogicalIndex(edgeIndices[j]);
		MPlug plugDescElement = plugDesc.elementByLogicalIndex(edgeIndices[j]);
		plugEdgeElement.setFloat(edgeParams[j]);
		plugDescElement.setInt(edgeIndices[j] - 0x80000000);
	}

	if (edgeIndices.length() == 4) {
		MObject nodeMirror = SGToolCommand::addNewNodeOnMesh(m_dagPathMesh.node(), nodeName, nodeInputName, nodeOutputName);
		MFnDependencyNode fnNode = nodeMirror;
		MPlug plugEdge = fnNode.findPlug("edge");
		MPlug plugDesc = fnNode.findPlug("desc");
		for (int j = 0; j < 2; j++)
		{
			MPlug plugEdgeElement = plugEdge.elementByLogicalIndex(edgeIndices[j]);
			MPlug plugDescElement = plugDesc.elementByLogicalIndex(edgeIndices[j]);
			plugEdgeElement.setFloat(edgeParams[j+2]);
			plugDescElement.setInt(edgeIndices[j + 2] - 0x80000000);
		}
	}
}



void SGToolCommand::polySplitRing(int rootEdge, float rootWeight, MIntArray& indicesEdge)
{
	MString nodeName = "polySplitRing";
	MString nodeInputName = "inputPolymesh";
	MString nodeOutputName = "output";
	MObject node = addNewNodeOnMesh(m_dagPathMesh.node(), nodeName, nodeInputName, nodeOutputName);

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


MStatus SGToolCommand::deleteBeforeNode(MDagPath dagPath, MString nodeName, MString inputName) {
	MFnMesh fnMesh = dagPath;
	MPlug plugInMesh = fnMesh.findPlug("inMesh");
	MPlugArray connections;
	MStringArray deleteTargets;

	plugInMesh.connectedTo(connections, true, false);
	MFnDependencyNode fnNode = connections[0].node();
	if (fnNode.typeName() != nodeName)
		return MS::kSuccess;
	else {
		deleteTargets.append(fnNode.name());

		MPlug plugInputGeo = fnNode.findPlug(inputName);
		plugInputGeo.connectedTo(connections, true, false);

		MIntArray indices;
		MPointArray points;
		if (connections.length()) {
			fnNode.setObject(connections[0].node());
			if (fnNode.typeName() == "polyTweak") {
				deleteTargets.append(fnNode.name());
				MPlug plugTweak = fnNode.findPlug("tweak");
				for (unsigned int i = 0; i < plugTweak.numElements(); i++) {
					int logicalIndex = plugTweak[i].logicalIndex();
					indices.append(logicalIndex);
					MPlug plugX = plugTweak[i].child(0);
					MPlug plugY = plugTweak[i].child(1);
					MPlug plugZ = plugTweak[i].child(2);
					MPoint point(plugX.asDouble(), plugY.asDouble(), plugZ.asDouble());
					points.append(point);
				}
			}
		}

		for (int i = 0; i < (int)deleteTargets.length(); i++) {
			char buffer[128];
			sprintf(buffer, "delete %s", deleteTargets[i].asChar());
			MGlobal::executeCommand(buffer);
		}
		if (points.length()) {
			MPlug plugPnts = fnMesh.findPlug("pnts");
			for (unsigned int i = 0; i < indices.length(); i++) {
				MPlug plugPntsElement = plugPnts.elementByLogicalIndex(indices[i]);
				MPlug plugX = plugPntsElement.child(0);
				MPlug plugY = plugPntsElement.child(1);
				MPlug plugZ = plugPntsElement.child(2);
				plugX.setDouble(points[i].x);
				plugY.setDouble(points[i].y);
				plugZ.setDouble(points[i].z);
			}
		}
	}
	return MS::kSuccess;
}


void SGToolCommand::deleteComponent(MDagPath dagPath, MIntArray edgeIndices, MIntArray polyIndices)
{
	MFnMesh fnMesh = dagPath;

	if (edgeIndices.length()) {
		MString delEdgeCommand = "polyDelEdge -cv true -ch 1 ";
		for (unsigned int i = 0; i < edgeIndices.length(); i++) {
			MString addString = fnMesh.fullPathName();
			char buffer[128];
			sprintf(buffer, ".e[%d] ", edgeIndices[i]);
			addString += buffer;
			delEdgeCommand += addString;
		}
		MGlobal::executeCommand(delEdgeCommand, false, false);
	}

	if (polyIndices.length()) {
		MString delPolyCommand = "delete ";
		for (unsigned int i = 0; i < polyIndices.length(); i++) {
			MString addString = fnMesh.fullPathName();
			char buffer[128];
			sprintf(buffer, ".f[%d] ", polyIndices[i]);
			addString += buffer;
			delPolyCommand += addString;
		}
		MGlobal::executeCommand(delPolyCommand, false, false);
	}
}