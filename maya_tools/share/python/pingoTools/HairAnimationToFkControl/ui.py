import maya.cmds as cmds
selA = cmds.ls( sl=1 )
class hairUI():
    def __init__(self, nameA):
        self.nameA = nameA
        #self.nameB = nameB
        #self.nameC = nameC
    def listSel(self): 
        selA = cmds.ls( sl=1 )
        TSL=cmds.textScrollList(edit=True, ra=True)
        for x in selA:
            TSL=cmds.textScrollList(append=selA[x], edit=True)
        
    def printSel(self): 
        someList = cmds.textScrollList('TSL', q=1, si=1)
        print someList
    
    window = cmds.window()
    form = cmds.formLayout( h=300)
    b1 = cmds.button(l='CONTROLLER\nLIST', w=180, command=listSel)
    b2 = cmds.button(l='SET')
    b3 = cmds.button(l='BAKE')
    RCY = cmds.rowColumnLayout(numberOfColumns=1)
    TSL = cmds.textScrollList(append=selA , numberOfRows=10, ams=1, w=200, h=100, dcc='printSel(self)')
    cmds.formLayout( form, edit=True,
    attachForm=[(b1, 'top', 15), (b1, 'left', 15), 
                (b2, 'left', 15), (b2, 'right', 15), 
                (b3, 'left', 15), (b3, 'bottom', 15), (b3, 'right', 15),
                (RCY, 'top', 15), (RCY, 'right', 15)], 
    attachControl=[(b1, 'bottom', 15, b2), (b2, 'bottom', 15, b3), (b2, 'top', 30, RCY)], 
    attachPosition=[(b2, 'top', 5, 50), (b3, 'top', 5, 75), (RCY, 'left', 0, 50), (RCY, 'bottom', 0, 50)])
    cmds.showWindow( window )


#_Jnt = hairUI('asd')
#_Jnt.scrollList()

#cmds.textScrollList(append=selA, ams=1, w=200, h=80)