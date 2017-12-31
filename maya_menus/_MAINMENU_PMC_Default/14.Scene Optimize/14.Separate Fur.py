import pymel.core
sels = pymel.core.ls( type='FurFeedback' )

furObjs = []
for sel in sels:
    furObjs.append( sel.getParent() )

furGrp = pymel.core.group( em=1, n='furGrp' )
pymel.core.parent( furObjs, furGrp )