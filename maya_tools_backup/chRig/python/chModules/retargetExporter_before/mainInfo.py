import maya.cmds as cmds

winName = 'retargetExporter'
title = 'Retarget Exporter'

width = 300
height = 400

pathInfoPath = 'from init'
uiInfoPath = 'from init'

motionExportPath = 'from init'
hikExportPath    = 'from init'

fileTypeOption   = 'froom init'
namespaceOption  = 'from init'
frontNameOption  = 'from init'
thisString       = 'from init'

setSpace  = lambda : cmds.text( l='', h=1 )
setSpaceH = lambda x : cmds.text( l='', h=x )