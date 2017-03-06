#include "SGIntPtrArray.h"


SGIntPtrArray::SGIntPtrArray()
{
	m_ptrArrayPtr = new int*[0];
	m_ptrEachLength = new unsigned int[0];
	m_length = 0;
}


SGIntPtrArray::SGIntPtrArray(const SGIntPtrArray& other)
{
	this->setLength(other.length());
	for (unsigned int i = 0; i < m_length; i++)
	{
		m_ptrEachLength[i] = other.m_ptrEachLength[i];
		delete[] m_ptrArrayPtr[i];
		m_ptrArrayPtr[i] = new int[m_ptrEachLength[i]];
		for (unsigned int j = 0; j < m_ptrEachLength[i]; j++)
		{
			m_ptrArrayPtr[i][j] = other.m_ptrArrayPtr[i][j];
		}
	}
}

SGIntPtrArray::~SGIntPtrArray()
{
	for (unsigned int i = 0; i < m_length; i++)
	{
		delete[] m_ptrArrayPtr[i];
	}
	delete[] m_ptrArrayPtr;
	delete[] m_ptrEachLength;
}


void SGIntPtrArray::setLength(unsigned int length)
{
	int** ptrNewArrayPtr = new int*[length];
	unsigned int*  ptrNewEachLength = new unsigned  int[length];

	unsigned int shortLength = m_length < length ? m_length : length;

	for (unsigned int i = 0; i < shortLength; i++)
	{
		ptrNewArrayPtr[i] = m_ptrArrayPtr[i];
		ptrNewEachLength[i] = m_ptrEachLength[i];
	}
	for (unsigned int i = shortLength; i < length; i++)
	{
		ptrNewArrayPtr[i] = new int[0];
		ptrNewEachLength[i] = 0;
	}

	delete[] m_ptrArrayPtr;
	delete[] m_ptrEachLength;

	m_ptrArrayPtr   = ptrNewArrayPtr;
	m_ptrEachLength = ptrNewEachLength;
	m_length = length;
}


unsigned int SGIntPtrArray::length() const
{
	return m_length;
}


void SGIntPtrArray::append(int* elementPtr, unsigned int elementLength)
{
	int** ptrNewArrayPtr = new int*[m_length+1];
	unsigned int*  ptrNewEachLength = new unsigned  int[m_length + 1];

	for (unsigned int i = 0; i < m_length; i++)
	{
		ptrNewArrayPtr[i] = m_ptrArrayPtr[i];
		ptrNewEachLength[i] = m_ptrEachLength[i];
	}
	ptrNewArrayPtr[m_length]   = elementPtr;
	ptrNewEachLength[m_length] = elementLength;
	
	delete[] m_ptrArrayPtr;
	delete[] m_ptrEachLength;

	m_ptrArrayPtr = ptrNewArrayPtr;
	m_ptrEachLength = ptrNewEachLength;
	m_length += 1;
}


int* SGIntPtrArray::operator[](unsigned int index)
{
	return m_ptrArrayPtr[index];
}


int* SGIntPtrArray::operator[](unsigned int index) const
{
	return m_ptrArrayPtr[index];
}