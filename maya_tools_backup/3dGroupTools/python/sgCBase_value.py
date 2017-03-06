


def singleToList( singleTarget ):
    
    if not type( singleTarget ) in [ list, tuple ]:
        return [singleTarget]
    else:
        return singleTarget






def getValueFromDict( argDict, *dictKeys ):
    
    items = argDict.items()
    
    for item in items:
        if item[0] in dictKeys: return item[1]
    
    return None