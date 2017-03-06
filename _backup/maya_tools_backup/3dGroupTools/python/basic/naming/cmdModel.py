from basic.naming.ui import view
import maya.cmds as cmds


mmShowNumberingUI = """import basic.naming.ui.view
basic.naming.ui.view.NumberingUI().show()
"""
    
    
mmShowReplaceNameUI = """import basic.naming.ui.view
basic.naming.ui.view.ReplaceNameUI().show()
"""
    
    
    
def removeNamespaceSelH( target ):
    
    children = cmds.listRelatives( target, c=1, ad=1, f=1, type='transform' )
    if not children: children = []
    children.append( target )
    for child in children:
        if not cmds.objExists( child ): print child; continue
        splitName = child.split( ':' )[-1]
        if splitName.find( '|' ) != -1: 
            splitName = splitName.split( '|' )[-1]
        cmds.rename( child, splitName )
        
        
        
        
mmRemoveNamespaceSelH = """import maya.cmds as cmds
import basic.naming.cmdModel
sels = cmds.ls( sl=1 )
for sel in sels:
    basic.naming.cmdModel.removeNamespaceSelH( sel )
"""
        
        
        

mmRenameShapeSelected = """import maya.cmds as cmds
trans_name_long = cmds.ls(selection=True, long=True);
trans_name_short= cmds.ls(selection=True);
for i in range(len(trans_name_long)):
    shape_name_long = (cmds.listRelatives(trans_name_long[i], s=True, f=True));
    shape_name_short = (cmds.listRelatives(trans_name_long[i], s=True));
    if (trans_name_short[i]+"Shape") != shape_name_short[0]:
        cmds.rename(shape_name_long[0],(trans_name_short[i]+"Shape"));
"""