#include "precompile.h"
#include "SGShape.h"


SGConeShape::SGConeShape()
{
	shape.numPoints = 10;
	shape.numPoly = 16;
	shape.interval = 3;
	shape.points = new float[shape.numPoints*3];
	shape.indices = new unsigned int[shape.numPoly * shape.interval];

	float conePoints[] = {
		0.212132f, 0.000000f, -0.212132f,
		0.000000f, 0.000000f, -0.300000f,
		-0.212132f, 0.000000f, -0.212132f,
		-0.300000f, 0.000000f, 0.000000f,
		-0.212132f, 0.000000f, 0.212132f,
		0.000000f, 0.000000f, 0.300000f,
		0.212132f, 0.000000f, 0.212132f,
		0.300000f, 0.000000f, 0.000000f,
		0.000000f, 0.000000f, 0.000000f,
		0.000000f, 1.000000f, 0.000000f };

	for (int i = 0; i < shape.numPoints*3; i++)
		shape.points[i] = conePoints[i];

	unsigned int coneIndices[48] = {
		1, 0, 8, 2, 1, 8, 3, 2, 8,
		4, 3, 8, 5, 4, 8, 6, 5, 8,
		7, 6, 8, 0, 7, 8, 0, 1, 9,
		1, 2, 9, 2, 3, 9, 3, 4, 9,
		4, 5, 9, 5, 6, 9, 6, 7, 9,
		7, 0, 9
	};

	for (int i = 0; i < shape.numPoly * shape.interval; i++)
		shape.indices[i] = coneIndices[i];

	coneDirection = MVector(0, 1, 0);
}

SGConeShape::~SGConeShape()
{
	delete[] shape.points;
	delete[] shape.indices;
}