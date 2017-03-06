#include "SGIntArray.h"


SGIntArray::SGIntArray() {
	m_ptr = new unsigned int[0];
	m_length = 0;
}


SGIntArray::~SGIntArray() {
	delete[] m_ptr;
}


void SGIntArray::setLength(int length) {
	delete[] m_ptr;
	m_ptr = new unsigned int[length];
	m_length = length;
}


unsigned int& SGIntArray::operator[](int index) {
	return m_ptr[index];
}


unsigned int& SGIntArray::operator[](int index) const {
	return m_ptr[index];
}


int  SGIntArray::length() {
	return m_length;
}

unsigned int* SGIntArray::getPointer() const{
	return m_ptr;
}