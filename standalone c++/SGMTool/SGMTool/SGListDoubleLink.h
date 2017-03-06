#pragma once


struct SGNodeDoubleLink
{
	void* ptrData;
	SGNodeDoubleLink* before;
	SGNodeDoubleLink* next;
};


class SGListDoubleLink
{
public:
	SGListDoubleLink();
	~SGListDoubleLink();

	template< typename T>
	void append( T input );

private:
	SGNodeDoubleLink* head;
	SGNodeDoubleLink* tail;
};