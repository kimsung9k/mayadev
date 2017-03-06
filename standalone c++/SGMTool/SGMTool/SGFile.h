#pragma once
#include <Windows.h>
#include <fstream>
#include <vector>


#include "SGDagNodeMesh.h"
#include "SGDagNodeContainer.h"


using namespace std;



class SGFile
{
public:
	static string readStringFromFile(const char* fileName);
	static void readObjFile(const char* fileName, SGDagNodeContainer& );
	static void readMeshFile(const char* fileName, SGDagNodeContainer& );
};


class SGObj
{
public:
	static vector<string>  splitStrByChar(const string& stringData, char splitCh );
};