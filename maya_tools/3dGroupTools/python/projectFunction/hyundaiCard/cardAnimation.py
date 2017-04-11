import maya.cmds as cmds
import math
import random

def excute( startFrame ):
    
    sels = cmds.ls( '*:ctl' )
    
    animCurves = cmds.listConnections( sels, type='animCurve' )
    cmds.delete( animCurves )
    
    timeLength = 1.7
    timeList = [startFrame, timeLength+startFrame]
    timeList2 = [(timeLength)*0.5+startFrame, timeLength+startFrame]
    valueList = [0.0, startFrame]
    valueList2 = [0.0, 0.5]
    
    rotTimeList = [startFrame, (timeLength)*0.1+startFrame, timeLength*0.7+startFrame]
    rotXValueList = [0.0, 1.0, 0.0]
    rotZValueList = [0.0, 1.3, 0.0]
    
    distanceLength = 60.0
    
    stretchTimeLength = 10
    distMult = stretchTimeLength / distanceLength
    rotSize = 1.5
    
    addTimeMult = 0.5
    timePowRate = 3.0
    
    selgoKeys = []
    
    for sel in sels:
        goPiv = sel.replace( 'ctl', 'goPiv' )
        dist = math.fabs( cmds.getAttr( goPiv+'.ty' ) )
        addTime = dist * distMult
        
        addTime = ( addTime/stretchTimeLength )**timePowRate * stretchTimeLength
        multValue = addTime*rotSize*random.uniform( -1.0, 1.0 )
        plusMinus = random.uniform( -1, 1 )
        if plusMinus < 0:
            pass#multValue *= -0.0
        addTime *= random.uniform( 0.95, 1.05 )
        
        for i in range( 2 ):
            cmds.setKeyframe( sel+'.go', t=timeList[i]+addTime, v=valueList[i] )
            cmds.setKeyframe( sel+'.change', t=timeList2[i]+addTime, v=valueList2[i] )
        cmds.scaleKey( sel+'.go', tp= timeList[0]+addTime, ts=(1+addTime*addTimeMult), vp=0, vs=1 )
        cmds.scaleKey( sel+'.change', tp= timeList[0]+addTime, ts=(1+addTime*addTimeMult), vp=0, vs=1 )
        endTime = cmds.keyframe( sel+'.go', q=1, tc=1 )[-1]
        cmds.keyTangent( sel+'.go', itt='spline', ott='spline' )
        
        cmds.setKeyframe( sel+'.change', t=endTime+0, v=valueList2[1] )
        cmds.setKeyframe( sel+'.change', t=endTime+1, v=1 )
        
        for i in range( 3 ):
            cmds.setKeyframe( sel+'.rotX', t=rotTimeList[i]+addTime, v=rotXValueList[i]*multValue )
            cmds.setKeyframe( sel+'.rotZ', t=rotTimeList[i]+addTime, v=rotZValueList[i]*multValue )
        cmds.scaleKey( sel+'.rotX', tp= rotTimeList[0]+addTime, ts=(1+addTime*addTimeMult), vp=0, vs=1 )
        cmds.scaleKey( sel+'.rotZ', tp= rotTimeList[0]+addTime, ts=(1+addTime*addTimeMult), vp=0, vs=1 )
        
        cmds.keyTangent( sel+'.rotX', itt='spline', ott='spline' )
        cmds.keyTangent( sel+'.rotZ', itt='spline', ott='spline' )
        
        selgoKeys += cmds.listConnections( sel+'.go', s=1, d=0, type='animCurve' )
        
        
    cmds.select( selgoKeys )



def getSurfaceColorValues( objs, surf ):
    
    closeSurf = cmds.createNode( 'closestPointOnSurface' )
    surfShape = cmds.listRelatives( surf, s=1 )[0]
    shadingEngins = cmds.listConnections( surfShape+'.instObjGroups[0]' )
    engin = shadingEngins[0]
    
    shaders = cmds.listConnections( engin+'.surfaceShader' )
    
    textures = cmds.listConnections( shaders[0]+'.color' )
    
    cmds.connectAttr( surfShape+'.worldSpace', closeSurf+'.inputSurface' )
    
    colorValues = []
    minValue = 2.0
    maxValue = -1.0
    for obj in objs:
        dcmp = cmds.createNode( 'decomposeMatrix' )
        
        cmds.setAttr( dcmp+'.imat', cmds.getAttr( obj+'.wm' ), type='matrix' )
        cmds.setAttr( closeSurf+'.inPosition', *cmds.getAttr( dcmp+'.ot' )[0] )
    
        colors = cmds.colorAtPoint( textures[0], u=cmds.getAttr( closeSurf+'.u' ),
                                                v=cmds.getAttr( closeSurf+'.v' ) )
        value = 0.0
        for color in colors:
            value += color
        value /= len( colors )
        
        if value > maxValue:
            maxValue = value
        if value < minValue:
            minValue = value
        
        colorValues.append( value )
        
    cmds.delete( closeSurf )
    
    return colorValues, minValue, maxValue



def setKeyCards( cards, surf, 
                 startFrame, changeLength, offsetLength,
                 rotXScale, rotYScale, rotZScale, rotStartOffset, rotEndOffset, randRate ):
    
    animCurves = cmds.listConnections( cards, type='animCurve' )
    cmds.delete( animCurves )
    
    colorValues, minValue, maxValue = getSurfaceColorValues( cards, surf )
    
    attrAndKeyList = []
    
    cValue = 0.5
    
    attrAndKeyList.append( ['change',
                           [startFrame, 0], 
                           [startFrame + changeLength,1]] )
    attrAndKeyList.append( ['rotX',
                           [startFrame+rotStartOffset, 0],
                           [startFrame+changeLength*cValue+rotStartOffset, rotXScale],
                           [startFrame+changeLength+rotEndOffset, 0]] )
    attrAndKeyList.append( ['rotY',
                           [startFrame+rotStartOffset, 0],
                           [startFrame+changeLength*cValue+rotStartOffset, rotYScale],
                           [startFrame+changeLength+rotEndOffset, 0]] )
    attrAndKeyList.append( ['rotZ',
                           [startFrame+rotStartOffset, 0],
                           [startFrame+changeLength*cValue+rotStartOffset, rotZScale],
                           [startFrame+changeLength+rotEndOffset, 0]] )
    
    decreasePow = 0.5
    for i in range( len( cards ) ):
        card = cards[i]
        colorValue = 1.0-colorValues[i]
        
        rate = (colorValues[i] - minValue)/(maxValue-minValue)
        decreaseRate = rate**decreasePow
        offsetRate = offsetLength * colorValue
        
        for attrAndKey in attrAndKeyList:
            attr = attrAndKey[0]
            keyAndValues = attrAndKey[1:]
            
            isRotAttr = False
            randOffset = 0.0
            if attr.find( 'rot' ) != -1:
                isRotAttr = True
                randOffset = random.uniform( -randRate, randRate )
            
            for key, value in keyAndValues:
                if isRotAttr:
                    value *= random.uniform( -1, 1 )
                    value *= decreaseRate
                
                key = (key-startFrame) * (colorValue+1)+startFrame
                cmds.setKeyframe( card+'.'+attr, 
                                  t= key + offsetRate + randOffset, 
                                  v= value )
                
                
def setKeyCards2( cards, surf,
                  startFrame, changeLength, offsetLength,
                  rotXScale, rotYScale, rotZScale, rotStartOffset, rotEndOffset, randRate ):
    
    colorValues, minValue, maxValue = getSurfaceColorValues( cards, surf )
    
    attrAndKeyList = []
    
    cValue = 0.5
    
    attrAndKeyList.append( ['go',
                           [startFrame, 0], 
                           [startFrame + changeLength,1]] )
    attrAndKeyList.append( ['rotX',
                           [startFrame+rotStartOffset, 0],
                           [startFrame+changeLength*cValue+rotStartOffset, rotXScale],
                           [startFrame+changeLength+rotEndOffset, 0]] )
    attrAndKeyList.append( ['rotY',
                           [startFrame+rotStartOffset, 0],
                           [startFrame+changeLength*cValue+rotStartOffset, rotYScale],
                           [startFrame+changeLength+rotEndOffset, 0]] )
    attrAndKeyList.append( ['rotZ',
                           [startFrame+rotStartOffset, 0],
                           [startFrame+changeLength*cValue+rotStartOffset, rotZScale],
                           [startFrame+changeLength+rotEndOffset, 0]] )
    
    decreasePow = 0.25
    for i in range( len( cards ) ):
        card = cards[i]
        colorValue = 1.0-colorValues[i]
        
        rate = (colorValues[i] - minValue)/(maxValue-minValue)
        decreaseRate = rate**decreasePow
        offsetRate = offsetLength * colorValue
        
        decreaseRate= 1.0
        
        for attrAndKey in attrAndKeyList:
            attr = attrAndKey[0]
            keyAndValues = attrAndKey[1:]
            
            isRotAttr = False
            randOffset = 0.0
            if attr.find( 'rot' ) != -1:
                isRotAttr = True
                randOffset = random.uniform( -randRate, randRate )
            
            
            for key, value in keyAndValues:
                if isRotAttr:
                    value *= random.uniform( -1, 1 )
                    value *= decreaseRate
                
                #key = (key-startFrame) * ((1-colorValue)**1.1)+startFrame
                cmds.setKeyframe( card+'.'+attr, 
                                  t= key + offsetRate + randOffset, 
                                  v= value )
        endKey = cmds.keyframe( card+'.go', q=1, tc=1 )[-1]
        cmds.setKeyframe( card+'.vis',
                          t= endKey, v=1 )
        cmds.setKeyframe( card+'.vis',
                          t= endKey+1, v=0 )
    