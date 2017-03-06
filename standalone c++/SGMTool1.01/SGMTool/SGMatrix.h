#pragma once

class SGVector;

class SGMatrix
{
public:
	SGMatrix();
	SGMatrix( const double* input);
	SGMatrix( const SGMatrix& input);

	SGMatrix inverseMatrix();
	const double& operator[](unsigned int index) const;
	double& operator[](unsigned int index);
	SGMatrix& operator=(const SGMatrix&other);
	SGMatrix operator*(const SGMatrix& right) const;
	SGMatrix& operator*=(const SGMatrix& right);
	void rotate( float radx, float rady, float radz);
	SGMatrix getRotatedMatrix(float radx, float rady, float radz);

private:
	double m_dptMtx[16];
};

SGMatrix getRotatationMatrix(float radValue, const SGVector& axis);