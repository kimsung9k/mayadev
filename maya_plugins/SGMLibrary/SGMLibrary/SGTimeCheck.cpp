#include "precompile.h"
#include "SGTimeCheck.h"
#include "SGPrintf.h"

void SGTimeCheck::start() {
	ftime(&m_start);
}


float SGTimeCheck::getInterval() {
	ftime(&m_end);

	int left, right;
	float interval;
	left = (int)(m_end.time - m_start.time);
	right = (int)(m_end.millitm - m_start.millitm);
	interval = (float)(left * 1000 + right) / 1000;
	return interval;
}


void SGTimeCheck::finish(MString frontName) {
	sgPrintf("%s : %f", frontName.asChar(), getInterval() );
}