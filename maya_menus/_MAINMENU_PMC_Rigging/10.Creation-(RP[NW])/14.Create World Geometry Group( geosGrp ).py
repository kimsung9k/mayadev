from sgMaya import sgCmds
import pymel.core

sels = pymel.core.ls( sl=1 )

geoGroups = []
for sel in sels:
    worldGeoGrp = sgCmds.createWorldGeometryGroup( sel )
    worldGeoGrp.rename( sel.nodeName() + '_worldGeo' )
    geoGroups.append( worldGeoGrp )
pymel.core.select( geoGroups )