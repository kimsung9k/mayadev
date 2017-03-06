#pragma once

#include "SGDagNodeMesh.h"
#include "SGMatrix.h"
#include "SGVectorArray.h"


class SGSelectInView
{
public:
	SGVectorArray getBoundingBoxPoints(const SGDagNodeMesh&);
};