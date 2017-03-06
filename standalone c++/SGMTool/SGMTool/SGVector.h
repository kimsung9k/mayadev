#pragma once

class SGMatrix;

class SGVector {
public:
	SGVector();
	SGVector(const SGVector&);
	SGVector(double,double,double,double=0);
	~SGVector();

	SGVector  operator+(const SGVector& other) const;
	SGVector  operator-(const SGVector& other) const;
	double    operator*(const SGVector& other) const;
	SGVector  operator*(const SGMatrix& right) const;
	SGVector  operator^(const SGVector& other) const;
	SGVector& operator+=(const SGVector& other);
	SGVector& operator-=(const SGVector& other);

	SGVector  operator*(double scalar) const;
	SGVector  operator/(double scalar) const;
	SGVector& operator*=(double scalar);
	SGVector& operator*=( const SGMatrix& right);
	SGVector& operator/=(double scalar);
	SGVector& operator-();

	SGVector normal() const;
	void normalize();

	double length() const;
	double lengthSquare() const;

	double x;
	double y;
	double z;
	double w;
};