#include "SGListDoubleLink.h"


SGListDoubleLink::SGListDoubleLink()
{
	head = new SGNodeDoubleLink;
	tail = new SGNodeDoubleLink;
	head->before = head;
	head->next = tail;
	tail->before = head;
	tail->next = tail;
}


SGListDoubleLink::~SGListDoubleLink()
{

}


template< typename T>
void SGListDoubleLink::append( T input )
{
	SGNodeDoubleLink* newNode = new SGNodeDoubleLink;
	newNode->ptrData = (void*)&input;

	SGNodeDoubleLink* beforeNode = tail->before;
	beforeNode->next = newNode;
	newNode->before = beforeNode;
	newNode->next = tail;
	tail->before = newNode;
}