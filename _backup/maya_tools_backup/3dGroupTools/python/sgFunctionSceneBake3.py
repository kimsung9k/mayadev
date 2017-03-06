import maya.cmds as cmds
import sgFunctionFileAndPath


def exportMesh( filePath ):
    
    sgFunctionFileAndPath.autoLoadPlugin( "sgSceneBake" )
    cmds.exportImportMesh( filePath, ex=1 )


def importMesh( filePath ):
    
    sgFunctionFileAndPath.autoLoadPlugin( "sgSceneBake" )
    cmds.exportImportMesh( filePath, im=1 )