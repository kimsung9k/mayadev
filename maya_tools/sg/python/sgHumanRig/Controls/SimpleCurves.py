'''
MixamoAutoRig.Controls.SimpleCurves
Handles:
    Creation of simple curves
'''
import pymel.core as pm

STYLES = { 'circle': {  'p': [(0.783612, 0, -0.783612),
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
          'circleBent': {  'p': [(0.783612, 0, -0.783612),
                              (0, -1, -1.108194),
                              (-0.783612, 0, -0.783612),
                              (-1.108194, 1, 0),
                              (-0.783612, 0, 0.783612),
                              (0, -1, 1.108194),
                              (0.783612, 0, 0.783612),
                              (1.108194, 1, 0)],
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
          'box': {  'p': [(1.0, 1.0, 1.0),
                          (1.0, 1.0, -1.0),
                          (-1.0, 1.0, -1.0),
                          (-1.0, -1.0, -1.0),
                          (1.0, -1.0, -1.0),
                          (1.0, 1.0, -1.0),
                          (-1.0, 1.0, -1.0),
                          (-1.0, 1.0, 1.0),
                          (1.0, 1.0, 1.0),
                          (1.0, -1.0, 1.0),
                          (1.0, -1.0, -1.0),
                          (-1.0, -1.0, -1.0),
                          (-1.0, -1.0, 1.0),
                          (1.0, -1.0, 1.0),
                          (-1.0, -1.0, 1.0),
                          (-1.0, 1.0, 1.0)],
                        'k': [],
                        'd': 1,
                        'closeCurve': True
                      },
          
          'triangle': {  'p': [(-1.03923, 0.0, -0.6),
                               (1.03923, 0.0, -0.6),
                               (0.0, 0.0, 1.2)],
                        'k': [],
                        'd': 1,
                        'closeCurve': True
                      },
          'circleWave': {  'p': [(0.783612, -.5, -0.783612),
                              (0, .5, -1.108194),
                              (-0.783612, -.5, -0.783612),
                              (-1.108194, .5, 0),
                              (-0.783612, -.5, 0.783612),
                              (0, .5, 1.108194),
                              (0.783612, -.5, 0.783612),
                              (1.108194, .5, 0)],
                        'k': [],
                        'd': 3,
                        'closeCurve': True
                      },
          'Pyramid': {  'p': [(0.0, 2.0, 0.0),
                             (1.0, 0.0, -1.0),
                             (-1.0, 0.0, -1.0),
                             (0.0, 2.0, 0.0),
                             (-1.0, 0.0, 1.0),
                             (1.0, 0.0, 1.0),
                             (0.0, 2.0, 0.0),
                             (1.0, 0.0, -1.0),
                             (1.0, 0.0, 1.0),
                             (-1.0, 0.0, 1.0),
                             (-1.0, 0.0, -1.0)],
                        'k': [],
                        'd': 1,
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
          'square': {  'p': [(1, 0, 1),
                              (-1, 0, 1),
                              (-1, 0, -1),
                              (1, 0, -1)],
                        'k': [],
                        'd': 1,
                        'closeCurve': True
                      },
          'square': {  'p': [(1, 0, 1),
                              (-1, 0, 1),
                              (-1, 0, -1),
                              (1, 0, -1)],
                        'k': [],
                        'd': 1,
                        'closeCurve': True
                      }
          }
          
          
          
          
          
''''circle',
'box',
'box1',
'footbox',
'circleWrapped',
'pin',
'pin1',
'pin2',
'options',
'hula',
'PoleVector']'''

class Curve():
    def __init__(self, style, name = None, transform = None):
        self.transformNode = None
        self.name = name if name else 'Control'
        self.transform = transform
        self.style = STYLES[style]
        self.create()
        
    def create(self):
        self.transformNode = pm.curve(p=self.style['p'], k= self.style['k'], d = self.style['d'])
        if self.style['closeCurve']:
            pm.closeCurve(self.transformNode, ch = False, replaceOriginal=True, object=True, preserveShape=False, blendKnotInsertion=True)
        pm.rename(self.transformNode, self.name)
            
    def delete(self):
        if self.transformNode:
            pm.delete(self.transformNode)
            self.transformNode = None
        