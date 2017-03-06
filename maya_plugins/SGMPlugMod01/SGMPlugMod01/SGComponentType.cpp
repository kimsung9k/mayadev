#include "precompile.h"
#include "SGComponentType.h"


SGComponentType::SGComponentType() {
	typ = kNone;
}


SGComponentType::SGComponentType(SGComponentType::Types typ) {
	this->typ = typ;
}


bool SGComponentType::operator==(SGComponentType::Types typ)
{
	if (this->typ == typ) return true;
	return false;
}


bool SGComponentType::operator!=(SGComponentType::Types typ)
{
	if (this->typ != typ) return true;
	return false;
}


void SGComponentType::operator=(SGComponentType::Types typ)
{
	this->typ = typ;
}


bool SGComponentType::operator==(const SGComponentType& typ)  const
{
	if (this->typ == typ.typ) return true;
	return false;
}


bool SGComponentType::operator!=(const SGComponentType& typ)  const
{
	if (this->typ != typ.typ) return true;
	return false;
}


void SGComponentType::operator=(const SGComponentType& typ)
{
	this->typ = typ.typ;
}


bool SGComponentType::isNone()
{
	if (this->typ == kNone) return true;
	return false;
}

bool SGComponentType::isVertex()
{
	if (this->typ == kVertex) return true;
	return false;
}

bool SGComponentType::isEdge()
{
	if (this->typ == kEdge) return true;
	return false;
}

bool SGComponentType::isPolygon()
{
	if (this->typ == kPolygon) return true;
	return false;
}