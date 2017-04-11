import maya.cmds as cmds


def getValueFromDict( argDict, dictKey ):
    
    if not type( dictKey ) in [type( [] ), type( () )]:
        dictKey = [dictKey]
    
    items = argDict.items()
    
    for item in items:
        if item[0] in dictKey: return item[1]
    
    return None


class PopupFieldUI:


    def __init__(self, label, popupLabel='Load Selected', typ='single', **options ):
        
        self._label = label
        self._popup = popupLabel
        self._position = getValueFromDict( options, 'position' )
        self._textWidth = getValueFromDict( options, 'textWidth' )
        self._addCommand = getValueFromDict( options, 'addCommand' )
        if self._textWidth == None: self._textWidth = 120
        self._field  =''
        self._type = typ
        self._cmdPopup = [self.cmdLoadSelected]



    def cmdLoadSelected(self):
        sels = cmds.ls( sl=1, sn=1 )
        if not sels: return None
        
        if self._type == 'single':
            cmds.textField( self._field, e=1, tx=sels[-1] )
        else:
            popupTxt = ''
            for sel in sels:
                popupTxt += sel + ' '
            cmds.textField( self._field, e=1, tx=popupTxt[:-1] )
        
        if self._addCommand: self._addCommand()
        


    def cmdPopup(self, *args ):
        for cmd in self._cmdPopup: cmd()
        


    def getFieldText(self):
        return cmds.textField( self._field, q=1, tx=1 )
    


    def getFieldTexts(self):
        
        texts = cmds.textField( self._field, q=1, tx=1 )
        splits = texts.split( ' ' )
        returnTexts = []
        
        splits2 = []
        
        for split in splits:
            splits2 += split.split( ',' )
        
        for split in splits2:
            split = split.strip()
            if split:
                returnTexts.append( split )
        return returnTexts
                


    def create(self):
        
        form = cmds.formLayout()
        text  = cmds.text( l= self._label, al='right', h=20, width = self._textWidth )
        field = cmds.textField(h=21)
        cmds.popupMenu()
        cmds.menuItem( l=self._popup, c=self.cmdPopup )
        
        cmds.formLayout( form, e=1,
                         af=[(text,'top',0), (text,'left',0),
                             (field,'top',0),(field,'right',0)],
                         ac=[(field, 'left', 0, text)] )
        
        if self._position:
            cmds.formLayout( form, e=1,
                             ap=[(text,'right',0,self._position)])
            
        cmds.setParent( '..' )
        
        self._text = text
        self._field = field
        self._form = form
        
        return form



def createMeshInstersectPointObject( sourcePointObject, destPointObject, mesh ):
    
    meshShapes = cmds.listRelatives( mesh, s=1, f=1 )
    
    meshShape = ''
    for shape in meshShapes:
        if not cmds.getAttr( shape+'.io' ):
            meshShape = shape
            break
    if not meshShape: 
        cmds.error( '%s has no shape' % mesh )
        return None
    
    dcmpSrc = cmds.createNode( 'decomposeMatrix' )
    dcmpDst = cmds.createNode( 'decomposeMatrix' )
    intersectNode = cmds.createNode( 'sgMeshIntersect' )
    
    cmds.connectAttr( sourcePointObject+'.wm', dcmpSrc+'.imat' )
    cmds.connectAttr( destPointObject  +'.wm', dcmpDst+'.imat' )
    
    cmds.connectAttr( mesh+'.wm', intersectNode+'.inputMeshMatrix' )
    cmds.connectAttr( meshShape+'.outMesh', intersectNode+'.inputMesh' )
    cmds.connectAttr( dcmpSrc+'.ot', intersectNode+'.pointSource' )
    cmds.connectAttr( dcmpDst+'.ot', intersectNode+'.pointDest' )

    trObj = cmds.createNode( 'transform' )
    cmds.setAttr( trObj+'.dh', 1 )
    
    crv = cmds.curve( p=[[0,0,0],[0,0,0]], d=1 )
    cmds.setAttr( crv+'.template', 1 )
    crvShape = cmds.listRelatives( crv, s=1 )[0]
    mmdcSource = cmds.createNode( 'sgMultMatrixDecompose' )
    mmdcDest   = cmds.createNode( 'sgMultMatrixDecompose' )
    cmds.connectAttr( sourcePointObject+'.wm', mmdcSource+'.i[0]' )
    cmds.connectAttr( destPointObject+'.wm',   mmdcDest+'.i[0]' )
    cmds.connectAttr( crv+'.wim', mmdcSource+'.i[1]' )
    cmds.connectAttr( crv+'.wim', mmdcDest+'.i[1]' )
    cmds.connectAttr( mmdcSource+'.ot', crvShape+'.controlPoints[0]' )
    cmds.connectAttr( mmdcDest+'.ot',   crvShape+'.controlPoints[1]' )
    
    cmds.connectAttr( trObj+'.pim', intersectNode+'.pim' )
    cmds.connectAttr( intersectNode+'.outPoint', trObj+'.t' )
    
    return trObj, crv




class Window:
    
    def __init__(self):
        
        try:
            cmds.loadPlugin( 'sgMatrix' )
            cmds.loadPlugin( 'sgMatchMove' )
        except:
            pass
        
        self.uiname = 'sgMeshIntersectUi'
        self.title  = 'SG Mesh Intersect UI'
        self.width = 300
        self.height = 50
        
        self.sourceField = PopupFieldUI( 'Source Locator : ', 'Load Selected', position = 40 )
        self.destField   = PopupFieldUI( 'Dest Locator : ', 'Load Selected', 'list', position = 40 )
        self.meshField   = PopupFieldUI( 'Target Mesh : ', 'Load Selected', position = 40 )
    
    
    def cmdSet(self, *args ):
        
        sourcePointObject = self.sourceField.getFieldText()
        destPointObjects  = self.destField.getFieldTexts()
        mesh              = self.meshField.getFieldText()
        
        trObjs = []
        crvs = []
        for destPointObject in destPointObjects:
            trObj, crv = createMeshInstersectPointObject( sourcePointObject, destPointObject, mesh )
            trObjs.append( trObj )
            crvs.append( crv )
        
        cmds.group( trObjs )
        cmds.group( crvs )



    def cmdClose(self, *args ):
        
        cmds.deleteUI( self.uiname, wnd=1 )

    
    def show(self):
        
        self.fields = []
        
        if cmds.window( self.uiname, ex=1 ):
            cmds.deleteUI( self.uiname, wnd=1 )
        
        cmds.window( self.uiname, title= self.title )
        
        cmds.columnLayout()
        
        columnWidth = self.width - 2
        firstWidth = ( columnWidth -2 ) / 2
        secondWidth = ( columnWidth -2 ) - firstWidth
        
        cmds.rowColumnLayout( nc=1, cw=[(1,columnWidth)] )
        self.sourceField.create()
        self.destField.create()
        self.meshField.create()
        cmds.setParent( '..' )
        
        cmds.rowColumnLayout( nc=2, cw=[(1,firstWidth),(2,secondWidth)])
        cmds.button( l='Create', c= self.cmdSet )
        cmds.button( l='Close', c= self.cmdClose )
        
        cmds.window( self.uiname, e=1, width= self.width, height = self.height )
        cmds.showWindow( self.uiname )