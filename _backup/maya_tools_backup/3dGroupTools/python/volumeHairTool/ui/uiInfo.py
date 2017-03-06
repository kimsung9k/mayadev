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


def intSlider( minValue, maxValue, fmx, v=0, cc=None ):
    
    slider = cmds.intSliderGrp( f=1, step=0.01, h=25, min=minValue, max=maxValue, fmx=fmx, v=v )
    if cc:
        cmds.intSliderGrp( slider, e=1, cc=cc )
    return slider


"""

class Grouping_ui:
    
    def __init__(self, groupList, elementList ):
        
        self._winName = 'Grouping_ui'
        self._title = "Grouping UI"
        
        self._groupList = groupList
        self._elementList = elementList
        
        self._width = 300
        self._height = 100
        
        self.core()
        
        
    def core(self):
        
        if cmds.window( self._winName, ex=1 ):
            cmds.deleteUI( self._winName, wnd=1 )
        cmds.window( self._winName, title = self._title )
        
        #form = cmds.formLayout()
        cmds.paneLayout( configuration='vertical2' )
        self._groupScrollList   = cmds.textScrollList( a=self._groupList, sc=self.leftSelCmd, ams=1 )
        self._elementScrollList = cmds.textScrollList( a=self._elementList, sc=self.rightSelCmd, ams=1 )
        '''
        cmds.formLayout( form, e=1, attachForm=[( self._groupScrollList, 'top', 5 ),
                                                ( self._groupScrollList, 'left', 5 ),
                                                ( self._groupScrollList, 'bottom', 5 ),
                                                ( self._elementScrollList, 'top', 5 ),
                                                ( self._elementScrollList, 'right', 5 ),
                                                ( self._elementScrollList, 'bottom', 5 )],
                                    attachPosition = [ ( self._groupScrollList, 'right', 2, 50),
                                                       ( self._elementScrollList, 'left', 2, 50) ] )'''
        
        cmds.window( self._winName, e=1, w=self._width, h=self._height )
        cmds.showWindow( self._winName )   
    
        
    def leftSelCmd(self):
        
        selItems  = cmds.textScrollList( self._groupScrollList, q=1, si=1 )
        cmds.select( selItems )
    
    
    def rightSelCmd(self):
        
        selItems  = cmds.textScrollList( self._elementScrollList, q=1, si=1 )
        cmds.select( selItems )
"""