#include "precompile.h"
#include "SGFile.h"
#include <SGBase.h>
#include <maya/MCommonSystemUtils.h>
#include <io.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <direct.h>
#include <fstream>


bool SGFile::directoryExists(const char* absolutePath)
{
	if (_access(absolutePath, 0) == 0) {
		struct stat status;
		stat(absolutePath, &status);

		return (status.st_mode & S_IFDIR) != 0;
	}
	return false;
}


bool SGFile::fileExists(const char* absolutePath) {
	ifstream f(absolutePath);
	return f.good();
}


MString SGFile::getKeySetupFilePath() {
	MString setupFilePath;
	MCommonSystemUtils::getEnv("APPDATA", setupFilePath);
	setupFilePath += "\\SGMPlugMod01";

	if ( !directoryExists(setupFilePath.asChar()) ) {
		_mkdir(setupFilePath.asChar() );
	}

	setupFilePath += "\\keySetup.txt";
	if (!fileExists(setupFilePath.asChar())) {
		FILE* file = fopen(setupFilePath.asChar(), "w");
		fclose(file);
	}
	return setupFilePath;
}