import maya.OpenMaya as om
from functools import partial
import sgBModel_callbackIds


sceneMessage = om.MSceneMessage()

enumIndexDict = {}
list_sceneMessageCmd = []


for item in dir( sceneMessage ):
    if not item[0] == 'k': continue
    index = 0
    exec( 'index = sceneMessage.%s' % item )
    enumIndexDict.update( { item : index } )
    list_sceneMessageCmd.append([])



def excuteList_sceneMessageCmd( enumIndex, *args ):
    for cmd in list_sceneMessageCmd[ enumIndex ]:
        try:cmd()
        except:pass



def addAllSceneMessageCallbacks():
    
    for callbackId in sgBModel_callbackIds.callbackIds:
        sceneMessage.removeCallback( callbackId )
    
    for enumLabel, enumIndex in enumIndexDict.items():
        enumTarget = None
        exec( 'enumTarget = om.MSceneMessage.%s' % enumLabel )
        try:
            callbackId = sceneMessage.addCallback( enumTarget, partial( excuteList_sceneMessageCmd, enumIndex ) )
            sgBModel_callbackIds.callbackIds.append( callbackId )
        except:
            pass



def appendCallback_sceneMessage( messageName, ptrFunction ):
    
    enumIndex = enumIndexDict[ messageName ]
    list_sceneMessageCmd[ enumIndex ].append( ptrFunction )