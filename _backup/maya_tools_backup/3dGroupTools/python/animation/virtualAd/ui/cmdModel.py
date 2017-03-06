import maya.cmds as cmds



def copyAndPastkey( first, second, start, end ):
    
    firstChild = cmds.listRelatives( first, c=1, ad=1 )
    secondChild = cmds.listRelatives( second, c=1, ad=1 )
    
    fCtls = []
    for child in firstChild:
        if child[-2:] == '_P':
            ctl = cmds.listRelatives( child, c=1 )[0]
            fCtls.append( ctl )
            
    sCtls = []
    for child in secondChild:
        if child[-2:] == '_P':
            ctl = cmds.listRelatives( child, c=1 )[0]
            sCtls.append( ctl )
            
    
    for i in range( len( fCtls ) ):
        
        fCtl = fCtls[i]
        
        