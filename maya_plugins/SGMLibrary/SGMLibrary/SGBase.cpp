#include "precompile.h"

#include "SGBase.h"


void SGExecuteCommand(bool undoable, const char *message, ...)
{
	size_t size = 500;
	char * result = (char*)malloc(size);
	if (!result) return; // error handling!
	while (1) {
		va_list ap;
		va_start(ap, message);
		size_t used = vsnprintf(result, size, message, ap);
		va_end(ap);
		char * newptr = (char*)realloc(result, size);
		if (!newptr) { // error
			free(result);
			return;
		}
		result = newptr;
		if (used <= size) break;
		size = used;
	}
	MGlobal::executeCommand(result, false, undoable );
	delete result;
}



MIntArray SGBase::isolateVtxMap;
MIntArray SGBase::isolatePolyMap;

void SGBase::getIsolateMap(const MDagPath& dagPath) {

	isolateVtxMap.clear();
	isolatePolyMap.clear();

	MFnMesh fnMesh = dagPath;
	int numVertices = fnMesh.numVertices();

	MStringArray results;
	MGlobal::executeCommand("getPanel -wf", results);
	if (!results.length()) return;

	MString nodeName;
	MString getSetCommand = "isolateSelect -q -viewObjects ";
	getSetCommand += results[0];
	MGlobal::executeCommand(getSetCommand, nodeName);

	if (!nodeName.length()) return;

	MSelectionList selList, selListGet;
	selList.add(nodeName);
	MObject oSet;
	selList.getDependNode(0, oSet);

	MFnSet fnSet(oSet);
	fnSet.getMembers(selListGet, false);

	MDagPath isolateDagPath;
	MObject  oComponent;
	selListGet.getDagPath(0, isolateDagPath, oComponent);

	if (oComponent.isNull()) {
		isolateVtxMap.setLength(fnMesh.numVertices());
		isolatePolyMap.setLength(fnMesh.numPolygons());
		for (unsigned int i = 0; i < isolateVtxMap.length(); i++)
			isolateVtxMap[i] = 1;
		for (unsigned int i = 0; i < isolatePolyMap.length(); i++)
			isolatePolyMap[i] = 1;
	}
	else {
		MFnSingleIndexedComponent singleComp(oComponent);
		MIntArray elements;
		singleComp.getElements(elements);

		MIntArray vtxList;
		isolateVtxMap.setLength(fnMesh.numVertices());
		isolatePolyMap.setLength(fnMesh.numPolygons());
		for (unsigned int i = 0; i < isolateVtxMap.length(); i++)
			isolateVtxMap[i] = 0;
		for (unsigned int i = 0; i < isolatePolyMap.length(); i++)
			isolatePolyMap[i] = 0;

		for (unsigned int i = 0; i < elements.length(); i++) {
			fnMesh.getPolygonVertices(elements[i], vtxList);
			isolatePolyMap[elements[i]] = 1;
			for (unsigned int j = 0; j < vtxList.length(); j++)
				isolateVtxMap[vtxList[j]] = 1;
		}
	}
}