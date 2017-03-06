#pragma once

#include "SGDefault.h"


class SGNode
{
public:
	SGNode();
	virtual ~SGNode();

	string type() const;
	string name() const;
	string m_name;

protected:
	string  m_typeName;
};