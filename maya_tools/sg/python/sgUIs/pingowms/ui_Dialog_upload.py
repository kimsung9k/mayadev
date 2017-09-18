#coding=utf8

from ui_ControlBase import *


class Window_upload( QtGui.QMainWindow ):
    
    objectName = 'ui_pingowms_upload'
    title = "업로드".decode('utf-8')
    defaultWidth  = 450
    defaultHeight = 500
    
    def __init__(self, *args, **kwargs ):
        
        args = tuple( [ControlBase.mayawin] )
        
        QtGui.QMainWindow.__init__( self, *args, **kwargs )
        self.installEventFilter( self )
        self.setWindowTitle( Window_upload.title )
        self.resize( Window_upload.defaultWidth, Window_upload.defaultHeight )

        widgetVLayoutWorks = QtGui.QWidget()
        self.setCentralWidget(widgetVLayoutWorks)



    def saveUIInfo( self ):
        ControlBase.makeFile( ControlBase.uiInfoPath )
        f = open( ControlBase.uiInfoPath, 'r' )
        try:data = json.load( f )
        except:data = {}
        f.close()
        
        manageProjectWindowDict = {}
        manageProjectWindowDict['size'] = [ self.width(), self.height() ]
        
        data[ 'manageProjectWindow' ] = manageProjectWindowDict
        
        f = open( ControlBase.uiInfoPath, 'w' )
        json.dump( data, f )
        f.close()
        


    def loadUIInfo( self ):
        ControlBase.makeFile( ControlBase.uiInfoPath )
        f = open( ControlBase.uiInfoPath, 'r' )
        try:data = json.load( f )
        except:data = {}
        f.close()
        if not data.items():
            ControlBase.mainui.resize( self.defaultWidth, self.defaultHeight )
            return
        
        try:
            width, height = data['manageProjectWindow']['size']
            pWidth, pHeight = data['mainWindow']['size']
        except:
            return
        
        x = ControlBase.mainui.x() + ControlBase.mainui.width() + 5
        y = ControlBase.mainui.y()
        self.move( x, y )
        self.resize( width, pHeight )
        
        self.lineEdit_projectName.setText( ControlBase.getCurrentProjectName() )
        TreeWidgetCmds.updateTaskList(self.workTreeWidget, False)
        


    def eventFilter( self, *args, **kwargs):
        event = args[1]
        if event.type() in [ QtCore.QEvent.Resize, QtCore.QEvent.Move ]:
            self.saveUIInfo()



