'''
DJB_Character.BlendshapeTracker
Handles:
    Keeps track of blendshapes on a rig
'''
import maya.cmds as mayac


class blendShapeAttrTracker(object):
    def __init__(self, blendShapeNode, attr, meshOrig):
        self.blendShapeNode = blendShapeNode
        self.attr = attr
        self.meshOrig = meshOrig
        self.attrFull = "%s.%s"%(self.blendShapeNode,self.attr)
        self.connection = mayac.listConnections(self.attrFull,plugs=True)
        if self.connection:
            self.connection = self.connection[0]
    def deleteConnection(self):
        if self.connection:
            mayac.disconnectAttr(self.connection, self.attrFull)
    def reconnect(self, blendShapeNodeOrigTempName = None):
        self.blendShapeNodeOrigTempName = blendShapeNodeOrigTempName
        if self.connection:
            mayac.connectAttr(self.connection, "%s.%s"%(self.blendShapeNodeOrigTempName,self.attr))
    def off(self):
        mayac.setAttr(self.attrFull, 0.0)
    def on(self):
        mayac.setAttr(self.attrFull, 1.0)
    def duplicateGeo(self):
        self.newGeo = mayac.duplicate(self.meshOrig, returnRootsOnly=True)[0]
        shapes = mayac.listRelatives(self.newGeo, children=True, shapes=True, fullPath=True)
        for shape in shapes:
            connections = mayac.listConnections(shape, connections=True, plugs=True, type='shadingEngine')
            if connections:
                i=0
                while i<len(connections):
                    verifyConnection = mayac.listConnections(connections[i], s=True, plugs=True, type='shadingEngine')
                    if verifyConnection:
                        try:
                            mayac.disconnectAttr(connections[i],verifyConnection[0])
                        except:
                            pass
                    i+=2
        
        self.newGeo = mayac.parent(self.newGeo, world=True)[0]
        self.newGeo = mayac.rename(self.newGeo, self.attr)
        mayac.setAttr("%s.visibility"%self.newGeo, lock=False, keyable=True)
        mayac.setAttr("%s.visibility"%self.newGeo, 0)
        
    def connectNewBlendShape(self, newBlendshapeNode):
        self.newBlendShapeNode = newBlendshapeNode
        #ensure naming of attr is good
        if self.newGeo != self.attr:
            mayac.aliasAttr(self.attr, "%s.%s"%(self.newBlendShapeNode,self.newGeo))
        self.newBlendshapeConnection = ["%s.%s"%(self.blendShapeNodeOrigTempName,self.attr), "%s.%s"%(self.newBlendShapeNode,self.attr)]
        mayac.connectAttr(self.newBlendshapeConnection[0], self.newBlendshapeConnection[1])
        
    def disconnectNewBlendShape(self):
        try:
            mayac.disconnectAttr(self.newBlendshapeConnection[0], self.newBlendshapeConnection[1])
        except:
            pass
        

class blendShapeTracker(object):
    def __init__(self, blendShapeNodeOrig, meshOrig):
        self.blendShapeNodeOrig = blendShapeNodeOrig
        self.meshOrig = meshOrig
        self.shapesOrig = mayac.aliasAttr(self.blendShapeNodeOrig, q=True)[::2]
        self.blendShapeAttrTrackers = []
        #create trackers and delete connections
        for attr in self.shapesOrig:
            if attr != "envelope":
                attrTracker = blendShapeAttrTracker(self.blendShapeNodeOrig, attr, self.meshOrig)
                attrTracker.deleteConnection()
                self.blendShapeAttrTrackers.append(attrTracker)
                attrTracker.off()
        
    def duplicate(self, newMesh):
        self.newMesh = newMesh
        #duplicate off blends as is
        for attrTracker in self.blendShapeAttrTrackers:
            for offAttr in self.blendShapeAttrTrackers:
                offAttr.off()
            attrTracker.on()
            attrTracker.duplicateGeo()
            attrTracker.off()
        #create new blendshape node and hook up attrs for baking
        self.blendShapeNodeOrigTempName = mayac.rename(self.blendShapeNodeOrig, "BACKUP_%s"%self.blendShapeNodeOrig)
        blendShapeCreationSelection = []
        for attrTracker in self.blendShapeAttrTrackers:
            blendShapeCreationSelection.append(attrTracker.newGeo)
        blendShapeCreationSelection.append(self.newMesh)
        self.blendShapeNodeNew = mayac.blendShape(blendShapeCreationSelection, name=self.blendShapeNodeOrig, frontOfChain=True)[0]
        for attrTracker in self.blendShapeAttrTrackers:
            attrTracker.reconnect(blendShapeNodeOrigTempName = self.blendShapeNodeOrigTempName)
        for attrTracker in self.blendShapeAttrTrackers:
            attrTracker.connectNewBlendShape(self.blendShapeNodeNew)
        self.bakeAttrs = []
        for attrTracker in self.blendShapeAttrTrackers:
            self.bakeAttrs.append(attrTracker.attrFull)
            
    
    def restoreScene(self):
        mayac.rename(self.blendShapeNodeOrigTempName, self.blendShapeNodeOrig)
        try:
            mayac.setAttr("%s.envelope"%self.blendShapeNodeOrig, 1.0)
        except:
            pass