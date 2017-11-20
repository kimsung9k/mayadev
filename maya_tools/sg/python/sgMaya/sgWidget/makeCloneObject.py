import maya.cmds as cmds
from functools import partial
import pymel.core


class WinA_Global:
    
    winName = 'makeCloneObject'
    title   = 'Make Clone Object'
    width   = 450
    height  = 50
    
    ui_clones   = ''
    chk_shapeOn = ''
    chk_connectionOn = ''
    fld_cloneaLabel = ''
        



class WinA_cloneLabel:
    
    def __init__(self, label, labelArea=30 ):
        
        self.label = label
        self.labelArea = labelArea
    
    
    def create(self):
        
        form = cmds.formLayout()
        tx  = cmds.text( l= self.label, al='right', h=22, w=120 )
        fld = cmds.textField( h=22, w=100, tx='_clone' )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1, 
                         af=[ ( tx, 'top', 0 ), ( tx, 'left', 0 ) ],
                         ac=[ ( fld, 'left', 0, tx ) ] )
        
        self.fld = fld
        WinA_Global.fld_cloneaLabel = fld
        
        return form



def makeCloneObject( target, **options  ):
    
    target = pymel.core.ls( target )[0]
    
    op_cloneAttrName = 'iscloneObj'
    op_shapeOn       = False
    op_connectionOn  = False
    
    if options.has_key( 'cloneAttrName' ):
        op_cloneAttrName = options['cloneAttrName']
        cloneLabel = op_cloneAttrName
    if options.has_key( 'shapeOn' ):
        op_shapeOn = options['shapeOn']
    if options.has_key( 'connectionOn' ):
        op_connectionOn = options['connectionOn']

    targets = target.getAllParents()
    targets.reverse()
    targets.append( target )
    
    def getSourceConnection( src, trg ):
        src = pymel.core.ls( src )[0]
        trg = pymel.core.ls( trg )[0]
        cons = src.listConnections( s=1, d=0, p=1, c=1 )
    
        if not cons: return None
    
        for destCon, srcCon in cons:
            srcCon = srcCon.name()
            destCon = destCon.name().replace( src, trg )
            if cmds.nodeType( src ) == 'joint' and cmds.nodeType( trg ) =='transform':
                destCon = destCon.replace( 'jointOrient', 'rotate' )
            if not cmds.ls( destCon ): continue
            if not cmds.isConnected( srcCon, destCon ):
                cmds.connectAttr( srcCon, destCon, f=1 )

    targetCloneParent = None
    for cuTarget in targets:
        if not pymel.core.attributeQuery( op_cloneAttrName, node=cuTarget, ex=1 ):
            cuTarget.addAttr( op_cloneAttrName, at='message' )
        cloneConnection = cuTarget.attr( op_cloneAttrName ).listConnections(s=1, d=0 )
        if not cloneConnection:
            targetClone = pymel.core.createNode( 'transform', n= cuTarget.split( '|' )[-1]+cloneLabel )
            targetClone.message >> cuTarget.attr( op_cloneAttrName )
            
            if op_shapeOn:
                cuTargetShape = cuTarget.getShape()
                if cuTargetShape:
                    duObj = pymel.core.duplicate( cuTarget, n=targetClone+'_du' )[0]
                    duShape = duObj.getShape()
                    pymel.core.parent( duShape, targetClone, add=1, shape=1 )[0]
                    duShape.rename( targetClone+'Shape' )
            if op_connectionOn:
                getSourceConnection( cuTarget, targetClone )
                cuTargetShape    = cuTarget.getShape()
                targetCloneShape = targetClone.getShape()
                
                if cuTargetShape and targetCloneShape:
                    getSourceConnection( cuTargetShape, targetCloneShape )
        else:
            targetClone = cloneConnection[0]
        
        targetCloneParentExpected = targetClone.getParent()
        if targetCloneParent and targetCloneParentExpected != targetCloneParent:
            pymel.core.parent( targetClone, targetCloneParent )

        cuTargetPos = cuTarget.m.get()
        pymel.core.xform( targetClone, os=1, matrix=cuTargetPos )

        targetCloneParent = targetClone
    return targetCloneParent.name()




class PopupFieldUI_b:


    def __init__(self, label, **options ):
        
        def getValueFromDict( argDict, *dictKeys ):
    
            items = argDict.items()
            
            for item in items:
                if item[0] in dictKeys: return item[1]
            
            return None
        
        popupLabel = getValueFromDict( options, *['popupLabel', 'popLabel'] )
        typ        = getValueFromDict( options, *['type', 'typ'] )
        addCommand = getValueFromDict( options, *['addCommand', 'addCmd'] )
        globalForm = getValueFromDict( options, *['globalForm', 'form'] )
        globalField = getValueFromDict( options, *['globalField', 'field'] )
        
        if not popupLabel: popupLabel = 'Load Selected'
        if not typ       : typ = 'single'
        if not addCommand: addCommand = []
        
        self._label = label
        self._popup = popupLabel
        self._position = getValueFromDict( options, 'position' )
        self._textWidth = getValueFromDict( options, 'textWidth' )
        self._olnyAddCommand = getValueFromDict( options, 'olnyAddCmd' )
        self._addCommand = addCommand
        if self._textWidth == None: self._textWidth = 120
        self._field  =''
        self._type = typ
        self._cmdPopup = [self.cmdLoadSelected]
        self._globalForm = globalForm
        self._globalField = globalField



    def cmdLoadSelected(self):
        
        if self._olnyAddCommand:
            if type( self._addCommand ) in [ type(()), type([]) ]:
                for command in self._addCommand: command()
            else:
                self._addCommand()
            return None
        
        sels = cmds.ls( sl=1, sn=1 )
        if not sels: return None
        
        if self._type == 'single':
            cmds.textField( self._field, e=1, tx=sels[-1] )
        else:
            popupTxt = ''
            for sel in sels:
                popupTxt += sel + ' '
            cmds.textField( self._field, e=1, tx=popupTxt[:-1] )
        
        if self._addCommand:
            if type( self._addCommand ) in [ type(()), type([]) ]:
                for command in self._addCommand: command()
            else:
                self._addCommand()
        


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
        
        self._globalForm = form
        self._globalField = field
        
        return form




class WinA_Cmd:
    
    @staticmethod
    def cmdCreateClone( *args ):
        
        clones = WinA_Global.ui_clones.getFieldTexts()
        cloneLabel = cmds.textField( WinA_Global.fld_cloneaLabel, q=1, tx=1 )
        shapeOn = cmds.checkBox( WinA_Global.chk_shapeOn, q=1, v=1 )
        connectionOn = cmds.checkBox( WinA_Global.chk_connectionOn, q=1, v=1 )
        
        if not cloneLabel:
            cmds.error( "Clone attrName must be exists" )

        def getChildrenShapeExists( clones ):
            selChildren = cmds.listRelatives( clones, c=1, ad=1, type='shape', f=1 )
            
            children = []
            for child in selChildren:
                childP = cmds.listRelatives( child, p=1, f=1 )[0]
                children.append( childP )
            return children
        
        clones = getChildrenShapeExists( clones )
        for clone in clones:
            makeCloneObject( clone, shapeOn=shapeOn, connectionOn=connectionOn, cloneAttrName=cloneLabel )



class WinA:

    
    def __init__(self):

        self.winName = WinA_Global.winName
        self.title   = WinA_Global.title
        self.width   = WinA_Global.width
        self.height  = WinA_Global.height
        
        self.uiCloneTargets = PopupFieldUI_b( 'Clone Targets : ', typ='multiple' )
        self.uiCloneLabel   = WinA_cloneLabel( 'Clone Attr Name : ' )
        

    def create(self):
        
        if cmds.window( self.winName, ex=1 ):
            cmds.deleteUI( self.winName, wnd=1 )
        cmds.window( self.winName, title=self.title )
        
        form = cmds.formLayout()
        form_cloneTarget = self.uiCloneTargets.create()
        form_cloneLabel  = self.uiCloneLabel.create()
        chk_shapeOn      = cmds.checkBox( l='Shape On', v=1 )
        chk_connectionOn = cmds.checkBox( l='Connection On', v=0 )
        bt_createClone   = cmds.button( l='C R E A T E   C L O N E', h=25, c = WinA_Cmd.cmdCreateClone )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1,
                         af = [( form_cloneTarget, 'top', 5 ), ( form_cloneTarget, 'left', 5 ), ( form_cloneTarget, 'right', 5 ),
                               ( form_cloneLabel, 'top', 5 ), ( form_cloneLabel, 'left', 5 ), ( form_cloneLabel, 'right', 5 ), 
                               ( chk_shapeOn, 'left', 50 ),
                               ( bt_createClone, 'left', 0 ),( bt_createClone, 'right', 0 )],
                         ac = [( form_cloneLabel, 'top', 10, form_cloneTarget ), 
                               ( chk_shapeOn, 'top', 10, form_cloneLabel ), 
                               ( chk_connectionOn, 'top', 10, form_cloneLabel ), ( chk_connectionOn, 'left', 30, chk_shapeOn ),
                               ( bt_createClone, 'top', 10, chk_connectionOn )] )
        
        cmds.window( self.winName, e=1, wh=[ self.width, self.height ], rtf=1 )
        cmds.showWindow( self.winName )
        
        WinA_Global.ui_clones = self.uiCloneTargets
        WinA_Global.chk_shapeOn = chk_shapeOn
        WinA_Global.chk_connectionOn = chk_connectionOn
        