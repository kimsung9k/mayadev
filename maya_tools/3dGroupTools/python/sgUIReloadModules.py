import maya.cmds as cmds
import sys


class ModuleNameField:
    
    def __init__(self, parentUi, width ):
        
        cmds.setParent( parentUi )
        cmds.rowColumnLayout( nc=1, cw=[(1, width-2)] )
        self.textField  = cmds.textField()
        cmds.setParent( '..' )



class Window:
    
    def __init__(self):
        
        self.uiname = 'sgReloadModulesUi'
        self.title  = 'SG ReLoad Modules UI'
        self.width = 300
        self.height = 50
    
    
    def cmdSet(self, *args ):
        
        print "----------------------------------------------------"
        for field in self.fields:
            txt = cmds.textField( field.textField, q=1, tx=1 )
            
            if not txt: continue
            try:
                reload( sys.modules['%s' % txt ] )
                print '"%s" module reloaded.' % txt
            except:
                cmds.warning( '"%s" module reload Failed.' % txt )
                pass
        print "----------------------------------------------------"
                
                
    def cmdAppend(self, *args ):
        
        field = ModuleNameField( self.rowColumnField, self.columnWidth )
        self.fields.append( field )
        
        
    def cmdCancel(self, *args ):
        
        cmds.deleteUI( self.uiname, wnd=1 )
        

    
    def show(self):
        
        self.fields = []
        
        if cmds.window( self.uiname, ex=1 ):
            cmds.deleteUI( self.uiname, wnd=1 )
        
        cmds.window( self.uiname, title= self.title )
        
        columnLayout = cmds.columnLayout()
        columnWidth = self.width - 2
        
        self.rowColumnField = cmds.rowColumnLayout( nc=1, cw=[( 1, self.width ) ] )
        cmds.button( l='Append', c= self.cmdAppend )
        field = ModuleNameField( columnLayout, columnWidth )
        self.fields.append( field )
        cmds.setParent( '..' )
        
        firstWidth = (columnWidth-2) / 2
        secondWidth =  columnWidth - 2 - firstWidth
        
        cmds.rowColumnLayout( nc=2, cw=[(1, firstWidth),(2, secondWidth) ] )
        cmds.button( l='Set', c= self.cmdSet )
        cmds.button( l='Cancel', c= self.cmdCancel )
        cmds.setParent( '..' )
        
        cmds.window( self.uiname, e=1, width= self.width, height = self.height )
        cmds.showWindow( self.uiname )
        
        self.columnWidth = self.width -2


mc_showWindow = """import sgUIReloadModules
sgUIReloadModules.Window().show()"""