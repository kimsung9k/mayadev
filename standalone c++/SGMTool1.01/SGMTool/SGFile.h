#pragma once

#include <fstream>
#include <vector>
#include "SGDagNodeContainer.h"


using namespace std;


class SGFile
{
public:
	static string readStringFromFile(const char* fileName);
	static vector<string>  splitStrByChar(const string& stringData, char splitCh);
};



class SGObjFile : public SGFile
{
public:
	static void readObjFile(const char* fileName, SGDagNodeContainer* container );
	static void getLineInfomation( vector<string>& lines, 
		vector<string>& vertexLines, vector<string>& normalLines, 
		vector<string>& uvLines, vector<string>& faceLines,
		vector<int>& lengthVtxs, vector<int>& lengthNormals,
		vector<int>& lengthUVs, vector<int>& lengthFaces);
};