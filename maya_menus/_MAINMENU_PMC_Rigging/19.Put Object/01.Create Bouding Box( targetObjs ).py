import pymel.core

for sel in pymel.core.ls( sl=1 ):
    bb = pymel.core.exactWorldBoundingBox( sel )    
    bbmin = bb[:3]
    bbmax = bb[-3:]
    points = [[] for i in range(8)]
    points[0] = [bbmin[0], bbmin[1], bbmax[2]]
    points[1] = [bbmax[0], bbmin[1], bbmax[2]]
    points[2] = [bbmin[0], bbmax[1], bbmax[2]]
    points[3] = [bbmax[0], bbmax[1], bbmax[2]]
    points[4] = [bbmin[0], bbmax[1], bbmin[2]]
    points[5] = [bbmax[0], bbmax[1], bbmin[2]]
    points[6] = [bbmin[0], bbmin[1], bbmin[2]]
    points[7] = [bbmax[0], bbmin[1], bbmin[2]]
    
    cube = pymel.core.polyCube( ch=1, o=1, cuv=4, n= sel.shortName() + '_boundingBox' )[0]
    cubeShape = cube.getShape()
    
    for i in range( 8 ):
        pymel.core.move( points[i][0], points[i][1], points[i][2], cube + '.vtx[%d]' % i )