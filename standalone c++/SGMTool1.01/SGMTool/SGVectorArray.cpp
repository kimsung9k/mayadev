#include "SGVector.h"
#include "SGVectorArray.h"


SGVectorArray::SGVectorArray()
{
	m_ptrArray = new SGVector[0];
	m_length = 0;
}


SGVectorArray::SGVectorArray(const SGVectorArray& other)
{
	this->setLength(other.length());
	for ( unsigned int i = 0; i < m_length; i++)
		m_ptrArray[i] = other.m_ptrArray[i];
}

SGVectorArray::~SGVectorArray()
{
	delete[] m_ptrArray;
}


void SGVectorArray::setLength(unsigned int length)
{
	SGVector* ptrNewArray = new SGVector[length];

	unsigned int shortLength = m_length < length ? m_length : length;

	for ( unsigned int i = 0; i < shortLength; i++)
		ptrNewArray[i] = m_ptrArray[i];

	m_length = length;

	delete[] m_ptrArray;
	m_ptrArray = ptrNewArray;
}


unsigned int SGVectorArray::length() const
{
	return m_length;
}


void SGVectorArray::append(SGVector element)
{
	SGVector* ptrNewArray = new SGVector[m_length + 1];

	for ( unsigned int i = 0; i < m_length; i++)
		ptrNewArray[i] = m_ptrArray[i];

	ptrNewArray[m_length] = element;
	m_length += 1;

	delete[] m_ptrArray;
	m_ptrArray = ptrNewArray;
}


SGVector& SGVectorArray::operator[](unsigned int index)
{
	return m_ptrArray[index];
}


SGVector& SGVectorArray::operator[](unsigned int index) const
{
	return m_ptrArray[index];
}