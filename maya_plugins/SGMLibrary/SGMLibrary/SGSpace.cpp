#include "precompile.h"
#include "SGSpace.h"

#include <maya/MMatrix.h>

MSpace::Space SGSpace::space = MSpace::kWorld;


void SGSpace::setObjectSpace()
{
	space = MSpace::kObject;
}


void SGSpace::setWorldSpace()
{
	space = MSpace::kWorld;
}