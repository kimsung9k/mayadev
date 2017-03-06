#pragma once

#include <stdio.h>
#include <fstream>

using namespace std;

class SGStringArray
{
public:
	SGStringArray();
	SGStringArray(const SGStringArray&);
	~SGStringArray();

	void clear();
	void setLength(unsigned int length);
	unsigned int  length() const;
	void append(string element);
	int index(string element);

	string& operator[](unsigned int index);
	string& operator[](unsigned int index) const;
	SGStringArray& operator=(const SGStringArray&);

private:
	string* m_ptrArray;
	unsigned int m_length;
};