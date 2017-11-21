from sgMaya import sgCmds

sels = sgCmds.listNodes( sl=1 )

for sel in sels:
    sgCmds.setCenter( sel )