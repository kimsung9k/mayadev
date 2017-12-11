#include "SGPrintf.h"
#include <Windows.h>

void sgPrintf(const char *message, ...) {
	size_t size = 500;
	char * result = (char*)malloc(size);
	if (!result) return; // error handling!
	while (1) {
		va_list ap;
		va_start(ap, message);
		size_t used = vsnprintf(result, size, message, ap);
		va_end(ap);
		char * newptr = (char*)realloc(result, size);
		if (!newptr) { // error
			free(result);
			return;
		}
		result = newptr;
		if (used <= size) break;
		size = used;
	}
	OutputDebugString(result);
	MGlobal::displayInfo(result);
	delete result;
}