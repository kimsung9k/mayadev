import sys

try:
	scriptPath = 'D:/wms/pipeline/scripts/common'
	if not scriptPath in sys.path:
		sys.path.append( scriptPath )
except:
	pass

import mayawms
reload(mayawms)
mayawms.UI()