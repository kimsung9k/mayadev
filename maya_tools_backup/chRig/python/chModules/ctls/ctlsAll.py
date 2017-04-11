import maya.cmds as cmds
import chModules.basecode as basecode

class CtlsAll( object ):
    def __init__(self):
        pass
    
    def getNamespace( self, target ):
        cons = cmds.listConnections( target+'.message', type='multDoubleLinear' )

        if not cons:
            return ''
        
        for con in cons:
            if cmds.attributeQuery( 'originalName', n=con, ex=1 ):
                if cmds.getAttr( con+'.originalName' ).find( 'RightClickObj' ) != -1:
                    return con.replace( cmds.getAttr( con+'.originalName' ), '' )
            
        return ''