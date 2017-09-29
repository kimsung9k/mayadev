import pymel.core
from sgMaya import sgCmds

sels = pymel.core.ls( sl=1 )
curves = []
for sel in sels:
	try:
		sgCmds.addCurveDistanceInfo( sel )
		curves.append( sel )
	except:pass
pymel.core.select( curves )