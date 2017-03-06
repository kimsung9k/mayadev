import maya.cmds as cmds

winName = 'retargetExporter'
title = 'Retarget Exporter'

width = 450
height = 410

userNameWidth = width * 0.4
fileWidth     = width - userNameWidth

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