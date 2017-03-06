#include "SGVec3Array.h"


SGVec3Array::SGVec3Array() {
	m_ptr = new float[0];
	m_length = 0;
}


SGVec3Array::~SGVec3Array() {
	delete[] m_ptr;
}


void SGVec3Array::setLength(int length) {
	delete[] m_ptr;
	m_ptr = new float[length*3];
	m_length = length;
}


SGVec3 SGVec3Array::get(int index) const{
	int startIndex = index * 3;
	return SGVec3(m_ptr[startIndex], m_ptr[startIndex + 1], m_ptr[startIndex + 2]);
}


void SGVec3Array::set( int index, const SGVec3& element ){
	int startIndex = index * 3;
	m_ptr[startIndex] = element.x;
	m_ptr[startIndex+1] = element.y;
	m_ptr[startIndex+2] = element.z;
}


int  SGVec3Array::length() {
	return m_length;
}

float* SGVec3Array::getPointer() const {
	return m_ptr;
}