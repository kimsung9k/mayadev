#pragma once


class SGComponentType
{
public:
	enum Types {
		kNone,
		kVertex,
		kEdge,
		kPolygon
	};

	SGComponentType();
	SGComponentType(SGComponentType::Types);

	bool operator==(SGComponentType::Types typ);
	bool operator!=(SGComponentType::Types typ);
	void operator=(SGComponentType::Types typ);
	bool operator==(const SGComponentType& typ) const;
	bool operator!=(const SGComponentType& typ) const;
	void operator=(const SGComponentType& typ);

	bool isNone();
	bool isVertex();
	bool isEdge();
	bool isPolygon();

	Types typ;
};