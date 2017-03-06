#include "precompile.h"
#include "SGNodeControl.h"
#include <maya/MDGModifier.h>
#include <maya/MFnMesh.h>
#include <maya/MPlugArray.h>
#include <maya/MGlobal.h>
#include "SGTimeCheck.h"
#include <maya/MSelectionList.h>
#include <maya/MDataHandle.h>



MObject SGNodeControl::getObjectFromName( MString nodeName ){
	MSelectionList selList;
	selList.add(nodeName);
	MObject oNode;
	selList.getDependNode(0, oNode);
	return oNode;
}


bool SGNodeControl::setPntsZero(MPlug plugPnts, MIntArray& indices, MPointArray& pnts)
{
	int numElements = plugPnts.numElements();
	for (int i = 0; i < numElements; i++) {
		MPlug plugPntx = plugPnts[i].child(0);
		MPlug plugPnty = plugPnts[i].child(1);
		MPlug plugPntz = plugPnts[i].child(2);

		MVector point(plugPntx.asDouble(), plugPnty.asDouble(), plugPntz.asDouble());
		if (point.x == 0 && point.y == 0 && point.z == 0) continue;
		indices.append(plugPnts[i].logicalIndex());
		pnts.append(point);
		plugPntx.setDouble(0);
		plugPnty.setDouble(0);
		plugPntz.setDouble(0);
	}
	if (indices.length()) return true;
	return false;
}




MPlug SGNodeControl::getCurrentMeshOutputConnection(MDagPath dagPath)
{
	MDGModifier dgmode;

	MFnMesh fnMesh = dagPath;
	MObject oParent = fnMesh.parent(0);
	MPlug plugInMesh = fnMesh.findPlug("inMesh");

	MPlugArray connections;
	plugInMesh.connectedTo(connections, true, false);

	MIntArray indices;
	MPointArray pnts;
	MPlug plugPnts = fnMesh.findPlug("pnts");
	bool pntsResult = setPntsZero(plugPnts, indices, pnts);

	if (!connections.length()) {
		MFnMesh copyMesh = fnMesh.copy(dagPath.node(), oParent);
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
			if (pnts[i].x == 0 && pnts[i].y == 0 && pnts[i].z == 0) continue;
			
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


MObject SGNodeControl::addNewNodeOnMesh(MDagPath dagPath, MString nodeType, MString nodeInputName, MString nodeOutputName)
{
	MFnMesh fnMesh = dagPath;

	MString nodeName = nodeType;
	MDGModifier mode;
	MObject node = mode.createNode(nodeName);
	mode.doIt();

	MFnDependencyNode fnNode = node;

	MPlug plugInMesh = fnMesh.findPlug("inMesh");
	MPlug plugOutput = SGNodeControl::getCurrentMeshOutputConnection(dagPath);

	MPlug plugInputPolyMesh = fnNode.findPlug(nodeInputName);
	mode.connect(plugOutput, plugInputPolyMesh);
	mode.doIt();

	MPlug plugNodeOutput = fnNode.findPlug(nodeOutputName);
	mode.disconnect(plugOutput, plugInMesh);
	mode.connect(plugNodeOutput, plugInMesh);
	mode.doIt();

	return node;
}


MStatus SGNodeControl::deleteBeforeNode(MDagPath dagPath, MString nodeName, MString inputName) {
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