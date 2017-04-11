import maya.cmds as cmds

def setSpace( h=5 ):
    
    cmds.text( l='', h=h )
    
    
def separator( w=300, h=5 ):
    
    cmds.rowColumnLayout( nc=1, cw=( 1,w ) )
    setSpace( h )
    cmds.separator()
    setSpace( h )
    cmds.setParent( '..' )
    


def addFrameLayout( uiName, label, vis=0, collapseAble=0, collapse=0 ):
    
    frame = cmds.frameLayout( uiName, l=label, vis=vis, cll=collapseAble, cl=collapse )
    cmds.frameLayout( lv=0, bs='out' )
    
    return frame
    
    
def getOutFrameLayout():
    
    cmds.setParent( '..' )
    cmds.setParent( '..' )
    

def setButton( command ):
    
    return cmds.button( l='Assign', h=30, c= command )


def floatSliderColumn( allWidth ):

    textWidth = allWidth / 3
    sliderWidth = allWidth - textWidth -10
    
    return cmds.rowColumnLayout( nc=2, cw=[(1,textWidth), (2,sliderWidth)] )
    

def floatSlider( minValue, maxValue, fmx, v=0, cc=None ):
    
    slider = cmds.floatSliderGrp( f=1, step=0.01, h=25, min=minValue, max=maxValue, fmx=fmx, v=v )
    if cc:
        cmds.floatSliderGrp( slider, e=1, cc=cc )
    return slider