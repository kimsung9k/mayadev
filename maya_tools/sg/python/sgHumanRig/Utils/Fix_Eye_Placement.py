'''
Utils.Fix_Eye_Placement
Handles:
    Temp Function for Fix the placement of the eyes
'''

def Fix_Eye_Placement():
    eyeNames = ['mixamorig:LeftEye', "mixamorig:RightEye"]
    import maya.cmds as mayac
    import maya.mel as mel
    
    for eye in eyeNames:
        if mayac.objExists(eye):
            skinClusters = mayac.listConnections(eye, type="skinCluster")
            if skinClusters:
                for sc in skinClusters:
                    
                    mayac.select(clear=True)
                    mayac.skinCluster(sc, e=True, selectInfluenceVerts=eye)
                    if mayac.ls(sl=True):
                        bbx = mayac.xform(mayac.ls(sl=True), q=True, bb=True, ws=True)
                        centerX = (bbx[0] + bbx[3]) / 2.0
                        centerY = (bbx[1] + bbx[4]) / 2.0
                        centerZ = (bbx[2] + bbx[5]) / 2.0
                        mel.eval("MoveSkinJointsTool;")
                        mayac.xform(eye, t=[centerX, centerY, centerZ], a=True, ws=True)
                        mayac.select(cl=True)
                        for mesh in mayac.ls(type="mesh"):
                            try:
                                mayac.setAttr("%s.template"%mesh, 0)
                            except:
                                pass
    
    
if __name__ == "__main__":
    Fix_Eye_Placement()