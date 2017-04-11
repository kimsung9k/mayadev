import part0_rootRoad
import part1_driverInfo
import part2_meshInfo
import part3_editMesh

rootDriver = ''
driverInfoInst = None
meshInfoInst = None
editMeshInst = None
targetDriverList = []

newElement = None

node = ''

overIndices = []
emptyIndices = []


def updateUiCondition():
    if driverInfoInst:
        driverInfoInst.updateCmd()
    if meshInfoInst:
        meshInfoInst.updateCmd()
    if editMeshInst:
        editMeshInst.updateCmd()