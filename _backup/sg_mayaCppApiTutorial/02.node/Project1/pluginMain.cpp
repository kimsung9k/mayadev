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

	static MObject aInput1;
	static MObject aInput2;
	static MObject aOutput;
};


MTypeId MyNode::id(0x12345678);

MObject MyNode::aInput1;
MObject MyNode::aInput2;
MObject MyNode::aOutput;


MyNode::MyNode() {}
MyNode::~MyNode() {}


MStatus MyNode::compute(const MPlug& plug, MDataBlock& data) {

	MDataHandle hInput1 = data.inputValue(aInput1);
	MDataHandle hInput2 = data.inputValue(aInput2);
	MDataHandle hOutput = data.outputValue(aOutput);

	double inputValue = hInput1.asDouble() + hInput2.asDouble();
	hOutput.setDouble(sin(inputValue));

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

	aInput1 = nAttr.create("input1", "input1", MFnNumericData::kDouble, 0.0);
	nAttr.setStorable(true);
	status = addAttribute(aInput1);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	aInput2 = nAttr.create("input2", "input2", MFnNumericData::kDouble, 0.0);
	nAttr.setStorable(true);
	status = addAttribute(aInput2);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	aOutput = nAttr.create("output", "output", MFnNumericData::kDouble, 0.0);
	nAttr.setStorable(false);
	status = addAttribute(aOutput);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	status = attributeAffects(aInput1, aOutput);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	status = attributeAffects(aInput2, aOutput);
	CHECK_MSTATUS_AND_RETURN_IT(status);

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