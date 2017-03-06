#include "SGMatrix.h"
#include <math.h>
#include "SGVector.h"


#define SQUARE( x )  pow( x, 2 )
#define SQ   SQUARE


SGMatrix::SGMatrix() {
	m_dptMtx[0] = 1.0f; m_dptMtx[1] = 0.0f; m_dptMtx[2] = 0.0f; m_dptMtx[3] = 0.0f;
	m_dptMtx[4] = 0.0f; m_dptMtx[5] = 1.0f; m_dptMtx[6] = 0.0f; m_dptMtx[7] = 0.0f;
	m_dptMtx[8] = 0.0f; m_dptMtx[9] = 0.0f; m_dptMtx[10] = 1.0f; m_dptMtx[11] = 0.0f;
	m_dptMtx[12] = 0.0f; m_dptMtx[13] = 0.0f; m_dptMtx[14] = 0.0f; m_dptMtx[15] = 1.0f;
}


SGMatrix::SGMatrix(const double* input) {
	for (int i = 0; i < 16; i++) {
		m_dptMtx[i] = input[i];
	}
}


SGMatrix::SGMatrix(const SGMatrix& input) {
	for (int i = 0; i < 16; i++) {
		m_dptMtx[i] = input.m_dptMtx[i];
	}
}


SGMatrix SGMatrix::inverseMatrix() {
	double det = m_dptMtx[0] * (m_dptMtx[5] * m_dptMtx[10] - m_dptMtx[6] * m_dptMtx[9]) +
		m_dptMtx[1] * (m_dptMtx[6] * m_dptMtx[8] - m_dptMtx[4] * m_dptMtx[10]) +
		m_dptMtx[2] * (m_dptMtx[4] * m_dptMtx[9] - m_dptMtx[5] * m_dptMtx[8]);
	SGMatrix trg;

	trg[0] = (m_dptMtx[5] * m_dptMtx[10] - m_dptMtx[6] * m_dptMtx[9]) / det;
	trg[1] = (m_dptMtx[2] * m_dptMtx[9] - m_dptMtx[1] * m_dptMtx[10]) / det;
	trg[2] = (m_dptMtx[1] * m_dptMtx[6] - m_dptMtx[2] * m_dptMtx[5]) / det;

	trg[4] = (m_dptMtx[6] * m_dptMtx[8] - m_dptMtx[4] * m_dptMtx[10]) / det;
	trg[5] = (m_dptMtx[0] * m_dptMtx[10] - m_dptMtx[2] * m_dptMtx[8]) / det;
	trg[6] = (m_dptMtx[2] * m_dptMtx[4] - m_dptMtx[0] * m_dptMtx[6]) / det;

	trg[8] = (m_dptMtx[4] * m_dptMtx[9] - m_dptMtx[5] * m_dptMtx[8]) / det;
	trg[9] = (m_dptMtx[1] * m_dptMtx[8] - m_dptMtx[0] * m_dptMtx[9]) / det;
	trg[10] = (m_dptMtx[0] * m_dptMtx[5] - m_dptMtx[1] * m_dptMtx[4]) / det;

	trg[12] = -(m_dptMtx[12] * trg[0] + m_dptMtx[13] * trg[4] + m_dptMtx[14] * trg[8]);
	trg[13] = -(m_dptMtx[12] * trg[1] + m_dptMtx[13] * trg[5] + m_dptMtx[14] * trg[9]);
	trg[14] = -(m_dptMtx[12] * trg[2] + m_dptMtx[13] * trg[6] + m_dptMtx[14] * trg[10]);
	trg[15] = m_dptMtx[15];

	return trg;
}

const double& SGMatrix::operator[](unsigned int index) const{
	return m_dptMtx[index];
}

double& SGMatrix::operator[](unsigned int index) {
	return m_dptMtx[index];
}

SGMatrix& SGMatrix::operator=( const SGMatrix& other) {
	for (int i = 0; i < 16; i++) {
		m_dptMtx[i] = other.m_dptMtx[i];
	}
	return *this;
}


SGMatrix SGMatrix::operator*( const SGMatrix& right) const
{
	SGMatrix temp;
	/*
	for (int i = 0; i < 4; i++)
	{
		for (int j = 0; j < 4; j++)
		{
			temp[i * 4 + j] = 0;
			for (int k = 0; k < 4; k++)
			{
				temp[i * 4 + j] += this->m_dptMtx[i * 4 + j] * right.m_dptMtx[i + j * 4];
			}
		}
	}
	*/
	temp[0] = (this->m_dptMtx[0] * right.m_dptMtx[0] + this->m_dptMtx[1] * right.m_dptMtx[4] + this->m_dptMtx[2] * right.m_dptMtx[8]);
	temp[1] = (this->m_dptMtx[0] * right.m_dptMtx[1] + this->m_dptMtx[1] * right.m_dptMtx[5] + this->m_dptMtx[2] * right.m_dptMtx[9]);
	temp[2] = (this->m_dptMtx[0] * right.m_dptMtx[2] + this->m_dptMtx[1] * right.m_dptMtx[6] + this->m_dptMtx[2] * right.m_dptMtx[10]);
	temp[3] = 0;

	temp[4] = (this->m_dptMtx[4] * right.m_dptMtx[0] + this->m_dptMtx[5] * right.m_dptMtx[4] + this->m_dptMtx[6] * right.m_dptMtx[8]);
	temp[5] = (this->m_dptMtx[4] * right.m_dptMtx[1] + this->m_dptMtx[5] * right.m_dptMtx[5] + this->m_dptMtx[6] * right.m_dptMtx[9]);
	temp[6] = (this->m_dptMtx[4] * right.m_dptMtx[2] + this->m_dptMtx[5] * right.m_dptMtx[6] + this->m_dptMtx[6] * right.m_dptMtx[10]);
	temp[7] = 0;

	temp[8] = (this->m_dptMtx[8] * right.m_dptMtx[0] + this->m_dptMtx[9] * right.m_dptMtx[4] + this->m_dptMtx[10] * right.m_dptMtx[8]);
	temp[9] = (this->m_dptMtx[8] * right.m_dptMtx[1] + this->m_dptMtx[9] * right.m_dptMtx[5] + this->m_dptMtx[10] * right.m_dptMtx[9]);
	temp[10] = (this->m_dptMtx[8] * right.m_dptMtx[2] + this->m_dptMtx[9] * right.m_dptMtx[6] + this->m_dptMtx[10] * right.m_dptMtx[10]);
	temp[11] = 0;

	temp[12] = (this->m_dptMtx[12] * right.m_dptMtx[0] + this->m_dptMtx[13] * right.m_dptMtx[4] + this->m_dptMtx[14] * right.m_dptMtx[8] + right.m_dptMtx[12]);
	temp[13] = (this->m_dptMtx[12] * right.m_dptMtx[1] + this->m_dptMtx[13] * right.m_dptMtx[5] + this->m_dptMtx[14] * right.m_dptMtx[9] + right.m_dptMtx[13]);
	temp[14] = (this->m_dptMtx[12] * right.m_dptMtx[2] + this->m_dptMtx[13] * right.m_dptMtx[6] + this->m_dptMtx[14] * right.m_dptMtx[10] + right.m_dptMtx[14]);
	temp[15] = 1;
	
	return temp;
}

SGMatrix& SGMatrix::operator*=(const SGMatrix& right)
{
	SGMatrix temp = *this;
	this->m_dptMtx[0] = (temp.m_dptMtx[0] * right.m_dptMtx[0] + temp.m_dptMtx[1] * right.m_dptMtx[4] + temp.m_dptMtx[2] * right.m_dptMtx[8]);
	this->m_dptMtx[1] = (temp.m_dptMtx[0] * right.m_dptMtx[1] + temp.m_dptMtx[1] * right.m_dptMtx[5] + temp.m_dptMtx[2] * right.m_dptMtx[9]);
	this->m_dptMtx[2] = (temp.m_dptMtx[0] * right.m_dptMtx[2] + temp.m_dptMtx[1] * right.m_dptMtx[6] + temp.m_dptMtx[2] * right.m_dptMtx[10]);
	this->m_dptMtx[3] = 0;

	this->m_dptMtx[4] = (temp.m_dptMtx[4] * right.m_dptMtx[0] + temp.m_dptMtx[5] * right.m_dptMtx[4] + temp.m_dptMtx[6] * right.m_dptMtx[8]);
	this->m_dptMtx[5] = (temp.m_dptMtx[4] * right.m_dptMtx[1] + temp.m_dptMtx[5] * right.m_dptMtx[5] + temp.m_dptMtx[6] * right.m_dptMtx[9]);
	this->m_dptMtx[6] = (temp.m_dptMtx[4] * right.m_dptMtx[2] + temp.m_dptMtx[5] * right.m_dptMtx[6] + temp.m_dptMtx[6] * right.m_dptMtx[10]);
	this->m_dptMtx[7] = 0;

	this->m_dptMtx[8] = (temp.m_dptMtx[8] * right.m_dptMtx[0] + temp.m_dptMtx[9] * right.m_dptMtx[4] + temp.m_dptMtx[10] * right.m_dptMtx[8]);
	this->m_dptMtx[9] = (temp.m_dptMtx[8] * right.m_dptMtx[1] + temp.m_dptMtx[9] * right.m_dptMtx[5] + temp.m_dptMtx[10] * right.m_dptMtx[9]);
	this->m_dptMtx[10] = (temp.m_dptMtx[8] * right.m_dptMtx[2] + temp.m_dptMtx[9] * right.m_dptMtx[6] + temp.m_dptMtx[10] * right.m_dptMtx[10]);
	this->m_dptMtx[11] = 0;

	this->m_dptMtx[12] = (temp.m_dptMtx[12] * right.m_dptMtx[0] + temp.m_dptMtx[13] * right.m_dptMtx[4] + temp.m_dptMtx[14] * right.m_dptMtx[8] + right.m_dptMtx[12]);
	this->m_dptMtx[13] = (temp.m_dptMtx[12] * right.m_dptMtx[1] + temp.m_dptMtx[13] * right.m_dptMtx[5] + temp.m_dptMtx[14] * right.m_dptMtx[9] + right.m_dptMtx[13]);
	this->m_dptMtx[14] = (temp.m_dptMtx[12] * right.m_dptMtx[2] + temp.m_dptMtx[13] * right.m_dptMtx[6] + temp.m_dptMtx[14] * right.m_dptMtx[10] + right.m_dptMtx[14]);
	this->m_dptMtx[15] = 1;

	return *this;
}


void SGMatrix::rotate(float radx, float rady, float radz) {
	SGMatrix temp = *this;
	SGMatrix& thisMatrix = *this;

	double rotx[9] = { 
		1,         0,         0,
		0,  cos(radx), sin(radx),
		0, -sin(radx), cos(radx) };

	double roty[9] = { 
		 cos(rady), 0, sin(rady),
		 0,         1,         0,
		 -sin(rady), 0, cos(rady) };

	double rotz[9] = {
		 cos(radz), sin(radz), 0,
		-sin(radz), cos(radz), 0,
		 0,         0,         1};


	thisMatrix[0] = temp[0];
	thisMatrix[1] = rotx[4] * temp[1] + rotx[7] * temp[2];
	thisMatrix[2] = rotx[5] * temp[1] + rotx[8] * temp[2];

	thisMatrix[4] = temp[4];
	thisMatrix[5] = rotx[4] * temp[5] + rotx[7] * temp[6];
	thisMatrix[6] = rotx[5] * temp[5] + rotx[8] * temp[6];

	thisMatrix[8] = temp[8];
	thisMatrix[9] = rotx[4] * temp[9] + rotx[7] * temp[10];
	thisMatrix[10] = rotx[5] * temp[9] + rotx[8] * temp[10];


	temp[0] = roty[0] * thisMatrix[0] + roty[6] * thisMatrix[2];
	temp[1] = thisMatrix[1];
	temp[2] = roty[2] * thisMatrix[0] + roty[8] * thisMatrix[2];

	temp[4] = roty[0] * thisMatrix[4] + roty[6] * thisMatrix[6];
	temp[5] = thisMatrix[5];
	temp[6] = roty[2] * thisMatrix[4] + roty[8] * thisMatrix[6];

	temp[8] = roty[0] * thisMatrix[8] + roty[6] * thisMatrix[10];
	temp[9] = thisMatrix[9];
	temp[10] = roty[2] * thisMatrix[8] + roty[8] * thisMatrix[10];


	thisMatrix[0] = rotz[0] * temp[0] + rotz[3] * temp[1];
	thisMatrix[1] = rotz[1] * temp[0] + rotz[4] * temp[1];
	thisMatrix[2] = temp[2];

	thisMatrix[4] = rotz[0] * temp[4] + rotz[3] * temp[5];
	thisMatrix[5] = rotz[1] * temp[4] + rotz[4] * temp[5];
	thisMatrix[6] = temp[6];

	thisMatrix[8] = rotz[0] * temp[8] + rotz[3] * temp[9];
	thisMatrix[9] = rotz[1] * temp[8] + rotz[4] * temp[9];
	thisMatrix[10] = temp[10];
}


SGMatrix SGMatrix::getRotatedMatrix(float radx, float rady, float radz) {
	SGMatrix target = *this;
	target.rotate(radx, rady, radz);
	return target;
}


SGMatrix getRotatationMatrix(float radValue, const SGVector& axis)
{
	double S = sin(radValue);
	double C = cos(radValue);
	SGVector A = axis.normal();

	SGMatrix mtx;

	mtx[0] = C + SQ(A.x)*(1.0 - C);
	mtx[1] = A.x*A.y*(1.0 - C) + A.z*S;
	mtx[2] = A.z*A.x*(1.0 - C) - A.y*S;

	mtx[4] = A.x*A.y*(1.0 - C) - A.z*S;
	mtx[5] = C + SQ(A.y)*(1.0 - C);
	mtx[6] = A.y*A.z*(1.0 - C) + A.x*S;

	mtx[8] = A.z*A.x*(1.0 - C) + A.y*S;
	mtx[9] = A.y*A.z*(1.0 - C) - A.x*S;
	mtx[10] = C + SQ(A.z)*(1.0 - C);

	return mtx;
}