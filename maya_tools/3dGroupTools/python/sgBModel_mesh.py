import maya.api.OpenMaya as openMaya



class CPolygonData:
    
    def __init__(self):

        self.points          = openMaya.MPointArray()
        self.polygonCounts   = openMaya.MIntArray()
        self.polygonConnects = openMaya.MIntArray()




class CUVData:
    
    def __init__(self):
        
        self.uvSetName = 'map1'
        
        self.uArray    = openMaya.MFloatArray()
        self.vArray    = openMaya.MFloatArray()
        self.uvCounts  = openMaya.MIntArray()
        self.uvIds     = openMaya.MIntArray()




class CMeshData:
    
    def __init__(self):
        
        self.polygonData     = CPolygonData()
        self.uvDatas         = []