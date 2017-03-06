#pragma once

class SGIntPtrArray
{
public:
	SGIntPtrArray();
	SGIntPtrArray(const SGIntPtrArray&);
	~SGIntPtrArray();

	void setLength(unsigned int length);
	unsigned int  length() const;
	void append(int* element, unsigned int elementLength);
	int* operator[](unsigned int index);
	int* operator[](unsigned int index) const;

private:
	int** m_ptrArrayPtr;
	unsigned int m_length;
	unsigned int* m_ptrEachLength;
};