#include "sgHair_controledCurve.h"


MStatus sgHair_controledCurve::updateObjectArray()
{
	MStatus status;
	MFnDependencyNode fnNode( thisMObject() );
	MPlug plugTopJoint = fnNode.findPlug( aTopJoint );

	MPlugArray plugArrConnection;
	
	plugTopJoint.connectedTo( plugArrConnection, true, false );
	MObject oTopJoint = plugArrConnection[0].node();
	MFnDagNode dagCurrent( oTopJoint, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	m_oArrJoints.clear();
	m_oArrTargets.clear();
	
	m_oArrJoints.append( oTopJoint );
	m_oArrTargets.append( oTopJoint );

	for( ;; )
	{
		int childCount = dagCurrent.childCount();
		if( !childCount ) break;

		MObject oChild = dagCurrent.child( 0 );
		m_oArrJoints.append( oChild );

		if( childCount > 1 )
			m_oArrTargets.append( dagCurrent.child( 1 ) );
		else
			m_oArrTargets.append( oChild );
		dagCurrent.setObject( oChild );
	}

	return MS::kSuccess;
}



MStatus sgHair_controledCurve::updateJointPosition()
{
	MStatus status;

	int lengthObject = m_oArrTargets.length();

	MObject oTarget;
	MDagPath dagPathTarget;
	MMatrix mtxTarget;

	m_pArrPosition.setLength( lengthObject );
	m_dArrKnots.setLength( lengthObject );

	for( int i=0; i< lengthObject; i++ )
	{
		if( !m_oArrTargets[i].isNull() )
			oTarget = m_oArrTargets[i];
		else if( !m_oArrJoints[i].isNull() )
			oTarget = m_oArrJoints[i];
		else
		{
			m_isDirtyUpdate = true;
			break;
		}

		dagPathTarget.getAPathTo( oTarget, dagPathTarget );
		mtxTarget = dagPathTarget.inclusiveMatrix();
		m_pArrPosition[i] = MPoint( mtxTarget( 3,0 ), mtxTarget( 3,1 ), mtxTarget( 3,2 ) );
		m_dArrKnots[i] = i;
	}
	return MS::kSuccess;
}