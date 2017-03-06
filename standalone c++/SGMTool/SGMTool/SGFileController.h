#pragma once

#include "SGFile.h"

using namespace std;

class SGFileController
{
public:
	SGFileController();
	~SGFileController();

	static void openFile(const char* filePath);
};