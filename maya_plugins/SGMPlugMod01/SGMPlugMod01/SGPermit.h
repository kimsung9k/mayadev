#pragma once

#include <SGBase.h>

struct IPv4
{
	unsigned char b1, b2, b3, b4;
};


class SGPermit
{
public:
	SGPermit();
	int getMyIP();
	IPv4 myIP;
};