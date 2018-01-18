from maya import cmds
from functools import partial


class Win_Global:
    
    winName = 'sg_controller_color_ui'
    title = "Index Color Editor"
    width = 200
    height = 50

    colors = [ [0.467,0.467,0.467],
        [0.000,0.000,0.000],
        [0.247,0.247,0.247],
        [0.498,0.498,0.498],
        [0.608,0.000,0.157],
        [0.000,0.016,0.373],
        [0.000,0.000,1.000],
        [0.000,0.275,0.094],
        [0.145,0.000,0.263],
        [0.780,0.000,0.780],
        [0.537,0.278,0.200],
        [0.243,0.133,0.122],
        [0.600,0.145,0.000],
        [1.000,0.000,0.000],
        [0.000,1.000,0.000],
        [0.000,0.255,0.600],
        [1.000,1.000,1.000],
        [1.000,1.000,0.000],
        [0.388,0.863,1.000],
        [0.263,1.000,0.635],
        [1.000,0.686,0.686],
        [0.890,0.675,0.475],
        [1.000,1.000,0.384],
        [0.000,0.600,0.325],
        [0.627,0.412,0.188],
        [0.620,0.627,0.188],
        [0.408,0.627,0.188],
        [0.188,0.627,0.365],
        [0.188,0.627,0.627],
        [0.188,0.404,0.627],
        [0.435,0.188,0.627],
        [0.627,0.188,0.412]]



class Win_Cmd:
    
    @staticmethod
    def setColor( colorIndex, evt=0 ):
        sels = cmds.ls( sl=1 )
        for sel in sels:
            selShape = cmds.listRelatives( sel, s=1, f=1 )
            if not selShape:
                cmds.setAttr( sel + '.overrideEnabled', 1 )
                cmds.setAttr( sel + '.overrideColor', colorIndex )
            else:
                for shape in selShape:
                    cmds.setAttr( shape + '.overrideEnabled', 1 )
                    cmds.setAttr( shape + '.overrideColor', colorIndex )
        cmds.select( cl=1 )



class Win:
    
    def __init__(self):
        
        pass


    def create(self):
        
        if cmds.window( Win_Global.winName, q=1, ex=1 ):
            cmds.deleteUI( Win_Global.winName )
        cmds.window( Win_Global.winName, title=Win_Global.title )
        
        cmds.columnLayout()
        cmds.gridLayout( nr=4, nc=8, cwh=[30,20] )
        for i in range( len( Win_Global.colors ) ):
            cmds.button( label='%d' % i, bgc=Win_Global.colors[i], c=partial( Win_Cmd.setColor, i ) )
        
        cmds.window( Win_Global.winName, e=1,
                     width = Win_Global.width, height = Win_Global.height,
                     rtf=1 )
        cmds.showWindow( Win_Global.winName )



def show():
    Win().create()


if __name__ == '__main__':
    show()


