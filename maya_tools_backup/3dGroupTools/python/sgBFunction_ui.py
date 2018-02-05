import maya.cmds as cmds
import sgBFunction_base
import sgBFunction_value
from functools import partial
import os



class PopupFieldUI:


    def __init__(self, label, popupLabel='Load Selected', typ='single', addCommend = [], **options ):
        
        self._label = label
        self._popup = popupLabel
        self._position = sgBFunction_value.getValueFromDict( options, 'position' )
        self._textWidth = sgBFunction_value.getValueFromDict( options, 'textWidth' )
        self._olnyAddCommand = sgBFunction_value.getValueFromDict( options, 'olnyAddCmd' )
        self._addCommand = addCommend
        if self._textWidth == None: self._textWidth = 120
        self._field  =''
        self._type = typ
        self._cmdPopup = [self.cmdLoadSelected]



    def cmdLoadSelected(self):
        
        if self._olnyAddCommand:
            if type( self._addCommand ) in [ type(()), type([]) ]:
                for command in self._addCommand: command()
            else:
                self._addCommand()
            return None
        
        sels = cmds.ls( sl=1, sn=1 )
        if not sels: return None
        
        if self._type == 'single':
            cmds.textField( self._field, e=1, tx=sels[-1] )
        else:
            popupTxt = ''
            for sel in sels:
                popupTxt += sel + ' '
            cmds.textField( self._field, e=1, tx=popupTxt[:-1] )
        
        if self._addCommand:
            if type( self._addCommand ) in [ type(()), type([]) ]:
                for command in self._addCommand: command()
            else:
                self._addCommand()
        


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



class PopupFieldUI_b:


    def __init__(self, label, **options ):
        
        import sgBFunction_value
        
        popupLabel = sgBFunction_value.getValueFromDict( options, *['popupLabel', 'popLabel'] )
        typ        = sgBFunction_value.getValueFromDict( options, *['type', 'typ'] )
        addCommand = sgBFunction_value.getValueFromDict( options, *['addCommand', 'addCmd'] )
        globalForm = sgBFunction_value.getValueFromDict( options, *['globalForm', 'form'] )
        globalField = sgBFunction_value.getValueFromDict( options, *['globalField', 'field'] )
        
        if not popupLabel: popupLabel = 'Load Selected'
        if not typ       : typ = 'single'
        if not addCommand: addCommand = []
        
        self._label = label
        self._popup = popupLabel
        self._position = sgBFunction_value.getValueFromDict( options, 'position' )
        self._textWidth = sgBFunction_value.getValueFromDict( options, 'textWidth' )
        self._olnyAddCommand = sgBFunction_value.getValueFromDict( options, 'olnyAddCmd' )
        self._addCommand = addCommand
        if self._textWidth == None: self._textWidth = 120
        self._field  =''
        self._type = typ
        self._cmdPopup = [self.cmdLoadSelected]
        self._globalForm = globalForm
        self._globalField = globalField



    def cmdLoadSelected(self):
        
        if self._olnyAddCommand:
            if type( self._addCommand ) in [ type(()), type([]) ]:
                for command in self._addCommand: command()
            else:
                self._addCommand()
            return None
        
        sels = cmds.ls( sl=1, sn=1 )
        if not sels: return None
        
        if self._type == 'single':
            cmds.textField( self._field, e=1, tx=sels[-1] )
        else:
            popupTxt = ''
            for sel in sels:
                popupTxt += sel + ' '
            cmds.textField( self._field, e=1, tx=popupTxt[:-1] )
        
        if self._addCommand:
            if type( self._addCommand ) in [ type(()), type([]) ]:
                for command in self._addCommand: command()
            else:
                self._addCommand()
        


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
        
        self._globalForm = form
        self._globalField = field
        
        return form

        

def updatePathPopupMenu( textField, popupMenu, addCommand=None, *args ):
    
    targetExtensions = ['mb', 'ma', 'fbx', 'obj']
    
    try:path = cmds.textFieldGrp( textField, q=1, tx=1 )
    except:path = cmds.textField( textField, q=1, tx=1 )
    
    splitPath = path.replace( '\\', '/' ).split( '/' )
    if not os.path.isfile(path) and not os.path.isdir(path):
        path = '/'.join( splitPath[:-1] )
    
    cmds.popupMenu( popupMenu, e=1, dai=1 )
    cmds.setParent( popupMenu, menu=1 )
    cmds.menuItem( l='Open File Browser', c=partial( sgBFunction_base.openFileBrowser, path ) )
    cmds.menuItem( d=1 )
    
    def backToUpfolder( path, *args ):
        print "back to folder"
        path = path.replace( '\\', '/' )
        
        if os.path.isdir( path ):
            path = '/'.join( path.split( '/' )[:-1] )
        else:
            path = '/'.join( path.split( '/' )[:-2] )
        try:cmds.textFieldGrp( textField, e=1, tx=path )
        except:cmds.textField( textField, e=1, tx=path )
        updatePathPopupMenu( textField, popupMenu, addCommand )
    
    if os.path.isfile(path) or os.path.isdir(path):
        splitPath = path.replace( '\\', '/' ).split( '/' )
        if splitPath and splitPath[-1] != '':
            cmds.menuItem( l='Back', c=partial( backToUpfolder, path ) )
    cmds.menuItem( d=1 )
    
    path = path.replace( '\\', '/' )
    if os.path.isfile(path):
        path = '/'.join( path.split( '/')[:-1] )
    
    def updateTextField( path, *args ):
        try:cmds.textFieldGrp( textField, e=1, tx=path )
        except:cmds.textField( textField, e=1, tx=path )
        updatePathPopupMenu( textField, popupMenu, addCommand )
    
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
    
    if addCommand != None: addCommand()
    
    try:
        cmds.textField( textField, e=1, ec=partial( updatePathPopupMenu, textField, popupMenu, addCommand ) )
        cmds.textField( textField, e=1, cc=partial( updatePathPopupMenu, textField, popupMenu, addCommand ) )
    except:
        cmds.textFieldGrp( textField, e=1, ec=partial( updatePathPopupMenu, textField, popupMenu, addCommand ) )
        cmds.textFieldGrp( textField, e=1, cc=partial( updatePathPopupMenu, textField, popupMenu, addCommand ) )




def createWaningWindow( parentWindowName, message, conntinueCommand, continueLabel = 'Continue' ):
    
    pTitle = cmds.window( parentWindowName, q=1, title=1 )
    
    winName = 'warning_window'
    title   = '%s Warning' % pTitle
    
    def cmdContinue( *args ):
        conntinueCommand()
        cmds.deleteUI( winName )
    
    def cmdClose( *args ):
        cmds.deleteUI( winName )
    
    if cmds.window( winName, ex=1 ): cmds.deleteUI( winName )
    cmds.window( winName, title=title )
    
    wh  = cmds.window( parentWindowName, q=1, wh=1 )
    tlc = cmds.window( parentWindowName, q=1, tlc=1 )
    width  = wh[0]-4
    
    cmds.columnLayout()
    cmds.rowColumnLayout( nc=1, cw=[(1,width)])
    cmds.text( l=message, al='center' )
    cmds.setParent( '..' )

    halfWidth = (width) * 0.5
    otherWidth = (width) - halfWidth
    cmds.rowColumnLayout( nc=2, cw=[(1,halfWidth),(2,otherWidth)] )
    cmds.button( l= continueLabel, c=cmdContinue )
    cmds.button( l= 'Close', c=cmdClose )
    
    cmds.showWindow( winName )
    cmds.window( winName, e=1, wh=[ width, 50 ], tlc=[ tlc[0]+wh[1]+38, tlc[1] ], rtf=1 )



class Slider:
    
    def __init__(self, **options ):
        
        self.options = options
    
    
    def create(self):

        form = cmds.formLayout()
        slider = cmds.floatSliderGrp( **self.options )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1,
                         af=[( slider, 'top', 0 ), ( slider, 'left', 0 ), ( slider, 'right', 0 )])
        
        self.form = form
        self.slider = slider
        
        return form




class Buttons_two:

    def __init__( self, label1='', label2='', h=25 ):
        
        self.label1 = label1
        self.label2 = label2
        self.height = h
    
    
    def create(self):
        
        form = cmds.formLayout()
        button1 = cmds.button( l= self.label1, h=self.height )
        button2 = cmds.button( l= self.label2, h=self.height )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1,
                         af=[( button1, 'top', 0 ), ( button1, 'left', 0 ),
                             ( button2, 'top', 0 ), ( button2, 'right', 0 )], 
                         ap=[( button1, 'right', 0, 50 ),
                             ( button2, 'left', 0, 50 )] )
        
        self.button1 = button1
        self.button2 = button2
        
        return form



class Button_changedCondition:
    
    def __init__( self, labels, colors=None, commands=None, **options ):
        
        self.labels = labels
        self.commands = commands
        self.colors = colors
        self.button = None
        self.currentIndex = 0
        
        self.options = options
    

    def create( self ):
        
        self.button = cmds.button( l=self.labels[0], c=self.cmdButton, **self.options )
        if self.colors: cmds.button( self.button, e=1, bgc=self.colors[0] )
        
        return self.button


    def setCommands( self, commands ):
        
        self.commands = commands


    def cmdButton( self, *args ):
        
        if self.commands:
            self.commands[ self.currentIndex ]()
        cmds.button( self.button, e=1, label=self.labels[ self.currentIndex ] )


    def gotoCondition( self, index ):
        
        cmds.button( self.button, e=1, label=self.labels[ index ] )
        if self.colors: cmds.button( self.button, e=1, bgc= self.colors[ index ] )
        self.currentIndex = index


class OptionMenu:
    
    def __init__(self, label, nameItems ):
        
        self._label = label
        self._nameItems  = nameItems
        
        self._items = []
        self._menu = ''
    
    
    def create(self, cw=[80,80] ):
        
        self._menu = cmds.optionMenuGrp( l=self._label, cw2=cw )

        for nameItem in self._nameItems:
            self._items.append( cmds.menuItem( l=nameItem ) )
    
    
    def resetMenu(self, nameItems ):
        
        for item in self._items:
            cmds.deleteUI( item )
        
        self._items = []
        
        for nameItem in nameItems:
            self._items.append( cmds.menuItem( l=nameItem, p=(self._menu+'|OptionMenu') ) )