import maya.cmds as cmds


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