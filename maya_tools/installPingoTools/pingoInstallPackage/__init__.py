#coding=utf8

from PySide import QtGui, QtCore
from PySide.QtGui import QListWidgetItem, QDialog, QListWidget, QMainWindow, QWidget, QColor, QLabel,\
    QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QAbstractItemView, QMenu,QCursor, QMessageBox, QBrush, QSplitter,\
    QScrollArea, QSizePolicy, QTextEdit, QApplication, QFileDialog, QCheckBox, QDoubleValidator, QSlider, QIntValidator,\
    QImage, QPixmap, QTransform, QPaintEvent, QTabWidget, QFrame, QTreeWidgetItem, QTreeWidget, QComboBox, QGroupBox, QAction,\
    QFont, QGridLayout



import os


class UI_Form( QMainWindow ):

    def __init__(self, *args, **kwargs ):
        
        QMainWindow.__init__( self, *args, **kwargs )
        self.installEventFilter( self )
        self.setWindowTitle( "  PingoTools Installer" )
        self.setWindowIcon( QtGui.QIcon( os.path.dirname( __file__ ) + '/images/letter-p.png')  )
        self.resize( 518, 400 )
        
        self.mainWidget = QWidget()
        self.setCentralWidget( self.mainWidget )
        self.mainLayout = QVBoxLayout()
        self.mainWidget.setLayout( self.mainLayout )
        
        self.firstPage()
        


    def firstPage(self):
        
        for i in range( self.mainLayout.count() ):
            item = self.mainLayout.itemAt(0)
            item.widget().setParent( None )
        
        title = QLabel( "<p style='color:rgb( 137,129,120 )'>Welcome to the PingoTools Installer</p>" )
        title.setFixedHeight( 50 )
        titleFont  = QFont()
        titleFont.setPixelSize( 18 )
        titleFont.setBold( True )
        titleFont.setFamily( "Helvetica [Cronyx]" )
        title.setAlignment( QtCore.Qt.AlignCenter )
        title.setFont( titleFont )
        
        description = QLabel()
        description.setAlignment( QtCore.Qt.AlignCenter )
        
        buttonsWidget = QWidget(); buttonsWidget.setMaximumHeight( 50 )
        buttonsLayout = QHBoxLayout( buttonsWidget )
        emptyArea = QLabel()
        buttonNext = QPushButton( 'Next > ' )
        buttonCancel = QPushButton( 'Cancel' )
        buttonsLayout.addWidget( emptyArea )
        buttonsLayout.addWidget( buttonNext ); buttonNext.setFixedWidth( 100 )
        buttonsLayout.addWidget( buttonCancel ); buttonCancel.setFixedWidth( 100 )
        
        self.mainLayout.addWidget( title )
        self.mainLayout.addWidget( description )
        self.mainLayout.addWidget( buttonsWidget )
        
        origWidth = 500

        frontImage = QImage()
        frontImage.load( os.path.dirname( __file__ ) + '/images/pingoTools_main.jpg' )
        trValue = QTransform().scale( float(origWidth)/frontImage.width(), float(origWidth)/frontImage.width() )
        transformedImage = frontImage.transformed( trValue )
        pixmap     = QPixmap.fromImage( transformedImage )
        description.setPixmap( pixmap )
        description.setGeometry( 0,0, transformedImage.width() , transformedImage.height() )
        description.paintEvent(QPaintEvent(QtCore.QRect( 0,0,self.width(), self.height() )))
        
        QtCore.QObject.connect( buttonNext, QtCore.SIGNAL( 'clicked()' ), self.secondPage )
        QtCore.QObject.connect( buttonCancel, QtCore.SIGNAL( 'clicked()' ), self.cmd_cancel )
    



    def secondPage(self):
        
        for i in range( self.mainLayout.count() ):
            item = self.mainLayout.itemAt(0)
            item.widget().setParent( None )
        
        title = QLabel( "설치할 플러그인을 선택하십시오.".decode( 'utf-8' ) )
        title.setFixedHeight( 50 )
        
        listWidget = QListWidget()
        listWidget.setFixedHeight( 273 )
        widgetItem_for2015 = QListWidgetItem("PingoTools for Maya2015", listWidget )
        widgetItem_for2016 = QListWidgetItem("PingoTools for Maya2016", listWidget )
        widgetItem_for2017 = QListWidgetItem("PingoTools for Maya2017", listWidget )
        
        widgetItem_for2015.setCheckState( QtCore.Qt.Checked )
        widgetItem_for2016.setCheckState( QtCore.Qt.Checked )
        widgetItem_for2017.setCheckState( QtCore.Qt.Checked )
        #widgetItem_for2015.setFlags( not QtCore.Qt.ItemIsSelectable )
        
        buttonsWidget = QWidget(); buttonsWidget.setMaximumHeight( 50 )
        buttonsLayout = QHBoxLayout( buttonsWidget )
        emptyArea = QLabel()
        buttonBack = QPushButton( 'Back < ' )
        buttonNext = QPushButton( 'Install' )
        buttonCancel = QPushButton( 'Cancel' )
        buttonsLayout.addWidget( emptyArea )
        buttonsLayout.addWidget( buttonBack ); buttonBack.setFixedWidth( 100 )
        buttonsLayout.addWidget( buttonNext ); buttonNext.setFixedWidth( 100 )
        buttonsLayout.addWidget( buttonCancel ); buttonCancel.setFixedWidth( 100 )
        
        self.mainLayout.addWidget( title )
        self.mainLayout.addWidget( listWidget )
        self.mainLayout.addWidget( buttonsWidget )
        
        QtCore.QObject.connect( buttonBack, QtCore.SIGNAL( 'clicked()' ), self.firstPage )
        QtCore.QObject.connect( buttonNext, QtCore.SIGNAL( 'clicked()' ), self.lastPage )
        QtCore.QObject.connect( buttonCancel, QtCore.SIGNAL( 'clicked()' ), self.cmd_cancel )




    def installPage(self):
        
        for i in range( self.mainLayout.count() ):
            item = self.mainLayout.itemAt(i)
            item.widget().setParent( None )
        pass    
    



    def lastPage(self):
        
        for i in range( self.mainLayout.count() ):
            item = self.mainLayout.itemAt(0)
            item.widget().setParent( None )
        
        title = QLabel( "".decode( 'utf-8' ) )
        title.setFixedHeight( 50 )
        
        description = QLabel( "<p style='line-height:150%';'><b>PingoTools</b> 인스톨이 완료되었습니다.<p>".decode( 'utf-8' ) )
        description.setAlignment( QtCore.Qt.AlignCenter )
        
        buttonsWidget = QWidget(); buttonsWidget.setMaximumHeight( 50 )
        buttonsLayout = QHBoxLayout( buttonsWidget )
        emptyArea = QLabel()
        buttonClose = QPushButton( 'Close' ); buttonClose.setFixedWidth( 100 )
        buttonsLayout.addWidget( emptyArea )
        buttonsLayout.addWidget( buttonClose )
        
        self.mainLayout.addWidget( title )
        self.mainLayout.addWidget( description )
        self.mainLayout.addWidget( buttonsWidget )
        
        QtCore.QObject.connect( buttonClose, QtCore.SIGNAL( 'clicked()' ), self.cmd_close )




    def cmd_cancel(self):
        
        messageBox = QMessageBox( self )
        messageBox.setModal( True )
        messageBox.setWindowTitle( "설치 취소".decode( 'utf-8' ))
        messageBox.setText( "설치를 취소하시겠습니까?".decode( 'utf-8' ) )
        messageBox.setStandardButtons( QMessageBox.Yes| QMessageBox.No )
        messageBox.setDefaultButton( QMessageBox.Yes )
        result = messageBox.exec_()
        
        if result == QMessageBox.Yes:
            cancelWaningMessageBox = QMessageBox( self )
            cancelWaningMessageBox.setModal( True )
            cancelWaningMessageBox.setWindowTitle( "취소완료".decode( 'utf-8' ) )
            cancelWaningMessageBox.setText( "설치가 취소되었습니다.".decode( 'utf-8' ) )
            cancelWaningMessageBox.setStandardButtons( QMessageBox.Ok )
            result = cancelWaningMessageBox.exec_()
            self.close()
        else:
            pass
    
    
    def cmd_close(self):
        
        self.close()
        
        


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication( sys.argv )
    ui = UI_Form()
    ui.show()
    print ui.width(), ui.height()
    sys.exit( app.exec_() )

