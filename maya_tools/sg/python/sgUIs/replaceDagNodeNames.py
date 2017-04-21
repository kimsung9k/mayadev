import maya.cmds as cmds
import maya.OpenMaya as om

    
class ReplaceNameUIInfo:
    
    _winName = 'sgui_replaceName'
    _title   = "replace name"
    
    _width = 300
    _height = 50
                
                

class ReplaceName:
    
    def __init__(self, targetStr, replaceStr, targets, hierarchy=False, isNamespace=False, *args ):
        
        def getMObject( node ):
            from maya import OpenMaya
            selList = OpenMaya.MSelectionList()
            selList.add( node )
            oNode = OpenMaya.MObject()
            selList.getDependNode( 0, oNode )
            return oNode
            
        
        
        mObjects = []
        for target in targets:
            if hierarchy:
                children = cmds.listRelatives( target, c=1, ad=1, f=1 )
                children.append( target )
                for child in children:
                    if not cmds.nodeType( child ) in ['transform', 'joint']: continue
                    mObjects.append( getMObject( child ) )
            else:
                mObjects.append( getMObject(target) )
        
        for mObj in mObjects:
            try:
                fnNode = om.MFnDagNode( mObj )
                name = fnNode.name()
                fullPathName = fnNode.fullPathName()
                if isNamespace and name.find( targetStr ) != 0: continue
                replacedName = name.replace( targetStr, replaceStr )
                print fullPathName, replacedName
                cmds.rename( fullPathName, replacedName )
            except:
                fnNode = om.MFnDependencyNode( mObj )
                nodeName = fnNode.name()
                if isNamespace:
                    if nodeName.find( targetStr ) != 0: continue
                cmds.rename( nodeName, nodeName.replace( targetStr, replaceStr ) )
            



class TwoButton:
    
    def __init__( self ):
        
        self._cmdFirst = []
        self._cmdSecond = []
    
    
    def cmdFirst( self, *args ):
        for cmd in self._cmdFirst:   cmd()
        
        
    def cmdSecond( self, *args ):
        for cmd in self._cmdSecond: cmd()
    
    
    def create(self, height = 21, firstName='SET', secondName='CLOSE'):
        
        form = cmds.formLayout()
        
        buttonFirst   = cmds.button( l=firstName,   c= self.cmdFirst,   h=height )
        buttonSecond  = cmds.button( l=secondName,  c= self.cmdSecond, h=height )
        
        cmds.formLayout( form, e=1,
                         attachForm = [( buttonFirst, 'top', 0), ( buttonSecond, 'top', 0 ),
                                       ( buttonFirst, 'left',0), ( buttonSecond, 'right',0)],
                         ap = [( buttonFirst, 'right', 0, 50),( buttonSecond, 'left', 0, 50)] )
        cmds.setParent('..' )
        self._form = form


        
        
        
class ReplaceNameUI:
    
    def __init__(self):
        
        self._uiInstButton = TwoButton()
        self._firstField = ''
        self._secondField = ''
        self._checkH = ''
        self._checkN = ''
        
    
    def appendCmdToSetButton(self):
        
        def cmdSet( *args ):
            firstTx = cmds.textField( self._firstField, q=1, tx=1 )
            secondTx = cmds.textField( self._secondField, q=1, tx=1 )
            checkH = cmds.checkBox( self._checkH, q=1, v=1 )
            checkN = cmds.checkBox( self._checkN, q=1, v=1 )
            ReplaceName( firstTx, secondTx, cmds.ls( sl=1 ), checkH, checkN )
            
        def cmdDeleteUI( *args ):
            cmds.deleteUI( ReplaceNameUIInfo._winName )
            
        self._uiInstButton._cmdFirst.append( cmdSet )
        self._uiInstButton._cmdSecond.append( cmdDeleteUI )
        
        
    def show(self):
        
        if cmds.window( ReplaceNameUIInfo._winName, ex=1 ):
            cmds.deleteUI( ReplaceNameUIInfo._winName )
        cmds.window( ReplaceNameUIInfo._winName, title=ReplaceNameUIInfo._title )
        
        cmds.columnLayout()
        
        firstWidth = ReplaceNameUIInfo._width * 0.3
        secondWidth = ReplaceNameUIInfo._width * 0.35
        thirdWidth = ReplaceNameUIInfo._width - firstWidth - secondWidth
        cmds.rowColumnLayout( nc=3, cw=[(1,firstWidth),(2,secondWidth),(3,thirdWidth)] )
        cmds.text( l='Repace Name : ', al='right' )
        firstTF = cmds.textField()
        secondTF = cmds.textField()
        cmds.setParent( '..' )
        
        self._firstField = firstTF
        self._secondField = secondTF
        
        firstWidth = ReplaceNameUIInfo._width * 0.5
        secondWidth = ReplaceNameUIInfo._width - firstWidth
        cmds.rowColumnLayout( nc=2, cw=[(1,firstWidth),(2,secondWidth)] )
        checkHierarchy = cmds.checkBox( l='Hierarchy' )
        isNamespace    = cmds.checkBox( l='Is Namespace' )
        cmds.setParent( '..' )
        
        self._checkH = checkHierarchy
        self._checkN = isNamespace
        
        cmds.rowColumnLayout( nc=1, cw=(1,ReplaceNameUIInfo._width) )
        self._uiInstButton.create( 23 )
        cmds.setParent( '..' )
        
        cmds.window( ReplaceNameUIInfo._winName, e=1,
                     width = ReplaceNameUIInfo._width,
                     height = ReplaceNameUIInfo._height )

        cmds.showWindow( ReplaceNameUIInfo._winName )
        
        self.appendCmdToSetButton()

