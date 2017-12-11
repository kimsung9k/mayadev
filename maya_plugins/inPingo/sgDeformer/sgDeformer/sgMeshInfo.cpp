#include "sgMeshInfo.h"
#include "sgPrintf.h"


sgMeshInfo::sgMeshInfo()
{

}


sgMeshInfo::sgMeshInfo( MObject oMesh, MMatrix mtxMesh )
{
	prv_oMesh = oMesh;
	prv_mtxMesh = mtxMesh;
}


sgMeshInfo::~sgMeshInfo()
{
}



void sgMeshInfo::setMesh(MObject oMesh)
{
	prv_oMesh = oMesh;
}


void sgMeshInfo::setMatrix(MObject oMatrix)
{
	MFnMatrixData mtxData( oMatrix );
	prv_mtxMesh = mtxData.matrix();
}


void sgMeshInfo::setMatrix(MMatrix mtxMesh)
{
	prv_mtxMesh = mtxMesh;
}


MBoundingBox sgMeshInfo::getLocalBoundingBox() const
{
	return MFnMesh(prv_oMesh).boundingBox();
}


MBoundingBox sgMeshInfo::getWorldBoundingBox() const
{
	MBoundingBox localBoundingBox = getLocalBoundingBox();

	MPoint bb_min = localBoundingBox.min();
	MPoint bb_max = localBoundingBox.max();

	MPointArray eightPoints; eightPoints.setLength(8);
	eightPoints[0] = bb_min;
	eightPoints[1].x = bb_max.x; eightPoints[1].y = bb_min.y; eightPoints[1].z = bb_min.z;
	eightPoints[2].x = bb_max.x; eightPoints[2].y = bb_max.y; eightPoints[2].z = bb_min.z;
	eightPoints[3].x = bb_max.x; eightPoints[3].y = bb_min.y; eightPoints[3].z = bb_max.z;
	eightPoints[4].x = bb_min.x; eightPoints[4].y = bb_max.y; eightPoints[4].z = bb_max.z;
	eightPoints[5].x = bb_min.x; eightPoints[5].y = bb_max.y; eightPoints[5].z = bb_min.z;
	eightPoints[6].x = bb_min.x; eightPoints[6].y = bb_min.y; eightPoints[6].z = bb_max.z;
	eightPoints[7] = bb_max;

	MBoundingBox worldBoundingBox;
	worldBoundingBox.clear();
	for (unsigned int i = 0; i < 8; i++) worldBoundingBox.expand(eightPoints[i] * prv_mtxMesh);

	return worldBoundingBox;
}



unsigned int sgMeshInfo::numVertice()
{
	MFnMesh fnMesh(prv_oMesh);
	return fnMesh.numVertices();
}