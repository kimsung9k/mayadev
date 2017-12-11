#pragma once

#include <maya/MMatrix.h>
#include <maya/MObject.h>
#include <maya/MFnMesh.h>
#include <maya/MBoundingBox.h>
#include <maya/MPointArray.h>
#include <maya/MFnMatrixData.h>


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

	unsigned int numVertice();

private:
	MObject prv_oMesh;
	MMatrix prv_mtxMesh;
};