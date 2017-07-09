import pymel.core
from sgMaya import sgCmds

sels = pymel.core.ls( sl=1 )
for sel in sels:
    combinedObj = sgCmds.combineMultiShapes( sel )
    
    pymel.core.polyReduce( combinedObj, ver=1, trm=0, p=90, vct=0, tct=0, shp=0, keepBorder=1, keepMapBorder=1, 
                           keepColorBorder=1, keepFaceGroupBorder=1, keepHardEdge=1, keepCreaseEdge=1, keepBorderWeight=0.5, 
                           keepMapBorderWeight=0.5, keepColorBorderWeight=0.5, keepFaceGroupBorderWeight=0.5, keepHardEdgeWeight=0.5, 
                           keepCreaseEdgeWeight=0.5, useVirtualSymmetry=0, symmetryTolerance=0.01, sx=0, sy=1, sz=0, sw=0, preserveTopology=1, keepQuadsWeight=1, vertexMapName="",
                           replaceOriginal=1, cachingReduce=1, ch=1 )
    combinedObj.rename( sel.shortName() + '_reduced' )
    pymel.core.select( combinedObj )
    cmds.DeleteHistory()