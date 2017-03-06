import maya.cmds as cmds
import maya.OpenMaya as om
from functools import partial
import sgBFunction_base



class WinA_Global:
    
    winName = 'sgPWindow_naming_replaceName'
    title   = 'UI Scene Name Replace'
    width   = 350
    height  = 50

    fld_source = ''
    fld_target = ''
    chk_isNamespace = ''



class WinA_Cmd:

    @staticmethod
    def replace(self, *args ):
        
        import sgBFunction_dag
        
        sourceName = cmds.textField( WinA_Global.fld_source, q=1, tx=1 )
        targetName = cmds.textField( WinA_Global.fld_target, q=1, tx=1 )
        isNamespace = cmds.checkBox( WinA_Global.chk_isNamespace, q=1, v=1 )
        
        if not sourceName: return None
        
        if isNamespace:
            targets = cmds.ls()
            fnTargets = []
            for target in targets:
                if target[:len(sourceName)] != sourceName: continue
                if cmds.attributeQuery( 'wm', node=target, ex=1 ):
                    fnTarget = om.MFnDagNode( sgBFunction_dag.getMDagPath( target ) )
                else:
                    fnTarget = om.MFnDependencyNode( sgBFunction_dag.getMObject( target ) )
                fnTargets.append( fnTarget )
            for fnTarget in fnTargets:
                if type( fnTarget ) == type( om.MFnDagNode() ):
                    cmds.rename( fnTarget.fullPathName(), targetName + fnTarget.name()[len(sourceName):] )
                else:
                    cmds.rename( fnTarget.name(), targetName + fnTarget.name()[len(sourceName):] )
            
        else:
            targets = cmds.ls()
            fnTargets = []
            for target in targets:
                if target.find( sourceName ) == -1: continue
                if cmds.attributeQuery( 'wm', node=target, ex=1 ):
                    fnTarget = om.MFnDagNode( sgBFunction_dag.getMDagPath( target ) )
                else:
                    fnTarget = om.MFnDependencyNode( sgBFunction_dag.getMObject( target ) )
                fnTargets.append( fnTarget )
            for fnTarget in fnTargets:
                if type( fnTarget ) == type( om.MFnDagNode() ):
                    cmds.rename( fnTarget.fullPathName(), fnTarget.name().replace( sourceName, targetName ) )
                else:
                    cmds.rename( fnTarget.name(), fnTarget.name().replace( sourceName, targetName ) )




class WinA_minMaxField:
    
    def __init__(self):
        
        pass
    
    
    def create(self):
        
        form = cmds.formLayout()
        
        sourceText  = cmds.text( l = 'Original : ', h=21, w=80, al='right' )
        sourceField = cmds.textField()
        targetText  = cmds.text( l = 'Replace : ', h=21, w=80, al='right' )
        targetField = cmds.textField()
        
        cmds.setParent( '..' )

        cmds.formLayout( form, e=1, 
                         af = [  ],
                         ap = [ ( sourceText, 'left', 0, 0 ), ( targetText, 'left', 0, 50 ), ( sourceField, 'right', 0, 50 ), ( targetField, 'right', 0, 100 ) ],
                         ac = [ ( sourceField, 'left', 0, sourceText ), ( targetField, 'left', 0, targetText )] )
        
        WinA_Global.fld_source = sourceField
        WinA_Global.fld_target = targetField
        
        return form





class WinA:


    def __init__(self):

        self.winName = WinA_Global.winName
        self.title   = WinA_Global.title
        self.width   = WinA_Global.width
        self.height  = WinA_Global.height
        
        self.uiMinMaxField = WinA_minMaxField()

    def create(self):

        if cmds.window( self.winName, ex=1 ):
            cmds.deleteUI( self.winName, wnd=1 )
        cmds.window( self.winName, title=self.title )

        form = cmds.formLayout()
        frm_minMaxField = self.uiMinMaxField.create()
        chk_isNamespace = cmds.checkBox( l='Is Namespace' )
        bt_rebuild = cmds.button( l='Replace', c= WinA_Cmd.replace )
        
        WinA_Global.chk_isNamespace = chk_isNamespace
        
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1, 
                         af=[( frm_minMaxField, 'left', 0 ), ( frm_minMaxField, 'right', 0 ), ( frm_minMaxField, 'top', 5 ),
                             ( bt_rebuild, 'left', 0 ), ( bt_rebuild, 'right', 0 ),
                             ( chk_isNamespace, 'left', 10 ), ( chk_isNamespace, 'right', 0 ) ],
                         ac = [( bt_rebuild, 'top', 5, chk_isNamespace ),
                               ( chk_isNamespace, 'top', 5, frm_minMaxField )] )

        cmds.window( self.winName, e=1, wh=[ self.width, self.height ], rtf=1 )
        cmds.showWindow( self.winName )
