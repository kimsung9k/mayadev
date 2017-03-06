#pragma once

#include "SGBase.h"
#include <maya/MString.h>
#include <sys/timeb.h> // timeb 구조체를 사용하기 위해 반드시 include!!

class SGTimeCheck {
public:
	void start();
	float getInterval();

	void finish(MString frontName);
	struct timeb m_start, m_end;
};