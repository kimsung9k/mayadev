import maya.cmds as cmds


class PopupFieldUI:
    
    def __init__(self, label, popupLabel='Load Selected', position=40 ):
        
        self._label = label
        self._popup = popupLabel
        self._position = position
        self._field  =''
        self._cmdPopup = [self.cmdLoadSelected]


    def cmdLoadSelected(self):
        sels = cmds.ls( sl=1, sn=1 )
        if not sels: return None
        cmds.textField( self._field, e=1, tx=sels[-1] )


    def cmdPopup(self, *args ):
        for cmd in self._cmdPopup: cmd()


    def create(self):
        
        form = cmds.formLayout()
        text  = cmds.text( l= self._label, al='right', h=20 )
        field = cmds.textField(h=21)
        cmds.popupMenu()
        cmds.menuItem( l=self._popup, c=self.cmdPopup )
        
        cmds.formLayout( form, e=1,
                         af=[(text,'top',0), (text,'left',0),
                             (field,'top',0),(field,'right',0)],
                         ap=[(text,'right',0,self._position)],
                         ac=[(field, 'left', 0, text)] )
        cmds.setParent( '..' )
        
        self._text = text
        self._field = field
        self._form = form
        
        return form