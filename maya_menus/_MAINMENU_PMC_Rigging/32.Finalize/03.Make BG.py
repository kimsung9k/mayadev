import pymel.core
sels = pymel.core.ls( sl=1 )
grp = pymel.core.group( sels, n='BG' )