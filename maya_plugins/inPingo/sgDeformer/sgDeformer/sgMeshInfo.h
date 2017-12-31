#pragma once

#include <maya/MMatrix.h>
#include <maya/MFloatMatrix.h>
#include <maya/MObject.h>
#include <maya/MFnMesh.h>
#include <maya/MBoundingBox.h>
#include <maya/MPointArray.h>
#include <maya/MFnMatrixData.h>
#include <maya/MMeshIntersector.h>
#include <maya/MFloatPointArray.h>
#include <maya/MFloatArray.h>
#include <maya/MFloatVectorArray.h>
#include <maya/MMatrixArray.h>

class sgMeshInfo
{
public:
	sgMeshInfo();
	sgMeshInfo( MObject oMesh, MMatrix mtxMesh );
	~sgMeshInfo();

	void setMesh(MObject oMesh);
	void setMatrix(MObject oMatrix);
	void setMatrix(MMatrix mtxMesh);
	MBoundingBox getLocalBoundingBox() const;
	MBoundingBox getWorldBoundingBox() const;
	MPoint getClosestPoint( const MPoint& targetPoint) const;
	MMatrix matrix() const;
	void getNormals(MFloatVectorArray& normals );
	void getPoints( MPointArray& points );
	void setBulge(double bulgeRadius, MSpace::Space space = MSpace::kObject );

	unsigned int numVertice();

	MObject mem_oMesh;
	MMatrix mem_mtxMesh;
	MMatrix mem_mtxMeshInv;
	MMeshIntersector* memPtr_intersector;
};