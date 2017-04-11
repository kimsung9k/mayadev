import maya.cmds as cmds
import cPickle


class CharacterBakeData:
    
    def __init__(self, topGrp ):
        
        children = cmds.listRelatives( topGrp, c=1, ad=1, type='transform' )

        self.ctls = []
        self.namespace = ''
        for child in children:
            if child[-9:] == 'BJT_World':
                self.namespace = child.replace( 'BJT_World', '' )
                self.ctls.append( child )
            if child[-12:] == 'Root_BJT_GRP':
                self.ctls.append( child )
            if child[-4:] == '_BJT':
                self.ctls.append( child )
        
        self.targets = []
        self.targetValuesPerFrames = []

        attrs = ['tx','ty','tz','rx','ry','rz','sx','sy','sz']

        for ctl in self.ctls:
            for attr in attrs:
                target = ctl.replace( self.namespace, '' ) +'.'+attr
                self.targets.append( target )
                self.targetValuesPerFrames.append( [] )


    def appendValue(self):
        
        for i in range( len( self.targets ) ):
            value = cmds.getAttr( self.namespace + self.targets[i] )
            self.targetValuesPerFrames[ i ].append( value )


    def importBakeData(self, filePath, startFrame=1 ):
        
        f = open( filePath, 'r' )
        chBakeData = cPickle.load( f )
        f.close()
        
        for i in range( len( chBakeData.targets ) ):
            fullAttrName = self.namespace + chBakeData.targets[i]
            attrValues = chBakeData.targetValuesPerFrames[i]
            
            node, attrName = fullAttrName.split( '.' )
            
            attrType = cmds.attributeQuery( attrName, node=node, at=1 )
            
            filterCurveTargets = []
            if attrType == 'doubleLinear':
                animCurve = cmds.createNode( 'animCurveTL', n= fullAttrName.replace( ':', '_' ) )
            elif attrType == 'doubleAngle':
                animCurve = cmds.createNode( 'animCurveTA', n= fullAttrName.replace( ':', '_' ) )
                filterCurveTargets.append( animCurve )
            else:
                animCurve = cmds.createNode( 'animCurveTU', n= fullAttrName.replace( ':', '_' ) )
            
            for j in range( len(attrValues) ):
                cmds.setKeyframe( animCurve, t= startFrame + j, v=attrValues[j] )
            
            cmds.connectAttr( animCurve+'.output', fullAttrName, f=1 )
            
            if cmds.nodeType( node ) == 'joint':
                cmds.setAttr( node+'.jo', 0,0,0 )
            
            cmds.filterCurve( filterCurveTargets )
            
                
            

def exportCharactersAnimationToFile( topGrps, filePath, start, end ):
    
    chBakeDatas = []
    bakeFilePaths = []
    for topGrp in topGrps:
        chBakeData = CharacterBakeData( topGrp )
        chBakeDatas.append( chBakeData )
        bakeFilePaths.append( filePath + '/' + chBakeData.namespace.replace( ':', '_' ) + '.sgCjbake' )

    import copy
    frame = copy.copy( start )
    while( frame < end ):
        cmds.currentTime( frame )
        frame += 1.0
        for chBakeData in chBakeDatas:
            chBakeData.appendValue()

    for i in range( len( bakeFilePaths ) ):
        import sgFunctionFileAndPath
        sgFunctionFileAndPath.makeFile( bakeFilePaths[i], False )
        f = open( bakeFilePaths[i], 'w' )
        cPickle.dump( chBakeDatas[i], f )
        f.close()



def importCharacterAnimationFromFile( topGrp, filePath, startFrame=1 ):
    
    chBakeData = CharacterBakeData( topGrp )
    chBakeData.importBakeData( filePath, startFrame )



class ControllerKeyData:

    def exportKeyData(self, topGrp, filePath, ns = '' ):

        import sgModelDg
        import sgFunctionFileAndPath

        children = cmds.listRelatives( topGrp, c=1, ad=1, type='transform' )
        children.append( topGrp )

        self.namespace = ns
        self.attrAndData = []
        for child in children:
            try:
                keyAttrs = cmds.listAttr( child, k=1 )
            except: continue
            if not keyAttrs: continue
            try:
                keyAttrs += cmds.listAttr( child, cb=1 )
            except: pass
            for attr in keyAttrs:
                if not cmds.ls( child+'.'+attr ): continue
                value = cmds.getAttr( child+'.'+attr )
                origName = child.replace( ns, '' )
                self.attrAndData.append( [ origName+'.'+attr, value, None ] )
                
                cons = cmds.listConnections( child+'.'+attr, s=1, d=0, type='animCurve' )
                if not cons: continue
                
                animCurveDataInst = sgModelDg.AnimCurveData( cons[0] )
                self.attrAndData[-1][2] = animCurveDataInst
    
        sgFunctionFileAndPath.makeFile( filePath, False )
        f = open( filePath, 'w' )
        cPickle.dump( self.attrAndData, f )
        f.close()


    def importKeyData(self, dstTarget, filePath, ns = '' ):
        
        import sgModelDg
        
        f = open( filePath, 'r' )
        data = cPickle.load( f )
        f.close()
        
        for attr, value, animCurveData in data:
            if not animCurveData: 
                try: cmds.setAttr( ns + attr, value )
                except: pass
            else:
                animCurve = animCurveData.createAnimCurve()
                animCurve = cmds.rename( animCurve, (ns+attr).replace( '.', '_' ) )
                try:
                    cmds.connectAttr( animCurve+'.output', ns+attr, f=1 )
                except:
                    print 'Failed Connect "%s" to "%s"' %( animCurve+'.output', ns+attr )