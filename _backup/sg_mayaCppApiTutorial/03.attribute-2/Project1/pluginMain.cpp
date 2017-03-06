#include <maya/MFnPlugin.h>
#include <maya/MGlobal.h>
#include <maya/MFnNumericAttribute.h>


class MyNode : public MPxNode
{
public:
	MyNode();
	virtual				~MyNode();

	virtual MStatus		compute(const MPlug& plug, MDataBlock& data);

	static  void*		creator();
	static  MStatus		initialize();

	static	MTypeId		id;

	static MObject aInputD2;
	static MObject aInputD3;
	static MObject aOutput;
};


MTypeId MyNode::id(0x12345678);

MObject MyNode::aInputD2;
MObject MyNode::aInputD3;
MObject MyNode::aOutput;

MyNode::MyNode() {}
MyNode::~MyNode() {}


MStatus MyNode::compute(const MPlug& plug, MDataBlock& data) {

	MDataHandle hInputD2 = data.inputValue(aInputD2);
	MDataHandle hInputD3 = data.inputValue(aInputD3);
	MDataHandle hOutput = data.outputValue(aOutput);

	double2& inputValueD2 = hInputD2.asDouble2();
	double3& inputValueD3 = hInputD3.asDouble3();
	hOutput.setDouble(sin(inputValueD2[0]+inputValueD3[0]));

	return MS::kSuccess;
}


void* MyNode::creator()
{
	MGlobal::displayInfo("create node");
	return new MyNode();
}


MStatus MyNode::initialize() {

	MStatus status;

	MFnNumericAttribute nAttr;

	aInputD2 = nAttr.create("inputD2", "inputD2", MFnNumericData::k2Double);
	nAttr.setStorable(true);
	status = addAttribute(aInputD2);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	aInputD3 = nAttr.create("inputD3", "inputD3", MFnNumericData::k3Double );
	nAttr.setStorable(true);
	status = addAttribute(aInputD3);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	aOutput = nAttr.create("output", "output", MFnNumericData::kDouble, 0.0);
	nAttr.setStorable(false);
	status = addAttribute(aOutput);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	CHECK_MSTATUS_AND_RETURN_IT(attributeAffects(aInputD2, aOutput));
	CHECK_MSTATUS_AND_RETURN_IT(attributeAffects(aInputD3, aOutput));

	return MS::kSuccess;
}



MStatus initializePlugin(MObject obj)
{
	MStatus result;
	MFnPlugin plugin(obj, "myplugin", "1.0");
	MGlobal::displayInfo("plugin loaded");

	result = plugin.registerNode("mynode", MyNode::id, MyNode::creator, MyNode::initialize);

	return result;
}

MStatus uninitializePlugin(MObject obj)
{
	MStatus result;
	MFnPlugin plugin(obj);
	MGlobal::displayInfo("plugin unloaded");

	result = plugin.deregisterNode(MyNode::id);

	return result;
}