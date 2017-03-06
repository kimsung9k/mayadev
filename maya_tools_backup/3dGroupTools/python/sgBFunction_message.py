import maya.OpenMaya as om
import sgBModel_message

def appendEventCallback( event, ptrFunction ):
    
    eventMessage = om.MEventMessage()
    callback = eventMessage.addEventCallback( event, ptrFunction )
    sgBModel_message.eventMessageCallbacks.append( callback )



def removeAllEventCallback():
    
    eventMessage = om.MEventMessage()
    for callbackId in sgBModel_message.eventMessageCallbacks:
        eventMessage.removeCallback( callbackId )
    sgBModel_message.eventMessageCallbacks = []