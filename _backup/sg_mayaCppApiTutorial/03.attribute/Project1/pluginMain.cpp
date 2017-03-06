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

	static MObject aInput_bool;
	static MObject aInput_short;
	static MObject aInput_int;
	static MObject aInput_long;
	static MObject aInput_float;
	static MObject aInput_double;
	static MObject aOutput;
};


MTypeId MyNode::id(0x12345678);

MObject MyNode::aInput_bool;
MObject MyNode::aInput_short;
MObject MyNode::aInput_int;
MObject MyNode::aInput_long;
MObject MyNode::aInput_float;
MObject MyNode::aInput_double;
MObject MyNode::aOutput;


MyNode::MyNode() {}
MyNode::~MyNode() {}


MStatus MyNode::compute(const MPlug& plug, MDataBlock& data) {

	MDataHandle hInput_bool = data.inputValue(aInput_bool);
	MDataHandle hInput_short = data.inputValue(aInput_short);
	MDataHandle hInput_int = data.inputValue(aInput_int);
	MDataHandle hInput_long = data.inputValue(aInput_long);
	MDataHandle hInput_float = data.inputValue(aInput_float);
	MDataHandle hInput_double = data.inputValue(aInput_double);

	MDataHandle hOutput = data.outputValue(aOutput);

	double inputValue = hInput_bool.asBool() + hInput_short.asShort() + hInput_int.asInt() + hInput_long.asLong() + hInput_float.asFloat() + hInput_double.asDouble();
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

	aInput_bool = nAttr.create("input_bool", "input_bool", MFnNumericData::kBoolean, 0.0);
	nAttr.setStorable(true);
	status = addAttribute(aInput_bool);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	aInput_short = nAttr.create("Input_short", "Input_short", MFnNumericData::kShort, 0.0);
	nAttr.setStorable(true);
	status = addAttribute(aInput_short);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	aInput_int = nAttr.create("Input_int", "Input_int", MFnNumericData::kInt, 0.0);
	nAttr.setStorable(true);
	status = addAttribute(aInput_int);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	aInput_long = nAttr.create("input_long", "input_long", MFnNumericData::kLong, 0.0);
	nAttr.setStorable(true);
	status = addAttribute(aInput_long);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	aInput_float = nAttr.create("input_float", "input_float", MFnNumericData::kFloat, 0.0);
	nAttr.setStorable(true);
	status = addAttribute(aInput_float);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	aInput_double = nAttr.create("input_double", "input_double", MFnNumericData::kDouble, 0.0);
	nAttr.setStorable(true);
	status = addAttribute(aInput_double);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	aOutput = nAttr.create("output", "output", MFnNumericData::kDouble, 0.0);
	nAttr.setStorable(false);
	status = addAttribute(aOutput);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	CHECK_MSTATUS_AND_RETURN_IT(attributeAffects(aInput_bool, aOutput));
	CHECK_MSTATUS_AND_RETURN_IT(attributeAffects(aInput_short, aOutput));
	CHECK_MSTATUS_AND_RETURN_IT(attributeAffects(aInput_int, aOutput));
	CHECK_MSTATUS_AND_RETURN_IT(attributeAffects(aInput_long, aOutput));
	CHECK_MSTATUS_AND_RETURN_IT(attributeAffects(aInput_float, aOutput));
	CHECK_MSTATUS_AND_RETURN_IT(attributeAffects(aInput_double, aOutput));

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