import maya.cmds as cmds
import dag
import popupCommand


def create( parent ):
    
    sels = cmds.ls( sl=1 )
    
    if not sels: return None
    
    if dag.getLocalName( sels[0] ).find( 'Std_' ) != -1:
        cmds.menuItem( l = "Make Symmetry  >> ", rp = "E", p=parent, c= popupCommand.makeSymmetryToL )
        cmds.menuItem( l = " <<  Make Symmetry",    rp = "W", p=parent, c= popupCommand.makeSymmetryToR )