#include "CreateJointContext.h"

/////////////////////////////////////////////////////////////////////////////////
//////////////////// CreateJointToolCommand /////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////


CreateJointToolCommand::CreateJointToolCommand()
{
	setCommandString( "createSmartIntersectJointTool" );
}


CreateJointToolCommand::~CreateJointToolCommand()
{
}


void* CreateJointToolCommand::creator()
{
	return new CreateJointToolCommand;
}


bool CreateJointToolCommand::isUndoable() const
{
	return true;
}


MStatus CreateJointToolCommand::doIt( const MArgList& args )
{
	return redoIt();
}


MStatus CreateJointToolCommand::redoIt()
{
	MStatus status;

	MGlobal::getActiveSelectionList( m_beforeSelect );

	MFnDagNode fnDagNode;
	m_oJoint = fnDagNode.create( "joint" );

	MSelectionList selList;
	selList.add( m_oJoint );
	MGlobal::setActiveSelectionList( selList );
	MGlobal::selectByName( fnDagNode.name() );

	return MS::kSuccess;
}


MStatus CreateJointToolCommand::undoIt()
{
	MStatus status;

	MGlobal::deleteNode( m_oJoint );
	if( !m_beforeSelect.length() ) return MS::kSuccess;
	MGlobal::setActiveSelectionList( m_beforeSelect );

	return MS::kSuccess;
}


MStatus CreateJointToolCommand::finalize()
{
	MArgList command;
	return MPxToolCommand::doFinalize( command );
}



///////////////////////////////////////////////////////////////////////////////
//////////////////// CreateJointContext ///////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////



CreateJointContext::CreateJointContext()
{
}



CreateJointContext::~CreateJointContext()
{
}



void CreateJointContext::toolOnSetup( MEvent& evt )
{
	MStatus status;

	m_view = M3dView::active3dView();
	status = m_view.getCamera( m_pathCamera );
	CHECK_MSTATUS( status );

	m_geometry.clear();
    status = getSelection( m_geometry );

	this->setCursor( MCursor::crossHairCursor );
}



void CreateJointContext::toolOffCleanup()
{
	this->setCursor( MCursor::defaultCursor );
}



void CreateJointContext::getClassName( MString& name ) const
{
	name.set( "createJointContext" );
}



MStatus CreateJointContext::doPress( MEvent& evt )
{
	MStatus status;

	short mouseX, mouseY;
    evt.getPosition( mouseX, mouseY );
	getMeshIntersection( mouseX, mouseY, m_pointsIntersect );
	MPoint pointGet = getCenterPoint( m_pointsIntersect );
	
	MGlobal::getActiveSelectionList( m_beforeSelect );
	CreateJointToolCommand* pToolCmd = (CreateJointToolCommand*)newToolCommand();
	pToolCmd->redoIt();
	MGlobal::getActiveSelectionList( m_afterSelect );

	setUpdateCondition( m_beforeSelect, m_afterSelect, pointGet );

	m_view.refresh();
	pToolCmd->finalize();

	return MS::kSuccess;
}



MStatus CreateJointContext::doDrag( MEvent& evt )
{
	MStatus status;

	short mouseX, mouseY;
    evt.getPosition( mouseX, mouseY );
	getMeshIntersection( mouseX, mouseY, m_pointsIntersect );
	MPoint pointGet = getCenterPoint( m_pointsIntersect );

	setUpdateCondition( m_beforeSelect, m_afterSelect, pointGet );

	m_view.refresh();
	return MS::kSuccess;
}



MStatus CreateJointContext::doRelease( MEvent& evt )
{
	MStatus status;
	return MS::kSuccess;
}



MStatus CreateJointContext::doPtrMoved(MEvent& evt)
{
	return MS::kSuccess;
}
MStatus CreateJointContext::doPtrMoved(MEvent &evt, MHWRender::MUIDrawManager &drawManager, MHWRender::MFrameContext const &frameContext)
{
	return MS::kSuccess;
}