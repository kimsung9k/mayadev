#ifndef _retargetingCommand_h
#define _retargetingCommand_h

#include <io.h>

#include <maya/MSceneMessage.h>

#include <maya/MPxCommand.h>
#include <maya/MGlobal.h>
#include <maya/MSelectionList.h>
#include <maya/MObject.h>
#include <maya/MDagPath.h>
#include <maya/MDagPathArray.h>
#include <maya/MFnDependencyNode.h>
#include <maya/MArgList.h>
#include <maya/MArgDatabase.h>
#include <maya/MSyntax.h>
#include <maya/MFnTransform.h>
#include <maya/MTransformationMatrix.h>
#include <maya/MQuaternion.h>
#include <maya/MPoint.h>
#include <maya/MFloatArray.h>

#include <maya/MString.h>
#include <maya/MMatrix.h>

#include <fstream>

#include "enableSet.h"
#include "weightSet.h"
#include "controlerSet.h"

const char flagImport[2][8] = { "-im", "-import" };
const char flagExport[2][8] = { "-ex", "-export" };
const char flagImportCAnim[2][13] = { "-ima", "-importCAnim" };
const char flagFileName[2][10] = { "-fn", "-fileName" };

const char flagSrcWorld[2][13]    = { "-sw", "-sourceWorld" };
const char flagTrgWorld[2][13]    = { "-tw", "-targetWorld" };
const char flagRetarget[2][10]    = { "-rtg", "-retarget" };
const char flagRetargetAnim[2][14]= { "-rta", "-retargetAnim" };
const char flagWeight[2][8]       = { "-w", "-weight" };
const char flagClearAll[2][10]    = { "-cl", "-clearAll" };
const char flagClearTarget[2][13] = { "-ct", "-clearTarget" };

const char flagFlip[2][6] = { "-fl", "-flip" };

const char flagEnablePart[2][13]  = { "-enp", "-enablePart" };
const char flagEnableCtl[2][18]   = { "-enc", "-enableControler" };
const char flagEnableFollow[2][16]= { "-enf", "-enableFollow" };

const char flagPartWeight[2][14] = { "-wp", "-weightPart" };
const char flagCtlWeight[2][14]  = { "-wc", "-weightCtl" };


class RetargetingCommand : public MPxCommand
{
public:
				RetargetingCommand();
	virtual		~RetargetingCommand();

	MStatus		doIt( const MArgList& );
	MStatus		redoIt();
	MStatus		undoIt();
	bool		isUndoable() const;

	static		void* creator();

	static  MSyntax newSyntax();

	MStatus     argChk_exportImport( MArgDatabase& argData );
	MStatus     arcChk_setClear( MArgDatabase& argData );
	MStatus     argChk_getSelectionList( MArgDatabase& argData );
	MStatus     argChk_setSrcWorldName( MArgDatabase& argData );
	MStatus     argChk_setTrgWorldName( MArgDatabase& argData );
	MStatus     argChk_getSrcMtxInfo( MArgDatabase& argData );
	MStatus     argChk_getTrgMtxInfo( MArgDatabase& argData );
	MStatus     argChk_setAble( MArgDatabase& argData );
	MStatus     argChk_flip( MArgDatabase& argData );
	MStatus     argChk_updateEachWeight( MArgDatabase& argData );
	MStatus     argChk_updateWeight( MArgDatabase& argData );
	MStatus     argChk_enable( MArgDatabase& argData );

	MStatus     chk_matrixUpdate();

	MStatus     exportFile( const MString& nameFile, MArgDatabase& argData );
	MStatus     importFile( const MString& nameFile, CtlSet& ctlSet, CtlSet& ctlSetFlip );
	MStatus     importCAnimFile( const MString& nameFile );

	void        retargetPose();
	MStatus     retargetCAnim();

	static  void clearCtlSet( void* data );

public:
	MSelectionList m_selList;
	double  m_weight;
	static  MString  m_nsSrc;
	static  MStringArray  m_nsArrTrg;

	static bool m_srcNsUpdated;
	static bool m_srcMtxRequired;
	static bool m_srcRootRequired;
	static int  m_trgNsUpdated;
	static int  m_trgMtxRequired;

	static CtlSetArray m_ctlSetAnim;
	static CtlSetArray m_ctlSetAnimFlip;

	static CtlSet m_ctlSetSrc;
	static CtlSet m_ctlSetSrcFlip;
	static CtlSetArray m_ctlSetArrTrgBase;
	       CtlSetArray m_ctlSetArrTrg;

	MIntArray  m_srcMtxUpdated;
	MIntArray  m_trgMtxUpdated;

	bool    m_flipAble;
	bool	m_setAble;
	bool	m_setCAnimAble;
	float   m_cAnimFrame;
	bool    m_setEdited;

	enum retargetType
	{
		dragType, setType, fileType
	};

	int retargetMethod;

	static MCallbackId m_callbackId;

public:
	EnableSet   m_enableSet;
	WeightSet   m_weightSet;
	static MFloatArray  m_fArrFrame;
};


#endif