import maya.cmds as cmds
import maya.mel as mel
import os


def appendPluginPath():

    putenvStr = mel.eval( 'getenv "MAYA_PLUG_IN_PATH"' )
    
    if os.name == 'posix':
        sepChar = ':'
    else:
        sepChar = ';'
    
    pythonPathName = sepChar + os.path.dirname( __file__.replace( '\\', '/' ) ) + '/pluginRoot'
    
    version = cmds.about(version=True)[:4]
    cppPathName = sepChar + os.path.dirname( __file__.replace( '\\', '/' ) ) + '/pluginRoot/' + version
    
    putenvStr = putenvStr.replace( pythonPathName, '' )
    putenvStr += pythonPathName
    putenvStr = putenvStr.replace( cppPathName, '' )
    putenvStr += cppPathName
    
    mel.eval( 'putenv "MAYA_PLUG_IN_PATH" "%s"' % putenvStr )
    putenvStr = mel.eval( 'getenv "MAYA_PLUG_IN_PATH"' )
    
    print "MAYA_PLUG_IN_PATH : "
    for path in putenvStr.split( sepChar ):
        print "    ", path


if __name__ == "sgPlugin":
    appendPluginPath()




def setTool_putFollicleContext( evt=0 ):
    appendPluginPath()
    if not cmds.pluginInfo( 'sgPutFollicleContext', q=1, l=1 ):
        cmds.loadPlugin( 'sgPutFollicleContext' )
    cmds.setToolTo( 'sgPutFollicleContext1' )




def setTool_putInsideContext( evt=0 ):
    appendPluginPath()
    if not cmds.pluginInfo( 'sgPutInsideContext', q=1, l=1 ):
        cmds.loadPlugin( 'sgPutInsideContext' )
    cmds.setToolTo( 'sgPutInsideContext1' )




def setTool_SGMPlugMod01( evt=0 ):
    appendPluginPath()
    import sgCppPlug_modelingTool
    if not cmds.pluginInfo( 'SGMPlugMod01', q=1, l=1 ):
        cmds.loadPlugin( 'SGMPlugMod01' )
    sgCppPlug_modelingTool.setTool()



def setTool_smoothSkinWeightBrush( evt=0 ):

    appendPluginPath()
    _cmdStr =  """global string $tf_skinSmoothPatin_selection[];
    
    global proc tf_smoothBrush( string $context )     
    {       
     artUserPaintCtx -e -ic "tf_init_smoothBrush"
     -svc "tf_set_smoothBrushValue"
     -fc "" -gvc "" -gsc "" -gac "" -tcc "" $context;
    }
    
    global proc tf_init_smoothBrush( string $name )
    {
        string $sel[] = `ls -sl -fl`;
        string $obj[] = `ls -sl -o`;
        
        sgSmoothWeightCommand $obj;
    }
    
    global proc tf_set_smoothBrushValue( int $slot, int $index, float $val )             
    {         
        sgSmoothWeightCommand -i $index -w $val;
    }
    
    ScriptPaintTool;     
    artUserPaintCtx -e -tsc "tf_smoothBrush" `currentCtx`;"""
    
    if not cmds.pluginInfo( 'sgSmoothWeightCommand', q=1, l=1 ):
        cmds.loadPlugin( 'sgSmoothWeightCommand' )
    mel.eval( _cmdStr )



def cmd_sgAverageVertex( *args, **kwargs ):
    
    appendPluginPath()
    if not cmds.pluginInfo( 'sgAverageVertex', q=1, l=1 ):
        cmds.loadPlugin( 'sgAverageVertex' )
    cmds.sgAverageVertex( *args, **kwargs )



def cmd_putObjectAtGround( *args, **kwargs ):
    
    appendPluginPath()
    if not cmds.pluginInfo( "sgPutObjectAtGround_test", q=1, l=1 ):
        cmds.loadPlugin( 'sgPutObjectAtGround_test' )
    
    name = ''
    source = ''
    
    if kwargs.has_key( 'n' ):
        name = kwargs['n']
    if kwargs.has_key( 's' ):
        source = kwargs[ 's' ]
    
    mel.eval( "sgPutObjectAtGroundCommand -s %s -n %s" %( source, name ) )
    
    
    
    
