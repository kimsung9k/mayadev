from sgModules import sgcommands
sels = sgcommands.listNodes( sl=1 )
ctl = sels[0]
shapes = sels[1].listRelatives( c=1 )
sgcommands.sliderVisibilityConnection( ctl.ty, shapes  )