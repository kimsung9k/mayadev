#include "SGFile.h"


string SGFile::readStringFromFile(const char* fileName)
{
	ifstream fileInput(fileName);
	if (!fileInput.good())
	{
		printf("File failed to load...\"%s\"\n", fileName);
		//while (1);
	}
	string returnTarget = string(istreambuf_iterator<char>(fileInput),
		istreambuf_iterator<char>());

	return returnTarget;
}



vector<string> SGFile::splitStrByChar(const string& stringData, char splitCh)
{
	int searchIndex = 0;
	int beforeIndex = -1;
	int lineLength;

	int numMeshData = 0;

	vector<string> lineStrs;
	while (true)
	{
		searchIndex = (int)stringData.find(splitCh, beforeIndex + 1);
		if (searchIndex == -1) lineLength = (int)stringData.length() - beforeIndex;
		else lineLength = searchIndex - beforeIndex;

		string lineStr = stringData.substr(beforeIndex + 1, lineLength - 1);
		lineStrs.push_back(lineStr);

		if (beforeIndex >= searchIndex) break;
		beforeIndex = searchIndex;
	}
	return lineStrs;
}




void SGObjFile::readObjFile(const char* fileName, SGDagNodeContainer* container )
{
	string fileData = readStringFromFile(fileName);

	vector<string> lines = splitStrByChar(fileData, '\n' );

	vector<SGDataMesh*> ptrDataMeshs;
	vector<string> vertexLines, normalLines, uvLines, faceLines;
	vector<int> lengthVtxs, lengthNormals, lengthUVs, lengthFaces;

	getLineInfomation(lines, vertexLines, normalLines, uvLines, faceLines, lengthVtxs, lengthNormals, lengthUVs, lengthFaces);

	int numMeshs = lengthVtxs.size();

	for (int i = 0; i < numMeshs; i++)
	{
		SGDataTransform*  ptrTransform  = new SGDataTransform;
		SGDataMesh*       ptrMesh = new SGDataMesh;
		SGDataPolygon* ptrPoly = ptrMesh->m_ptrPoly;
		SGDataUv*      ptrUv = ptrMesh->m_ptrsUvs[0];

		ptrDataMeshs.push_back(ptrMesh);

		ptrMesh->m_name         = "meshShape";
		ptrTransform->m_name    = "meshTransform";
		ptrUv->m_name = "map1";
		ptrMesh->m_ptrTransform = ptrTransform;


	}
}




void SGObjFile::getLineInfomation(vector<string>& lines,
	vector<string>& vertexLines, vector<string>& normalLines,
	vector<string>& uvLines, vector<string>& faceLines,
	vector<int>& lengthVtxs, vector<int>& lengthNormals,
	vector<int>& lengthUVs, vector<int>& lengthFaces)
{
	bool faceStarted = false;

	int indexMesh = 0;
	for (int i = 0; i < lines.size(); i++)
	{
		string& line = lines[i];
		if (line.at(0) == 'v' && line.at(1) == ' ')
		{
			if (faceStarted)
			{
				lengthVtxs.push_back(vertexLines.size() - lengthVtxs[lengthVtxs.size() - 1]);
				lengthNormals.push_back(normalLines.size() - lengthNormals[lengthVtxs.size() - 1]);
				lengthUVs.push_back(uvLines.size() - lengthUVs[lengthVtxs.size() - 1]);
				lengthFaces.push_back(faceLines.size() - lengthFaces[lengthVtxs.size() - 1]);
				indexMesh += 1;
				faceStarted = false;
			}
			vertexLines.push_back(line);
			lengthVtxs[indexMesh] += 1;
		}
		if (line.at(0) == 'v' && line.at(1) == 'n')
		{
			normalLines.push_back(line);
			lengthNormals[indexMesh] += 1;
		}
		else if (line.at(0) == 'v' && line.at(1) == 't')
		{
			uvLines.push_back(line);
			lengthUVs[indexMesh] += 1;
		}
		else if (line.at(0) == 'f' && line.at(1) == ' ')
		{
			faceLines.push_back(line);
			lengthFaces[indexMesh] += 1;
			faceStarted = true;
		}
	}
}