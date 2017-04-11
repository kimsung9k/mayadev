import maya.cmds as cmds


progressUiName = 'volumeHairTool_progress'
progressUiTitle = 'Volume Hair Tool Progress'
uiInst = None
progressIndex = 0

progressCurrent = 0
progressLength = 1



def start():
    global uiInst
    global progressIndex
    progressIndex = 0
    uiInst = UI()
    uiInst.show()
    cmds.refresh()
    
    
def append( progressStr ):
    global uiInst
    uiInst.append( progressStr )
    
    
def end():
    global uiInst
    uiInst.hide()
    #cmds.refresh( suspend=0 )


def nextIndex():
    global progressIndex
    progressIndex += 1

    
def setLength( length ):
    global progressCurrent
    global progressLength
    progressCurrent = 0
    progressLength = length


def addCount():
    global progressCurrent
    global progressLength
    
    progressCurrent += 1
    
    row, left, right = uiInst._progressBarList[ progressIndex ]
    
    percent = progressCurrent/float(progressLength)
        
    leftWidth = percent*200
    rightWidth = 200-leftWidth
    
    if leftWidth < 1:
        leftWidth = 1
        rightWidth = 199
    if rightWidth < 1:
        leftWidth = 199
        rightWidth = 1
    
    cmds.rowColumnLayout( row, e=1, cw=[ (1,leftWidth),(2,rightWidth)] )
    if progressCurrent == 1: cmds.text( left, e=1, bgc=[1,1,0] )
    elif progressCurrent == progressLength: cmds.text( right, e=1, bgc=[1,1,0] )
    
    cmds.refresh()
    
    
class UI:
    
    def __init__( self ):
        
        global progressUiName
        global progressUiTitle
        
        self._progressList = []
        self._progressBarList = []
    
        self._winName = progressUiName
        self._title = progressUiTitle
        
        self._width = 300
        self._height = 2
        
    
    def append( self, progressStr ):
        
        cmds.setParent( self._mainLayout )
        cmds.rowColumnLayout( nc=2, cw=[(1,100),(2,200)])
        cmds.text( l=progressStr+'  : ', al='right' )
        cmds.frameLayout(cll=0,lv=0, bs='in' )
        row = cmds.rowColumnLayout( nc=2, cw=[(1,1),(2,199)])
        left = cmds.text( l='' )
        right = cmds.text( l='' )
        
        self._progressBarList.append( [row,left,right] )
        
        self._height += 19
        
        cmds.window( self._winName, e=1, h=self._height )
        
        
    def show(self):
        
        if cmds.window( self._winName, ex=1 ):
            cmds.deleteUI( self._winName, wnd=1 )
        cmds.window( self._winName, title = self._title )
        
        self._mainLayout = cmds.columnLayout()
        
        cmds.window( self._winName, e=1, w=self._width, h=self._height )
        cmds.showWindow( self._winName )


    def hide(self):
        cmds.deleteUI( self._winName )