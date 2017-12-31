#include "sgMeshInfo.h"
#include "sgPrintf.h"


sgMeshInfo::sgMeshInfo()
{
	memPtr_intersector = new MMeshIntersector();
}


sgMeshInfo::sgMeshInfo( MObject oMesh, MMatrix mtxMesh )
{
	mem_oMesh = oMesh;
	mem_mtxMesh = mtxMesh;
	mem_mtxMeshInv = mem_mtxMesh.inverse();

	memPtr_intersector = new MMeshIntersector();
	memPtr_intersector->create(mem_oMesh);
}


sgMeshInfo::~sgMeshInfo()
{
	delete memPtr_intersector;
}



void sgMeshInfo::setMesh(MObject oMesh)
{
	mem_oMesh = oMesh;

	delete memPtr_intersector;
	memPtr_intersector = new MMeshIntersector();
	memPtr_intersector->create(mem_oMesh);
}


void sgMeshInfo::setMatrix(MObject oMatrix)
{
	MFnMatrixData mtxData( oMatrix );
	mem_mtxMesh = mtxData.matrix();
	mem_mtxMeshInv = mem_mtxMesh.inverse();
}


void sgMeshInfo::setMatrix(MMatrix mtxMesh)
{
	mem_mtxMesh = mtxMesh;
	mem_mtxMeshInv = mem_mtxMesh.inverse();
}


MBoundingBox sgMeshInfo::getLocalBoundingBox() const
{
	return MFnMesh(mem_oMesh).boundingBox();
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
	for (unsigned int i = 0; i < 8; i++) worldBoundingBox.expand(eightPoints[i] * mem_mtxMesh);

	return worldBoundingBox;
}



unsigned int sgMeshInfo::numVertice()
{
	MFnMesh fnMesh(mem_oMesh);
	return fnMesh.numVertices();
}



MMatrix sgMeshInfo::matrix() const
{
	return mem_mtxMesh;
}



MPoint sgMeshInfo::getClosestPoint( const MPoint& targetPoint) const
{
	MStatus status;

	MPointOnMesh pointOnMesh;
	memPtr_intersector->getClosestPoint( targetPoint, pointOnMesh );

	return MPoint(pointOnMesh.getPoint());
}


void sgMeshInfo::getNormals(MFloatVectorArray& normals)
{
	MFnMesh fnMesh(mem_oMesh);
	fnMesh.getVertexNormals(false, normals);
}


void sgMeshInfo::getPoints(MPointArray& points)
{
	MFnMesh fnMesh(mem_oMesh);
	fnMesh.getPoints(points);
}


void sgMeshInfo::setBulge(double bulgeRadius, MSpace::Space space)
{
	MMatrix mtxToWorld;
	MMatrix mtxToLocal;

	if (space == MSpace::kWorld)
	{
		mtxToWorld = matrix();
		mtxToLocal = mtxToWorld.inverse();
	}

	MPointArray pointsOrig;
	MFloatVectorArray normals;
	MPointArray pointsResult;

	getPoints( pointsOrig );
	getNormals( normals );
	pointsResult.setLength(pointsOrig.length());

	for( unsigned int i = 0; i < numVertice(); i++ )
	{
		MVector bulgeVector = (MVector(normals[i]) * mem_mtxMesh * bulgeRadius) * mtxToLocal;
		pointsResult[i] = pointsOrig[i] + bulgeVector;
	}
	MFnMesh fnMesh(mem_oMesh);
	fnMesh.setPoints(pointsResult);
}