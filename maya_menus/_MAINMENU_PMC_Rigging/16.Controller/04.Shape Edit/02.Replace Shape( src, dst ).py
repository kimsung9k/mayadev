from sgMaya import sgCmds
import pymel.core

sels = pymel.core.ls( sl=1 )
for sel in sels[1:]:
    sgCmds.replaceShape( sels[0], sel )