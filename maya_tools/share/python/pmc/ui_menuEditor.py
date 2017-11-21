#coding=utf8

import maya.cmds as cmds
import maya.OpenMayaUI
from functools import partial
import ntpath
import shutil
from commands import *



class Model:

    folderColor = QColor( 235, 220, 170 )
    fileColor = QColor( 200, 200, 200 )
        


class Cmds():
    
    @staticmethod
    def renamePaths( orderedTargetPaths ):
        
        renameTargets = []
        for i in range( len( orderedTargetPaths ) ):
            if ntpath.split( orderedTargetPaths[i] )[-1].split( '.' )[0].isdigit():
                extension = os.path.splitext( orderedTargetPaths[i] )[-1]
                renameTargets.append( orderedTargetPaths[i] )
            else:
                renameTargets.append( None )
        
        tempTargets = []
        for i in range( len( renameTargets ) ):
            tempTargets.append( None )
            if not renameTargets[i]: continue
            folderName, fileName = ntpath.split( renameTargets[i] )
            fileSplits = [ splitName for splitName in fileName.split( '.' ) if splitName ]
            replacedFileName = '%02d..' % (i+1) + '.'.join( fileSplits[1:] )
            tempName = folderName + '/' + replacedFileName
            try:
                os.rename( renameTargets[i], tempName )
                tempTargets[-1] = tempName
            except:
                pass
            
        
        resultNames = []
        for i in range( len( tempTargets ) ):
            if not tempTargets[i]:
                resultNames.append( None )
                continue
            folderName, fileName = ntpath.split( tempTargets[i] )
            fileSplits = [ splitName for splitName in fileName.split( '.' ) if splitName ]
            replacedFileName = '%02d.' % (i+1) + '.'.join( fileSplits[1:] )
            resultName = folderName + '/' + replacedFileName
            try:
                os.rename( tempTargets[i], resultName )
                resultNames.append( resultName )
            except:
                print "failed to rename : ", resultName
                resultNames.append( None )
        
        return resultNames


    @staticmethod
    def makeFolder( pathName ):
    
        if os.path.exists( pathName ):return None
        os.makedirs( pathName )
        return pathName
    
    
    @staticmethod
    def makeFile( filePath ):
        if os.path.exists( filePath ): return None
        filePath = filePath.replace( "\\", "/" )
        splits = filePath.split( '/' )
        folder = '/'.join( splits[:-1] )
        Cmds.makeFolder( folder )
        f = open( filePath, "w" )
        f.close()
    
    @staticmethod
    def getCleanNameFromPath( targetPath ):
        
        folderPath, itemName = ntpath.split( targetPath )
        if os.path.isdir(targetPath):
            return '.'.join( [ split for split in itemName.split( '.' ) if not split.isdigit() ] )
        elif os.path.isfile( targetPath ):
            itemName = os.path.splitext( itemName )[0]
            return '.'.join( [ split for split in itemName.split( '.' ) if not split.isdigit() ] )
    
    
    @staticmethod
    def getSeparatedRPAndRPPosition( cleanName ):
        
        print cleanName
    
    
    
    @staticmethod
    def loadMenuList( targetPath, menuHIndex ):
        
        removeTargetWidgets = []
        for i in range( menuHIndex, Window.mainui.layoutListWidget.count() ):
            removeTargetWidgets.append( Window.mainui.layoutListWidget.itemAt( i ).widget() )
        
        for removeTargetWidget in removeTargetWidgets:
            removeTargetWidget.setParent( None )
        
        listWidget = MenuListWidget( targetPath )
        listWidget.setSizePolicy( Window.mainui.listWidgetSizePolicy )
        Window.mainui.layoutListWidget.addWidget( listWidget )
        listWidget.loadMenu()
        
        def cmd_itemClickedEvent( *args ):
            listWidgetItem = args[0]
            listWidget = listWidgetItem.listWidget()
            if os.path.isfile( listWidgetItem.targetPath ):
                Cmds.showScript( listWidgetItem.targetPath, listWidget.menuHIndex+1 )
            elif os.path.isdir( listWidgetItem.targetPath ):
                listWidget.nextWidget = Cmds.loadMenuList( listWidgetItem.targetPath, listWidget.menuHIndex+1 )
        
        listWidget.itemClicked.connect( cmd_itemClickedEvent )
        listWidget.menuHIndex = menuHIndex
        Window.mainui.scriptTextEdit.setText( "" )
        Window.mainui.setButtonDisabled()
        
        return listWidget
        


    @staticmethod
    def showScript( targetPath, menuHIndex ):
        
        removeTargetWidgets = []
        for i in range( menuHIndex, Window.mainui.layoutListWidget.count() ):
            removeTargetWidgets.append( Window.mainui.layoutListWidget.itemAt( i ).widget() )
        
        for removeTargetWidget in removeTargetWidgets:
            removeTargetWidget.setParent( None )
        
        if not os.path.exists( targetPath ) or not os.path.isfile( targetPath ): return None
        f = open( targetPath, 'r' )
        data = f.read()
        f.close()
        Window.mainui.scriptTextEdit.setText( data.decode( 'utf-8') )
        Window.mainui.setButtonDisabled()
        
        Window.mainui.currentScriptPath = targetPath
        Window.mainui.defaultTextValue = data
        Window.mainui.currentMenuHIndex = menuHIndex





class MenuItemWidget( QListWidgetItem ):
    
    def __init_(self, *args, **kwargs ):
        QListWidgetItem.__init__( self, *args, **kwargs )




class Dialog_create( QDialog ):
    
    def __init__(self, parent, title, **kwargs ):
        
        QDialog.__init__( self, parent, **kwargs )
        
        self.setWindowTitle( title )
        self.resize(300,50)
        self.setModal(True)
        
        layoutMain = QVBoxLayout( self )
        layoutLabel = QHBoxLayout()
        layoutButtons  = QHBoxLayout()
        
        label = QLabel( "Name : " )
        lineEdit = QLineEdit()
        layoutLabel.addWidget( label )
        layoutLabel.addWidget( lineEdit )
        
        buttonCreate = QPushButton( 'Create' )
        buttonClose = QPushButton( 'Close' )
        layoutButtons.addWidget( buttonCreate )
        layoutButtons.addWidget( buttonClose )
        
        layoutMain.addLayout( layoutLabel )
        layoutMain.addLayout( layoutButtons )
        
        self.buttonCreate = buttonCreate
        self.buttonClose = buttonClose
        self.lineEdit = lineEdit
        
        QtCore.QObject.connect( buttonClose, QtCore.SIGNAL('clicked()'), self.close )
        QtCore.QObject.connect( buttonCreate, QtCore.SIGNAL('clicked()'), self.create )
        QtCore.QObject.connect( lineEdit, QtCore.SIGNAL('returnPressed()'), self.create )
    
        self.lineEdit = lineEdit
        self.createCmd = None
    
    
    def assignCreateCmd(self, targetCmd ):
    
        self.createCmd = targetCmd
    
    
    def create(self):
        
        self.createCmd()


    def getLineEditWidget(self):
        
        return self.lineEdit


    def getButtonCreateWidget(self):
        
        return self.buttonCreate        
    
    


class MenuListWidget( QListWidget ):


    def __init__(self, basePath, **kwargs ):
        
        QListWidget.__init__( self, *[], **kwargs )
        
        self.basePath = basePath
        self.setDragDropMode( QAbstractItemView.InternalMove )
        self.setDragDropOverwriteMode(True)
        self.installEventFilter( self )
        
        self.setContextMenuPolicy( QtCore.Qt.CustomContextMenu )
        QtCore.QObject.connect( self, QtCore.SIGNAL('customContextMenuRequested(QPoint)'),  self.loadContextMenu )
    

    def setRadialPositionName(self, rp ):
        
        for selItem in self.selectedItems():
            MenuName.setRadialPositionName( selItem.targetPath, rp )
        self.loadMenu()
        try: self.nextWidget.setParent( None )
        except: pass
    
    
    def removeRadialPositionName(self):
        
        for selItem in self.selectedItems():
            MenuName.removeRadialPositionName( selItem.targetPath )
        self.loadMenu()
        try: self.nextWidget.setParent( None )
        except: pass


    def loadContextMenu(self):
        
        menu = QMenu( self )
        menu.addAction( "Add Separator".decode( "utf-8" ), self.addSeparator )
        menu.addAction( "Add Label Separator".decode( "utf-8" ), self.addLabelSeparator )
        menu.addSeparator()
        radialMenu = menu.addMenu( "Set Radial Position" )
        radialMenu.addAction( "Top", partial( self.setRadialPositionName, 'N' ) )
        radialMenu.addAction( "Right", partial( self.setRadialPositionName, 'E' ) )
        radialMenu.addAction( "Left", partial( self.setRadialPositionName, 'W' ) )
        radialMenu.addAction( "Bottom", partial( self.setRadialPositionName, 'S' ) )
        radialMenu.addSeparator()
        radialMenu.addAction( "Top Right", partial( self.setRadialPositionName, 'NE' ) )
        radialMenu.addAction( "Top Left", partial( self.setRadialPositionName, 'NW' ) )
        radialMenu.addAction( "Bottom Right", partial( self.setRadialPositionName, 'SE' ) )
        radialMenu.addAction( "Bottom Left", partial( self.setRadialPositionName, 'SW' ) )
        radialMenu.addSeparator()
        radialMenu.addAction( "Remove Radial Position", self.removeRadialPositionName )
        menu.addSeparator()
        menu.addAction( "Add File( python )".decode( 'utf-8' ), self.addFile_python )
        menu.addAction( "Add File( mel )".decode( 'utf-8' ), self.addFile_mel )
        menu.addAction( "Add Folder".decode( 'utf-8' ), self.addFolder )
        menu.addSeparator()
        menu.addAction( "Rename Target".decode( 'utf-8' ), self.renameTarget )
        menu.addAction( "Delete Target".decode( 'utf-8' ), self.removeTarget )
        pos = QCursor.pos()
        point = QtCore.QPoint( pos.x()+10, pos.y() )
        menu.exec_( point )
    


    def addFile_python(self):
    
        dialog = Dialog_create( self, 'Add Python File' )
        dialog.show()
        
        def cmd_create():
            textValue = dialog.getLineEditWidget().text()
            
            createIndex = 99
            if not textValue:
                msgBox = QMessageBox(dialog)
                msgBox.setWindowTitle( "Warning" )
                msgBox.setText("이름을 입력하세요.".decode( 'utf-8' ) )
                msgBox.exec_()
                return
            else:
                sepName = '%s'.decode( 'utf-8' ) % textValue
            for selItem in self.selectedItems():
                selItemPath = selItem.targetPath
                selItemName = ntpath.split( selItemPath )[-1]
                splits = selItemName.split( '.' )
                if len( splits[0] ) == 2 and splits[0].isdigit():
                    createIndex = int( splits[0] )+1
            
            sepFileName = '%02d.' % createIndex + sepName + '.py'
            sepFilePath = self.basePath + '/' + sepFileName
            Cmds.makeFile( sepFilePath )
            
            self.loadMenu()
            dialog.close()

        dialog.assignCreateCmd(cmd_create)



    def addFile_mel(self):
        
        dialog = Dialog_create( self, 'Add Mel File' )
        dialog.show()
        
        def cmd_create():
            textValue = dialog.getLineEditWidget().text()
            
            createIndex = 99
            if not textValue:
                msgBox = QMessageBox(dialog)
                msgBox.setWindowTitle( "Warning" )
                msgBox.setText("이름을 입력하세요.".decode( 'utf-8' ) )
                msgBox.exec_()
                return
            else:
                sepName = '%s'.decode( 'utf-8' ) % textValue
            for selItem in self.selectedItems():
                selItemPath = selItem.targetPath
                selItemName = ntpath.split( selItemPath )[-1]
                splits = selItemName.split( '.' )
                if len( splits[0] ) == 2 and splits[0].isdigit():
                    createIndex = int( splits[0] )+1
            
            sepFileName = '%02d.' % createIndex + sepName + '.mel'
            sepFilePath = self.basePath + '/' + sepFileName
            Cmds.makeFile( sepFilePath )
            
            self.loadMenu()
            dialog.close()

        dialog.assignCreateCmd(cmd_create)
    


    def addFolder(self):
        
        dialog = Dialog_create( self, 'Add Folder' )
        dialog.show()
        
        def cmd_create():
            textValue = dialog.getLineEditWidget().text()
            
            createIndex = 99
            if not textValue:
                msgBox = QMessageBox(dialog)
                msgBox.setWindowTitle( "Warning" )
                msgBox.setText("이름을 입력하세요.".decode( 'utf-8' ) )
                msgBox.exec_()
                return
            else:
                sepName = '%s'.decode( 'utf-8' ) % textValue
            for selItem in self.selectedItems():
                selItemPath = selItem.targetPath
                selItemName = ntpath.split( selItemPath )[-1]
                splits = selItemName.split( '.' )
                if len( splits[0] ) == 2 and splits[0].isdigit():
                    createIndex = int( splits[0] )+1
            
            sepFileName = '%02d.' % createIndex + sepName
            sepFilePath = self.basePath + '/' + sepFileName
            Cmds.makeFolder( sepFilePath )
            
            self.loadMenu()
            dialog.close()

        dialog.assignCreateCmd(cmd_create)



    def addSeparator(self):
        
        createIndex = 99
        sepName = '# ---------------'
        for selItem in self.selectedItems():
            selItemPath = selItem.targetPath
            selItemName = ntpath.split( selItemPath )[-1]
            splits = selItemName.split( '.' )
            if len( splits[0] ) == 2 and splits[0].isdigit():
                createIndex = int( splits[0] )+1
        
        sepFileName = '%02d.' % createIndex + sepName + '.txt'
        sepFilePath = self.basePath + '/' + sepFileName
        Cmds.makeFile( sepFilePath )
        
        self.loadMenu()



    def addLabelSeparator(self):
        
        dialog = Dialog_create( self, 'Add Separator' )
        dialog.show()
        
        def cmd_create():
            textValue = dialog.getLineEditWidget().text()
            
            createIndex = 99
            sepName = ''
            if not textValue:
                sepName = '# ---------------'
            else:
                sepName = '#------%s------'.decode( 'utf-8' ) % textValue
            for selItem in self.selectedItems():
                selItemPath = selItem.targetPath
                selItemName = ntpath.split( selItemPath )[-1]
                splits = selItemName.split( '.' )
                if len( splits[0] ) == 2 and splits[0].isdigit():
                    createIndex = int( splits[0] )+1
            
            sepFileName = '%02d.' % createIndex + sepName + '.txt'
            sepFilePath = self.basePath + '/' + sepFileName
            Cmds.makeFile( sepFilePath )
            
            self.loadMenu()
            dialog.close()

        QtCore.QObject.connect( dialog.getButtonCreateWidget(), QtCore.SIGNAL('clicked()'), cmd_create )

    
    def loadMenu(self):
        
        for i in range(self.count()):
            self.takeItem(0)
        
        items = []
        for root, dirs, names in os.walk( self.basePath ):
            if dirs:items += [ [dirname, root + '/' + dirname] for dirname in dirs ]
            if names:items += [ [filename, root + '/' + filename] for filename in names ]
            break
        items.sort()
        items = filter( lambda x:x[0], [ [StringEdit.convertFilenameToMenuname(shortname), fullname] for shortname, fullname in items] )
        
        resultNames = Cmds.renamePaths( [fullName for shortName, fullName in items ] )
        
        for i in range( len( items ) ):
            items[i][1] = resultNames[i]
        
        for shortname, fullname in items:
            self.addItem( shortname, fullname )
        self.setFixedWidth( self.sizeHintForColumn(0)+20 )
    
    

    def addItem(self, shortName, fullName ):
        
        if not fullName: return None
        widgetItem = MenuItemWidget( shortName, self )
        if os.path.isdir( fullName ):
            brush = QBrush( Model.folderColor )
        else:
            brush = QBrush( Model.fileColor )
        widgetItem.setForeground( brush )
        widgetItem.targetPath = fullName
    
    
    
    def renameTarget(self):
        
        if not self.selectedItems():
            return None
        
        editNameType = 'file'
        selItem = self.selectedItems()[0]
        
        cleanName = Cmds.getCleanNameFromPath(selItem.targetPath)
        if cleanName[0] == '#':
            editNameType = 'separator'
        elif os.path.isdir( selItem.targetPath ):
            editNameType = 'folder'
        
        dialog = QDialog( self )
        dialog.setWindowTitle( "Rename target" )
        dialog.resize( 300, 50 )
        
        layout = QVBoxLayout( dialog )
        
        layout_name = QHBoxLayout()
        label_name = QLabel( 'Target Name : ' )
        lineEdit_name = QLineEdit(); lineEdit_name.setText( cleanName )
        layout_name.addWidget( label_name )
        layout_name.addWidget( lineEdit_name )
        
        layout_buttons = QHBoxLayout()
        button_rename = QPushButton( 'Rename' )
        button_close  = QPushButton( 'Close' )
        layout_buttons.addWidget( button_rename )
        layout_buttons.addWidget( button_close )
        
        layout.addLayout( layout_name )
        layout.addLayout( layout_buttons )
        dialog.show()
        
        def cmd_rename():
            targetName = lineEdit_name.text()
            dirName = os.path.dirname( selItem.targetPath )
            fileName = ntpath.split( selItem.targetPath )[-1]
            index = fileName.split( '.' )[0]
            if os.path.isfile( selItem.targetPath ):
                ext = os.path.splitext( selItem.targetPath )[-1]
                resultPath = dirName + '/' + index + '.' + targetName + ext
            else:
                resultPath = dirName + '/' + index + '.' + targetName
            os.rename( selItem.targetPath, resultPath )
            dialog.close()
            Cmds.loadMenuList( os.path.dirname( selItem.targetPath ), self.menuHIndex )
        
        def cmd_close():
            dialog.close()
        
        QtCore.QObject.connect( button_rename, QtCore.SIGNAL( 'clicked()' ), cmd_rename )
        QtCore.QObject.connect( button_close,  QtCore.SIGNAL( 'clicked()' ), cmd_close )
        


    def removeTarget(self):
        
        itemType= None
        if not self.selectedItems():
            return None
        
        for selItem in self.selectedItems():
            if os.path.isdir( selItem.targetPath ):
                itemType = '폴더'.decode( 'utf-8' )
            else:
                f = open( selItem.targetPath, 'r' )
                data = f.read()
                f.close()
                if not data:
                    os.remove( selItem.targetPath )
                    self.loadMenu()
                else:
                    itemType = '파일'.decode( 'utf-8' )
        
        if itemType:
            dialog = QDialog( self )
            dialog.setWindowTitle( "Remove target" )
            dialog.resize( 300, 50 )
            
            layout = QVBoxLayout( dialog )
            label = QLabel( "해당 %s를 삭제하시겠습니까?".decode( 'utf-8' ) % itemType )
            
            layoutButtons = QHBoxLayout()
            buttonOk     = QPushButton( '삭제'.decode( 'utf-8' ) )
            buttonCancel = QPushButton( '취소'.decode( 'utf-8' ) )
            layoutButtons.addWidget( buttonOk )
            layoutButtons.addWidget( buttonCancel )
            layout.addWidget( label )
            layout.addLayout( layoutButtons )
            
            def cmd_remove():
                if os.path.isfile( selItem.targetPath ):
                    os.remove( selItem.targetPath )
                elif os.path.isdir( selItem.targetPath ):
                    shutil.rmtree( selItem.targetPath )
                
                try: self.nextWidget.setParent( None )
                except: pass
                self.loadMenu()
                dialog.close()
            
            def cmd_cancel():
                dialog.close()
            
            dialog.show()
            
            QtCore.QObject.connect( buttonOk, QtCore.SIGNAL( 'clicked()' ), cmd_remove )
            QtCore.QObject.connect( buttonCancel, QtCore.SIGNAL( 'clicked()' ), cmd_cancel )


    def dragEnterEvent( self, *args, **kwargs ):
        QListWidget.dragEnterEvent( self, *args )


    
    def dragLeaveEvent(self, *args, **kwargs ):
        QListWidget.dragLeaveEvent( self, *args )


    
    def dropEvent(self, *args, **kwargs ):    
        
        QListWidget.dropEvent( self, *args )
        orderedPaths = []
        for i in range( self.count() ):
            orderedPaths.append( self.item(i).targetPath )
        Cmds.renamePaths( orderedPaths )
        self.loadMenu()
        
        




class Window( QMainWindow ):
    
    mayaWin = shiboken.wrapInstance( long( maya.OpenMayaUI.MQtUtil.mainWindow() ), QWidget )
    objectName = "sg_menuEditor"
    title = "UI - Menu Editor"
    defaultWidth = 600
    defaultHeight = 600
    
    infoBaseDir = cmds.about( pd=1 ) + "/sg/menuEditor"
    uiInfoPath = infoBaseDir + '/uiInfo.json'
    defaultMenuPath = infoBaseDir + '/defaultMenuPath.txt'
    defaultSearchPath = infoBaseDir + '/defaultSearchPath.txt'
    
    mainui = None


    def __init__(self, *args, **kwargs ):
        
        Window.mainui = self
        
        QMainWindow.__init__( self, *args, **kwargs )
        self.installEventFilter( self )
        
        self.centralWidget = QWidget()
        self.setCentralWidget( self.centralWidget )
        self.setWindowFlags(QtCore.Qt.Dialog)
        
        self.layoutBase = QVBoxLayout( self.centralWidget )
        
        layout_menuPath   = QHBoxLayout()
        label_menuPath    = QLabel( "Menu path" )
        lineEdit_menuPath = QLineEdit()
        button_menuPath = QPushButton( '...' )
        [ layout_menuPath.addWidget( widget ) for widget in [label_menuPath,lineEdit_menuPath,button_menuPath] ]
        
        splitter = QSplitter( QtCore.Qt.Vertical )
        splitter.setStretchFactor(1,1)
        
        scrollArea = QScrollArea()
        listWidgetSizePolicy = QSizePolicy()
        listWidgetSizePolicy.setVerticalPolicy( QSizePolicy.Preferred )
        listWidgetSizePolicy.setHorizontalPolicy( QSizePolicy.Maximum )
        
        layoutMenuListWidget = QWidget()
        layoutListWidgetAndEmpty = QHBoxLayout( layoutMenuListWidget )
        layoutListWidgetAndEmpty.setContentsMargins(1,1,1,1)
        layoutListWidget = QHBoxLayout()
        layoutListWidget.setContentsMargins(1,1,1,1)
        widgetEmpty = QWidget()
        layoutListWidgetAndEmpty.addLayout( layoutListWidget )
        layoutListWidgetAndEmpty.addWidget( widgetEmpty )
        
        scrollArea.setWidget( layoutMenuListWidget )
        scrollArea.setWidgetResizable( True )
        
        layoutScriptWidget = QWidget()
        layoutScript = QHBoxLayout( layoutScriptWidget );layoutScript.setContentsMargins(1,1,1,1)
        scriptTextEdit = QTextEdit()
        layoutScriptSave = QVBoxLayout(); layoutScriptSave.setContentsMargins(1,1,1,1)
        buttonSave = QPushButton( "Save" ); buttonSave.setEnabled(False)
        buttonDefault = QPushButton( "Load Default" ); buttonDefault.setEnabled(False)
        labelEmpty = QLabel()
        layoutScriptSave.addWidget( buttonSave )
        layoutScriptSave.addWidget( buttonDefault )
        layoutScriptSave.addWidget( labelEmpty )
        layoutScript.addWidget( scriptTextEdit )
        layoutScript.addLayout( layoutScriptSave )
        
        splitter.addWidget( scrollArea )
        splitter.addWidget( layoutScriptWidget )
        
        buttonReload = QPushButton( "Reload" )
        
        self.layoutBase.addLayout( layout_menuPath )
        self.layoutBase.addWidget( splitter )
        self.layoutBase.addWidget( buttonReload )        
        splitter.setSizes( [100,100] )

        
        QtCore.QObject.connect( button_menuPath, QtCore.SIGNAL( 'clicked()'), self.getMenuPath )
        QtCore.QObject.connect( scriptTextEdit, QtCore.SIGNAL( 'textChanged()' ), self.setButtonEnabled )
        QtCore.QObject.connect( buttonSave, QtCore.SIGNAL( 'clicked()' ), self.saveScript )
        QtCore.QObject.connect( buttonDefault, QtCore.SIGNAL( 'clicked()' ), self.loadDefaultScript )
        QtCore.QObject.connect( buttonReload, QtCore.SIGNAL( 'clicked()' ), loadMenu )
    
        self.layoutListWidget  = layoutListWidget
        self.lineEdit_menuPath = lineEdit_menuPath
        self.listWidgetSizePolicy = listWidgetSizePolicy
        self.scriptTextEdit = scriptTextEdit
        self.buttonSave = buttonSave
        self.buttonDefault = buttonDefault

    


    def show(self, *args, **kwangs ):
        
        self.loadUIInfo()
        self.lineEdit_menuPath.setText( FileAndPaths.getStringDataFromFile( Window.defaultMenuPath ) )
        if os.path.exists( self.lineEdit_menuPath.text() ):
            Cmds.loadMenuList( self.lineEdit_menuPath.text(), 0 )
        QMainWindow.show( self, *args, **kwangs )



    def eventFilter(self, *args, **kwargs ):
        event = args[1]
        if event.type() in [ QtCore.QEvent.Resize, QtCore.QEvent.Move ]:
            self.saveUIInfo()



    def saveUIInfo( self ):
        
        FileAndPaths.makeFile( Window.uiInfoPath )
        f = open( Window.uiInfoPath, 'r' )
        try:data = json.load( f )
        except:data = {}
        f.close()
        
        mainWindowDict = {}
        mainWindowDict['position'] = [ self.x(), self.y() ]
        mainWindowDict['size'] = [ self.width(), self.height() ]
        
        data[ 'mainWindow' ] = mainWindowDict
        
        f = open( Window.uiInfoPath, 'w' )
        json.dump( data, f )
        f.close()



    def loadUIInfo( self ):
        
        FileAndPaths.makeFile( Window.uiInfoPath )
        f = open( Window.uiInfoPath, 'r' )
        try:data = json.load( f )
        except:data = {}
        f.close()
        if not data.items():
            self.resize( self.defaultWidth, self.defaultHeight )
            return
        try:
            posX, posY = data['mainWindow']['position']
            width, height = data['mainWindow']['size']
        except:
            return
        desktop = QApplication.desktop()
        desktopWidth = desktop.width()
        desktopHeight = desktop.height()
        
        if posX + width > desktopWidth: posX = desktopWidth - width
        if posY + height > desktopWidth: posY = desktopHeight - height
        if posX < 0 : posX = 0
        
        self.move( posX, posY )
        self.resize( width, height )
    
    
    
    def setButtonEnabled(self):
        
        self.buttonSave.setEnabled( True )
        self.buttonDefault.setEnabled( True )
    
    
    def setButtonDisabled(self):
        
        self.buttonSave.setEnabled( False )
        self.buttonDefault.setEnabled( False )



    def getMenuPath(self):
        
        FileAndPaths.makeFile( Window.defaultSearchPath )
        defaultPath = FileAndPaths.getStringDataFromFile( Window.defaultSearchPath )
        
        menuPath = FileAndPaths.getFolderFromBrowser( self, defaultPath )
        if not menuPath: return None
        if not filter( lambda x : menuPath.find( x ) != -1 , ['_MAINMENU_','_POPUPMENU_','_MENU_'] ):
            QMessageBox.critical( self, "Error", "_MAINMENU_, '_MENU_', _POPUPMENU_ 중 하나라도 포함하는 이름의 폴더를 선택하십시요.".decode( 'utf-8' ) )
            return None 
        self.lineEdit_menuPath.setText( menuPath )
        
        FileAndPaths.setStringDataToFile( os.path.dirname( menuPath ), Window.defaultSearchPath )
        FileAndPaths.makeFile( Window.defaultMenuPath )
        FileAndPaths.setStringDataToFile( menuPath, Window.defaultMenuPath )
        self.lineEdit_menuPath.setText( FileAndPaths.getStringDataFromFile( Window.defaultMenuPath ) )
        if os.path.exists( self.lineEdit_menuPath.text() ):
            Cmds.loadMenuList( self.lineEdit_menuPath.text(), 0 )
    
    
    
    def loadDefaultScript(self):
        self.scriptTextEdit.setText( self.defaultTextValue )
    


    def saveScript(self):
        textEditData = self.scriptTextEdit.toPlainText()
        f = open( self.currentScriptPath, 'w' )
        f.write( textEditData.encode( 'utf-8') )
        f.close()




def show( evt=0 ):
    
    if cmds.window( Window.objectName, ex=1 ):
        cmds.deleteUI( Window.objectName )
    
    mainui = Window(Window.mayaWin)
    mainui.setObjectName( Window.objectName )
    mainui.setWindowTitle( Window.title )
    mainui.resize( Window.defaultWidth, Window.defaultHeight )
    mainui.show()


