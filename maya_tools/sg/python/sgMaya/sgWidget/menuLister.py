from maya import cmds



class Win_Global:
    
    winName = 'sg_menuLister'
    title   = 'Menu Lister'





class UI_folderList:
    
    def __init__(self):
        
        self.buttonSize = 23
        self.frameLabel = ''
        
    
    def create(self):
        
        frame = cmds.frameLayout( l=self.frameLabel )
        form = cmds.formLayout()
        textList = cmds.textScrollList()
        addButton = cmds.button( l='+', w=self.buttonSize, h=self.buttonSize )
        cmds.setParent('..')
        cmds.setParent('..' )
        
        cmds.formLayout( form, e=1,
                         af=[( textList, 'left', 0), ( textList, 'top', 0 ), ( textList, 'bottom', 0 ), ( textList, 'right', 0 ),
                             ( addButton, 'top', 10), ( addButton, 'right', 10)] )
        
        self.textList      = textList
        self.addButton     = addButton
        
        return frame




class Win:
    
    def __init__(self ):
        
        self.ui_folderLists = []


    def addListUI(self, frameLabel ):
        
        ui = UI_folderList()
        ui.frameLabel = frameLabel
        self.ui_folderLists.append( ui )    
    
    
    def create(self):
        
        if cmds.window( Win_Global.winName, q=1, ex=1 ):
            cmds.deleteUI( Win_Global.winName )
        
        cmds.window( Win_Global.winName, title= Win_Global.title )
        
        formOuter = cmds.formLayout()
        
        formInner = cmds.paneLayout( configuration='horizontal4' )
        for folderList in self.ui_folderLists:
            folderList.create()
        cmds.setParent( '..' )

        closeButton = cmds.button( l='CLOSE', c="cmds.deleteUI('%s')" % Win_Global.winName )
        cmds.formLayout( formOuter, e=1, 
                         af=[ ( formInner, 'top', 0 ), ( formInner, 'left', 0 ), ( formInner, 'right', 0 ),
                              ( closeButton, 'bottom', 0 ), ( closeButton, 'left', 0 ), ( closeButton, 'right', 0 ) ],
                         ac=[ ( formInner, 'bottom', 0, closeButton )] )
        cmds.setParent( '..' )
        
        cmds.showWindow( Win_Global.winName )


def show():
    Win.create()


if __name__ == '__main__':
    show()


