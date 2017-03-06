#include "SGPrintf\SGPrintf.h"
#include "SGFunctions.h"
#include "SGMesh.h"


MStatus getMeshPath(MDagPath& targetPath)
{
	MStatus status;

	unsigned int numShape;
	targetPath.numberOfShapesDirectlyBelow(numShape);

	bool shapeExists = false;
	for (int i = 0; i<(int)numShape; i++)
	{
		status = targetPath.extendToShapeDirectlyBelow(i);
		CHECK_MSTATUS_AND_RETURN_IT(status);
		if (targetPath.apiType() == MFn::kMesh)
		{
			return MS::kSuccess;
		}
		targetPath.pop();
	}
	return MS::kFailure;
}


void SGFunctions::getMeshs( vector<SGMesh*>& meshs )
{
	MSelectionList selList;
	MGlobal::getActiveSelectionList(selList);

	for (int i = 0; i < (int)selList.length(); i++) {
		MObject oNode;
		selList.getDependNode(i, oNode);
		if (oNode.apiType() == MFn::kMesh ) {
			SGMesh* ptrMesh = new SGMesh;
			selList.getDagPath(i, ptrMesh->m_dagPath);
			meshs.push_back(ptrMesh);
		}
		else if (oNode.apiType() == MFn::kTransform) {
			MDagPath dagPath;
			selList.getDagPath(i, dagPath);
			if (getMeshPath(dagPath)) {
				SGMesh* ptrMesh = new SGMesh;
				selList.getDagPath(i, ptrMesh->m_dagPath);
				meshs.push_back(ptrMesh);
			}
		}
	}
	for (int i = 0; i < meshs.size(); i++) {
		meshs[i]->setFromDagPath();
	}
}


void SGFunctions::getCamera(SGCam* cam) {

	MStatus status;

	MSelectionList selList;
	MDagPath dagPath;
	selList.add("persp|perspShape");
	status = selList.getDagPath(0, cam->m_dagPath);

	MFnCamera fnCam = cam->m_dagPath;
	MPlug plugFL = fnCam.findPlug("focalLength");
	MPlug plugHFA = fnCam.findPlug("horizontalFilmAperture");

	float fl = plugFL.asFloat();
	float hfa = plugHFA.asFloat() * 25.4f;

	sgPrintf("focalLength : %5.3f", fl);
	sgPrintf("hfa : %5.3f", hfa);
}