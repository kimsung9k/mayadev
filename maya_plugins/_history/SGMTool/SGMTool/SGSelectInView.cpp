#include "SGSelectInView.h"



SGVectorArray SGSelectInView::getBoundingBoxPoints( const SGDagNodeMesh& dataMesh )
{
	SGVectorArray bb;
	bb.setLength(2);
	bb[0] = dataMesh.m_boundingBoxMin;
	bb[1] = dataMesh.m_boundingBoxMax;

	SGVectorArray points;
	points.setLength(8);

	double x, y, z;
	int cuIndex = 0;

	for (int i = 0; i < 2; i++)
	{
		x = bb[i].x;
		for (int j = 0; j < 2; j++)
		{
			y = bb[i].y;
			for (int k = 0; k < 2; k++)
			{
				z = bb[i].z;
				points[cuIndex] = SGVector(x, y, z)*SGMatrix(&dataMesh.m_matrix[0]);
				cuIndex++;
			}
		}
	}
	return points;
}