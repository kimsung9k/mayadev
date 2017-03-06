import maya.cmds as cmds



class AttrAndValueField:
    
    def __init__(self, parentUi, width ):
        
        cmds.setParent( parentUi )
        firstWidth = (width-2)/2
        secondWidth = (width-2) - firstWidth
        cmds.rowColumnLayout( nc=2, cw=[(1, firstWidth), (2, secondWidth )] )
        self.attrField  = cmds.textField()
        self.valueField = cmds.textField()
        cmds.setParent( '..' )



class Window:
    
    def __init__(self):
        
        self.uiname = 'sgSetAttrUi'
        self.title  = 'SG Set Attr UI'
        self.width = 300
        self.height = 50
    
    
    def cmdSet(self, *args ):
        
        sels = cmds.ls( sl=1 )
        
        for field in self.fields:
            attr = cmds.textField( field.attrField, q=1, tx=1 )
            value = cmds.textField( field.valueField, q=1, tx=1 )
            
            if not attr: continue
            for sel in sels:
                attrType = cmds.attributeQuery( attr.split( '[' )[0], node=sel, at=1 )
                try: exec( "cmds.setAttr( '%s.%s', %s )" %( sel, attr, value ) )
                except: exec( "cmds.setAttr( '%s.%s', %s, type='%s' )" %( sel, attr, value, attrType ) )
                
                
    def cmdAppend(self, *args ):
        
        field = AttrAndValueField( self.rowColumnField, self.columnWidth )
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
        field = AttrAndValueField( columnLayout, columnWidth )
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



mc_showWindow = """import sgUISetAttr 
sgUISetAttr.Window().show()"""