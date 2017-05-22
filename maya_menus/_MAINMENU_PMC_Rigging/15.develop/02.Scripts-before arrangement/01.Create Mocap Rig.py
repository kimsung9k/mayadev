import sgProject.pingo
from sgModules import sgRig

className = 'CH_Pipi'
exec( "mocCreateTarget = sgProject.pingo.%s.mocCreatTarget" % className )
sgRig.createMocapJoints( mocCreateTarget )