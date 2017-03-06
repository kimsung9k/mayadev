#!/usr/bin/python
#-*- coding: utf-8 -*-
#-*- encoding: cp949 -*-

import maya.cmds as cmds
import functions.path as pathFunctions
import cmdModel
import view

class Window_addTab:
    
    def __init__(self, pWindow ):
        
        self.pWindow = pWindow
        self.pWinName= pWindow.winName
        self.winName = self.pWinName+'_deleteTab'
        self.title = cmds.window( self.pWinName, q=1, title=1  )+' - Delete Tab'
        
    
    def cmdAdd(self, *args ):
        
        tabLabel = cmds.textFieldGrp( self.tabLabel, q=1, tx=1 )
        self.pWindow.cmd.addChild( self.pWindow.tab, tabLabel )
        cmds.deleteUI( self.winName )
        
    
    def create(self, *args ):
        
        self.width  = 300
        self.height = 50
        pWidth = cmds.window( self.pWinName, q=1, width=1  )
        pHeight= cmds.window( self.pWinName, q=1, height=1 )
        
        top, left = cmds.window( self.pWinName, q=1, tlc=1 )
        
        self.top  = top  + pHeight*0.5 - self.height*0.5
        self.left = left + pWidth*0.5 - self.width*0.5
        
        if cmds.window( self.winName, ex=1 ):
            cmds.deleteUI( self.winName )
        cmds.window( self.winName, title=self.title )
        
        cmds.columnLayout()
        columnWidth = self.width -2
        firstWidth = (columnWidth-2) * 0.4
        secondWidth = ( columnWidth-2) - firstWidth
        cmds.rowColumnLayout( nc=1, cw=[(1,columnWidth)] )
        tabLabel = cmds.textFieldGrp( l='Tab Label : ', cw=[(1,firstWidth),(2,secondWidth)] )
        cmds.button( l='Add', c=self.cmdAdd )
        cmds.showWindow( self.winName )
        cmds.window( self.winName, e=1,
                     width=self.width, height=self.height,
                     tlc=[self.top, self.left] )
        
        self.tabLabel = tabLabel
        
        

class Window_deleteTab:
    
    def __init__(self, pWindow ):
        
        self.pWindow = pWindow
        self.pWinName = pWindow.winName
        self.winName = self.pWinName+'_deleteTab'
        self.title = cmds.window( self.pWinName, q=1, title=1  )+' - Delete Tab'
    
    
    def cmdDelete(self, *args ):
    
        self.pWindow.cmd.deleteChild()
        cmds.deleteUI( self.winName )
        
    
    def cmdCancel(self, *args ):
        
        cmds.deleteUI( self.winName )
    
    
    def create(self, *args ):
        
        self.width  = 300
        self.height = 50
        pWidth = cmds.window( self.pWinName, q=1, width=1  )
        pHeight= cmds.window( self.pWinName, q=1, height=1 )
        
        top, left = cmds.window( self.pWinName, q=1, tlc=1 )
        
        self.top  = top  + pHeight*0.5 - self.height*0.5
        self.left = left + pWidth*0.5 - self.width*0.5
        
        if cmds.window( self.winName, ex=1 ):
            cmds.deleteUI( self.winName )
        cmds.window( self.winName, title=self.title )
        
        cmds.columnLayout()
        columnWidth = self.width -2
        firstWidth = (columnWidth-2) * 0.5
        secondWidth = ( columnWidth-2) - firstWidth
        cmds.rowColumnLayout( nc=1, cw=[(1,columnWidth)] )
        cmds.text( l='Delete the current tab?', h=30 )
        cmds.setParent('..')
        cmds.rowColumnLayout( nc=2, cw=[(1,firstWidth),(2,secondWidth)] )
        cmds.button( l='Delete', c=self.cmdDelete )
        cmds.button( l='Cancel', c=self.cmdCancel )
        cmds.setParent( '..' )
        
        cmds.showWindow( self.winName )
        cmds.window( self.winName, e=1,
                     width=self.width, height=self.height,
                     tlc=[self.top, self.left] )
        
        
        
        
        
class UI_makeANewCategory:
    
    def __init__(self, pUI, width, cmdLoadCategory ):
        
        self.pUI = pUI
        self.width = width
        self.rowColumn = ''
        self.cmdLoadCategory = cmdLoadCategory

    
    def cmdCreateMakeDefaultButton(self):
        
        try:
            cmds.deleteUI( self.rowColumn )
        except: pass
        
        cmds.setParent( self.pUI )
        columnWidth = self.width - 2
        rowColumn = cmds.rowColumnLayout( nc=1, cw=(1,columnWidth) )
        cmds.button( l='Make New Category', c=self.cmdMakeANewCategory )
        cmds.setParent( '..' )
        
        self.rowColumn = rowColumn
        
        
    def cmdCreateMakeAddCategoryUI(self):
        
        try:
            cmds.deleteUI( self.rowColumn )
        except: pass
        
        cmds.setParent( self.pUI )
        firstWidth = ( self.width -2 )*0.3
        fieldWidth = ( self.width - 2 )*0.4
        buttonWidth = ( self.width -2 ) - firstWidth - fieldWidth
        rowColumn = cmds.rowColumnLayout( nc=3, cw=[(1,firstWidth),(2,fieldWidth),(3,buttonWidth)] )
        cmds.text( l='Category Name :', al='right' )
        field = cmds.textField()
        cmds.button( l='Create', c=self.cmdCreate )
        cmds.setParent( '..' )
        
        self.rowColumn = rowColumn
        self.field = field
        
        
    def cmdMakeANewCategory(self, *args ):

        self.cmdCreateMakeAddCategoryUI()


    def cmdCreate(self, *args ):

        category = cmds.textField( self.field, q=1, tx=1 )
        cmdModel.makeCategory( category )

        self.cmdCreateMakeDefaultButton()
        self.cmdLoadCategory( category )




class UI_currentCategory:
    
    def __init__(self, pUI, width ):
        
        self.pUI = pUI
        self.width = width
        self.rowColumn = ''
        self.optionMenu = ''
        
    
    def cmdLoadCategoryList(self, categoryName=None ):
        
        categoryList = cmdModel.getCategoryList()
        if not categoryList: return None
        
        try:
            cmds.deleteUI( self.rowColumn )
        except:pass
        
        cmds.setParent( self.pUI )
        firstWidth = (self.width-2)*0.5
        secondWidth = ( self.width-2 ) - firstWidth
        self.rowColumn = cmds.rowColumnLayout( nc=3, cw=[(1,firstWidth),(2,secondWidth)] )
        cmds.text( l='Category : ' )
        self.optionMenu = cmds.optionMenu()
        cmds.menuItem( l='None' )
        for category in categoryList:
            cmds.menuItem( l=category )
        cmds.setParent( '..' )
        
        if categoryName in categoryList:
            index = categoryList.index( categoryName )
            cmds.optionMenu( self.optionMenu, e=1, sl=index+1 )



class Window_updateApp:

    def __init__(self, pWindow):

        self.pWindow = pWindow
        self.pWinName = self.pWindow.winName
        self.winName = pWindow.winName + '_updateApp'
        self.title   = pWindow.title   + ' - Update App'
        self.width  = 320
        self.height = 50
        self.makeCategoryInst = None
        self.currentCategoryInst = None


    def cmdLoadCategory( self, categoryName = None ):
        
        self.currentCategoryInst.cmdLoadCategoryList( categoryName )


    def cmdUpdateApp( self, *args ):

        title   = cmds.textField( self.pWindow.titleField, q=1, tx=1 )
        selItem = cmds.radioCollection( self.pWindow.collection, q=1, sl=1 )
        collectionItems = cmds.radioCollection( self.pWindow.collection, q=1, collectionItemArray=1 )
        selItems = ['mel','python']

        for i in range( len( collectionItems ) ):
            if collectionItems[i].find( selItem ) != -1:
                break

        cmdModel.cmdUpdateApp( self.pWindow.tab, self.currentCategoryInst.optionMenu, title, selItems[i] )
        cmds.deleteUI( self.winName, wnd=1 )

        view.showUserSetupMenu()


    def create(self, *args ):

        pWidth = cmds.window( self.pWinName, q=1, width=1  )
        pHeight= cmds.window( self.pWinName, q=1, height=1 )

        top, left = cmds.window( self.pWinName, q=1, tlc=1 )

        self.top  = top  + pHeight*0.5 - self.height*0.5
        self.left = left + pWidth*0.5 - self.width*0.5

        if cmds.window( self.winName, ex=1 ):
            cmds.deleteUI( self.winName )
        cmds.window( self.winName, title=self.title )
        column = cmds.columnLayout()

        makeCategoryFrame = cmds.frameLayout( lv=0, bs='etchedIn' )
        cmds.setParent( '..' )
        currentCategoryFrame = cmds.frameLayout( lv=0, bs='etchedIn' )
        cmds.setParent( '..' )

        self.makeCategoryInst = UI_makeANewCategory( makeCategoryFrame, self.width-2, self.cmdLoadCategory )
        self.currentCategoryInst = UI_currentCategory( currentCategoryFrame, self.width-2 )

        self.makeCategoryInst.cmdCreateMakeDefaultButton()
        self.currentCategoryInst.cmdLoadCategoryList()
        
        cmds.setParent( column )
        cmds.rowColumnLayout( nc=1, cw=(1,self.width-2))
        cmds.button( l='UPDATE APP', c=self.cmdUpdateApp )
        
        cmds.showWindow( self.winName )
        cmds.window( self.winName, e=1,
                     width=self.width, height=self.height,
                     tlc=[self.top, self.left] )



class Window_deleteApp:
    
    def __init__(self, pWindow ):
        
        self.pWindow = pWindow
        self.pWinName = self.pWindow.winName
        self.winName = pWindow.winName + '_deleteApp'
        self.title   = pWindow.title   + ' - Delete App'
        self.width  = 320
        self.height = 50


    def cmdCancel( self, *args ):

        cmds.deleteUI( self.winName )


    def cmdDeleteApp(self, *args):

        pathFunctions.deletePathHierarchy( self.pWindow.appPath )
        pathFunctions.os.rmdir( self.pWindow.appPath )
        cmds.deleteUI( self.winName )
        cmds.deleteUI( self.pWinName )
        view.showUserSetupMenu()


    def create(self):
        
        pWidth = cmds.window( self.pWinName, q=1, width=1  )
        pHeight= cmds.window( self.pWinName, q=1, height=1 )
        
        top, left = cmds.window( self.pWinName, q=1, tlc=1 )
        
        self.top  = top  + pHeight*0.5 - self.height*0.5
        self.left = left + pWidth*0.5 - self.width*0.5
        
        if cmds.window( self.winName, ex=1 ):
            cmds.deleteUI( self.winName )
        cmds.window( self.winName, title=self.title )
        
        column = cmds.columnLayout()
        columnWidth = self.width -2
        cmds.rowColumnLayout( nc=1, cw=[(1,columnWidth)] )
        cmds.text( 'Delete App, continue?', h=30 )
        cmds.setParent( '..' )
        
        firstWidth = ( columnWidth-2 ) * 0.5
        secondWidth = ( columnWidth-2 ) - firstWidth
        cmds.rowColumnLayout( nc=2, cw=[(1,firstWidth),(2,secondWidth)])
        cmds.button( l='Delete', c=self.cmdDeleteApp )
        cmds.button( l='Cancel', c=self.cmdCancel )
        
        cmds.showWindow( self.winName )
        cmds.window( self.winName, e=1,
                     width=self.width, height=self.height,
                     tlc=[self.top, self.left] )
        
        

class Window_editApp:

    def __init__(self, pWindow ):

        self.pWindow = pWindow
        self.pWinName = self.pWindow.winName
        self.winName = pWindow.winName + '_editApp'
        self.title   = pWindow.title   + ' - Edit App'
        self.width  = 320
        self.height = 50


    def cmdCancel( self, *args ):

        cmds.deleteUI( self.winName )


    def cmdEditApp(self, *args):

        title   = cmds.textField( self.pWindow.titleField, q=1, tx=1 )
        selItem = cmds.radioCollection( self.pWindow.collection, q=1, sl=1 )
        collectionItems = cmds.radioCollection( self.pWindow.collection, q=1, collectionItemArray=1 )
        selItems = ['mel','python']

        for i in range( len( collectionItems ) ):
            if collectionItems[i].find( selItem ) != -1:
                break

        self.pWindow.appPath = self.pWindow.appPath.replace( '\\', '/' )
        targetPath = '/'.join( self.pWindow.appPath.split( '/' )[:-1] )
        cmdModel.cmdEditApp( self.pWindow.tab, targetPath, title, selItems[i] )

        cmds.deleteUI( self.winName )
        cmds.deleteUI( self.pWinName )

        view.showUserSetupMenu()


    def create(self):

        pWidth = cmds.window( self.pWinName, q=1, width=1  )
        pHeight= cmds.window( self.pWinName, q=1, height=1 )

        top, left = cmds.window( self.pWinName, q=1, tlc=1 )

        self.top  = top  + pHeight*0.5 - self.height*0.5
        self.left = left + pWidth*0.5 - self.width*0.5

        if cmds.window( self.winName, ex=1 ):
            cmds.deleteUI( self.winName )
        cmds.window( self.winName, title=self.title )

        column = cmds.columnLayout()
        columnWidth = self.width -2
        cmds.rowColumnLayout( nc=1, cw=[(1,columnWidth)] )
        cmds.text( 'App Change, continue?', h=30 )
        cmds.setParent( '..' )

        firstWidth = ( columnWidth-2 ) * 0.5
        secondWidth = ( columnWidth-2 ) - firstWidth
        cmds.rowColumnLayout( nc=2, cw=[(1,firstWidth),(2,secondWidth)])
        cmds.button( l='Edit', c=self.cmdEditApp )
        cmds.button( l='Cancel', c=self.cmdCancel )

        cmds.showWindow( self.winName )
        cmds.window( self.winName, e=1,
                     width=self.width, height=self.height,
                     tlc=[self.top, self.left] )



class Window_DeleteCategory:

    def __init__(self, pWindow ):

        self.pWindow = pWindow
        self.pWinName = self.pWindow.winName
        self.winName = self.pWinName + '_deleteCategory'
        self.title   = self.pWindow.title + ' - Delete Category'
        self.width = 300
        self.height = 50
        
        
    def cmdDelete( self, *args ):
        
        for checkBox in self.pWindow.checkBoxList:
            value = cmds.checkBox( checkBox, q=1, v=1 )
            enable = cmds.checkBox( checkBox, q=1, v=1 )
            if value and enable:
                categoryName = cmds.checkBox( checkBox, q=1, l=1 )
                cmdModel.deleteCategory(categoryName)
        cmds.deleteUI( self.winName )
        
        self.pWindow.reloadCategoryList()
        
        
    def cmdCancel(self , *args ):
        
        cmds.deleteUI( self.winName )
        


    def create(self):
        
        pWidth = cmds.window( self.pWinName, q=1, width=1  )
        pHeight= cmds.window( self.pWinName, q=1, height=1 )

        top, left = cmds.window( self.pWinName, q=1, tlc=1 )

        self.top  = top  + pHeight*0.5 - self.height*0.5
        self.left = left + pWidth*0.5 - self.width*0.5

        if cmds.window( self.winName, q=1, ex=1 ):
            cmds.deleteUI( self.winName, wnd=1 )
        cmds.window( self.winName, title= self.title )

        cmds.columnLayout()
        cmds.rowColumnLayout( nc=1, cw=(1,self.width-2) )
        cmds.text( l='Category And Apps will be deleted, continue ?', h=30 )
        cmds.setParent( '..' )
        
        firstWidth = ( self.width - 2 ) * 0.5
        secondWidth = ( self.width - 2 ) - firstWidth
        cmds.rowColumnLayout( nc=2, cw=[(1,firstWidth), (2,secondWidth)])
        cmds.button( l='Delete', c= self.cmdDelete )
        cmds.button( l='Cancel', c= self.cmdCancel )

        cmds.showWindow( self.winName )
        cmds.window( self.winName, e=1,
                     width=self.width, height=self.height,
                     tlc=[self.top, self.left] )