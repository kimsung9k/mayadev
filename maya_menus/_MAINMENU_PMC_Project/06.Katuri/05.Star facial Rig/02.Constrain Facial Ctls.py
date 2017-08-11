import pymel.core

ctlList = pymel.core.ls( 'Ctl_MouthDt*' )

const1 = pymel.core.parentConstraint( ctlList[3], ctlList[0], ctlList[1].getParent(), mo=1 )
const2 = pymel.core.parentConstraint( ctlList[3], ctlList[0], ctlList[2].getParent(), mo=1 )
const3 = pymel.core.parentConstraint( ctlList[3], ctlList[6], ctlList[4].getParent(), mo=1 )
const4 = pymel.core.parentConstraint( ctlList[3], ctlList[6], ctlList[5].getParent(), mo=1 )
const5 = pymel.core.parentConstraint( ctlList[9], ctlList[6], ctlList[7].getParent(), mo=1 )
const6 = pymel.core.parentConstraint( ctlList[9], ctlList[6], ctlList[8].getParent(), mo=1 )
const7 = pymel.core.parentConstraint( ctlList[9], ctlList[0], ctlList[10].getParent(), mo=1 )
const8 = pymel.core.parentConstraint( ctlList[9], ctlList[0], ctlList[11].getParent(), mo=1 )

const1.listAttr( ud=1 )[0].set( 0.5 )
const2.listAttr( ud=1 )[0].set( 4 )
const3.listAttr( ud=1 )[0].set( 4 )
const4.listAttr( ud=1 )[0].set( 0.5 )
const5.listAttr( ud=1 )[0].set( 0.5 )
const6.listAttr( ud=1 )[0].set( 4 )
const7.listAttr( ud=1 )[0].set( 4 )
const8.listAttr( ud=1 )[0].set( 0.5 )