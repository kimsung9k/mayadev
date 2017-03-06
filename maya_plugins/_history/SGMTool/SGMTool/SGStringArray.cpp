#include "SGStringArray.h"


SGStringArray::SGStringArray()
{
	m_ptrArray = new string[0];
	m_length = 0;
}


SGStringArray::SGStringArray(const SGStringArray& other)
{
	this->setLength(other.length());
	for (unsigned int i = 0; i < m_length; i++)
		m_ptrArray[i] = other.m_ptrArray[i];
}

SGStringArray::~SGStringArray()
{
	delete[] m_ptrArray;
}


void SGStringArray::setLength(unsigned int length)
{
	string* ptrNewArray = new string[length];

	unsigned int shortLength = m_length < length ? m_length : length;

	for (unsigned int i = 0; i < shortLength; i++)
		ptrNewArray[i] = m_ptrArray[i];

	m_length = length;

	delete[] m_ptrArray;
	m_ptrArray = ptrNewArray;
}


unsigned int SGStringArray::length() const
{
	return m_length;
}


void SGStringArray::append(string element)
{
	string* ptrNewArray = new string[m_length + 1];

	for (unsigned int i = 0; i < m_length; i++)
		ptrNewArray[i] = m_ptrArray[i];

	ptrNewArray[m_length] = element;
	m_length += 1;

	delete[] m_ptrArray;
	m_ptrArray = ptrNewArray;
}


int SGStringArray::index(string element)
{
	for (unsigned int i = 0; i < m_length; i++)
	{
		if (m_ptrArray[i] == element)
			return i;
	}
}


string& SGStringArray::operator[](unsigned int index)
{
	return m_ptrArray[index];
}


string& SGStringArray::operator[](unsigned int index) const
{
	return m_ptrArray[index];
}


SGStringArray& SGStringArray::operator=(const SGStringArray& other)
{
	delete[] this->m_ptrArray;
	this->m_ptrArray = new string[other.m_length];

	for (unsigned int i = 0; i < other.m_length; i++)
	{
		this->m_ptrArray[i] = other.m_ptrArray[i];
	}
	this->m_length = other.m_length;
	return *this;
}



void SGStringArray::clear()
{
	delete[] m_ptrArray;
	m_ptrArray = new string[0];
	m_length = 0;
}