#include "sgCurveDraw_context.h"

/////////////////////////////////////////////////////////////////////////////////
//////////////////// sgCurveDraw_ToolCommand /////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////


sgCurveDraw_ToolCommand::sgCurveDraw_ToolCommand()
{
	setCommandString( "sgCurveDrawTool" );
}


sgCurveDraw_ToolCommand::~sgCurveDraw_ToolCommand()
{
}


void* sgCurveDraw_ToolCommand::creator()
{
	return new sgCurveDraw_ToolCommand;
}


bool sgCurveDraw_ToolCommand::isUndoable() const
{
	return true;
}


MStatus sgCurveDraw_ToolCommand::doIt( const MArgList& args )
{
	return redoIt();
}


MStatus sgCurveDraw_ToolCommand::redoIt()
{
	MStatus status;

	MFnNurbsCurve fnCurveOrig = m_dagPathOrigCurve;
	MMatrix mtxInverseCurve = m_dagPathOrigCurve.inclusiveMatrixInverse();
	double curveLength = fnCurveOrig.length();
	int degree = fnCurveOrig.degree();
	int spans  = fnCurveOrig.numSpans();
	MFnNurbsCurve::Form form = fnCurveOrig.form();

	if( m_startParam > m_endParam )
	{
		int lastIndex = m_curve_points.length()-1;
		MPointArray pointsReverse;
		pointsReverse.setLength( m_curve_points.length() );
		for( int i=0; i< m_curve_points.length(); i++ )
		{
			pointsReverse[ lastIndex-i ] = m_curve_points[i];
		}
		m_curve_points = pointsReverse;
		double tempParam = m_startParam;
		m_startParam = m_endParam;
		m_endParam = tempParam;
	}

	if( !m_editMode )
	{
		MSelectionList selList;

		MFnNurbsCurve fnCurveCreate;
		MFnTransform fnTransform;

		m_oCurveTransform = fnTransform.create();
		fnTransform.setObject( m_oCurveTransform );

		

		MObject oCurveCreated = fnCurveCreate.createWithEditPoints( m_curve_points, degree, form, false, false, false, m_oCurveTransform );

		fnCurveCreate.setObject( oCurveCreated );
		int renumSpans = spans * fnCurveCreate.length() / curveLength;

		char buffer[512];
		sprintf( buffer, "rebuildCurve -rpo 1 -rt 0 -end 1 -kcp 0 -kep 1 -kt 0 -s %d -d %d -tol 0.01 %s", renumSpans, degree, fnTransform.name().asChar() );
		MGlobal::executeCommand( buffer );
	}
	else
	{
		double origMinParam = fnCurveOrig.findParamFromLength( 0 );
		double origMaxParam = fnCurveOrig.findParamFromLength( curveLength );
		double origParamRange = origMaxParam - origMinParam;
		double eachSpanParamRange = origParamRange / spans;

		int origStartEPIndex = 0;
		double closeRate_start;
		for( int i=0; i< spans; i++ )
		{
			double paramRange = eachSpanParamRange * i;
			if( paramRange+eachSpanParamRange > m_startParam )
			{
				origStartEPIndex = i;
				closeRate_start = 1.0-(m_startParam - paramRange);
				break;
			}
		}

		int origEndEPIndex = 0;
		double closeRate_end = 0.0;
		if( m_paramIsLocked )
		{
			origEndEPIndex = spans+1;
		}
		else
		{
			for( int i=origStartEPIndex; i< spans+1; i++ )
			{
				double paramRange = eachSpanParamRange * i;
				if( paramRange+eachSpanParamRange > m_endParam )
				{
					origEndEPIndex = i+1;
					closeRate_end = m_endParam-paramRange;
					break;
				}
			}
		}
		/*
		cout << "start ep Index : " << origStartEPIndex << endl;
		cout << "end ep Index :   " << origEndEPIndex << endl;
		cout << "start offset :" << closeRate_start << endl;
		cout << "end offset   :" << closeRate_end << endl;
		*/
		MFnNurbsCurve fnCurveCreate;
		MFnNurbsCurveData dataCurve;
		MObject oCurveData = dataCurve.create();

		MPointArray points_origLocal;
		for( int i=0; i< origStartEPIndex+1; i++ )
		{
			MPoint point;
			fnCurveOrig.getPointAtParam( eachSpanParamRange * i, point );
			points_origLocal.append( point );
		}
		for( int i=0; i< m_curve_points.length(); i++ )
		{
			points_origLocal.append( m_curve_points[i] * mtxInverseCurve );
		}
		for( int i=origEndEPIndex; i< spans+1; i++ )
		{
			MPoint point;
			fnCurveOrig.getPointAtParam( eachSpanParamRange * i, point );
			points_origLocal.append( point );
		}

		fnCurveCreate.createWithEditPoints( points_origLocal, degree, form, false, false, false, oCurveData );
		MFnNurbsCurve fnCurveData( oCurveData );
		double curveDataLength = fnCurveData.length();

		double minParam_curveData = 0;
		double maxParam_curveData = fnCurveData.findParamFromLength( fnCurveData.length() );
		double eachParamRate = ( maxParam_curveData - minParam_curveData )/spans;

		MPointArray points_output;
		for( int i=0; i< spans+1; i++ )
		{
			MPoint point;
			fnCurveData.getPointAtParam( i*eachParamRate, point );
			points_output.append( point );
		}
		
		MFnNurbsCurveData dataCurve2;
		MObject oCurveData2 = dataCurve.create();
		fnCurveCreate.createWithEditPoints( points_output, degree, form, false, false, false, oCurveData2 );
		fnCurveData.setObject( oCurveData2 );
		
		MPointArray points_resultCVs;
		fnCurveOrig.getCVs( m_pointsCVsOrig );
		fnCurveData.getCVs( points_resultCVs );
		fnCurveOrig.setCVs( points_resultCVs );
		fnCurveOrig.updateCurve();
	}
	return MS::kSuccess;
}


MStatus sgCurveDraw_ToolCommand::undoIt()
{
	MStatus status;
	if( !m_editMode )
	{
		MFnTransform fnTransform( m_oCurveTransform );
		MGlobal::deleteNode( m_oCurveTransform );
	}
	else
	{
		MFnNurbsCurve fnCurveOrig( m_dagPathOrigCurve );
		fnCurveOrig.setCVs( m_pointsCVsOrig );
		fnCurveOrig.updateCurve();
	}
	return MS::kSuccess;
}


MStatus sgCurveDraw_ToolCommand::finalize()
{
	MArgList command;
	return MPxToolCommand::doFinalize( command );
}



///////////////////////////////////////////////////////////////////////////////
//////////////////// sgCurveDraw_context ///////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////



sgCurveDraw_context::sgCurveDraw_context()
{
	m_editMode = false;
}

sgCurveDraw_context::~sgCurveDraw_context()
{
}


void sgCurveDraw_context::toolOnSetup( MEvent& evt )
{
	MStatus status;

	MSelectionList selList;
	MGlobal::getActiveSelectionList( selList, true );

	MDagPath dagPathCurve;
	for( int i=0; i< selList.length(); i++ )
	{
		status = selList.getDagPath( i, dagPathCurve );
		getShapeNode( dagPathCurve );
		if( !status ) continue;
		if( dagPathCurve.apiType() != MFn::kNurbsCurve ) continue;
		
	}

	if( dagPathCurve.node().isNull() )
	{
		MGlobal::displayError( "Select one curve" );
		toolOffCleanup();
		return;
	}

	m_dagPathOrigCurve = dagPathCurve;

	this->setCursor( MCursor::crossHairCursor );
}


void sgCurveDraw_context::toolOffCleanup()
{
	this->deleteManipulators();
	this->setCursor( MCursor::defaultCursor );
}


void sgCurveDraw_context::getClassName( MString& name ) const
{
	name.set( "sgCurveDraw_context" );
}


MStatus sgCurveDraw_context::doPress( MEvent& evt )
{
	MStatus status;

	m_pointsDrawed.clear();
	m_pointsDrawed.setLength( 0 );
	m_lockParam = false;
	m_paramLast = -1;

	m_pContextCommand = ( sgCurveDraw_ToolCommand* )newToolCommand();
	m_pContextCommand->m_dagPathOrigCurve = m_dagPathOrigCurve;

	status = createWorldCurve( m_dagPathOrigCurve );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	m_view = M3dView::active3dView();
	status = m_view.getCamera( m_dagPathCam );
	CHECK_MSTATUS( status );

	short mouseX, mouseY;
    evt.getPosition( mouseX, mouseY );
	m_view.refresh( false, false, false );
	drawCurve( mouseX, mouseY );

	return MS::kSuccess;
}



MStatus sgCurveDraw_context::doDrag( MEvent& evt )
{
	MStatus status;

	short mouseX, mouseY;
    evt.getPosition( mouseX, mouseY );

	drawCurve( mouseX, mouseY );

	return MS::kSuccess;
}



MStatus sgCurveDraw_context::doRelease( MEvent& evt )
{
	MStatus status;

	MFnNurbsCurve fnCurveCreate;

	m_pContextCommand->m_curve_points = m_pointsDrawed;
	m_pContextCommand->m_editMode = m_editMode;
	m_pContextCommand->m_startParam = m_startParam;
	m_pContextCommand->m_endParam   = m_paramLast;
	m_pContextCommand->m_paramIsLocked   = m_lockParam;

	m_pContextCommand->redoIt();
	m_pContextCommand->finalize();

	return MS::kSuccess;
}