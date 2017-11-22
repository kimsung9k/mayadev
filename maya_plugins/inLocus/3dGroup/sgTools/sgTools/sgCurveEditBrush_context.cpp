#include "sgCurveEditBrush_context.h"

/////////////////////////////////////////////////////////////////////////////////
//////////////////// sgCurveEditBrush_ToolCommand /////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////


sgCurveEditBrush_ToolCommand::sgCurveEditBrush_ToolCommand()
{
	setCommandString( "sgCurveEditBrushTool" );
}


sgCurveEditBrush_ToolCommand::~sgCurveEditBrush_ToolCommand()
{
}


void* sgCurveEditBrush_ToolCommand::creator()
{
	return new sgCurveEditBrush_ToolCommand;
}


bool sgCurveEditBrush_ToolCommand::isUndoable() const
{
	return true;
}


MStatus sgCurveEditBrush_ToolCommand::doIt( const MArgList& args )
{
	return redoIt();
}


MStatus sgCurveEditBrush_ToolCommand::redoIt()
{
	//cout << "Re Do It  - Create Joint" << endl;
	MStatus status;
	MSelectionList selList;

	for(unsigned int i=0; i< m_dagPathCurves.length(); i++ )
	{
		MFnNurbsCurve fnCurve( m_dagPathCurves[i] );
		fnCurve.setCVs( m_pointArrsCurvesAfter[i] );
		fnCurve.updateCurve();
	}

	return MS::kSuccess;
}


MStatus sgCurveEditBrush_ToolCommand::undoIt()
{
	MStatus status;

	for(unsigned int i=0; i< m_dagPathCurves.length(); i++ )
	{
		MFnNurbsCurve fnCurve( m_dagPathCurves[i] );
		fnCurve.setCVs( m_pointArrsCurvesBefore[i] );
		fnCurve.updateCurve();
	}

	return MS::kSuccess;
}


MStatus sgCurveEditBrush_ToolCommand::finalize()
{
	MArgList command;
	return MPxToolCommand::doFinalize( command );
}



///////////////////////////////////////////////////////////////////////////////
//////////////////// sgCurveEditBrush_context ///////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////



sgCurveEditBrush_context::sgCurveEditBrush_context()
{
	m_radiusEditOn  = false;
	m_radiusCurrent = 10;
}

sgCurveEditBrush_context::~sgCurveEditBrush_context()
{
}


#include "sgPrintf.h"

void sgCurveEditBrush_context::toolOnSetup( MEvent& evt )
{
	MStatus status;

	m_view = M3dView::active3dView();
	status = m_view.getCamera( m_pathCamera );
	CHECK_MSTATUS( status );

	MString nameManip = "sgCurveEditBrush_manip";
	m_manipulator = ( sgCurveEditBrush_manip* )sgCurveEditBrush_manip::newManipulator( nameManip, m_oManip );

	if( m_manipulator == NULL )
	{
		sgPrintf("manip is null");
	}

	MSelectionList selList;
	MGlobal::getActiveSelectionList( selList, true );

	m_dagPathCurves.clear();
	for( unsigned int i=0; i< selList.length(); i++ )
	{
		MDagPath dagPath;
		status = selList.getDagPath( i, dagPath );
		if( !status ) continue;
		status = getShapeNode( dagPath );
		if( !status ) continue;
		if( dagPath.apiType() != MFn::kNurbsCurve ) continue;
		m_dagPathCurves.append( dagPath );
	}
	
	m_dArrsCurvesLength.setLength( m_dagPathCurves.length() );
	for( unsigned int i=0; i< m_dagPathCurves.length(); i++ )
	{
		MFnNurbsCurve fnCurve = m_dagPathCurves[i];
		MMatrix mtxCurve = m_dagPathCurves[i].inclusiveMatrix();
		MPointArray points;
		fnCurve.getCVs( points );
		m_dArrsCurvesLength[i].setLength( points.length() );
		for( unsigned int j=1; j< points.length(); j++ )
		{
			MPoint pPoint = points[j-1];
			MPoint point  = points[j];
			m_dArrsCurvesLength[i][j] = pPoint.distanceTo( point );
		}
	}

	this->addManipulator( m_oManip );
	this->setCursor( MCursor::crossHairCursor );
}


void sgCurveEditBrush_context::toolOffCleanup()
{
	this->deleteManipulators();
	this->setCursor( MCursor::defaultCursor );
}


void sgCurveEditBrush_context::getClassName( MString& name ) const
{
	name.set( "sgCurveEditBrushContext" );
}


MStatus sgCurveEditBrush_context::doPress( MEvent& evt )
{
	MStatus status;

	short mouseX, mouseY;
    evt.getPosition( mouseX, mouseY );

	if( m_radiusEditOn )
	{
		m_radiusEditX  = mouseX;
		m_beforeRadius = m_radiusCurrent;
		this->setCursor( MCursor::pencilCursor );
	}
	else
	{
		m_mouseBeforeX = mouseX;
		m_mouseBeforeY = mouseY;
		this->setCursor( MCursor::crossHairCursor );

		m_pToolCmd = (sgCurveEditBrush_ToolCommand*)newToolCommand();

		m_pToolCmd->m_dagPathCurves = m_dagPathCurves;
		m_pToolCmd->m_pointArrsCurvesAfter.setLength( m_dagPathCurves.length() );
		m_pToolCmd->m_pointArrsCurvesBefore.setLength( m_dagPathCurves.length() );

		for( unsigned int i=0; i< m_dagPathCurves.length(); i++ )
		{
			MFnNurbsCurve fnCurve = m_dagPathCurves[i];
			MMatrix mtxCurve = m_dagPathCurves[i].inclusiveMatrix();
			MPointArray points;
			fnCurve.getCVs( points );
			m_pToolCmd->m_pointArrsCurvesBefore[i] = points;
			m_pToolCmd->m_pointArrsCurvesAfter[i] = points;
		}
	}
	m_view.refresh();

	if (m_manipulator != NULL) {
		m_manipulator->m_mouseX = mouseX;
		m_manipulator->m_mouseY = mouseY;

		m_manipulator->m_radiusCircle = m_radiusCurrent;
		m_manipulator->m_drawOn = true;
	}
	return MS::kSuccess;
}



MStatus sgCurveEditBrush_context::doDrag( MEvent& evt )
{
	MStatus status;

	short mouseX, mouseY;
    evt.getPosition( mouseX, mouseY );

	if( m_radiusEditOn )
	{
		double diffValue = ( mouseX - m_radiusEditX ); 
		m_radiusCurrent = (float)(m_beforeRadius + diffValue);
		if(m_manipulator) m_manipulator->m_radiusCircle = m_radiusCurrent;
	}
	else
	{
		if (m_manipulator) {
			m_manipulator->m_mouseX = mouseX;
			m_manipulator->m_mouseY = mouseY;
			m_manipulator->m_radiusCircle = m_radiusCurrent;
		}

		for(unsigned int i=0; i< m_dagPathCurves.length(); i++ )
		{
			status = editCurve( m_dagPathCurves[i],
				m_mouseBeforeX, m_mouseBeforeY, mouseX, mouseY, m_radiusCurrent,
				m_dArrsCurvesLength[i], m_pToolCmd->m_pointArrsCurvesAfter[i]  );
		}
	}

	m_mouseBeforeX = mouseX;
	m_mouseBeforeY = mouseY;

	if( m_radiusEditOn )
		m_view.refresh( true, false, false );
	else
		m_view.refresh( false, false, false );

	return MS::kSuccess;
}



MStatus sgCurveEditBrush_context::doRelease( MEvent& evt )
{

	MStatus status;
	if(m_manipulator)
		m_manipulator->m_drawOn = false;

	if( !m_radiusEditOn )
	{
		m_pToolCmd->redoIt();
		m_pToolCmd->finalize();
	}

	return MS::kSuccess;
}

MStatus sgCurveEditBrush_context::doPtrMoved(MEvent& evt)
{
	return MS::kSuccess;
}
MStatus sgCurveEditBrush_context::doPtrMoved(MEvent &evt, MHWRender::MUIDrawManager &drawManager, MHWRender::MFrameContext const &frameContext)
{
	return MS::kSuccess;
}