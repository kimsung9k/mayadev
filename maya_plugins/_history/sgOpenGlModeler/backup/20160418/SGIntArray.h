#pragma once

class SGIntArray
{
public:
	SGIntArray();
	~SGIntArray();

	int  length();
	void setLength(int length);
	int& operator[](int index);
	int& operator[](int index) const;

	int* getPointer() const;

private:
	int  m_length;
	int* m_ptr;
};