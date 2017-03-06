'''
DJB_Character.FacePlusRig
Handles:
    -Creation of GUI for Face Plus compatible rigs
'''
import maya.cmds as mayac
import maya.mel as mel
from MayaAutoControlRig.Utils.General import *

CURVE_STYLES = { 'circle': {  'p': [(0.783612, 0, -0.783612),
                              (0, 0, -1.108194),
                              (-0.783612, 0, -0.783612),
                              (-1.108194, 0, 0),
                              (-0.783612, 0, 0.783612),
                              (0, 0, 1.108194),
                              (0.783612, 0, 0.783612),
                              (1.108194, 0, 0)],
                        'k': [],
                        'd': 3,
                        'closeCurve': True
                      },
          'squareConvex': { 'p': [(0.25, 0, -0.25),
                              (0, 0, -1.375),
                              (-0.25, 0, -0.25),
                              (-1.375, 0, 0),
                              (-0.25, 0, 0.25),
                              (0, 0, 1.375),
                              (0.25, 0, 0.25),
                              (1.375, 0, 0)],
                        'k': [],
                        'd': 3,
                        'closeCurve': True
                      },
          'square': {  'p': [(1, 0, 1),
                             (-1, 0, 1),
                             (-1, 0, -1),
                             (1, 0, -1)],
                        'k': [],
                        'd': 1,
                        'closeCurve': True
                      },
          }

class Curve(object):
    def __init__(self, style, name = 'Control', color = None, transform = [0,0,0,0,0,0,1.0,1.0,1.0]):
        self.transformNode = None
        self.name = name
        self.style = CURVE_STYLES[style]
        self.color = color
        self.transform = transform
        self.create()
      
    def create(self):
        self.transformNode = mayac.curve(p=self.style['p'], k= self.style['k'], d = self.style['d'])
        if self.style['closeCurve']:
            mayac.closeCurve(self.transformNode, ch = False, replaceOriginal=True, object=True, preserveShape=False, blendKnotInsertion=True)
        self.transformNode = mayac.rename(self.transformNode, self.name)
        DJB_ChangeDisplayColor(self.transformNode, color = self.color)
        shapeNodes = mayac.listRelatives(self.transformNode, children=True, shapes=True, fullPath=True)
        if shapeNodes:
            for shapeNode in shapeNodes:
                DJB_ChangeDisplayColor(shapeNode, color = self.color)
        for i,attr in enumerate(['tx','ty','tz', 'rx','ry','rz','sx','sy','sz']):
            mayac.setAttr("%s.%s"%(self.transformNode,attr),self.transform[i])
        mayac.delete(self.transformNode, ch=True)
        mayac.refresh()
        mayac.makeIdentity("%s"%self.transformNode, apply=True, t=1, r=1, s=1, n=0)
        mayac.select(clear=True)
        
COMBO_STYLES = { 'celtic': {  'curves': ['circle',
                                         'circle',
                                         'circle',
                                         'squareConvex',
                                         'squareConvex',
                                         'squareConvex'],
                        'curveTransforms': [[0,0,0,0,0,0,1.0,1.0,1.0],
                                            [0,0,0,0,0,0,0.726,0.726,0.726],
                                            [0,0,0,0,0,0,0.558,0.558,0.558],
                                            [0,0,0,0,0,0,1.0,1.0,1.0],
                                            [0,0,0,0,30,0,1.0,1.0,1.0],
                                            [0,0,0,0,60,0,1.0,1.0,1.0]]
                      }
          }

class ComboCurve(object):
    def __init__(self, style, name = 'Control', color = None, transform = [0,0,0,0,0,0,1.0,1.0,1.0]):
        self.name = name
        self.transformNode = None
        self.transform = transform
        self.style = COMBO_STYLES[style]
        self.color = color
        self.controlShapes = []
        self.create()
    
    def create(self):
        self.transformNode = mayac.group(em=True, name=self.name)
        for i in range(len(self.style['curves'])):
            subCurve= Curve(self.style['curves'][i], name = "%s_%d"%(self.name,i), color = self.color, transform = self.style['curveTransforms'][i])
            shape = mayac.listRelatives(subCurve.transformNode, children=True, shapes=True, fullPath=True)[0]
            self.controlShapes.append(mayac.parent(shape, self.transformNode, r=True, s=True)[0])
            mayac.delete(subCurve.transformNode)
        DJB_ChangeDisplayColor(self.transformNode, color = self.color)
        for i,attr in enumerate(['tx','ty','tz', 'rx','ry','rz','sx','sy','sz']):
            mayac.setAttr("%s.%s"%(self.transformNode,attr),self.transform[i])
        mayac.delete(self.transformNode, ch=True)
        mayac.refresh()
        mayac.makeIdentity("%s"%self.transformNode, apply=True, t=1, r=1, s=1, n=0)
        mayac.select(clear=True)

def createText(label_, scale=[1,1,1], pos=[0,0,0], normalizeScale=True):
    textXform = None
    if label_:
        textXform = mayac.textCurves(t=label_, ch=False, f="Arial|w400|h-11")[0] #(Times New Roman|h-13|w400|c0, Arial|w400|h-11)
        shapes = mayac.listRelatives(textXform, ad=True, type='nurbsCurve')
        transforms = mayac.listRelatives(textXform, ad=True, type='transform')
        for transform in transforms:
            connections = mayac.listConnections(transform, connections=True,plugs=True, source=True)
            if connections:
                mayac.disconnectAttr(connections[1], connections[0])
            mayac.refresh()
            mayac.makeIdentity(transform, apply=True, t=1, r=1, s=1, n=0)
        for shape in shapes:
            mayac.parent(shape, textXform, r=True, s=True)
        mayac.delete(transforms)
        bbox = mayac.exactWorldBoundingBox(textXform)
        centerX = bbox[3]/2
        mayac.setAttr("%s.tx"%textXform, centerX*-1)
        mayac.move(0, 0, 0, textXform+".scalePivot",textXform+".rotatePivot", absolute=True)
        if normalizeScale:
            scaleFactor = 1/bbox[4]/2
            mayac.scale(scaleFactor, scaleFactor, scaleFactor, textXform)
            mayac.refresh()
            mayac.makeIdentity(textXform, apply=True, t=1, r=1, s=1, n=0)
        mayac.move(pos[0], pos[1], pos[2], textXform)
        mayac.scale(scale[0], scale[1], scale[2], textXform)
        mayac.refresh()
        mayac.makeIdentity(textXform, apply=True, t=1, r=1, s=1, n=0)
    return textXform

BOX_STYLES = { 's_Y_NY_X_NX_': {  
                        'controlCurve': 'circle',
                        'controlTransforms': [0,0,0,90,0,0,0.25,1.0,0.25],      
                        'boxCurve': 'square',
                        'boxTransforms': [0,0,0,90,0,0,1.0,1.0,1.0],
                        'controlLimits': { 'tx': [-1,1],
                                        'ty': [-1,1],
                                        'tz': [0,0]},
                        'grpScale': [1,1,1],
                        'textScale': [1,1,1],
                        'boxScale': [1,1,1],
                        'boxMove': [0,0,0] 
                    },
              's_Y_': {  
                        'controlCurve': 'circle',
                        'controlTransforms': [0,0,0,90,0,0,0.125,1.0,0.05],      
                        'boxCurve': 'square',
                        'boxTransforms': [0,0.5,0,90,0,0,0.05,1.0,0.5],
                        'controlLimits': { 'tx': [0,0],
                                            'ty': [0,1],
                                            'tz': [0,0]},
                        'grpScale': [1,1,1],
                        'textScale': [1,1,1],
                        'boxScale': [2,2,2],
                        'boxMove': [0,-1,0]    
                    },
              's_Y_X_': {  
                        'controlCurve': 'circle',
                        'controlTransforms': [0,0,0,90,0,0,0.125,1.0,0.125],      
                        'boxCurve': 'square',
                        'boxTransforms': [0.5,0.5,0,90,0,0,0.5,1.0,0.5],
                        'controlLimits': { 'tx': [0,1],
                                            'ty': [0,1],
                                            'tz': [0,0]},
                        'grpScale': [1,1,1],
                        'textScale': [1,1,1],
                        'boxScale': [2,2,2],
                        'boxMove': [-1,-1,0]    
                    },
               's_Y_NY_': {  'controlCurve': 'circle',
                        'controlTransforms': [0,0,0,90,0,0,0.25,1.0,0.1],      
                        'boxCurve': 'square',
                        'boxTransforms': [0,0,0,90,0,0,0.1,1.0,1.0],
                        'controlLimits': { 'tx': [0,0],
                                            'ty': [-1,1],
                                            'tz': [0,0]},
                        'grpScale': [1,1,1],
                        'textScale': [1,1,1],
                        'boxScale': [1,1,1],
                        'boxMove': [0,0,0]            
                    },
              's_Y_NY_X_': {  'controlCurve': 'circle',
                        'controlTransforms': [0,0,0,90,0,0,0.25,1.0,0.25],      
                        'boxCurve': 'square',
                        'boxTransforms': [.5,0,0,90,0,0,0.5,1.0,1.0],
                        'controlLimits': { 'tx': [0,1],
                                            'ty': [-1,1],
                                            'tz': [0,0]},
                        'grpScale': [1,1,1],
                        'textScale': [1,1,1],
                        'boxScale': [1,1,1],
                        'boxMove': [-.5,0,0]            
                    },
              's_Y_NY_NX_': {  'controlCurve': 'circle',
                        'controlTransforms': [0,0,0,90,0,0,0.25,1.0,0.25],      
                        'boxCurve': 'square',
                        'boxTransforms': [-.5,0,0,90,0,0,0.5,1.0,1.0],
                        'controlLimits': { 'tx': [-1,0],
                                            'ty': [-1,1],
                                            'tz': [0,0]},
                        'grpScale': [1,1,1],
                        'textScale': [1,1,1],
                        'boxScale': [1,1,1],
                        'boxMove': [.5,0,0]            
                    },
              's_NY_NX_': {  'controlCurve': 'circle',
                        'controlTransforms': [0,0,0,90,0,0,0.125,1.0,0.125],      
                        'boxCurve': 'square',
                        'boxTransforms': [-0.5,-0.5,0,90,0,0,0.5,1.0,0.5],
                        'controlLimits': { 'tx': [-1,-0],
                                            'ty': [-1,0],
                                            'tz': [0,0]},
                        'grpScale': [1,1,1],
                        'textScale': [1,1,1],
                        'boxScale': [2,2,2],
                        'boxMove': [1,1,0]         
                    }
          }
  
class BoxControl(object):
    def __init__(self, style, name='Control', label_Y='', label_NY='', label_X='', label_NX='', label_Y_X='', label_Y_NX='', label_NY_X='', label_NY_NX='', label_O_U='', label_O_D='', title='', subtitle='', pos=[0,0,0], scale=[1,1,1]):
        self.name = name
        self.style = BOX_STYLES[style]
        self.GRP = mayac.group(em=True, n="%s_POS_GRP"%self.name)
        self.BoxGRP = mayac.group(em=True, n="%s_GRP"%self.name)
        self.TextGRP = mayac.group(em=True, n="%s_Text_GRP"%self.name)
        self.LabelGRP = mayac.group(em=True, n="%s_Label_GRP"%self.name)
        self.CTRL = Curve(self.style['controlCurve'], name='%s_CTRL'%self.name, color='white', transform=self.style['controlTransforms'])
        self.Box = Curve(self.style['boxCurve'], name='%s_Box'%self.name, color='black', transform=self.style['boxTransforms'])
        self.label_Y = createText(label_Y, pos=[0,1.1,0], scale=[0.6,0.6,0.6], normalizeScale=True)
        self.label_NY = createText(label_NY, pos=[0,-1.3,0], scale=[0.6,0.6,0.6], normalizeScale=True)
        self.label_X = createText(label_X, pos=[1.2,0,0], scale=[0.6,0.6,0.6], normalizeScale=True)
        self.label_NX = createText(label_NX, pos=[-1.2,0,0], scale=[0.6,0.6,0.6], normalizeScale=True)
        self.label_Y_X = createText(label_Y_X, pos=[1.2,1.1,0], scale=[0.6,0.6,0.6], normalizeScale=True)
        self.label_Y_NX = createText(label_Y_NX, pos=[-1.2,1.1,0], scale=[0.6,0.6,0.6], normalizeScale=True)
        self.label_NY_X = createText(label_NY_X, pos=[1.2,-1.3,0], scale=[0.6,0.6,0.6], normalizeScale=True)
        self.label_NY_NX = createText(label_NY_NX, pos=[-1.2,-1.3,0], scale=[0.6,0.6,0.6], normalizeScale=True)
        self.label_O_U = createText(label_O_U, pos=[0,0.1,0], scale=[0.6,0.6,0.6], normalizeScale=True)
        self.label_O_D = createText(label_O_D, pos=[0,-0.3,0], scale=[0.6,0.6,0.6], normalizeScale=True)
        titlePos = [0,2.0,0] if subtitle else [0,1.5,0] 
        titleScale = [1.3,1.3,1.3] if subtitle else [1.4,1.4,1.4]
        self.title = createText(title, pos=titlePos, scale=titleScale, normalizeScale=True)
        self.subtitle = createText(subtitle, pos=[0,1.4,0], scale=[0.75,0.75,0.75], normalizeScale=True)
        for thing in [self.Box.transformNode, self.label_Y, self.label_NY, self.label_X, self.label_NX, self.label_Y_X, self.label_Y_NX, self.label_NY_X, self.label_NY_NX, self.label_O_U, self.label_O_D, self.title, self.subtitle]:
            if thing:
                mayac.setAttr("%s.overrideEnabled"%thing, 1)
                mayac.setAttr("%s.overrideDisplayType"%thing, 2)
                thingShape = mayac.listRelatives(thing, children=True, shapes=True)[0]
                mayac.setAttr("%s.overrideEnabled"%thingShape, 1)
                mayac.setAttr("%s.overrideDisplayType"%thingShape, 2)
                if thing == self.title or thing == self.subtitle:
                    mayac.parent(thing, self.TextGRP)
                elif thing == self.Box.transformNode:
                    mayac.parent(thing, self.BoxGRP)
                else:
                    mayac.parent(thing, self.LabelGRP)
        for attr in ['rx','ry','rz','sx','sy','sz','visibility']:
            mayac.setAttr('%s.%s'%(self.CTRL.transformNode,attr), l=True, k=False)
        mayac.transformLimits(self.CTRL.transformNode, etx = [1,1], tx=self.style['controlLimits']['tx'], ety = [1,1], ty=self.style['controlLimits']['ty'], etz = [1,1], tz=self.style['controlLimits']['tz'])
        for attr in self.style['controlLimits'].keys():
            if self.style['controlLimits'][attr][0] == 0 and self.style['controlLimits'][attr][1] == 0:
                mayac.setAttr('%s.%s'%(self.CTRL.transformNode,attr), l=True, k=False)
        mayac.parent(self.CTRL.transformNode, self.BoxGRP)
        mayac.parent(self.BoxGRP, self.GRP)
        mayac.parent(self.TextGRP, self.GRP)
        mayac.parent(self.LabelGRP, self.GRP)
        self.scaleBox(self.style['boxScale'])
        self.scaleText(self.style['textScale'])
        self.scale(self.style['grpScale'])
        self.moveBox(self.style['boxMove'])
        self.move(pos)
        self.scale(scale)
        
    def move(self, pos):
        mayac.setAttr('%s.translate'%self.GRP, pos[0],pos[1],pos[2])
    def moveBox(self, pos):
        mayac.setAttr('%s.translate'%self.BoxGRP, pos[0],pos[1],pos[2])
    def moveText(self, pos):
        mayac.setAttr('%s.translate'%self.TextGRP, pos[0],pos[1],pos[2])
    def scale(self, pos):
        mayac.setAttr('%s.scale'%self.GRP, pos[0],pos[1],pos[2])
    def scaleBox(self, pos):
        mayac.setAttr('%s.scale'%self.BoxGRP, pos[0],pos[1],pos[2])
    def scaleText(self, pos):
        mayac.setAttr('%s.scale'%self.TextGRP, pos[0],pos[1],pos[2])
        

class FacePlusHookupAttr(object):
    def __init__(self, hookupNode, attr):
        self.hookupNode = hookupNode
        self.attr = attr
        self.clampNode = None
        self.negMultNode = None
        self.addNode=None
        mayac.addAttr(self.hookupNode, longName=self.attr, keyable=True)
        self.currentConnection = "%s.%s"%(self.hookupNode, self.attr)
        ###"%s.input1D[1]"%self.addNode
    def createClampNode(self):   
        self.clampNode = mayac.shadingNode('clamp', asUtility=True, n="%s_Clamp"%self.attr)
        mayac.setAttr("%s.maxR"%self.clampNode, 1.0)
        self.connect("%s.outputR"%self.clampNode, setCurrent="%s.inputR"%self.clampNode)
    def createNegMult(self):
        self.negMultNode = mayac.shadingNode('multiplyDivide', asUtility=True, n="%s_NegativeMult"%self.attr)
        mayac.setAttr("%s.input2X"%self.negMultNode, -1)
        self.connect("%s.outputX"%self.negMultNode, setCurrent="%s.input1X"%self.negMultNode)
    def createAddNode(self):
        self.addNode = mayac.shadingNode('plusMinusAverage', asUtility=True, n="%s_Add"%self.attr)
        self.connect("%s.output1D"%self.addNode, setCurrent="%s.input1D[0]"%self.addNode)
    def connect(self, connection, setCurrent = False):
        mayac.connectAttr(connection, self.currentConnection)
        if setCurrent:
            self.currentConnection = setCurrent
        
class FacePlusRig(object):
    def __init__(self):
        self.Sync = BoxControl('s_Y_NY_X_NX_', name='Sync', title='Lip-Sync', pos=[0,-18,0], scale=[1.2,1.2,1.2])
        self.Sync.scaleText([1.4,1.4,1.4])
        self.Sync.moveText([0,-.7,0])
        self.Smile = BoxControl('s_Y_X_', name='Smile', title='Smile', label_NY_X='L', label_Y_NX='R', pos=[5,-18,0], scale=[1,1,1])
        self.Frown = BoxControl('s_NY_NX_', name='Frown', title='Frown', label_NY_X='L', label_Y_NX='R', pos=[5,-23,0], scale=[1,1,1])
        self.MouthPosition = BoxControl('s_Y_NY_X_NX_', name='MouthPosition', title='Mouth Position', pos=[9,-18,0], scale=[.6,.6,.6])
        self.Tongue = BoxControl('s_Y_', name='Tongue', title='Tongue', pos=[9,-23,0], scale=[.6,.6,.6])
        self.LowerLipDown = BoxControl('s_NY_NX_', name='LowerLipDown', title='Lower Lip', subtitle='Down', label_NY_X='L', label_Y_NX='R', pos=[-1.0,-23,0], scale=[1,1,1])
        self.LowerLipInOut = BoxControl('s_Y_NY_', name='LowerLipInOut', subtitle = 'In Out', pos=[1.0,-23,0], scale=[1,1,1])
        mayac.setAttr('%s.translate'%self.LowerLipDown.title, 1,0,0)
        self.Whistle = BoxControl('s_Y_X_', name='Whistle', title='Whistle', label_NY_X='L', label_Y_NX='R', pos=[-5,-23,0], scale=[1,1,1])
        self.MouthNarrow = BoxControl('s_Y_X_', name='MouthNarrow', title='Narrow', label_NY_X='L', label_Y_NX='R', pos=[-5,-18,0], scale=[1,1,1])
        self.UpperLipUp = BoxControl('s_Y_X_', name='UpperLipUp', title='Upper Lip', subtitle='Up', label_NY_X='L', label_Y_NX='R', pos=[-1.0,-13,0], scale=[1,1,1])
        self.UpperLipInOut = BoxControl('s_Y_NY_', name='UpperLipInOut', subtitle='In Out', pos=[1.0,-13,0], scale=[1,1,1])
        mayac.setAttr('%s.translate'%self.UpperLipUp.title, 1,0,0)
        self.JawPos = BoxControl('s_Y_NY_X_NX_', name='JawPos', subtitle='Position', pos=[-3,-28,0], scale=[1,1,1])
        self.JawRot = BoxControl('s_Y_NY_X_NX_', name='JawRot', title='Jaw', subtitle='Rotation', pos=[0,-28,0], scale=[1,1,1])
        self.JawInOut = BoxControl('s_Y_NY_', name='JawInOut', subtitle='In Out', pos=[2,-28,0], scale=[1,1,1])
        mayac.setAttr('%s.scale'%self.JawRot.title, 2,2,2)
        
        self.NoseScrunch = BoxControl('s_Y_X_', name='NoseScrunch', title='Nose Scrunch', label_NY_X='L', label_Y_NX='R', pos=[-5,-13,0], scale=[.85,.85,.85])
        self.CheekPuff = BoxControl('s_Y_X_', name='CheekPuff', title='Cheek Puff', label_NY_X='L', label_Y_NX='R', pos=[5,-13,0], scale=[.85,.85,.85])
        self.Squint = BoxControl('s_Y_X_', name='Squint', title='Squint', label_NY_X='L', label_Y_NX='R', pos=[4,-8,0], scale=[.85,.85,.85])
        self.LeftEyeBlink = BoxControl('s_Y_NY_', name='LeftEyeBlink', pos=[1,-8,0], title='Blink', subtitle='Left', scale=[1,1,1])
        self.RightEyeBlink = BoxControl('s_Y_NY_', name='RightEyeBlink', pos=[-1,-8,0], subtitle='Right', scale=[1,1,1])
        mayac.setAttr('%s.translate'%self.LeftEyeBlink.title, -1,0,0)
        
        self.LeftBrow = BoxControl('s_Y_NY_NX_', name='LeftBrow', title='Left Brow', subtitle='Position', pos=[2,-4,0], scale=[1,1,1])
        self.LeftBrowOuterLower = BoxControl('s_Y_', name='LeftBrowOuterLower', subtitle='Worry', pos=[4,-4,0], scale=[1,1,1])
        mayac.setAttr('%s.translate'%self.LeftBrow.title, 1,0,0)
        self.RightBrow = BoxControl('s_Y_NY_X_', name='RightBrow', title='Right Brow', subtitle='Position', pos=[-2,-4,0], scale=[1,1,1])
        self.RightBrowOuterLower = BoxControl('s_Y_', name='RightBrowOuterLower', subtitle='Worry', pos=[-4,-4,0], scale=[1,1,1])
        mayac.setAttr('%s.translate'%self.RightBrow.title, -1,0,0)
        self.MoverCTRL = ComboCurve('celtic', name='Facial_CTRLs_Mover', color='white', transform = [0,0,0,90,0,0,1.0,1.0,1.0])
        mayac.addAttr(self.MoverCTRL.transformNode, longName='Follow_Head', niceName='FollowHead', max=1.0, min=0.0, defaultValue = 1.0, keyable=True)
        self.FaceCam = str(mayac.camera(n='FaceCam')[0])
        self.FaceControlCam = str(mayac.camera(n='FaceControlCam')[0])
        mayac.setAttr("%s.translate"%self.FaceCam, -14.972, -23.851, 67.116)
        mayac.setAttr("%s.rotate"%self.FaceCam, 4.2, -.4, 0)
        mayac.setAttr("%s.translate"%self.FaceControlCam, 0.451, -17.281, 32.972)
        mayac.setAttr("%s.visibility"%self.FaceCam, 0)
        mayac.setAttr("%s.visibility"%self.FaceControlCam, 0)
        self.POS_GRP = mayac.group(em=True, n="FacialControl_POS_GRP")
        self.allCtrls = [self.Sync, self.Smile, self.Frown, self.MouthPosition, self.Tongue, self.LowerLipDown, self.LowerLipInOut, self.Whistle, 
                    self.MouthNarrow, self.UpperLipUp, self.UpperLipInOut, self.JawPos, self.JawRot, self.JawInOut, self.NoseScrunch,
                    self.Squint, self.CheekPuff, self.LeftEyeBlink, self.RightEyeBlink, self.LeftBrow, self.LeftBrowOuterLower, 
                    self.RightBrow, self.RightBrowOuterLower]
        for ctrl in self.allCtrls:
            mayac.parent(ctrl.GRP, self.MoverCTRL.transformNode)
        mayac.parent(self.FaceCam, self.MoverCTRL.transformNode, self.POS_GRP)
        mayac.parent(self.FaceControlCam, self.MoverCTRL.transformNode, self.POS_GRP)
        mayac.setAttr("%s.translate"%self.POS_GRP, 21.164, 187, 10.5)
        
        self.FacialHookupNode = mayac.group(em=True, n='Facial_Hookup')
        DJB_LockNHide(self.FacialHookupNode)
        self.facePlusBlends = ["Blink_Left", "Blink_Right", "BrowsDown_Left", "BrowsDown_Right", "BrowsIn_Left", "BrowsIn_Right", "BrowsOuterLower_Left",
                                "BrowsOuterLower_Right", "BrowsUp_Left", "BrowsUp_Right", "CheekPuff_Left", "CheekPuff_Right", "EyesWide_Left", "EyesWide_Right",
                                "Frown_Left", "Frown_Right", "JawBackward", "JawForeward", "JawRotateY_Left", "JawRotateY_Right", "JawRotateZ_Left",
                                "JawRotateZ_Right", "Jaw_Down", "Jaw_Left", "Jaw_Right", "Jaw_Up", "LowerLipDown_Left", "LowerLipDown_Right",
                                "LowerLipIn", "LowerLipOut", "Midmouth_Left", "Midmouth_Right", "MouthDown", "MouthNarrow_Left", "MouthNarrow_Right",
                                "MouthOpen", "MouthUp", "MouthWhistle_NarrowAdjust_Left", "MouthWhistle_NarrowAdjust_Right", "NoseScrunch_Left",
                                "NoseScrunch_Right", "Smile_Left", "Smile_Right", "Squint_Left", "Squint_Right", "TongueUp", "UpperLipIn",
                                "UpperLipOut", "UpperLipUp_Left", "UpperLipUp_Right"]
        self.hookupAttrs = {}
        for attr in self.facePlusBlends:
            self.hookupAttrs[attr] = FacePlusHookupAttr(self.FacialHookupNode, attr)
            
        self.hookupAttrs['MouthOpen'].createClampNode()
        self.hookupAttrs['MouthOpen'].createNegMult()
        self.hookupAttrs['MouthOpen'].connect("%s.ty"%self.Sync.CTRL.transformNode)
        
        self.hookupAttrs['Smile_Left'].createClampNode()
        self.hookupAttrs['Smile_Left'].createAddNode()
        self.hookupAttrs['Smile_Left'].connect("%s.tx"%self.Smile.CTRL.transformNode)
        self.hookupAttrs['Smile_Left'].currentConnection = "%s.input1D[1]"%self.hookupAttrs['Smile_Left'].addNode
        self.hookupAttrs['Smile_Left'].createClampNode()
        self.hookupAttrs['Smile_Left'].connect("%s.tx"%self.Sync.CTRL.transformNode)
        self.hookupAttrs['Smile_Right'].createClampNode()
        self.hookupAttrs['Smile_Right'].createAddNode()
        self.hookupAttrs['Smile_Right'].connect("%s.ty"%self.Smile.CTRL.transformNode)
        self.hookupAttrs['Smile_Right'].currentConnection = "%s.input1D[1]"%self.hookupAttrs['Smile_Right'].addNode
        self.hookupAttrs['Smile_Right'].createClampNode()
        self.hookupAttrs['Smile_Right'].connect("%s.tx"%self.Sync.CTRL.transformNode)
        
        self.hookupAttrs['MouthNarrow_Left'].createClampNode()
        self.hookupAttrs['MouthNarrow_Left'].createAddNode()
        self.hookupAttrs['MouthNarrow_Left'].connect("%s.tx"%self.MouthNarrow.CTRL.transformNode)
        self.hookupAttrs['MouthNarrow_Left'].currentConnection = "%s.input1D[1]"%self.hookupAttrs['MouthNarrow_Left'].addNode
        self.hookupAttrs['MouthNarrow_Left'].createClampNode()
        self.hookupAttrs['MouthNarrow_Left'].createNegMult()
        self.hookupAttrs['MouthNarrow_Left'].connect("%s.tx"%self.Sync.CTRL.transformNode)
        self.hookupAttrs['MouthNarrow_Right'].createClampNode()
        self.hookupAttrs['MouthNarrow_Right'].createAddNode()
        self.hookupAttrs['MouthNarrow_Right'].connect("%s.ty"%self.MouthNarrow.CTRL.transformNode)
        self.hookupAttrs['MouthNarrow_Right'].currentConnection = "%s.input1D[1]"%self.hookupAttrs['MouthNarrow_Right'].addNode
        self.hookupAttrs['MouthNarrow_Right'].createClampNode()
        self.hookupAttrs['MouthNarrow_Right'].createNegMult()
        self.hookupAttrs['MouthNarrow_Right'].connect("%s.tx"%self.Sync.CTRL.transformNode)
        
        self.hookupAttrs['MouthUp'].createClampNode()
        self.hookupAttrs['MouthUp'].createAddNode()
        self.hookupAttrs['MouthUp'].createClampNode()
        self.hookupAttrs['MouthUp'].connect("%s.ty"%self.MouthPosition.CTRL.transformNode)
        self.hookupAttrs['MouthUp'].currentConnection = "%s.input1D[1]"%self.hookupAttrs['MouthUp'].addNode
        self.hookupAttrs['MouthUp'].createClampNode()
        self.hookupAttrs['MouthUp'].connect("%s.ty"%self.Sync.CTRL.transformNode)
        
        self.hookupAttrs['Midmouth_Left'].createClampNode()
        self.hookupAttrs['Midmouth_Left'].connect("%s.tx"%self.MouthPosition.CTRL.transformNode)
        self.hookupAttrs['Midmouth_Right'].createClampNode()
        self.hookupAttrs['Midmouth_Right'].createNegMult()
        self.hookupAttrs['Midmouth_Right'].connect("%s.tx"%self.MouthPosition.CTRL.transformNode)
        self.hookupAttrs['MouthDown'].createClampNode()
        self.hookupAttrs['MouthDown'].createNegMult()
        self.hookupAttrs['MouthDown'].connect("%s.ty"%self.MouthPosition.CTRL.transformNode)
        
        self.hookupAttrs['Blink_Left'].createClampNode()
        self.hookupAttrs['EyesWide_Left'].createClampNode()
        self.hookupAttrs['Blink_Left'].createNegMult()
        self.hookupAttrs['Blink_Left'].connect("%s.ty"%self.LeftEyeBlink.CTRL.transformNode)
        self.hookupAttrs['EyesWide_Left'].connect("%s.ty"%self.LeftEyeBlink.CTRL.transformNode)
        self.hookupAttrs['Blink_Right'].createClampNode()
        self.hookupAttrs['EyesWide_Right'].createClampNode()
        self.hookupAttrs['Blink_Right'].createNegMult()
        self.hookupAttrs['Blink_Right'].connect("%s.ty"%self.RightEyeBlink.CTRL.transformNode)
        self.hookupAttrs['EyesWide_Right'].connect("%s.ty"%self.RightEyeBlink.CTRL.transformNode)
        
        
        self.hookupAttrs['BrowsUp_Left'].createClampNode()
        self.hookupAttrs['BrowsDown_Left'].createClampNode()
        self.hookupAttrs['BrowsDown_Left'].createNegMult()
        self.hookupAttrs['BrowsUp_Left'].connect("%s.ty"%self.LeftBrow.CTRL.transformNode)
        self.hookupAttrs['BrowsDown_Left'].connect("%s.ty"%self.LeftBrow.CTRL.transformNode)
        self.hookupAttrs['BrowsIn_Left'].createNegMult()
        self.hookupAttrs['BrowsIn_Left'].connect("%s.tx"%self.LeftBrow.CTRL.transformNode)   
        self.hookupAttrs['BrowsUp_Right'].createClampNode()
        self.hookupAttrs['BrowsDown_Right'].createClampNode()
        self.hookupAttrs['BrowsDown_Right'].createNegMult()
        self.hookupAttrs['BrowsUp_Right'].connect("%s.ty"%self.RightBrow.CTRL.transformNode)
        self.hookupAttrs['BrowsDown_Right'].connect("%s.ty"%self.RightBrow.CTRL.transformNode)
        self.hookupAttrs['BrowsIn_Right'].connect("%s.tx"%self.RightBrow.CTRL.transformNode)  
        
        self.hookupAttrs['TongueUp'].connect("%s.ty"%self.Tongue.CTRL.transformNode)
        self.hookupAttrs['CheekPuff_Left'].connect("%s.tx"%self.CheekPuff.CTRL.transformNode)
        self.hookupAttrs['CheekPuff_Right'].connect("%s.ty"%self.CheekPuff.CTRL.transformNode)
        self.hookupAttrs['BrowsOuterLower_Right'].connect("%s.ty"%self.RightBrowOuterLower.CTRL.transformNode)
        self.hookupAttrs['BrowsOuterLower_Left'].connect("%s.ty"%self.LeftBrowOuterLower.CTRL.transformNode)
        self.hookupAttrs['NoseScrunch_Left'].connect("%s.tx"%self.NoseScrunch.CTRL.transformNode)
        self.hookupAttrs['NoseScrunch_Right'].connect("%s.ty"%self.NoseScrunch.CTRL.transformNode)
        self.hookupAttrs['Squint_Left'].connect("%s.tx"%self.Squint.CTRL.transformNode)
        self.hookupAttrs['Squint_Right'].connect("%s.ty"%self.Squint.CTRL.transformNode)
        self.hookupAttrs['MouthWhistle_NarrowAdjust_Left'].connect("%s.tx"%self.Whistle.CTRL.transformNode)
        self.hookupAttrs['MouthWhistle_NarrowAdjust_Right'].connect("%s.ty"%self.Whistle.CTRL.transformNode)
        self.hookupAttrs['UpperLipUp_Left'].connect("%s.tx"%self.UpperLipUp.CTRL.transformNode)
        self.hookupAttrs['UpperLipUp_Right'].connect("%s.ty"%self.UpperLipUp.CTRL.transformNode)
        self.hookupAttrs['LowerLipDown_Left'].createNegMult()
        self.hookupAttrs['LowerLipDown_Right'].createNegMult()
        self.hookupAttrs['LowerLipDown_Right'].connect("%s.tx"%self.LowerLipDown.CTRL.transformNode)
        self.hookupAttrs['LowerLipDown_Left'].connect("%s.ty"%self.LowerLipDown.CTRL.transformNode)
        self.hookupAttrs['Frown_Left'].createNegMult()
        self.hookupAttrs['Frown_Right'].createNegMult()
        self.hookupAttrs['Frown_Right'].connect("%s.tx"%self.Frown.CTRL.transformNode)
        self.hookupAttrs['Frown_Left'].connect("%s.ty"%self.Frown.CTRL.transformNode)
        
        self.hookupAttrs['JawRotateY_Left'].createClampNode()
        self.hookupAttrs['JawRotateY_Right'].createClampNode()
        self.hookupAttrs['JawRotateZ_Left'].createClampNode()
        self.hookupAttrs['JawRotateZ_Right'].createClampNode()
        self.hookupAttrs['JawRotateY_Right'].createNegMult()
        self.hookupAttrs['JawRotateZ_Left'].createNegMult()
        self.hookupAttrs['JawRotateY_Left'].connect("%s.tx"%self.JawRot.CTRL.transformNode)
        self.hookupAttrs['JawRotateY_Right'].connect("%s.tx"%self.JawRot.CTRL.transformNode)
        self.hookupAttrs['JawRotateZ_Left'].connect("%s.ty"%self.JawRot.CTRL.transformNode)
        self.hookupAttrs['JawRotateZ_Right'].connect("%s.ty"%self.JawRot.CTRL.transformNode)
        self.hookupAttrs['JawForeward'].createClampNode()
        self.hookupAttrs['JawBackward'].createClampNode()
        self.hookupAttrs['JawForeward'].createNegMult()
        self.hookupAttrs['JawForeward'].connect("%s.ty"%self.JawInOut.CTRL.transformNode)
        self.hookupAttrs['JawBackward'].connect("%s.ty"%self.JawInOut.CTRL.transformNode)
        self.hookupAttrs['Jaw_Up'].createClampNode()
        self.hookupAttrs['Jaw_Down'].createClampNode()
        self.hookupAttrs['Jaw_Left'].createClampNode()
        self.hookupAttrs['Jaw_Right'].createClampNode()
        self.hookupAttrs['Jaw_Down'].createNegMult()
        self.hookupAttrs['Jaw_Right'].createNegMult()
        self.hookupAttrs['Jaw_Up'].connect("%s.ty"%self.JawPos.CTRL.transformNode)
        self.hookupAttrs['Jaw_Down'].connect("%s.ty"%self.JawPos.CTRL.transformNode)
        self.hookupAttrs['Jaw_Left'].connect("%s.tx"%self.JawPos.CTRL.transformNode)
        self.hookupAttrs['Jaw_Right'].connect("%s.tx"%self.JawPos.CTRL.transformNode)

        self.hookupAttrs['LowerLipIn'].createClampNode()
        self.hookupAttrs['LowerLipOut'].createClampNode()
        self.hookupAttrs['LowerLipOut'].createNegMult()
        self.hookupAttrs['LowerLipIn'].connect("%s.ty"%self.LowerLipInOut.CTRL.transformNode)
        self.hookupAttrs['LowerLipOut'].connect("%s.ty"%self.LowerLipInOut.CTRL.transformNode)
        self.hookupAttrs['UpperLipIn'].createClampNode()
        self.hookupAttrs['UpperLipOut'].createClampNode()
        self.hookupAttrs['UpperLipIn'].createNegMult()
        self.hookupAttrs['UpperLipIn'].connect("%s.ty"%self.UpperLipInOut.CTRL.transformNode)
        self.hookupAttrs['UpperLipOut'].connect("%s.ty"%self.UpperLipInOut.CTRL.transformNode)
        
        
        
        
        

if __name__ == "__main__": 
    FacePlusRig()