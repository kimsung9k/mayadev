#pragma once

class SGVector;

class SGVectorArray
{
public:
	SGVectorArray();
	SGVectorArray(const SGVectorArray&);
	~SGVectorArray();

	void setLength(unsigned int length);
	unsigned int  length() const;
	void append(SGVector element);
	SGVector& operator[](unsigned int index);
	SGVector& operator[](unsigned int index) const;

private:
	SGVector* m_ptrArray;
	unsigned int m_length;
};