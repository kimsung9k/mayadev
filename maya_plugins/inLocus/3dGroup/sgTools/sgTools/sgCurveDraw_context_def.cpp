#include "sgCurveDraw_context.h"

MStatus sgCurveDraw_context::getShapeNode( MDagPath& path )
{
    MStatus status;

    if ( path.apiType() == MFn::kNurbsCurve )
    {
        return MS::kSuccess;
    }

    unsigned int numShapes;
    status = path.numberOfShapesDirectlyBelow( numShapes );
    CHECK_MSTATUS_AND_RETURN_IT( status );

    for ( unsigned int i = 0; i < numShapes; ++i )
    {
        status = path.extendToShapeDirectlyBelow( i );
        CHECK_MSTATUS_AND_RETURN_IT( status );

        if ( !path.hasFn( MFn::kNurbsCurve ) )
        {
            path.pop();
            continue;
        }

        MFnDagNode fnNode( path, &status );
        CHECK_MSTATUS_AND_RETURN_IT( status );
        if ( !fnNode.isIntermediateObject() )
        {
            return MS::kSuccess;
        }
        path.pop();
    }

    return MS::kFailure;
}


MPoint getCamPoint( MDagPath dagPath )
{
	return MPoint( dagPath.inclusiveMatrix()[3] );
}



MStatus sgCurveDraw_context::createWorldCurve( const MDagPath& dagPathCurve )
{
	MStatus status;
	MMatrix mtxCurve = dagPathCurve.inclusiveMatrix();

	MFnNurbsCurve fnCurve( dagPathCurve );

	MPointArray cvPoints;
	fnCurve.getCVs( cvPoints );
	int degree = fnCurve.degree();

	MDoubleArray knots;
	fnCurve.getKnots( knots );

	MFnNurbsCurveData dataCurve;
	MObject oDataCurve = dataCurve.create();

	for(unsigned int i=0; i< cvPoints.length(); i++ )
	{
		cvPoints[i] *= mtxCurve;
	}

	fnCurve.create( cvPoints, knots, degree, fnCurve.form(), 0, 0, oDataCurve );
	m_oWorldCurve = oDataCurve;

	return MS::kSuccess;
}



double sgCurveDraw_context::getClosestParamFromCurveWidthRay( MPoint pointNear, MVector rayDir, MObject oCurve )
{
	MFnNurbsCurve fnCurve( oCurve );

	int numSpans = fnCurve.numSpans();

	double curveLength = fnCurve.length();
	double sepCurveLength = curveLength / ( numSpans-1 );

	float maxDot = -1.0;
	double closestParamFirst;

	MVector drawPoint = pointNear + rayDir;

	rayDir.normalize();
	for( int i=0; i< numSpans; i++ )
	{
		MPoint pointAtParam;
		double param = fnCurve.findParamFromLength( sepCurveLength * i );
		fnCurve.getPointAtParam( param, pointAtParam );

		MVector vectorOther = pointAtParam - pointNear;
		vectorOther.normalize();

		double dot = vectorOther*rayDir;
		if( dot > maxDot )
		{
			maxDot = (float)dot;
			closestParamFirst = param;
		}
	}

	double minParam = fnCurve.findParamFromLength( 0 );
	double maxParam = fnCurve.findParamFromLength( curveLength );
	
	double paramDist = maxParam - minParam;
	double minAddParam = paramDist * 0.001;

	if( closestParamFirst - minAddParam < minParam || closestParamFirst + minAddParam > maxParam )
		return closestParamFirst;

	double currentParam = closestParamFirst;
	double eachParam    = (maxParam - minParam)/( numSpans-1.0 )/2.0;

	for( int i=0; i< 7; i++ )
	{
		MPoint pointAtParamForSign;
		double paramForSign = currentParam + minAddParam;

		fnCurve.getPointAtParam( paramForSign, pointAtParamForSign );

		MVector vectorOtherForSign = pointAtParamForSign - pointNear;
		vectorOtherForSign.normalize();

		double dotForSign = vectorOtherForSign*rayDir;
		if( dotForSign > maxDot )
			currentParam += eachParam;
		else
			currentParam -= eachParam;

		MPoint pointAtParam;
		fnCurve.getPointAtParam( currentParam, pointAtParam );
		MVector vectorOther = pointAtParam - pointNear;
		vectorOther.normalize();
		
		double dot = vectorOther*rayDir;
		maxDot = (float)dot;

		eachParam *= 0.5;
	}

	MPoint pointDisplay;
	fnCurve.getPointAtParam( currentParam, pointDisplay );
	
	return currentParam;
}


MPoint sgCurveDraw_context::getClosestPoint_of_rayAndCurve( MPoint pointCam, MVector vectorDir, MObject oCurve )
{
	if( !m_lockParam )
		m_currentParam = getClosestParamFromCurveWidthRay( pointCam, vectorDir, oCurve );
	else
		m_currentParam = m_paramLast;

	if( !m_pointsDrawed.length() )
		m_startParam = m_currentParam;

	MPoint pointAtParam;
	MFnNurbsCurve fnCurve( oCurve );
	fnCurve.getPointAtParam( m_currentParam, pointAtParam );

	MVector vCurvePoint = pointAtParam - pointCam;

	vectorDir.normalize();

	return (vCurvePoint * vectorDir) * vectorDir + pointCam;
}


MStatus sgCurveDraw_context::drawCurve( int mouseX, int mouseY )
{
	MPoint  pointNear;
	MPoint pointFar;
	m_view.viewToWorld( mouseX, mouseY, pointNear, pointFar );

	MVector vectorDir = pointFar - pointNear;
	vectorDir.normalize();

	MPoint camPoint = getCamPoint( m_dagPathCam );
	MPoint returnPoint = getClosestPoint_of_rayAndCurve( camPoint, vectorDir, m_oWorldCurve );

	if( m_pointsDrawed.length() > 3 )
	{
		MVector vDirBefore  = returnPoint - m_pointsDrawed[ m_pointsDrawed.length() -1 ];
		MVector vDirCurrent = returnPoint - m_pointsDrawed[ m_pointsDrawed.length() -1 ];

		if( vDirBefore*vDirCurrent > 0.5 )
		{
			m_lockParam = true;
			MGlobal::displayWarning( "Param Search is locked" );
			returnPoint = getClosestPoint_of_rayAndCurve( camPoint, vectorDir, m_oWorldCurve );
		}
		else
		{
			m_paramLast = m_currentParam;
		}
	}

	m_pointsDrawed.append( returnPoint );

	return MS::kSuccess;
}