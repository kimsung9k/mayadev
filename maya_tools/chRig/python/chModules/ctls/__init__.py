import maya.cmds as cmds
import copy

import allCtlsMenu
import headCtlsMenu
import torsoCtlsMenu
import armandlegCtlsMenu
import initCtlsMenu
import bjtsMenu
import ctlsAll

from chModules import basecode



def getProperClassInMenuModule( targetName, menuModule, targetClass=None ):
    moduleClassList = dir( menuModule )
    
    targetName = basecode.removeNumber_str( targetName ).replace( '_L_', '_' ).replace( '_R_', '_' )
    
    matchLen = 0
    targetClassString = ''
    for cls in moduleClassList:
        if targetName.find( cls ) != -1:
            cuLen = len( cls )
            if matchLen < cuLen:
                targetClassString = cls
                matchLen = cuLen
    if targetClassString:
        exec( 'targetClass = %s.%s' % ( menuModule.__name__.split('.')[-1], targetClassString ) )
        
    return targetClass



def getNamespace( target ):
    cons = cmds.listConnections( target+'.message', type='multDoubleLinear' )
    if not cons:
        return ''
        
    for con in cons:
        if cmds.attributeQuery( 'isRightClickObj', n=con, ex=1 ):
            return con.replace( cmds.getAttr( con+'.originalName' ), '' )
            
    return ''



def openMarkingMenu( *args ):
    targetClass = allCtlsMenu.CTL_basic
    
    sels = cmds.ls( sl=1 )
    if not sels: 
        targetClass( 'locusChrigPopup', sels ).openMenu()
        return None
    
    namespace = getNamespace( sels[-1] )
    
    target = sels[-1].replace( '_L_', '_' ).replace( '_R_', '_' ).replace( namespace, '' )
    
    for module in [ allCtlsMenu, initCtlsMenu,  headCtlsMenu, torsoCtlsMenu, armandlegCtlsMenu, bjtsMenu ]:
        targetClass = getProperClassInMenuModule( target, module, targetClass )
        if targetClass != allCtlsMenu.CTL_basic:
            break
    targetClass( 'locusChrigPopup', sels ).openMenu()



if cmds.popupMenu( 'locusChrigPopup', ex=1 ):
    cmds.deleteUI( 'locusChrigPopup' )
cmds.popupMenu( 'locusChrigPopup', sh=1, alt=1, button=3, mm=1, p='viewPanes', pmc=openMarkingMenu )
