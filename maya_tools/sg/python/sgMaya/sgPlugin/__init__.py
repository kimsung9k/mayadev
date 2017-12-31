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



def setTool_hardSkinWeightBrush( evt=0 ):

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
        sgSmoothWeightCommand -h 1 -i $index -w $val;
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
    
    

def setTool_curveEditBrush( evt=0 ):
    
    import maya.cmds as cmds
    import maya.mel as mel
    
    appendPluginPath()
    if not cmds.pluginInfo( "sgTools", q=1, l=1 ):
        cmds.loadPlugin( 'sgTools' )
    
    melScript = '''
    proc int isGreasePencilContext()
    //
    //    Description:
    //        Returns true if this is Grease Pencil context.
    //
    {
        string $tc = currentToolClass();
        return ($tc == "greasePencil");
    }
    
    
    global proc artActivateScreenSlider(
        string $sliderName
    )
    //
    //    Description:
    //        Global procs for activating screen sliders
    //        - sets the flag to activate them.
    //
    {
        // New Artisan Tools.
        if ( isArtisanCtx() ) {
            string $artisanCmd = artisanCommand();
            if( $sliderName == "upper_radius" ) {
                artBaseCtx -e -dragSlider "radius" `currentCtx`;
            } else if( $sliderName == "lower_radius" ) {
                artBaseCtx -e -dragSlider "lowradius" `currentCtx`;
            } else if( $sliderName == "opacity" ) {
                artBaseCtx -e -dragSlider "opacity" `currentCtx`;
            } else if( $sliderName == "value" ) {
                artBaseCtx -e -dragSlider "value" `currentCtx`;
            } else if( $sliderName == "stamp_depth" ) {
                artBaseCtx -e -dragSlider "depth" `currentCtx`;
            } else if( $sliderName == "displacement" ) {
                artBaseCtx -e -dragSlider "displacement" `currentCtx`;
            } else if( $sliderName == "uv_vector" ) {
                artBaseCtx -e -dragSlider "uvvector" `currentCtx`;
            }
        }
        else if ( isGreasePencilContext() )
        {
            if( $sliderName == "upper_radius" )
            {
                // Map B to radius
                artBaseCtx -e -dragSlider "radius" greasePencilContext;
            }
            else if( $sliderName == "displacement" )
            {
                // Map m to opacity rather than value but not for the eraser
                // as this has no effect
                if ( 4 != `greasePencilCtx -query -greasePencilType greasePencilContext` )
                {
                    artBaseCtx -e -dragSlider "opacity" greasePencilContext;
                }
            }
        }
        // UV Smudge Tool
        else if ( isSmudgeCtx() ) {
            texSmudgeUVContext -edit -dragSlider "radius" texSmudgeUVCtx;
        }
        // Soft Mod
        else if ( size( getActiveSoftMod() ) > 0 )
        {
            string $ctx = `currentCtx`;
            if( `contextInfo -c $ctx` != "softMod" )
                $ctx = "softModContext";
            softModCtx -e -dragSlider "radius" $ctx;
        }
        // Paint Effects.
        else if ((`isTrue "MayaCreatorExists"`) && isDynPaint())
        {
            if( $sliderName == "displacement" ) {
                dynPaintResize("offset");
            } else if( $sliderName == "lower_radius" ) {
                dynPaintResize("width");
            } else {
                dynPaintResize("size");
            }
        }
        else if ($sliderName == "upper_radius")
        {
            // upper_radius is the "b" key by default.  We only want to use that one
            // for soft select.  The "n" and "m" keys can also come in here so we want
            // to filter those out.
            global string $gSoftSelectOptionsCtx;
            softSelectOptionsCtx -edit -buttonDown $gSoftSelectOptionsCtx;
            if( `currentCtx` == "sgCurveEditBrushContext1" )
            {
                sgCurveEditBrushContext -e -radiusEditOn 1 sgCurveEditBrushContext1;
            }
        }
    }
    
    global proc artDeactivateScreenSlider()
    //
    //    Description:
    //        Global procs for deactivating screen sliders - sets the flag to
    //        deactivate them.
    //
    {
        // New Artisan Tools.
        if ( isArtisanCtx() ) {
            artBaseCtx -e -dragSlider "none" `currentCtx`;
        }
        else if ( isGreasePencilContext() )
        {
            artBaseCtx -e -dragSlider "none" greasePencilContext;
        }
        // UV Smudge
        else if ( isSmudgeCtx() ) {
            texSmudgeUVContext -e -dragSlider "none" texSmudgeUVCtx;
        }
        // Soft Mod
        else if ( size( getActiveSoftMod() ) > 0 )
        {
            string $ctx = `currentCtx`;
            if( `contextInfo -c $ctx` != "softMod" )
                $ctx = "softModContext";
            softModCtx -e -dragSlider "none" $ctx;
        }
        // Paint Effects.
        else if (`isTrue "MayaCreatorExists"` && isDynPaint())
        {
            dynPaintResize("none");
        }
        else
        {
            // We filter out the "n" and "m" keys in the activate call
            // but don't here because there isn't a slider name passed
            // in for deactivate.  To soft select context is smart
            // enough to know that it didn't start and edit so we are
            // ok to just call this in case we did.
            global string $gSoftSelectOptionsCtx;
            softSelectOptionsCtx -edit -buttonUp $gSoftSelectOptionsCtx;
        }
        if( `currentCtx` == "sgCurveEditBrushContext1" )
        {
            sgCurveEditBrushContext -e -radiusEditOn 0 sgCurveEditBrushContext1;
        }
    }
    
    global proc sgCurveEditBrush_contextProperties()
    {
    }
    
    global proc sgCurveEditBrush_contextValues( string $context )
    {
    }
    '''
    
    mel.eval( melScript )
    if not cmds.contextInfo( "sgCurveEditBrushContext1", ex=1 ):
        mel.eval( 'sgCurveEditBrushContext sgCurveEditBrushContext1' )
    cmds.setToolTo( "sgCurveEditBrushContext1" )
    
