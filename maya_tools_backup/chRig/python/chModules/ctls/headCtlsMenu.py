import allCtlsMenu

class Head_CTL( allCtlsMenu.CTL_basic ):
    def __init__( self, parentUi, sels ):
        allCtlsMenu.CTL_basic.__init__( self, parentUi, sels )
        
    def openMenu(self):
        self.defaultMenu()
        self.mirrorMenu()
        self.addMenu()