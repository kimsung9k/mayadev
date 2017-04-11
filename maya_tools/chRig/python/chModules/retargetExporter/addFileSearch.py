import maya.cmds as cmds
import mainInfo



class Cmd:
    
    def __init__(self):
        
        pass




class Add( Cmd ):

    def __init__(self ):
        
        self._sideWidth = 7
        self._width = mainInfo.fileWidth - self._sideWidth*2 - 2
        
        self.core()
        
        Cmd.__init__( self )

    
    def core(self):
        
        buttonWidth = 50
        fieldWidth = self._width - buttonWidth
        cmds.rowColumnLayout( nc=4, cw=[(1,self._sideWidth),
                                        (2,fieldWidth),
                                        (3,buttonWidth),
                                        (4,self._sideWidth)] )
        mainInfo.setSpace()
        self._searchField = cmds.textField( )
        cmds.button( l='search' )
        mainInfo.setSpace()
        cmds.setParent( '..' )
        
        mainInfo.setSpaceH(10)
        
        addSideWidth = 20
        resizeWidth = self._width - addSideWidth*2
        firstWidth  = resizeWidth*0.37
        secondWidth = resizeWidth*0.42
        thirdWidth  = resizeWidth - firstWidth - secondWidth
        cmds.rowColumnLayout( nc=5, cw=[(1,self._sideWidth+addSideWidth),
                                        (2,firstWidth),
                                        (3,secondWidth),
                                        (4,thirdWidth),
                                        (5,self._sideWidth+addSideWidth)] )
        self._fileTypeCollection = cmds.radioCollection()
        mainInfo.setSpace()
        cmds.radioButton( l='Motion File', sl=1 )
        cmds.radioButton( l='Human IK File' )
        cmds.radioButton( l='All' )
        mainInfo.setSpace()
        cmds.setParent( '..' )
        
        mainInfo.setSpaceH( 10 )
        
        cmds.rowColumnLayout( nc=3, cw=[(1,self._sideWidth),
                                        (2,self._width),
                                        (3,self._sideWidth) ] )
        mainInfo.setSpace()
        self._fileNameScrollList = cmds.textScrollList( ams=1 )
        mainInfo.setSpace()
        cmds.setParent( '..' )