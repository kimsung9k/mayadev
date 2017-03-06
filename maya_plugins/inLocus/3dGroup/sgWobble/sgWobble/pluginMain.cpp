#include "sgWobbleCurve.h"
#include "sgWobbleCurve2.h"

#include <maya/MFnPlugin.h>

MStatus initializePlugin( MObject obj )
{
    MStatus status;

    MFnPlugin fnPlugin( obj, "sggim", "1.0", "Any" );

	status = fnPlugin.registerNode( "sgWobbleCurve", sgWobbleCurve::id, sgWobbleCurve::creator, sgWobbleCurve::initialize );
    CHECK_MSTATUS_AND_RETURN_IT( status );

	status = fnPlugin.registerNode( "sgWobbleCurve2", sgWobbleCurve2::id, sgWobbleCurve2::creator, sgWobbleCurve2::initialize );
    CHECK_MSTATUS_AND_RETURN_IT( status );
    
    return MS::kSuccess;
}


MStatus uninitializePlugin( MObject obj )
{
    MStatus status;

    MFnPlugin fnPlugin( obj );

	status = fnPlugin.deregisterNode( sgWobbleCurve::id );
    CHECK_MSTATUS_AND_RETURN_IT( status );

	status = fnPlugin.deregisterNode( sgWobbleCurve2::id );
    CHECK_MSTATUS_AND_RETURN_IT( status );

    return MS::kSuccess;
}