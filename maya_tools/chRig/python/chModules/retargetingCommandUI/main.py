import model, view, view_sub, control
import maya.cmds as cmds

global _win

def Show( *args ):
    
    global _win
    
    view.UI().create()
    control.SetClearCmd()
    
    inst = view_sub.RenameUI()
    model.FolderUIInfo._cmdOpenRenameSub.append( inst.create )
    inst = view_sub.DeleteUI()
    model.FolderUIInfo._cmdOpenDeleteSub.append( inst.create )
    
    control.SetUICmd()
    control.SetCmd()
    
    cmds.showWindow( model.WindowInfo._window )
    
    try:
        from BorderlessFrame import BorderlessFrame, toQtObject
        dlg = toQtObject( model.WindowInfo._window )
        _win = BorderlessFrame()
        _win.setContent( dlg )
        _win.setTitle( model.WindowInfo._title )
        _win.show()
        _win.resize(842,539)
    except: pass