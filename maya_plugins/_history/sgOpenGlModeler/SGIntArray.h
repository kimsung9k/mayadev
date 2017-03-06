#pragma once

class SGIntArray
{
public:
	SGIntArray();
	~SGIntArray();

	int  length();
	void setLength(int length);
	unsigned int& operator[](int index);
	unsigned int& operator[](int index) const;

	unsigned int* getPointer() const;

private:
	int  m_length;
	unsigned int* m_ptr;
};