#pragma once

#include "SGVec3.h"

class SGVec3Array
{
public:
	SGVec3Array();
	~SGVec3Array();

	int  length();
	void setLength( int length );
	SGVec3 get(int index) const;
	void   set(int index, const SGVec3& element );

	float* getPointer() const;

private:
	int    m_length;
	float* m_ptr;
};