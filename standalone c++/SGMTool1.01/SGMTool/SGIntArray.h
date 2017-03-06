#pragma once

class SGIntArray
{
public:
	SGIntArray();
	SGIntArray(const SGIntArray& );
	~SGIntArray();

	void clear();
	void setLength(unsigned int length );
	unsigned int  length() const;
	void append(int element);
	int index(int element);
	int* asIntPtr();
	int& operator[](unsigned int index);
	int& operator[](unsigned int index) const;
	SGIntArray& operator=(const SGIntArray&);

private:
	int* m_ptrArray;
	unsigned int m_length;
};