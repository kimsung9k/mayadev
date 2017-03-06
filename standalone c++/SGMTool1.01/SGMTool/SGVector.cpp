#include "SGVector.h"
#include "SGMatrix.h"
#include <math.h>


SGVector::SGVector() :x(1.0), y(0.0), z(0.0), w(0.0) {
}


SGVector::SGVector( double x, double y, double z, double w ){
	this->x = x;
	this->y = y;
	this->z = z;
	this->w = w;
}


SGVector::SGVector( const SGVector& input) {
	this->x = input.x;
	this->y = input.y;
	this->z = input.z;
	this->w = input.w;
}

SGVector::~SGVector()
{
}


SGVector SGVector::operator+(const SGVector& other) const
{
	SGVector target;
	target.x = x + other.x;
	target.y = y + other.y;
	target.z = z + other.z;
	return target;
}

SGVector SGVector::operator-(const SGVector& other) const
{
	SGVector target;
	target.x = x - other.x;
	target.y = y - other.y;
	target.z = z - other.z;
	return target;
}

double SGVector::operator*(const SGVector& other) const
{
	return x*other.x + y*other.y + z*other.z;
}


SGVector SGVector::operator*(const SGMatrix& right) const
{
	SGVector target;
	target.x = right[0] * x + right[4] * y + right[8] * z;
	target.y = right[1] * x + right[5] * y + right[9] * z;
	target.z = right[2] * x + right[6] * y + right[10] * z;
	return target;
}



SGVector& SGVector::operator*=(const SGMatrix& right)
{
	double x, y, z;
	x = right[0] * x + right[4] * y + right[8] * z;
	y = right[1] * x + right[5] * y + right[9] * z;
	z = right[2] * x + right[6] * y + right[10] * z;
	this->x = x; this->y = y; this->z = z;
	return *this;
}



SGVector SGVector::operator^(const SGVector& other) const
{
	SGVector target;
	target.x = y * other.z - z * other.y;
	target.y = z * other.x - x * other.z;
	target.z = x * other.y - y * other.x;
	return target;
}


SGVector& SGVector::operator+= (const SGVector& other) {
	this->x += other.x;
	this->y += other.y;
	this->z += other.z;
	return *this;
}


SGVector& SGVector::operator-= (const SGVector& other) {
	this->x -= other.x;
	this->y -= other.y;
	this->z -= other.z;
	return *this;
}


SGVector SGVector::operator*(double scalar) const {
	SGVector target;
	target.x = x*scalar;
	target.y = y*scalar;
	target.z = z*scalar;
	return target;
}


SGVector SGVector::operator/(double scalar) const {
	SGVector target;
	target.x = x / scalar;
	target.y = y / scalar;
	target.z = z / scalar;
	return target;
}


SGVector& SGVector::operator*=(double scalar) {
	this->x *= scalar;
	this->y *= scalar;
	this->z *= scalar;
	return *this;
}


SGVector& SGVector::operator/=(double scalar) {
	this->x /= scalar;
	this->y /= scalar;
	this->z /= scalar;
	return *this;
}


SGVector& SGVector::operator-(){
	this->x *= -1;
	this->y *= -1;
	this->z *= -1;
	return *this;
}


double SGVector::length() const {
	return sqrt(x*x + y*y + z*z);
}


double SGVector::lengthSquare() const {
	return x*x + y*y + z*z;
}


SGVector SGVector::normal() const{
	double thisLength = length();
	SGVector target;
	target.x = this->x / thisLength;
	target.y = this->y / thisLength;
	target.z = this->z / thisLength;
	return target;
}


void SGVector::normalize()
{
	double thisLength = length();
	SGVector target;
	target.x = this->x / thisLength;
	target.y = this->y / thisLength;
	target.z = this->z / thisLength;
	x = target.x;
	y = target.y;
	z = target.z;
}