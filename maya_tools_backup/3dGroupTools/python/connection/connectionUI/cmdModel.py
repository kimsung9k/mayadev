import maya.cmds as cmds


def connectObject( first, second, firstAttrUIs, secondAttrUIs ):

    for i in range( len( secondAttrUIs ) ):
        firstAttr  = cmds.textField( firstAttrUIs[i], q=1, tx=1 )
        secondAttr = cmds.textField( secondAttrUIs[i], q=1, tx=1 )
        cmds.connectAttr( first+'.'+firstAttr, second+'.'+secondAttr,f=1 )
        
        
        

def uiCmd_connectObjectMulti( firstAttrUIs, secondAttrUIs ):

    sels = cmds.ls( sl=1 )

    first = sels[0]

    for sel in sels[1:]:
        connectObject( first, sel, firstAttrUIs, secondAttrUIs )
        
        

def uiCmd_connectObjectSeparate( firstAttrUIs, secondAttrUIs ):

    sels = cmds.ls( sl=1 )

    firsts = sels[::2]
    seconds = sels[1::2]

    for i in range( len( firsts ) ):
        connectObject( firsts[i], seconds[i], firstAttrUIs, secondAttrUIs )