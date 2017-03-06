#ifndef matrixFromPolygon_def_h
#define matrixFromPolygon_def_h

#include <maya/MPoint.h>
#include <maya/MVector.h>

void  getMatrixByPoints( MMatrix& targetMatrix, int polygonIndex, double u, double v, MObject meshObject )
{
	MItMeshPolygon itMesh( meshObject );

	int dumyIndex;
	itMesh.setIndex( polygonIndex, dumyIndex );

	MPointArray polyIndies;

	itMesh.getPoints( polyIndies );

	MPoint zPoint = polyIndies[0];
	MPoint cPoint = polyIndies[1];
	MPoint yPoint = polyIndies[2];

	MVector zVector = zPoint - cPoint;
	MVector yVector = yPoint - cPoint;
	MVector xVector = yVector^zVector;

	double zLength = zVector.length();
	double yLength = yVector.length();

	xVector.normalize();
	xVector *= ( zLength + yLength )/2.0;

	MVector uPos = yVector*u;
	MVector vPos = zVector*v;

	cPoint += uPos + vPos;

	double buildMatrix[4][4] = { xVector.x, xVector.y, xVector.z, 0,
		                         yVector.x, yVector.y, yVector.z, 0,
								 zVector.x, zVector.y, zVector.z, 0,
								 cPoint.x,  cPoint.y,  cPoint.z,  1 };
	
	targetMatrix = MMatrix( buildMatrix );
}

#endif