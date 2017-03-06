#pragma once

#include<maya/MString.h>

class SGFile
{
public:
	static bool directoryExists(const char* absolutePath);
	static bool fileExists(const char* absolutePath);
	static MString getKeySetupFilePath();
};