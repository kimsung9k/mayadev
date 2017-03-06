
#include <maya/MFnPlugin.h>
#include "sgSkinWeightExportImport.h"


MStatus initializePlugin( MObject obj )
{
    MStatus status;

    MFnPlugin fnPlugin( obj, "skkim", "1.0", "Any" );

    status = fnPlugin.registerFileTranslator( 
        "weight", "none", sgSkinWeightExportImport::creator,
        (char *)optionScript,
        (char *)defaultOptions );        
    CHECK_MSTATUS_AND_RETURN_IT( status );

	MGlobal::executeCommand( "global proc int exportWeightOptions( string $parent,string $action,string $initialSettings,string $resultCallback ){return 0;}" );
    
    return MS::kSuccess;
}


MStatus uninitializePlugin( MObject obj )
{
    MStatus status;

    MFnPlugin fnPlugin( obj );

    status = fnPlugin.deregisterFileTranslator( "weight" );
    CHECK_MSTATUS_AND_RETURN_IT( status );

    return MS::kSuccess;
}