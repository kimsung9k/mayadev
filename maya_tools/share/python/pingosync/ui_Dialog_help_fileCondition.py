#coding=utf8

import Models
from __qtImport import *


class Dialog_help_fileCondition( QDialog ):
    
    objectName = 'ui_pingowm_help_fileCondition'
    title = "파일상태정보".decode('utf-8')
    defaultWidth= 450
    defaultHeight = 50
    
    def __init__(self, *args, **kwargs ):
        
        if not args: args = tuple( [Models.ControlBase.mayawin] )
        
        QDialog.__init__( self, *args, **kwargs )
        self.installEventFilter( self )
        self.setWindowTitle( Dialog_help_fileCondition.title )
        self.resize( Dialog_help_fileCondition.defaultWidth, Dialog_help_fileCondition.defaultHeight )
        
        mainLayout = QVBoxLayout(self)
        localOnly_icon = QLabel()
        localOnly_label = QLabel( "로컬에만 존제".decode( 'utf-8' ) )
        localOnly_icon.setStyleSheet('background-color:red')
        
        localOnly_layout = QHBoxLayout()
        localOnly_layout.addWidget( localOnly_icon )
        localOnly_layout.addWidget( localOnly_label )
        mainLayout.addLayout( localOnly_layout )