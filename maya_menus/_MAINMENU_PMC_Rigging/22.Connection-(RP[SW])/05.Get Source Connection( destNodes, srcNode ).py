import maya.cmds as cmds

sels = cmds.ls( sl=1 )

targets = sels[:-1]
source  = sels[-1]


def getSourceConnection( src, trg ):

    src = cmds.ls( src )[0]
    trg = cmds.ls( trg )[0]
    cons = cmds.listConnections( src, s=1, d=0, p=1, c=1 )

    if not cons: return None

    srcCons  = cons[1::2]
    destCons = cons[::2]

    for i in range( len( srcCons ) ):
        srcCon = srcCons[i]
        destCon = destCons[i].replace( src, trg )

        if cmds.nodeType( src ) == 'joint' and cmds.nodeType( trg ) =='transform':
            destCon = destCon.replace( 'jointOrient', 'rotate' )

        if not cmds.ls( destCon ): continue

        if not cmds.isConnected( srcCon, destCon ):
            cmds.connectAttr( srcCon, destCon, f=1 )


for target in targets:
    getSourceConnection( source, target )

cmds.select( targets )