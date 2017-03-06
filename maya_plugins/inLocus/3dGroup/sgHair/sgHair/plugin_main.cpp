#include "sgHair_cutInfo.h"
#include "sgHair_attachStartPointCurve.h"
#include "sgHair_controlJoint.h"
#include "sgHair_controledCurve.h"
#include "sgHair_controledCurveB.h"
#include "sgHair_keyCurve.h"
#include "sgHair_fixCurvePointOnMatrix.h"

#include <maya/MFnPlugin.h>

MStatus initializePlugin( MObject obj )
{
    MStatus status;

    MFnPlugin fnPlugin( obj, "sggim", "1.0", "Any" );

	fnPlugin.registerNode( "sgHair_cutInfo",
		sgHair_cutInfo::id, sgHair_cutInfo::creator,
		sgHair_cutInfo::initialize );
	
	fnPlugin.registerNode( "sgHair_attachStartPointCurve",
		sgHair_attachStartPointCurve::id, sgHair_attachStartPointCurve::creator,
		sgHair_attachStartPointCurve::initialize );

	fnPlugin.registerNode( "sgHair_controlJoint",
		sgHair_controlJoint::id, sgHair_controlJoint::creator,
		sgHair_controlJoint::initialize );
	
	fnPlugin.registerNode( "sgHair_controledCurve",
		sgHair_controledCurve::id, sgHair_controledCurve::creator,
		sgHair_controledCurve::initialize );
	
	fnPlugin.registerNode( "sgHair_controledCurveB",
		sgHair_controledCurveB::id, sgHair_controledCurveB::creator,
		sgHair_controledCurveB::initialize );

	fnPlugin.registerNode( "sgHair_keyCurve",
		sgHair_keyCurve::id, sgHair_keyCurve::creator,
		sgHair_keyCurve::initialize, MPxNode::kDeformerNode );

	fnPlugin.registerNode( "sgHair_fixCurvePointOnMatrix",
		sgHair_fixCurvePointOnMatrix::id, sgHair_fixCurvePointOnMatrix::creator,
		sgHair_fixCurvePointOnMatrix::initialize );
		
    return MS::kSuccess;
}



MStatus uninitializePlugin( MObject obj )
{
    MStatus status;

    MFnPlugin fnPlugin( obj );
	fnPlugin.deregisterNode( sgHair_cutInfo::id );
	fnPlugin.deregisterNode( sgHair_attachStartPointCurve::id );
	fnPlugin.deregisterNode( sgHair_controlJoint::id );
	fnPlugin.deregisterNode( sgHair_controledCurve::id );
	fnPlugin.deregisterNode( sgHair_controledCurveB::id );
	fnPlugin.deregisterNode( sgHair_keyCurve::id );
	fnPlugin.deregisterNode( sgHair_fixCurvePointOnMatrix::id );

    return MS::kSuccess;
}