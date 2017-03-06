#include <stdio.h>
#include "SGFileBefore.h"
#include "SGStringArray.h"


string SGFileBefore::readStringFromFile(const char* fileName)
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



vector<string> SGObj::splitStrByChar(const string& stringData, char splitCh)
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



void SGFileBefore::readMeshFile( const char* fileName, SGDagNodeContainer& container )
{
	ifstream fileInput(fileName, ios::binary);
	if (!fileInput.good())
	{
		printf("File failed to load...\"%s\"\n", fileName);
		return;
	}

	short sizeofInt    = sizeof(int);
	short sizeofDouble = sizeof(double);

	int numDataMesh;
	fileInput.read((char*)&numDataMesh, sizeofInt);

	for (int i = 0; i < numDataMesh; i++ )
	{
		SGDagNodeMesh* ptrDagNodeMesh = new SGDagNodeMesh;
		SGDagNodeMesh& meshData = *ptrDagNodeMesh;
		fileInput.read((char*)&meshData.m_numVertices, sizeofInt);
		fileInput.read((char*)&meshData.m_numPolygons, sizeofInt);
		fileInput.read((char*)&meshData.m_numIdArrayVertices, sizeofInt);
		fileInput.read((char*)&meshData.m_numUVs, sizeofInt);
		meshData.m_uvArrays = new vector<vector2d>[meshData.m_numUVs];
		for (int i = 0; i < meshData.m_numUVs; i++)
			meshData.m_uvArrays[i].resize(0);

		meshData.m_points.resize(meshData.m_numVertices);
		meshData.m_countArrayVertices.resize(meshData.m_numPolygons);
		meshData.m_idArrayVertices.resize(meshData.m_numIdArrayVertices);

		fileInput.read((char*)&meshData.m_matrix[0], sizeofDouble *16 );
		fileInput.read((char*)&meshData.m_points[0], sizeofDouble*meshData.m_numVertices * 3);
		fileInput.read((char*)&meshData.m_countArrayVertices[0], sizeofInt*meshData.m_numPolygons);
		fileInput.read((char*)&meshData.m_idArrayVertices[0], sizeofInt*meshData.m_numIdArrayVertices);

		meshData.updateBoundingBox();
		meshData.setDatasComopnentRelationship();
		meshData.setVertexNormals();
		meshData.setBuffer();

		container.append(ptrDagNodeMesh);
	}
	fileInput.close();
}



void SGFileBefore::readObjFile(const char* fileName, SGDagNodeContainer& container )
{
	string stringData = readStringFromFile(fileName);

	vector<string> lineStrs = SGObj::splitStrByChar(stringData, '\n');

	vector<SGDagNodeMesh*> ptrDagNodeMeshs;
	vector<string> vertexLines, normalLines, uvLines, faceLines;
	vector<int> startIndicesVtx, startIndicesNormal, startIndicesUV, startIndicesFace;

	startIndicesVtx.push_back(0);
	startIndicesNormal.push_back(0);
	startIndicesUV.push_back(0);
	startIndicesFace.push_back(0);

	bool normalExists = false;
	bool uvExists = false;

	int  numMeshs = 0;
	bool faceStart = false;
	
	for (int i = 0; i < lineStrs.size(); i++)
	{
		string& lineStr = lineStrs[i];
		if (!lineStr.size())continue;
		if (lineStr.at(0) == 'v' && lineStr.at(1) == ' ')
		{
			if (faceStart)
			{
				numMeshs++;
				startIndicesVtx.push_back(vertexLines.size());
				startIndicesNormal.push_back(normalLines.size());
				startIndicesUV.push_back(uvLines.size());
				startIndicesFace.push_back(faceLines.size());
				faceStart = false;
			}
			vertexLines.push_back(lineStr);
		}
		else if (lineStr.at(0) == 'v' && lineStr.at(1) == 'n')
		{
			normalExists = true;
			normalLines.push_back(lineStr);
		}
		else if (lineStr.at(0) == 'v' && lineStr.at(1) == 't')
		{
			uvExists = true;
			uvLines.push_back(lineStr);
		}
		else if (lineStr.at(0) == 'f' && lineStr.at(1) == ' ')
		{
			faceLines.push_back(lineStr);
			faceStart = true;
		}
	}
	numMeshs++;

	startIndicesVtx.push_back(vertexLines.size());
	startIndicesNormal.push_back(normalLines.size());
	startIndicesUV.push_back(uvLines.size());
	startIndicesFace.push_back(faceLines.size());

	for (int i = 0; i < numMeshs; i++)
	{
		SGDagNodeMesh* newMesh = new SGDagNodeMesh;
		newMesh->m_numUVs = 1;
		delete[] newMesh->m_uvArrays;
		newMesh->m_uvArrays = new vector<vector2d>[1];
		newMesh->m_uvArrays[0].resize(0);
		newMesh->m_numUVArrays.resize(1);
		newMesh->m_numUVArrays[0] = 0;
		ptrDagNodeMeshs.push_back(newMesh);
	}

	for (int i = 0; i < ptrDagNodeMeshs.size(); i++)
	{
		SGDagNodeMesh*& ptrDagNodeMesh = ptrDagNodeMeshs[i];

		ptrDagNodeMesh->m_points.resize(startIndicesVtx[i + 1] - startIndicesVtx[i]);
		for (int k = startIndicesVtx[i]; k < startIndicesVtx[i + 1]; k++)
		{
			vector3d& point = ptrDagNodeMesh->m_points[k - startIndicesVtx[i]];
			vector<string> firstSplits = SGObj::splitStrByChar(vertexLines[k], ' ');
			vector<string> splits;

			for (int m = 0; m < firstSplits.size(); m++)
			{
				if (firstSplits[m].size() == 0)continue;
				splits.push_back(firstSplits[m]);
			}

			point.x = atof(splits[1].c_str());
			point.y = atof(splits[2].c_str());
			point.z = atof(splits[3].c_str());
		}

		ptrDagNodeMesh->m_normals.resize(startIndicesNormal[i + 1] - startIndicesNormal[i]);/**/
		for (int k = startIndicesNormal[i]; k < startIndicesNormal[i + 1]; k++)
		{
			vector3d& normal = ptrDagNodeMesh->m_normals[k - startIndicesNormal[i]];
			vector<string> firstSplits = SGObj::splitStrByChar(normalLines[k], ' ');
			vector<string> splits;

			for (int m = 0; m < firstSplits.size(); m++)
			{
				if (firstSplits[m].size() == 0)continue;
				splits.push_back(firstSplits[m]);
			}
			normal.x = atof(splits[1].c_str());
			normal.y = atof(splits[2].c_str());
			normal.z = atof(splits[3].c_str());
		}

		ptrDagNodeMesh->m_uvArrays[0].resize(startIndicesUV[i + 1] - startIndicesUV[i]);/**/
		for (int k = startIndicesUV[i]; k < startIndicesUV[i + 1]; k++)
		{
			vector2d& UV = ptrDagNodeMesh->m_uvArrays[0][k - startIndicesUV[i]];
			vector<string> firstSplits = SGObj::splitStrByChar(uvLines[k], ' ');
			vector<string> splits;

			for (int m = 0; m < firstSplits.size(); m++)
			{
				if (firstSplits[m].size() == 0)continue;
				splits.push_back(firstSplits[m]);
			}
			UV.u = atof(splits[1].c_str());
			UV.v = atof(splits[2].c_str());
		}
	}

	for (int i = 0; i<ptrDagNodeMeshs.size(); i++)
	{
		SGDagNodeMesh* ptrDagNodeMesh = ptrDagNodeMeshs[i];
		SGDagNodeMeshBuffer* ptrBuffer = ptrDagNodeMesh->m_buffer;

		vector< vector<string> > splitsForTriangles;
		vector< vector<string> > splitsForQuads;
		vector< vector<string> > splitsForOverQuads;

		vector<int> triangleToPolygonMap;
		vector<int> quadToPolygonMap;
		vector<int> overQuadToPolygonMap;

		for (int k = startIndicesFace[i]; k < startIndicesFace[i+1]; k++)
		{
			vector<string> firstSplits = SGObj::splitStrByChar(faceLines[k], ' ');
			vector<string> splits;

			int originIndex = k - startIndicesFace[i];

			for (int m = 1; m < firstSplits.size(); m++)
			{
				if (firstSplits[m].size() == 0)continue;
				splits.push_back(firstSplits[m]);
			}

			if (splits.size() == 3) {
				splitsForTriangles.push_back(splits);
				ptrBuffer->m_numTriangles++;
				triangleToPolygonMap.push_back(originIndex);
			}
			else if (splits.size() == 4) {
				splitsForQuads.push_back(splits);
				ptrBuffer->m_numQuads++;
				quadToPolygonMap.push_back(originIndex);
			}
			else {
				splitsForOverQuads.push_back(splits);
				ptrBuffer->m_numOverQuads++;
				overQuadToPolygonMap.push_back(originIndex);
			}
			ptrDagNodeMesh->m_countArrayVertices.push_back(splits.size());
		}

		ptrBuffer->m_countArrayOverQuad.setLength(ptrBuffer->m_numOverQuads);
		ptrBuffer->m_sizeOverQuads = 0;
		for (int k = 0; k < ptrBuffer->m_numOverQuads; k++)
		{
			ptrBuffer->m_countArrayOverQuad[k] = splitsForOverQuads[k].size();
			ptrBuffer->m_sizeOverQuads += splitsForOverQuads[k].size();
		}

		ptrBuffer->m_bufferTriangles = new SGVertexBuffer[ptrBuffer->m_numTriangles*3];
		ptrBuffer->m_bufferQuads = new SGVertexBuffer[ptrBuffer->m_numQuads*4];
		ptrBuffer->m_bufferOverQuads = new SGVertexBuffer[ptrBuffer->m_sizeOverQuads];
		
		ptrDagNodeMeshs[i]->m_numVertices = ptrDagNodeMeshs[i]->m_points.size();
		ptrDagNodeMeshs[i]->m_numPolygons = startIndicesFace[i + 1] - startIndicesFace[i];
		ptrDagNodeMesh->m_vertexToPolygonsMap.resize(ptrDagNodeMeshs[i]->m_numVertices);
		ptrDagNodeMesh->m_polygonToVerticesMap.resize(ptrDagNodeMeshs[i]->m_numPolygons);

		for (int k = 0; k < splitsForTriangles.size(); k++)
		{
			int polygonIndex = triangleToPolygonMap[k];
			for (int m = 0; m < 3; m++)
			{
				SGVertexBuffer& vtxBuffer = ptrBuffer->m_bufferTriangles[k *3 + m];
				vector<string> element = SGObj::splitStrByChar(splitsForTriangles[k][m], '/');

				int vtxIndex = atoi(element[0].c_str()) - startIndicesVtx[i] - 1;
				vector3d& point = ptrDagNodeMesh->m_points[vtxIndex];
				vtxBuffer.x = point.x; vtxBuffer.y = point.y; vtxBuffer.z = point.z;

				ptrDagNodeMesh->m_vertexToPolygonsMap[vtxIndex].append(polygonIndex);
				ptrDagNodeMesh->m_polygonToVerticesMap[polygonIndex].append(vtxIndex);

				if (element.size() == 2)
				{
					int uvIndex = atoi(element[1].c_str()) - startIndicesUV[i] - 1;
					vector2d& uv = ptrDagNodeMesh->m_uvArrays[0][uvIndex];
					vtxBuffer.u = uv.u; vtxBuffer.v = uv.v;
				}
				else if (element.size() == 3)
				{
					int normalIndex = atoi(element[2].c_str()) - startIndicesNormal[i] - 1;
					vector3d& normal = ptrDagNodeMesh->m_normals[normalIndex];
					vtxBuffer.nx = normal.x; vtxBuffer.ny = normal.y; vtxBuffer.nz = normal.z;
				}
			}
		}

		for (int k = 0; k < splitsForQuads.size(); k++)
		{
			int polygonIndex = quadToPolygonMap[k];
			for (int m = 0; m < 4; m++)
			{
				SGVertexBuffer& vtxBuffer = ptrBuffer->m_bufferQuads[k*4+m];
				vector<string> element = SGObj::splitStrByChar(splitsForQuads[k][m], '/');
				
				int vtxIndex = atoi(element[0].c_str()) - startIndicesVtx[i] - 1;
				vector3d& point = ptrDagNodeMesh->m_points[vtxIndex];
				vtxBuffer.x = point.x; vtxBuffer.y = point.y; vtxBuffer.z = point.z;

				ptrDagNodeMesh->m_vertexToPolygonsMap[vtxIndex].append(polygonIndex);
				ptrDagNodeMesh->m_polygonToVerticesMap[polygonIndex].append(vtxIndex);

				if (element.size() == 2)
				{
					int uvIndex = atoi(element[1].c_str()) - startIndicesUV[i] - 1;
					vector2d& uv = ptrDagNodeMesh->m_uvArrays[0][uvIndex];
					vtxBuffer.u = uv.u; vtxBuffer.v = uv.v;
				}
				else if (element.size() == 3)
				{
					int normalIndex = atoi(element[2].c_str()) - startIndicesNormal[i] - 1;
					vector3d& normal = ptrDagNodeMesh->m_normals[normalIndex];
					vtxBuffer.nx = normal.x; vtxBuffer.ny = normal.y; vtxBuffer.nz = normal.z;
				}
			}
		}

		int targetIndex = 0;
		for (int k = 0; k < splitsForOverQuads.size(); k++)
		{
			int polygonIndex = overQuadToPolygonMap[k];
			for (int m = 0; m < ptrBuffer->m_countArrayOverQuad[k]; m++)
			{
				SGVertexBuffer& vtxBuffer = ptrBuffer->m_bufferOverQuads[targetIndex];
				vector<string> element = SGObj::splitStrByChar(splitsForOverQuads[k][m], '/');

				int vtxIndex = atoi(element[0].c_str()) - startIndicesVtx[i] - 1;
				vector3d& point = ptrDagNodeMesh->m_points[vtxIndex];
				vtxBuffer.x = point.x; vtxBuffer.y = point.y; vtxBuffer.z = point.z;

				ptrDagNodeMesh->m_vertexToPolygonsMap[vtxIndex].append(polygonIndex);
				ptrDagNodeMesh->m_polygonToVerticesMap[polygonIndex].append(vtxIndex);

				if (element.size() == 2)
				{
					int uvIndex = atoi(element[1].c_str()) - startIndicesUV[i] - 1;
					vector2d& uv = ptrDagNodeMesh->m_uvArrays[0][uvIndex];
					vtxBuffer.u = uv.u; vtxBuffer.v = uv.v;
				}
				else if (element.size() == 3)
				{
					int normalIndex = atoi(element[2].c_str()) - startIndicesNormal[i] - 1;
					vector3d& normal = ptrDagNodeMesh->m_normals[normalIndex];
					vtxBuffer.nx = normal.x; vtxBuffer.ny = normal.y; vtxBuffer.nz = normal.z;
				}
				targetIndex++;
			}
		}
	}
	
	for (int i = 0; i < ptrDagNodeMeshs.size(); i++)
	{
		SGDagNodeMeshBuffer* buffer = ptrDagNodeMeshs[i]->m_buffer;
		if (!normalExists)
		{
			ptrDagNodeMeshs[i]->setVertexNormals();
			ptrDagNodeMeshs[i]->setBuffer();
		}
		container.append(ptrDagNodeMeshs[i]);
	}
}