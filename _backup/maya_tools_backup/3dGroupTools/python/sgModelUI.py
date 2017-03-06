import maya.cmds as cmds
import sgFunctionFileAndPath
import sgModelData
from functools import partial
import os


class PopupFieldUI:


    def __init__(self, label, popupLabel='Load Selected', typ='single', **options ):
        
        self._label = label
        self._popup = popupLabel
        self._position = sgModelData.getValueFromDict( options, 'position' )
        self._textWidth = sgModelData.getValueFromDict( options, 'textWidth' )
        self._addCommand = sgModelData.getValueFromDict( options, 'addCommand' )
        if self._textWidth == None: self._textWidth = 120
        self._field  =''
        self._type = typ
        self._cmdPopup = [self.cmdLoadSelected]



    def cmdLoadSelected(self):
        sels = cmds.ls( sl=1, sn=1 )
        if not sels: return None
        
        if self._type == 'single':
            cmds.textField( self._field, e=1, tx=sels[-1] )
        else:
            popupTxt = ''
            for sel in sels:
                popupTxt += sel + ' '
            cmds.textField( self._field, e=1, tx=popupTxt[:-1] )
        
        if self._addCommand: self._addCommand()
        


    def cmdPopup(self, *args ):
        for cmd in self._cmdPopup: cmd()
        


    def getFieldText(self):
        return cmds.textField( self._field, q=1, tx=1 )
    


    def getFieldTexts(self):
        
        texts = cmds.textField( self._field, q=1, tx=1 )
        splits = texts.split( ' ' )
        returnTexts = []
        
        splits2 = []
        
        for split in splits:
            splits2 += split.split( ',' )
        
        for split in splits2:
            split = split.strip()
            if split:
                returnTexts.append( split )
        return returnTexts
                


    def create(self):
        
        form = cmds.formLayout()
        text  = cmds.text( l= self._label, al='right', h=20, width = self._textWidth )
        field = cmds.textField(h=21)
        cmds.popupMenu()
        cmds.menuItem( l=self._popup, c=self.cmdPopup )
        
        cmds.formLayout( form, e=1,
                         af=[(text,'top',0), (text,'left',0),
                             (field,'top',0),(field,'right',0)],
                         ac=[(field, 'left', 0, text)] )
        
        if self._position:
            cmds.formLayout( form, e=1,
                             ap=[(text,'right',0,self._position)])
            
        cmds.setParent( '..' )
        
        self._text = text
        self._field = field
        self._form = form
        
        return form





def updatePathPopupMenu( textField, popupMenu, addCommand=None, *args ):
    
    targetExtensions = ['mb', 'ma', 'fbx', 'obj']
    
    try:path = cmds.textFieldGrp( textField, q=1, tx=1 )
    except:path = cmds.textField( textField, q=1, tx=1 )
    
    cmds.popupMenu( popupMenu, e=1, dai=1 )
    cmds.setParent( popupMenu, menu=1 )
    cmds.menuItem( l='Open File Browser', c=partial( sgFunctionFileAndPath.openFileBrowser, path ) )
    cmds.menuItem( d=1 )
    
    def backToUpfolder( path, *args ):
        path = path.replace( '\\', '/' )
        if sgFunctionFileAndPath.isFile( path ):
            path = '/'.join( path.split( '/' )[:-2] )
        else:
            path = '/'.join( path.split( '/' )[:-1] )
        try:cmds.textFieldGrp( textField, e=1, tx=path )
        except:cmds.textField( textField, e=1, tx=path )
        updatePathPopupMenu( textField, popupMenu, addCommand )
    
    if sgFunctionFileAndPath.isFile(path) or sgFunctionFileAndPath.isFolder(path):
        splitPath = path.replace( '\\', '/' ).split( '/' )
        if splitPath and splitPath[-1] != '':
            cmds.menuItem( l='Back', c=partial( backToUpfolder, path ) )
    cmds.menuItem( d=1 )
    
    path = path.replace( '\\', '/' )
    if sgFunctionFileAndPath.isFile(path):
        path = '/'.join( path.split( '/')[:-1] )
    
    def updateTextField( path, *args ):
        try:cmds.textFieldGrp( textField, e=1, tx=path )
        except:cmds.textField( textField, e=1, tx=path )
        updatePathPopupMenu( textField, popupMenu, addCommand )
        if( addCommand != None ): addCommand()
    
    for root, dirs, names in os.walk( path ):
        dirs.sort()
        for dir in dirs:
            cmds.menuItem( l= dir, c= partial( updateTextField, root+'/'+dir ) )
        names.sort()
        for name in names:
            extension = name.split( '.' )
            if len( extension ) == 1: continue
            extension = extension[1]
            if not extension.lower() in targetExtensions:continue
            cmds.menuItem( l= name, c= partial( updateTextField, root+'/'+name ) )
        break
    
    try:
        cmds.textField( textField, e=1, ec=partial( updatePathPopupMenu, textField, popupMenu, addCommand ) )
        cmds.textField( textField, e=1, cc=partial( updatePathPopupMenu, textField, popupMenu, addCommand ) )
    except:
        cmds.textFieldGrp( textField, e=1, ec=partial( updatePathPopupMenu, textField, popupMenu, addCommand ) )
        cmds.textFieldGrp( textField, e=1, cc=partial( updatePathPopupMenu, textField, popupMenu, addCommand ) )



def updatePathPopupMenu_forScrollList( scrollList, popupMenu, addCommand=None, *args ):
    
    targetExtensions = ['mb', 'ma', 'fbx', 'obj']
    
    selItems = cmds.textScrollList( scrollList, q=1, si=1 )
    if not selItems: return None
    selItem = selItems[0]

    fileName, cacheBodyPath = selItem.split( ' --> ' )
    cacheBodyPath = cacheBodyPath.split( '{' )[0]

    allItems = cmds.textScrollList( scrollList, q=1, ai=1 )
    selItemIndex = allItems.index( selItem )
    
    cmds.popupMenu( popupMenu, e=1, dai=1 )
    cmds.setParent( popupMenu, menu=1 )
    cmds.menuItem( l='Open File Browser', c=partial( sgFunctionFileAndPath.openFileBrowser, cacheBodyPath ) )
    cmds.menuItem( d=1 )
    
    def backToUpfolder( path, *args ):
        path = path.replace( '\\', '/' )
        if sgFunctionFileAndPath.isFile( path ):
            path = '/'.join( path.split( '/' )[:-2] )
        else:
            path = '/'.join( path.split( '/' )[:-1] )
        insertItem = fileName + ' --> ' + path
        allItems[ selItemIndex ] = insertItem
        cmds.textScrollList( scrollList, e=1, ra=1, append=allItems )
        updatePathPopupMenu_forScrollList( scrollList, popupMenu, addCommand )
        cmds.textScrollList( scrollList, e=1, si= insertItem )
    
    if sgFunctionFileAndPath.isFile(cacheBodyPath) or sgFunctionFileAndPath.isFolder(cacheBodyPath):
        splitPath = cacheBodyPath.replace( '\\', '/' ).split( '/' )
        if splitPath and splitPath[-1] != '':
            cmds.menuItem( l='Back', c=partial( backToUpfolder, cacheBodyPath ) )
    cmds.menuItem( d=1 )
    
    path = cacheBodyPath.replace( '\\', '/' )
    if sgFunctionFileAndPath.isFile(path):
        path = '/'.join( path.split( '/')[:-1] )
    
    def updateTextField( path, *args ):
        insertItem = fileName + ' --> ' + path
        allItems[ selItemIndex ] = insertItem
        cmds.textScrollList( scrollList, e=1, ra=1, append=allItems )
        updatePathPopupMenu_forScrollList( scrollList, popupMenu, addCommand )
        if( addCommand != None ): addCommand()
        cmds.textScrollList( scrollList, e=1, si= insertItem )
    
    for root, dirs, names in os.walk( path ):
        dirs.sort()
        for dir in dirs:
            cmds.menuItem( l= dir, c= partial( updateTextField, root+'/'+dir ) )
        names.sort()
        for name in names:
            extension = name.split( '.' )
            if len( extension ) == 1: continue
            extension = extension[1]
            if not extension.lower() in targetExtensions:continue
            cmds.menuItem( l= name, c= partial( updateTextField, root+'/'+name ) )
        break
    
    cmds.textScrollList( scrollList, e=1, sc=partial( updatePathPopupMenu_forScrollList, scrollList, popupMenu, addCommand ) )