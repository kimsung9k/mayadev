import maya.cmds as cmds

import os, sys
import copy
from functools import partial
import maya.cmds as cmds
import maya.mel as mel

import model
import uiModel
import cmdModel
import sub_view

import socket


class cmdWindowInfo:
    
    mayaDocPath = cmdModel.getMayaDocPath()
    windowSizeInfoPath = mayaDocPath+'/LocusCommPackagePrefs/commTeamCostomApp/windowSize.txt'
    cmdModel.makeFile( windowSizeInfoPath )



mc_checkIdAndOpenWindow ="""import mayaWindow.commTeamCostomApp.cmdModel
import mayaWindow.commTeamCostomApp.view
if mayaWindow.commTeamCostomApp.cmdModel.checkIdExists():
    mayaWindow.commTeamCostomApp.view.Window().create()
else:
    mayaWindow.commTeamCostomApp.view.RegistrationUI().create()"""




class RegistrationUI:
    
    def __init__( self ):
        
        self.winName = uiModel.winName + 'id_registeration'
        self.title = uiModel.title + ' - ID Registration'
        self.width = 200
        self.height = 50

 
 
    def cmdCreate( self, *args ):
        
        idName = cmds.textField( self.idField, q=1, tx=1 )
        
        if idName.find( ' ' ) != -1:
            cmds.textField( self.helpField, e=1, tx='Name is not exists' )
            return None
        
        if cmdModel.checkSameIdExists( idName ):
            cmds.textField( self.helpField, e=1, tx='"%s" is already Exists' % idName )
            return None
        else:
            cmds.textField( self.helpField, e=1, tx='' )

        f = open( model.idPath, 'r' )
        data = f.read()
        f.close()

        lines = []

        for line in data.split( '\n' ):
            lines.append( line.strip() )

        hostName = socket.gethostname()
        date = cmdModel.getTimeString()

        lines.append( '%s:%s:%s' %( hostName, idName, date ) )
        writeData = '\n'.join( lines )
        
        f = open( model.idPath, 'w' )
        f.write( writeData )
        f.close()
        
        Window().create()
        
        cmds.deleteUI( self.winName, wnd=1 )



    def cmdCancel( self, *args ):
        
        cmds.deleteUI( self.winName, wnd=1 )



    def create( self, *args ):
        
        if cmds.window( self.winName, ex=1 ):
            cmds.deleteUI( self.winName, wnd=1 )
        cmds.window( self.winName, title= self.title, titleBarMenu=0 )
        
        cmds.columnLayout()
        cmds.rowColumnLayout( nc=1, cw=[( 1,self.width-2)] )
        cmds.text( l='Register ID', h=30 )
        idField = cmds.textField( h=25 )
        helpField = cmds.textField( en=0 )
        cmds.setParent( '..' )
        
        firstWidth = (self.width-2)*0.5
        secondWidth = (self.width-2)-firstWidth
        cmds.rowColumnLayout( nc=2, cw=[(1,firstWidth),(2,secondWidth)])
        cmds.button( l='Create', h=25, c=self.cmdCreate )
        cmds.button( l='Cancel', h=25, c=self.cmdCancel )
        cmds.setParent( '..' )
        
        cmds.window( self.winName, e=1,
                     width = self.width,
                     height = self.height )
        cmds.showWindow( self.winName )
        
        self.idField = idField
        self.helpField = helpField
        
        
        
        
class Window_idEditor:
    
    def __init__(self):
        
        self.winName = uiModel.winName + '_idEditor'
        self.title   = uiModel.title   + ' - ID Editor'
        self.width   = 250
        self.height  = 50
        
        
    def loadBeforeId(self):
        
        myHostName = socket.gethostname()
        
        f = open( model.idPath, 'r' )
        data = f.read()
        f.close()
        
        for line in data.split( '\n' ):
            host, id, time = line.strip().split( ':' )
            if host == myHostName:
                myId = id
        
        cmds.textField( self.idField, e=1, tx=myId )
        
        self.myId = myId
    
    
    
    def cmdEditId( self, *args ):
        
        myHostName = socket.gethostname()
        
        idName = cmds.textField( self.idField, q=1, tx=1 )
        if self.myId and self.myId == idName:
            return None
            cmds.deleteUI( self.winName, wnd=1 )
        
        if idName.find( ' ' ) != -1:
            cmds.textField( self.helpField, e=1, tx='Name is not exists' )
            return None
        
        if cmdModel.checkSameIdExists( idName ):
            cmds.textField( self.helpField, e=1, tx='"%s" is already Exists' % idName )
            return None
        else:
            cmds.textField( self.helpField, e=1, tx='' )

        f = open( model.idPath, 'r' )
        data = f.read()
        f.close()

        lines = []

        for line in data.split( '\n' ):
            host, id, time = line.strip().split( ':' )
            if host != myHostName:
                lines.append( line.strip() )

        hostName = socket.gethostname()
        date = cmdModel.getTimeString()

        lines.append( '%s:%s:%s' %( hostName, idName, date ) )
        writeData = '\n'.join( lines )
        
        f = open( model.idPath, 'w' )
        f.write( writeData )
        f.close()
        
        cmds.deleteUI( self.winName, wnd=1 )



    def cmdCancel( self, *args ):
        
        cmds.deleteUI( self.winName, wnd=1 )



    def create( self ):
        
        if cmds.window( self.winName, ex=1 ):
            cmds.deleteUI( self.winName, wnd=1 )
        cmds.window( self.winName, title= self.title, titleBarMenu=0 )
        
        cmds.columnLayout()
        cmds.rowColumnLayout( nc=1, cw=[( 1,self.width-2)] )
        cmds.text( l='Edit ID', h=30 )
        idField = cmds.textField( h=25 )
        helpField = cmds.textField( en=0 )
        cmds.setParent( '..' )
        
        firstWidth = (self.width-2)*0.5
        secondWidth = (self.width-2)-firstWidth
        cmds.rowColumnLayout( nc=2, cw=[(1,firstWidth),(2,secondWidth)])
        cmds.button( l='Edit ID', h=25, c=self.cmdEditId )
        cmds.button( l='Cancel', h=25, c=self.cmdCancel )
        cmds.setParent( '..' )
        
        cmds.window( self.winName, e=1,
                     width = self.width,
                     height = self.height )
        cmds.showWindow( self.winName )
        
        self.idField = idField
        self.helpField = helpField
        
        self.loadBeforeId()




class Window:
    
    def __init__(self):
        
        self.winName = uiModel.winName
        self.title   = uiModel.title
        self.width   = uiModel.width
        self.height  = uiModel.height
        
        self.cmd = cmdModel.uiCmd( self )
    
    
    def create(self, *args ):
        
        if cmds.window( self.winName, ex=1 ):
            cmds.deleteUI( self.winName, wnd=1 )
        cmds.window( self.winName, title= self.title, titleBarMenu=0 )
        
        form = cmds.formLayout()
        
        columnWidth = self.width - 2
        firstWidth = ( columnWidth - 2 )* 0.4
        secondWidth = ( columnWidth - 2 )*0.3
        thirdWidth = ( columnWidth -2 ) - firstWidth - secondWidth
        
        appName = self.applicationTitle()
        frame = cmds.frameLayout( lv=0, bs='etchedIn' )
        cmds.rowColumnLayout( nc=3, cw=[(1,firstWidth),(2,secondWidth),(3,thirdWidth)] )
        cmds.text( l='Source Type : ', al='center', h=26 )
        collection = cmds.radioCollection()
        self.collection = collection
        cmds.radioButton( l='Mel', sl=1 )
        cmds.radioButton( l='Python' )
        cmds.setParent( '..' )
        cmds.setParent( '..' )

        tab = cmds.tabLayout()
        self.tab = tab
        self.cmd.addChild( tab, 'MainCommand' )
        cmds.setParent( '..' )
        
        button = self.buttons()
        
        cmds.formLayout( form, e=1, af=[(appName,'top',0), (appName,'left',0),   (appName,'right',0),
                                        (frame,'left',0), (frame,'right',0),
                                        (button,'left',0),(button,'right',0),(button,'bottom',0),
                                        (tab,'left',0),(tab,'right',0)],
                                    ac=[(frame,'top',0,appName),(tab,'bottom',0,button),
                                        (tab,'top',0,frame)] )
        cmds.setParent( '..' )
        
        cmds.window( self.winName, e=1,
                     w = self.width, h = self.height )
        cmds.showWindow( self.winName )
        
        for root, dirs, names in os.walk( cmdModel.getTempCmdFolder() ):
            if dirs:
                cmdModel.cmdLoadBeforeSetting( self, self.titleField, tab, collection, root+'/'+dirs[0] )
            break


    def applicationTitle( self ):
        
        form = cmds.formLayout()
        title = cmds.text( l='Application Title :', w=100, h=30, al='right' )
        field = cmds.textField()
        
        cmds.formLayout( form, e=1,
                         af=[(title,'top',0),(title,'left',0),(field,'top',5),(field,'bottom',5),(field,'right',5)],
                         ac=[(field,'left',5, title)])
        cmds.setParent( '..' )
        self.titleField = field
        return form



    def buttons( self ):
        
        form = cmds.formLayout()
        testApp     = cmds.button( l='TEST APP', h=25, c=self.cmd.testApp  )
        updateApp   = cmds.button( l='UPDATE APP', h=25, c=self.cmd.openUpdateApp )
        closeWindow = cmds.button( l='CLOSE',h=25, c=self.cmd.close )
        
        cmds.formLayout( form, e=1, 
                         af=[(testApp,'top',0), (testApp,'left',0),
                             (updateApp,'top',0), (updateApp,'right',0),
                             (closeWindow,'left',0),(closeWindow,'right',0),(closeWindow,'bottom',0)],
                         ap=[(testApp,'right',0,50),(updateApp,'left',0,50),
                             (testApp,'bottom',0,50),(updateApp,'bottom',0,50), (closeWindow,'top',0,50)] )
        cmds.setParent( '..' )
        return form
    


def execString( string ):
    exec( string )



def melCmdExcute( string, *args ):
    print "------------------------------------------------------------------"
    print string
    print "------------------------------------------------------------------"
    mel.eval( string )
    
    

class MayaMenu_OptionWindow:
    
    def __init__(self, appPath ):
        
        self.winName = uiModel.optionWinName
        self.title   = uiModel.optionWinTitle
        self.width   = uiModel.width
        self.height  = uiModel.height
        self.appPath = appPath
        
        self.cmd = cmdModel.uiCmd( self )
    
    
    def create(self, *args ):
        
        if cmds.window( self.winName, ex=1 ):
            cmds.deleteUI( self.winName, wnd=1 )
        cmds.window( self.winName, title= self.title, titleBarMenu=0 )
        
        form = cmds.formLayout()
        
        columnWidth = self.width - 2
        firstWidth = ( columnWidth - 2 )* 0.4
        secondWidth = ( columnWidth - 2 )*0.3
        thirdWidth = ( columnWidth -2 ) - firstWidth - secondWidth
        
        appName = self.applicationTitle()
        frame = cmds.frameLayout( lv=0, bs='etchedIn' )
        cmds.rowColumnLayout( nc=3, cw=[(1,firstWidth),(2,secondWidth),(3,thirdWidth)] )
        cmds.text( l='Source Type : ', al='center', h=26 )
        collection = cmds.radioCollection()
        self.collection = collection
        cmds.radioButton( l='Mel', sl=1 )
        cmds.radioButton( l='Python' )
        cmds.setParent( '..' )
        cmds.setParent( '..' )

        tab = cmds.tabLayout()
        self.tab = tab
        self.cmd.addChild( tab, 'MainCommand' )
        cmds.setParent( '..' )
        
        button = self.buttons()
        
        cmds.formLayout( form, e=1, af=[(appName,'top',0), (appName,'left',0),   (appName,'right',0),
                                        (frame,'left',0), (frame,'right',0),
                                        (button,'left',0),(button,'right',0),(button,'bottom',0),
                                        (tab,'left',0),(tab,'right',0)],
                                    ac=[(frame,'top',0,appName),(tab,'bottom',0,button),
                                        (tab,'top',0,frame)] )
        cmds.setParent( '..' )
        
        cmds.window( self.winName, e=1,
                     w = self.width, h = self.height )
        cmds.showWindow( self.winName )
        
        cmdModel.cmdLoadBeforeSetting( self, self.titleField, tab, collection, self.appPath )



    def applicationTitle( self ):
        
        form = cmds.formLayout()
        title = cmds.text( l='Application Title :', w=100, h=30, al='right' )
        field = cmds.textField()
        
        cmds.formLayout( form, e=1,
                         af=[(title,'top',0),(title,'left',0),(field,'top',5),(field,'bottom',5),(field,'right',5)],
                         ac=[(field,'left',5, title)])
        cmds.setParent( '..' )
        self.titleField = field
        return form



    def buttons( self ):
        
        form = cmds.formLayout()
        testApp     = cmds.button( l='TEST APP', h=25, c=self.cmd.testApp )
        editApp     = cmds.button( l='EDIT APP', h=25, c=self.cmd.editApp  )
        deleteApp   = cmds.button( l='DELETE APP', h=25, c=self.cmd.deleteApp )
        closeWindow = cmds.button( l='CLOSE',h=25, c=self.cmd.close )
        
        cmds.formLayout( form, e=1, 
                         af=[(testApp,'top',0), (testApp,'left',0),
                             (editApp,'top',0),
                             (deleteApp,'top',0), (deleteApp,'right',0),
                             (closeWindow,'left',0),(closeWindow,'right',0),(closeWindow,'bottom',0)],
                         ap=[(testApp,'right',0,33.3), (editApp,'left',0,33.3), (editApp,'right',0,66.6) ,(deleteApp,'left',0,66.6),
                             (testApp,'bottom',0,50),(editApp,'bottom',0,50),(deleteApp,'bottom',0,50), (closeWindow,'top',0,50)] )
        cmds.setParent( '..' )
        return form


class MayaMenu:
    
    def __init__( self, path, title ):
        
        self.uiName = 'autoLoadMayaMenu_' + title
        self.title = title
        self.parentUIName = 'MayaWindow'
        self.path = path
        
    
    def pyCommand( self, importString, *args ):
        
        try:reload( sys.modules['%s' % importString] )
        except:exec( 'import %s' % importString )
        
        
    def melCommand(self, execPath, *args ):
        mel.eval( 'source "%s";' % execPath )
        
        
    def optionMenuCommand(self, path, *args ):
        
        MayaMenu_OptionWindow( path ).create()
    
        
    def create( self, *args ):
        
        if cmds.menu( self.uiName, ex=1 ):
            cmds.deleteUI( self.uiName )
        cmds.menu( self.uiName, l= self.title, p=self.parentUIName, to=1 )
        
        beforeSplits = []
        checkPath = self.path+'/'+self.title
        checkPath = checkPath.replace( '\\', '/' )
        
        if not checkPath in sys.path:
            sys.path.append( checkPath )

        for root, dirs, names in os.walk( checkPath ):
            
            root = root.replace( '\\', '/' )
            
            if checkPath == root: continue
            
            splits = root.replace( checkPath, '' )[1:].split( '/' )
            folderName = splits[-1]
            
            mainCommand = None
            
            for name in names:
                if name == 'MainCommand.py':
                    isCommandFolder = True
                    importString = root.replace( checkPath+'/', '' ).replace( '/', '.' )+'.'+name.split( '.' )[0]
                    mainCommand = name
                    break
                elif name == 'MainCommand.mel':
                    isCommandFolder = True
                    commandPath = root +'/'+ name
                    mainCommand = name
                    break
                    
            reloadTargets = []
            sourceTargets = []
            for name in names:
                if name.find( 'MainCommand' ) != -1:
                    continue
                if name.find( '.py' ) != -1:
                    reloadTargets.append( root.replace( checkPath+'/', '' ).replace( '/', '.' )+'.'+name.split( '.' )[0] )
                elif name.find( '.mel' ) != -1:
                    mel.eval( 'source "%s";' % ( root + '/' + name ) )
                    sourceTargets.append( root+'.'+name )
            
            if mainCommand:
                if mainCommand == 'MainCommand.py':
                    cmds.menuItem( l= folderName, c=partial( self.pyCommand, importString ) )
                    if cmdModel.checkHostIsMine( root ):
                        cmds.menuItem( ob=1, c= partial( self.optionMenuCommand, root ) )
                elif mainCommand == 'MainCommand.mel':
                    cmds.menuItem( l= folderName, c=partial( self.melCommand, commandPath ) )
                    if cmdModel.checkHostIsMine( root ):
                        cmds.menuItem( ob=1, c= partial( self.optionMenuCommand, root ) )
            else:
                setParentNum = 0
                for i in range( len( beforeSplits ) ):
                    if i >= len( splits ): 
                        setParentNum += 1
                        continue
                    if beforeSplits[i] != splits[i]:
                        setParentNum += 1
                for num in range( setParentNum ):
                    cmds.setParent( '..', menu=1 )
                if not names: continue
                cmds.menuItem( l= folderName, sm=1, to=1 )
                beforeSplits = splits
        return self.uiName



class MayaMenuModel:
    
    mayaMenuName = ''



def deleteUserSetupMenu( *args ):
    
    print "commTeamCostomApp deleted"
    cmds.deleteUI( MayaMenuModel.mayaMenuName )



class UI_CategoryLister:
    
    def __init__(self, pWindow ):
        
        self.pWinName = pWindow.winName
        self.pWidth   = pWindow.width
        self.categoryPath = model.categoryBasePath


    def loadFolder(self):
        
        f = open( model.idPath, 'r' )
        data = f.read()
        f.close()
        
        idName = ''
        for line in data.split( '\n' ):
            hostName, id, date = line.split( ':' )
            if hostName.strip() == socket.gethostname():
                idName = id
        
        self.checkBoxList = []
        if not idName: return None
        
        path = model.categoryBasePath + '/' + idName

        pathList = []
        for root, dirs, names in os.walk( path ):
            root = root.replace( '\\', '/' )
            
            if path == root: continue
            
            mainCommandExists = False
            for name in names:
                if name.find( 'MainCommand' ) != -1:
                    mainCommandExists = True
            if not mainCommandExists and names:
                pathList.append( root.replace( path+'/', '' ) )
        
        self.checkBoxList = []
        
        for path in pathList:
            checkBox = cmds.checkBox( l=path, parent = self.scroll,
                                      cc = self.cmdCheckBoxChange )
            self.checkBoxList.append( checkBox )
            
            
    def cmdCheckBoxChange( self, *args ):
        checkedLabelList = []
        for checkBox in self.checkBoxList:
            if not cmds.checkBox( checkBox, q=1, v=1 ): continue
            label = cmds.checkBox( checkBox, q=1, l=1 )
            checkedLabelList.append( label )
        
        for checkBox in self.checkBoxList:
            cmds.checkBox( checkBox, e=1, en=1 )
            for label in checkedLabelList:
                checkBoxLabel = cmds.checkBox( checkBox, q=1, label=1 )
                if checkBoxLabel == label: continue
                if checkBoxLabel.find( label ) != -1:
                    cmds.checkBox( checkBox, e=1, en=0 )


    def create(self):
        
        form = cmds.formLayout()
        
        scroll = cmds.scrollLayout()
        cmds.setParent( '..' )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1,
                         af=[(scroll, 'top', 0 ), (scroll, 'left', 0 ),
                             (scroll, 'bottom', 0 ), (scroll, 'right', 0 )] )
        
        self.scroll = scroll
        
        self.loadFolder()
        
        return form
    
    
    def reload( self ):
        
        childArr = cmds.scrollLayout( self.scroll, q=1, ca=1 )
        for child in childArr:
            cmds.deleteUI( child )
        self.loadFolder()




class Window_CategoryEditor:
    
    def __init__(self):
        
        self.winName = uiModel.winName + '_categoryEditor'
        self.title   = uiModel.title + ' - Category Editor'
        self.width   = 300
        self.height  = 250
        
        self.categoryLister = UI_CategoryLister( self )
        
        
    def cmdRemoveCategory(self, *args ):
        
        sub_view.Window_DeleteCategory( self ).create()
        
        
    def reloadCategoryList(self):
        
        self.categoryLister.reload()
        self.checkBoxList = self.categoryLister.checkBoxList


    def create(self ):

        if cmds.window( self.winName, ex=1 ):
            cmds.deleteUI( self.winName )
        cmds.window( self.winName, title= self.title )

        form = cmds.formLayout()
        categoryLister = self.categoryLister.create()
        self.checkBoxList = self.categoryLister.checkBoxList
        button = cmds.button( l = 'Remove Category', h=30, c= self.cmdRemoveCategory )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1,
                         af = [( categoryLister, 'top', 0 ), ( categoryLister, 'left', 0 ), ( categoryLister, 'right', 0 ),
                               ( button, 'left', 0 ), ( button, 'right', 0 ), ( button, 'bottom', 0 )],
                         ac = [( categoryLister, 'bottom', 0, button )] )
        

        cmds.showWindow( self.winName )
        cmds.window( self.winName, e=1,
                     w = self.width,
                     h = self.height )

mc_showCategoryEditor = """import mayaWindow.commTeamCostomApp.view
mayaWindow.commTeamCostomApp.view.Window_CategoryEditor().create()
"""


mc_showIdEditor = """import mayaWindow.commTeamCostomApp.view
mayaWindow.commTeamCostomApp.view.Window_idEditor().create()
"""


mc_showUserSetupMenu = """import os
import mayaWindow.commTeamCostomApp.model
import mayaWindow.commTeamCostomApp.view
for root, dirs, names in os.walk( mayaWindow.commTeamCostomApp.model.commTeamCostomAppPath ):
    rootChildren = os.listdir( root )
    for rootChild in rootChildren:
        if os.path.isfile( root+'/'+rootChild ): continue
        mayaWindow.commTeamCostomApp.view.MayaMenuModel.mayaMenuName = mayaWindow.commTeamCostomApp.view.MayaMenu( root, rootChild ).create()
    break
"""