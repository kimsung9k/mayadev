#include "SGMesh.h"
#include "SGFunction.cpp"



SGMesh::SGMesh()
{
	m_typeName = "mesh";
	m_pPoly = new SGStructPolygon;
	m_pUvs.resize(1);
	m_pUvs[0] = new SGStructUv;
	m_pShaders.resize(1);
	m_pBufferMeshs.resize(1);
	m_pBufferMeshs[0] = new SGBufferMesh;
}



SGMesh::~SGMesh()
{
	delete m_pPoly;
	SGFnc::deletePointers(m_pUvs, (int)m_pUvs.size());
}



void SGMesh::update()
{
}


void SGMesh::rebuildBuffer()
{
	m_pBufferMeshs.clear();
	m_pBufferMeshs.resize(m_pShaders.size());

	SGStructPolygon&     structPoly = *m_pPoly;
	vector<vector<int>>& mapPolyToVtxs = structPoly.m_mapPolyToVtxs;
	vector<vector<int>>& mapPolyToNors = structPoly.m_mapPolyToNors;

	int numPolygon = m_mapPolyToShader.size();

	for (int i = 0; i < numPolygon; i++)
	{
		int indexShader = m_mapPolyToShader[i];
		vector<int>& idsVtxs = mapPolyToVtxs[i];
		SGBufferMesh* pBufferMesh = m_pBufferMeshs[indexShader];

		if (idsVtxs.size() == 3){
			pBufferMesh->trianglePolyIds.push_back(i);
			pBufferMesh->numTriangleVtxs += 3;
		}
		else if (idsVtxs.size() == 4) {
			pBufferMesh->quadPolyIds.push_back(i);
			pBufferMesh->numQuadsVtxs += 4;
		}
		else{
			pBufferMesh->eachNumOverQuads.push_back(idsVtxs.size());
			pBufferMesh->overQuadPolyIds.push_back(i);
			pBufferMesh->numOverQuadsVtxs += idsVtxs.size();
		}
	}
	
	for (int i = 0; i < m_pShaders.size(); i++)
	{
		SGBufferMesh* pBufferMesh = m_pBufferMeshs[i];
		int numAllVtxs = pBufferMesh->numTriangleVtxs
			           + pBufferMesh->numQuadsVtxs 
			           + pBufferMesh->numOverQuadsVtxs;
		delete[] pBufferMesh->m_buffer;
		pBufferMesh->m_buffer = new SGBufferVtx[numAllVtxs];

		int cuBufferIndex = 0;

		vector<vector<int>> ids;
		ids.push_back(pBufferMesh->trianglePolyIds);
		ids.push_back(pBufferMesh->quadPolyIds);
		ids.push_back(pBufferMesh->overQuadPolyIds);

		for (int j = 0; j < ids.size(); j++)
		{
			for (int k = 0; k < ids[j].size(); k++)
			{
				int polygonId = ids[j][k];
				vector<int>& vtxIds = mapPolyToVtxs[polygonId];
				vector<int>& norIds = mapPolyToNors[polygonId];
				for (int m = 0; m < vtxIds.size(); m++)
				{
					SGVector& pos = structPoly.m_poses[vtxIds[m]];
					SGVector& nor = structPoly.m_nors[norIds[m]];

					SGBufferVtx& bufferVtx = pBufferMesh->m_buffer[cuBufferIndex];

					bufferVtx.pos.x = pos.x; bufferVtx.pos.y = pos.y; bufferVtx.pos.z = pos.z;
					bufferVtx.nor.x = nor.x; bufferVtx.nor.y = nor.y; bufferVtx.nor.z = nor.z;
					cuBufferIndex++;
				}
			}
		}
	}
}



void SGMesh::display()
{

}