from model import *
from view import *
import os
import copy
import maya.mel as mel


def getKeyValue( value, overValue = 0.05 ):
    
    intValue = int( value )
    minusValue = value - intValue
    
    if minusValue < overValue or minusValue > 1-overValue:
        return intValue
    else:
        return value


def getCtlKeys( ctl ):
    
    attrs = cmds.listAttr( ctl, k=1 )
    
    getFrames = []
    for attr in attrs:
        cuAttrFrames = cmds.keyframe( ctl+'.'+attr, q=1, tc=1 )
        if not cuAttrFrames: continue
        for cuFrame in cuAttrFrames:
            if not cuFrame in getFrames:
                getFrames.append( getKeyValue( cuFrame ) )
    
    getFrames.sort()
    return getFrames


def getCheckKeyframes( ctls ):
    frames = []
    for ctl in ctls:
        cuFrames = getCtlKeys( ctl )
        
        for cuFrame in cuFrames:
            if not cuFrame in frames:
                frames.append( cuFrame )
                
    frames.sort()
    return frames


def cutFrame( start, end, frames ):
    
    if not frames: return []
    
    newFrames = [ float( start )]
    
    startIndex = -1
    for i in range( len( frames ) ):
        if frames[i] > start:
            startIndex = i
            break

    endIndex = -1
    for i in range( startIndex, len( frames ) ):
        if frames[i] >= end:
            endIndex = i
            break
    
    if startIndex == -1:
        startIndex = len( frames )
    if endIndex == -1:
        endIndex = len( frames )
        
    newFrames += frames[startIndex:endIndex]
    newFrames.append( float( end ) )
    
    return newFrames



class ExportData:

    def setCharacter(self, worldCtl ):
        
        namespace = worldCtl.replace( 'World_CTL', '' )
        if not namespace:
            cmds.warning( "%s has no name space" % worldCtl )
            return None
        ExportDataInfo._namespace = worldCtl.replace( 'World_CTL', '' )


    def setEnableDefault( self, value ):
        
        ExportDataInfo._enablePartList = []
        ExportDataInfo._enableCtlList = []
        ExportDataInfo._enableDefault = value
        

    def setPartEnable(self, key, value ):
        
        ExportDataInfo._enablePartList.append( [key, value] )
        
        
    def setCtlEnable(self, nameCtl, value ):
        
        ExportDataInfo._enableCtlList.append( [nameCtl, value] )
        
        
    def setEnable(self ):
        
        cmds.retargetingCommand( enp = [ 'All', ExportDataInfo._enableDefault ] )
        
        for part, value in ExportDataInfo._enablePartList:
            print "export : " , part, value
            cmds.retargetingCommand( enp=[ part, value ] )
        for ctl , value in ExportDataInfo._enableCtlList:
            cmds.retargetingCommand( enc=[ ctl , value ] )
        
        ImportDataInfo._enablePartList = []
        ImportDataInfo._enableCtlList  = []

    
    def getFrames(self, start, end ):
        
        offsetStart = int( start )
        if offsetStart != start :
            if offsetStart < 0: offsetStart -= 1
        
        ExportDataInfo._startFrame  = start - offsetStart
        ExportDataInfo._endFrame    = end   - offsetStart
        ExportDataInfo._offsetFrame = offsetStart
        
        ns = ExportDataInfo._namespace
        ctlSet = ExportDataInfo._ctlSet
        
        ExportDataInfo._checkFrames = []
        
        enableParts = []
        disableParts = []
        enableCtls = []
        disableCtls = []
        
        exportKeyCtls = []
        
        for part, value in ExportDataInfo._enablePartList:
            if value: enableParts.append( part )
            else:     disableParts.append( part )
        for ctl, value in ExportDataInfo._enableCtlList:
            if value: enableCtls.append( ctl )
            else:     disableCtls.append( ctl )
        
        if ExportDataInfo._enableDefault:
            for key in ExportDataInfo._ctlParts:
                if key in disableParts: continue
                for item in ctlSet[ key ]._items:
                    exportKeyCtls.append( ns+item )
        else:
            for key in ExportDataInfo._ctlParts:
                if not key in enableParts: continue
                for item in ctlSet[ key ]._items:
                    exportKeyCtls.append( ns+item )
                    
        for ctl in enableCtls:
            if not ns+ctl in exportKeyCtls: exportKeyCtls.append( ns+ctl )
        for ctl in disableCtls:
            if ns+ctl in exportKeyCtls: exportKeyCtls.remove( ns+ctl )
        
        ExportDataInfo._exportKeyCtls = exportKeyCtls
        
        keyframes = getCheckKeyframes( exportKeyCtls )
        for keyframe in keyframes:
            if not float( keyframe ) in ExportDataInfo._checkFrames:
                ExportDataInfo._checkFrames.append( float(keyframe) )

        ExportDataInfo._checkFrames.sort()
        ExportDataInfo._checkFrames = cutFrame( start, end, ExportDataInfo._checkFrames )
        
    
    def exportPose(self, path ):
            
        cmds.retargetingCommand( ex=ExportDataInfo._namespace+'World_CTL', fn=path )

        
    def exportAnim(self, path, start, end ):
        
        self.getFrames( start, end )
        
        fldList = path.split( '/' )
        for i in range( 2, len( fldList )+1 ):
            folder = '/'.join( fldList[:i] )
            if not os.path.isdir( folder ):
                os.mkdir( folder )
        
        cposeFiles = []
        for root, dirs, names in os.walk( path ):
            for name in names:
                if name.split( '.' )[1] == 'cpose': 
                    cposeFiles.append( root+'/'+name )
            break
        
        for cposeFile in cposeFiles:
            os.remove( cposeFile )
        
        self.exportCAnim( path )
        self.exportKeyInfo( path )


    def exportCAnim(self, path ):
        
        if not ExportDataInfo._checkFrames: return None
        
        options = { 'ex':ExportDataInfo._namespace+'World_CTL' }
        
        lastIndex = len( ExportDataInfo._checkFrames )
        
        frameByFrameList = [ float( i ) for i in range( int( ExportDataInfo._checkFrames[0] ), int( ExportDataInfo._checkFrames[lastIndex-1]+1 ) ) ]
        
        frameByFrameList += ExportDataInfo._checkFrames
        frameByFrameList = list( set( frameByFrameList ) )
        frameByFrameList.sort()
        
        for checkFrame in frameByFrameList:
            cmds.currentTime( checkFrame )
            
            num1, num2 = str(checkFrame).split('.')
            
            num1 = int( num1 )
            if num2[0] != 0:
                num2 = int( num2 ) * 10
            else:
                num2 = int( num2 )
                
            num1 -= ExportDataInfo._offsetFrame
            options.update( {'fn':(path+'/frame%04d_%02d.cpose' %( num1, num2 ) )} )
            cmds.retargetingCommand( **options )


    def exportKeyInfo(self, path ):
        
        path += '/aKeyframeInfo.txt'
        
        f = open( path, 'w' )
        
        strs = ''
        
        checkStartFrame = ExportDataInfo._startFrame + ExportDataInfo._offsetFrame
        checkEndFrame   = ExportDataInfo._endFrame   + ExportDataInfo._offsetFrame
        
        for ctl in ExportDataInfo._exportKeyCtls:
            strs += ctl.replace( ExportDataInfo._namespace, '' )+"^\r\n"
            attrs = cmds.listAttr( ctl, k=1 )
            for attr in attrs:
                frames = cmds.keyframe( ctl+'.'+attr, q=1, tc=1, time=( checkStartFrame, checkEndFrame ) )
                if not frames: continue
                strs += attr +"|"
                for frame in frames:
                    strs += str( frame-ExportDataInfo._offsetFrame )+','
                strs = strs[:-1] + "|"
                for tangent in cmds.keyTangent( ctl+'.'+attr, q=1, itt=1, time=( checkStartFrame, checkEndFrame ) ):
                    strs += tangent+','
                strs = strs[:-1] + "|"
                for tangent in cmds.keyTangent( ctl+'.'+attr, q=1, ott=1, time=( checkStartFrame, checkEndFrame ) ):
                    strs += tangent+','
                strs = strs[:-1] + "\r"
                strs +='\n'
            strs += "#\r\n"
        strs = strs[:-5]

        f.write( strs )
        f.close()



class ImportData:


    def setCharacter(self, *worldCtls ):
        ImportDataInfo._namespaceList = []
        cmds.retargetingCommand( ct=1 )

        for worldCtl in worldCtls:
            namespace = worldCtl.replace( 'World_CTL', '' )
            if not namespace:
                cmds.warning( "%s has no name space" % worldCtl )
                continue
            ImportDataInfo._namespaceList.append( worldCtl.replace( 'World_CTL', '' ) )
            cmds.retargetingCommand( worldCtl, tw=1 )


    def setEnableDefault(self, value ):
        
        ImportDataInfo._enableDefault = value
        ImportDataInfo._enablePartList = []
        ImportDataInfo._enableCtlList = []
        ImportDataInfo._enableFollowList = []


    def setPartEnable(self, part, value ):
        
        ImportDataInfo._enablePartList.append( [part, value] )


    def setCtlEnable(self, nameCtl, value ):
        
        ImportDataInfo._enableCtlList.append( [nameCtl, value] )


    def setFollowEnable(self, followType, value ):
        
        ImportDataInfo._enableFollowList.append( [followType, value] )


    def setEnable(self, targetWorld ):
        
        cmds.retargetingCommand( targetWorld, enp=[ 'All', ImportDataInfo._enableDefault ] )
        
        for part, value in ImportDataInfo._enablePartList:
            cmds.retargetingCommand( targetWorld, enp= [part, value] )
        for ctl,  value in ImportDataInfo._enableCtlList:
            cmds.retargetingCommand( targetWorld, enc= [ctl, value] )
        for follow, value in ImportDataInfo._enableFollowList:
            cmds.retargetingCommand( targetWorld, enf= [follow, value] )


    def importAnim(self, path ):
        
        ImportDataInfo._canimPath = path
        cmds.retargetingCommand( ima=1, fn=path )


    def importPose(self, path ):
        
        cmds.retargetingCommand( im=1, fn=path )


    def setSpeed(self, value ):
        
        ImportDataInfo._speedFrame = value


    def setOffset(self, value ):
        
        ImportDataInfo._offsetFrame = value


    def retargetPose(self, flip=0 ):
        
        cmds.retargetingCommand( rtg=1, w=1, fl=flip )


    def retargetFrame(self, frame, flip=0 ):
        
        if   frame <  ImportDataInfo._startFrame: return None
        elif frame >  ImportDataInfo._endFrame : return None
        
        baseOffset = ImportDataInfo._baseOffsetframe
        offset = ImportDataInfo._offsetFrame
        speed  = ImportDataInfo._speedFrame
        
        #print "before :", frame,
        frame = (frame-baseOffset-offset) * speed
        #print "after  :", frame
        
        print "retarget frame : ", frame
        
        cmds.retargetingCommand( rta=frame, w=1, fl=flip )


    def retargetAnim(self, flip=0 ):
        
        mel.eval( 'python( "import chModules.retargetingCommand.control as retargetingCommandControl" )' )
        
        if cmds.ls( 'ImportRetargetingEachCommand' ): cmds.delete( 'ImportRetargetingEachCommand' )
        cmds.expression( s='python( "retargetingCommandControl.ImportData().retargetFrame( " + frame + ", %d )" );' % flip,  o = "",ae=1, uc='all', n='ImportRetargetingEachCommand' )
        ImportDataInfo._fliped = flip


    def setFrameRange( self, start, end ):
        
        ImportDataInfo._baseOffsetframe = start
        ImportDataInfo._startFrame = start
        ImportDataInfo._endFrame   = end


    def setWeightDefault( self, value ):
        
        ImportDataInfo._weightDefault = value
        ImportDataInfo._weightPartList = []
        ImportDataInfo._weightCtlList = []


    def setCtlWeight(self, ctl, value ):
        
        ImportDataInfo._weightCtlList.append( [ctl, value] )


    def setPartWeight(self, part, value ):
        
        ImportDataInfo._weightPartList.append( [part, value] )


    def setWeight(self, targetWorld ):
        
        cmds.retargetingCommand( targetWorld, wp=[ 'All', ImportDataInfo._weightDefault ])
        
        for part, value in ImportDataInfo._weightPartList:
            cmds.retargetingCommand( targetWorld, wp = [part, value] )
        
        for ctl , value in ImportDataInfo._weightCtlList:
            cmds.retargetingCommand( targetWorld, wc = [ctl , value] )


    def bake(self, fbf=False ):
        
        cmds.select( cl=1 )
        
        keyInfoPath = ImportDataInfo._canimPath+'/aKeyframeInfo.txt'
        frameLength = self.getFrameLength( ImportDataInfo._canimPath )
        if not os.path.exists( keyInfoPath ): return None
        
        f = open( keyInfoPath, 'r' )
        readValues = f.read()
        
        ctlInfos = readValues.split( '#\r\n' )
        checkCtls = []

        partList = [ [i,True] for i in ImportDataInfo._ctlParts ]
        
        for part, value in ImportDataInfo._enablePartList:
            print "part :", part, "," "value :", value
            partList[ ImportDataInfo._ctlParts.index( part ) ] = value
        
        for i in range( len( partList ) ):
            if partList[i]:
                key = ImportDataInfo._ctlParts[i]
                checkCtls += ImportDataInfo._ctlSet[key]._items
        
        for enableCtl, value in ImportDataInfo._enableCtlList:
            if not value:
                if enableCtl in checkCtls:
                    checkCtls.remove( enableCtl )
                continue
            if not enableCtl in checkCtls:
                checkCtls.append( enableCtl )
        
        for ns in ImportDataInfo._namespaceList:
            for ctl in checkCtls:
                cmds.cutKey( ns+ctl, time=( ImportDataInfo._startFrame, ImportDataInfo._endFrame ) )
        
        keyAttrList = []
        keyframesList = []
        inTangentList = []
        outTangentList = []

        if not checkCtls: return None

        for ctlInfo in ctlInfos:

            try: ctl, attrsAndFrames = ctlInfo.split( '^\r\n' )
            except:
                print ctlInfo 
                continue
            
            if ImportDataInfo._fliped:
                if ctl.find( '_L_' ) != -1:
                    ctl = ctl.replace( '_L_', '_R_' )
                elif ctl.find( '_R_' ) != -1:
                    ctl = ctl.replace( '_R_', '_L_' )
            
            if not ctl in checkCtls: continue
            
            for attrAndFrames in attrsAndFrames.split( '\r\n' ):
                if not attrAndFrames: continue
                attr, frames, inTangents, outTangents = attrAndFrames.split( '|' )
                strFrames = frames.split( ',' )
                valueFrames = []
                for strFrame in strFrames:
                    valueFrames.append( float( strFrame ) )
                
                for ns in ImportDataInfo._namespaceList:
                    if not cmds.attributeQuery( attr, node=ns+ctl , ex=1 ):
                        continue
                    keyAttrList.append( ns+ctl+'.'+attr )
                    keyframesList.append( valueFrames )
                    inTangentList.append( inTangents.split( ',' ) )
                    outTangentList.append( outTangents.split( ',' ) )
        
        if fbf:
            start      = ImportDataInfo._startFrame
            end        = ImportDataInfo._endFrame
            baseOffset = ImportDataInfo._baseOffsetframe
            offset     = ImportDataInfo._offsetFrame
            speed      = ImportDataInfo._speedFrame
            
            frameLength = end - start
            while offset < 0: offset += frameLength
            
            frames = []
            for root, dir, names in os.walk( ImportDataInfo._canimPath ):
                for name in names:
                    if name.find( '.cpose' ) == -1: continue
                    frames.append( float( name.split( '.' )[0].replace( 'frame', '' ).replace( '_', '.' ) ) )
                break

            index = 0
            addFrameLength = 0
            
            cmds.undoInfo( swf=0 )
            cmds.currentTime( start )
            cmds.undoInfo( swf=1 )
            for i in range( len( keyAttrList ) ):
                cmds.setKeyframe( keyAttrList[i] )
                cmds.keyTangent( keyAttrList[i], e=1, time=(start,start), itt='flat', ott='linear' )
            
            while( 1 ):
                if index >= len( frames ): 
                    index = 0
                    addFrameLength += frameLength
                frame = frames[index]+addFrameLength
                afterFrame = (frame) / speed + offset + baseOffset
                frame -= addFrameLength
                
                index += 1
                
                if start > afterFrame: continue
                if end < afterFrame : break
                
                if afterFrame >= end:
                    cmds.undoInfo( swf=0 )
                    cmds.currentTime( end )
                    cmds.undoInfo( swf=1 )
                    for i in range( len( keyAttrList ) ):
                        cmds.setKeyframe( keyAttrList[i] )
                        cmds.keyTangent( keyAttrList[i], e=1, time=(end,end), itt='linear', ott='flat' )
                
                cmds.undoInfo( swf=0 )
                cmds.currentTime( afterFrame )
                cmds.undoInfo( swf=1 )
                
                for i in range( len( keyAttrList ) ):
                    if frame in keyframesList[i]:
                        cmds.setKeyframe( keyAttrList[i] )
            
        else:
            for i in range( int(ImportDataInfo._startFrame), int(ImportDataInfo._endFrame)+1 ):
                cmds.undoInfo( swf=0 )
                cmds.currentTime( i )
                cmds.undoInfo( swf=1 )
                for keyAttr in keyAttrList:
                    cmds.setKeyframe( keyAttr )
        
        for ns in ImportDataInfo._namespaceList:
            for checkCtl in checkCtls:
                rxCon = cmds.listConnections( ns+checkCtl+'.rotateX', s=1, d=0, type='animCurveTA' )
                ryCon = cmds.listConnections( ns+checkCtl+'.rotateY', s=1, d=0, type='animCurveTA' )
                rzCon = cmds.listConnections( ns+checkCtl+'.rotateZ', s=1, d=0, type='animCurveTA' )
                
                if not rxCon or not ryCon or not rzCon: continue
                cmds.filterCurve( rxCon[0], ryCon[0], rzCon[0] )
        
        if cmds.ls( 'ImportRetargetingEachCommand' ): cmds.delete( 'ImportRetargetingEachCommand' )

        ImportDataInfo._enablePartList = []
        ImportDataInfo._enableCtlList = []
        ImportDataInfo._enableFollowList = []
        ImportDataInfo._weightPartList = []
        ImportDataInfo._weightCtlList = []


    def getFrameLength(self, path ):
        
        for root, dir, names in os.walk( path ):
            firstValue = float( names[ 1].split( '.' )[0].replace( 'frame', '' ).replace( '_', '.' ) )
            lastValue  = float( names[-1].split( '.' )[0].replace( 'frame', '' ).replace( '_', '.' ) )
            floatRoofValue = lastValue - firstValue + 1
            intRoofValue = int( floatRoofValue )
            if floatRoofValue > intRoofValue:
                intRoofValue += 1
            return float( intRoofValue )