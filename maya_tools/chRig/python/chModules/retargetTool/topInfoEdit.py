import topInfo
import ctlInfo
import maya.cmds as cmds


def EditNameSpaceInfo( sourceWorldCtl, targetWorldCtl ):
    
    topInfo.sourceNS = sourceWorldCtl.replace( 'World_CTL', '' )
    topInfo.targetNS = targetWorldCtl.replace( 'World_CTL', '' )

    

def EditCtlInfo( target ):
    
    origName = target.replace( topInfo.targetNS, '' )
    
    digitStr = 'NUM'
    for i in origName:
        if i.isdigit():
            if digitStr == 'NUM':
                digitStr = str(i)
            else:
                digitStr += str(i)
    
    side = '_SIDE_'
    
    if origName.find( '_L_' ) != -1:
        side = '_L_'
    elif origName.find( '_R_' ) != -1:
        side = '_R_'
    
    className = origName.replace( digitStr, 'NUM' ).replace( side, '_SIDE_' )
    
    targetClass = None
    exec( 'targetClass = ctlInfo.%s' % className )
    
    orientOrigin = ''
    transParent = ''
    orientOriginRate = False
    transOriginRate = False
    transDirect = False
    try: transDirect = targetClass.transDirect
    except: pass
    try: orientOrigin = targetClass.orientOrigin
    except: pass
    try: transParent = targetClass.transParent
    except: pass
    try: orientOriginRate = targetClass.orientOrientRate
    except: pass
    try: transOriginRate = targetClass.transOriginRate
    except: pass
    
    parentList = []
    for parentStr in targetClass.parentList:
        if digitStr != 'NUM':
            digit = int( digitStr )
            if digit != 0:
                strLen = len( digitStr )
                digitLen = len( str( digit ) )
                replaceDigitStr = '0'*(strLen-digitLen)+str( digit-1 )
                parentList = [ origName.replace( digitStr, replaceDigitStr )]
                break
        
        parentList.append( parentStr.replace( '_SIDE_', side ) )
    
    if transParent.find( '_SIDE_' ):
        transParent = transParent.replace( '_SIDE_', side )
        
    udAttrs = cmds.listAttr( target, k=1, ud=1 )
    if not udAttrs: udAttrs = []
    
    topInfo.target = target
    topInfo.parentList = parentList
    topInfo.orientOrigin = orientOrigin
    topInfo.transDirect = transDirect
    topInfo.orientOriginRate = orientOriginRate
    topInfo.transOriginRate = transOriginRate
    topInfo.transParent = transParent
    topInfo.udAttrs = udAttrs