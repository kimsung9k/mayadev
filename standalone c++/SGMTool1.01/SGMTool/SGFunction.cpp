#include "SGFunction.h"


template <typename T>
int SGFnc::deletePointers(T data, int numPtrs)
{
	for (int i = 0; i < numPtrs; i++)
	{
		delete data[i];
	}
	return 0;
}