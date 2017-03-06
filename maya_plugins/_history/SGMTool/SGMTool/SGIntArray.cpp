#include "SGIntArray.h"
#include "stdio.h"

SGIntArray::SGIntArray()
{
	m_ptrArray = new int[0];
	m_length = 0;
}


SGIntArray::SGIntArray(const SGIntArray& other)
{
	this->setLength( other.length() );
	for ( unsigned int i = 0; i < m_length; i++)
		m_ptrArray[i] = other.m_ptrArray[i];
}

SGIntArray::~SGIntArray()
{
	delete[] m_ptrArray;
}


void SGIntArray::setLength( unsigned int length )
{
	int* ptrNewArray = new int[length];

	unsigned int shortLength = m_length < length ? m_length : length;

	for ( unsigned int i = 0; i < shortLength; i++)
		ptrNewArray[i] = m_ptrArray[i];

	m_length = length;

	delete[] m_ptrArray;
	m_ptrArray = ptrNewArray;
}


unsigned int SGIntArray::length() const
{
	return m_length;
}


void SGIntArray::append(int element)
{
	int* ptrNewArray = new int[m_length+1];

	for ( unsigned int i = 0; i < m_length; i++)
		ptrNewArray[i] = m_ptrArray[i];

	ptrNewArray[m_length] = element;
	m_length += 1;

	delete[] m_ptrArray;
	m_ptrArray = ptrNewArray;
}


int SGIntArray::index(int element)
{
	for (unsigned int i = 0; i < m_length; i++)
	{
		if (m_ptrArray[i] == element)
			return i;
	}
}


int& SGIntArray::operator[](unsigned int index)
{
	return m_ptrArray[index];
}


int& SGIntArray::operator[](unsigned int index) const
{
	return m_ptrArray[index];
}

int* SGIntArray::asIntPtr()
{
	return m_ptrArray;
}


SGIntArray& SGIntArray::operator=(const SGIntArray& other)
{
	delete[] this->m_ptrArray;
	this->m_ptrArray = new int[other.m_length];

	for ( unsigned int i = 0; i < other.m_length; i++)
	{
		this->m_ptrArray[i] = other.m_ptrArray[i];
	}
	this->m_length = other.m_length;
	return *this;
}



void SGIntArray::clear()
{
	delete[] m_ptrArray;
	m_ptrArray = new int[0];
	m_length = 0;
}