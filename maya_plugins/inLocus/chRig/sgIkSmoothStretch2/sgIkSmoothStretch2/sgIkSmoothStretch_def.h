#ifndef _sgIkSmoothStretch_def_h
#define _sgIkSmoothStretch_def_h

#include <math.h>

double getKValue( double a, double b, double c )
{
	return ( pow( a, 2 ) - pow( b, 2 ) + pow( c, 2 ) ) / c / 2.0;
}

double getHValue( double a, double b, double c )
{
	double pow2 = pow( a, 2 ) + pow( b, 2 ) + pow( c, 2 );
	double pow4 = pow( a, 4 ) + pow( b, 4 ) + pow( c, 4 );

	if( c < 0.01 )
	{
		return 1.0;
	}

	double sqrtVal = pow( pow2, 2 ) - 2*pow4;

	if( sqrtVal < 0 )
		return 0.0;

	return sqrt( sqrtVal ) / c / 2.0;
}

double powStep( double originMin, double originMax, double inputValue )
{
	double lineValue = ( inputValue - originMin ) / ( originMax - originMin );

	double originalValue = inputValue;
	double smoothValue = - fabs( pow( ( lineValue - 1 ), 2 ) ) + 1;

	return smoothValue*( originMax - originMin ) + originMin;
}

double getHRate( double minValue, double maxValue, double cuValue )
{
	double lineValue = ( cuValue - minValue )/(maxValue-minValue);

	double replaceRate;
	if( lineValue < 0.5 )
	{
		replaceRate = lineValue*2;
	}
	else
	{
		replaceRate = 1;
	}
	double powValue = fabs( pow( lineValue - 1, 2 ) );

	return powValue*replaceRate + (1-lineValue)*( 1-replaceRate );
}

double getSmoothRate( double first, double second, double poseDist, double distArea )
{
	double a = first;
	double b = second;
	double c = poseDist;
	double allDist = first + second;

	distArea *= allDist;

	if( allDist-distArea > poseDist || allDist < poseDist)
	{
		return 1;
	}

	double d = powStep( allDist - distArea, allDist, poseDist );

	double k = getKValue( a, b, c );
	double h = getHValue( a, b, d );

	double firstEdit = sqrt( pow( k, 2 ) + pow( h, 2 ) );
	double secondEdit = sqrt( pow( c-k, 2 ) + pow( h, 2 ) );

	return (firstEdit + secondEdit)/allDist;
}


double getSmoothStretchRate( double first, double second, double poseDist, double distArea )
{
	double a = first;
	double b = second;
	double c = poseDist;
	double allDist = first + second;
	double distRate = 1.0;

	distArea *= allDist;

	double minDist = allDist-distArea;
	double maxDist = allDist+distArea;

	if( allDist-distArea > poseDist )
	{
		return 1;
	}
	else if( allDist+distArea > poseDist )
	{
		double maxDistRate = (distArea+allDist)/allDist-1;
		
		distRate = (poseDist-minDist)/(maxDist-minDist)*maxDistRate+1;
	}
	else
	{
		return poseDist /allDist;
	}

	double minH = getHValue( a, b, allDist-distArea );
	double hRate = getHRate( minDist, maxDist, poseDist );

	double k = getKValue( a*distRate, b*distRate, c );

	double firstEdit = sqrt( pow( k, 2 ) + pow( minH*hRate, 2 ) );
	double secondEdit = sqrt( pow( c-k, 2 ) + pow( minH*hRate, 2 ) );

	return (firstEdit + secondEdit)/allDist;
}

#endif