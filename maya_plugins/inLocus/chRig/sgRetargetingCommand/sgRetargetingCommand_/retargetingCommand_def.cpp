#include "retargetingCommand.h"



MStatus RetargetingCommand::argChk_getSelectionList( MArgDatabase& argData )
{
	MStatus status;
	argData.getObjects( m_selList );
	return status;
}



MStatus RetargetingCommand::arcChk_setClear( MArgDatabase& argData )
{
	MStatus status;

	bool clearAll = argData.flagArgumentBool( flagClearAll[0], 0, &status );
	if( !status ) clearAll=false;
	bool clearTarget = argData.flagArgumentBool( flagClearTarget[0], 0, &status );
	if( !status ) clearTarget = false;

	if( clearTarget )
	{
		m_nsArrTrg.clear();
		m_ctlSetArrTrgBase.setLength( 0 );
	}
	if( clearAll )
	{
		m_nsSrc = "";
		m_srcNsUpdated = false;
		m_srcMtxRequired = false;
		m_ctlSetSrc = CtlSet();
		m_ctlSetSrcFlip = CtlSet();
		m_nsArrTrg.clear();
		m_ctlSetArrTrgBase.setLength( 0 );
	}

	return MS::kSuccess;
}



MStatus RetargetingCommand::argChk_setSrcWorldName( MArgDatabase& argData )
{
	MStatus status;

	bool m_srcReplaced = argData.flagArgumentBool( flagSrcWorld[0], 0, &status );

	if( !status || !m_selList.length()  )
	{
		if( !m_nsSrc.length() )
			m_srcNsUpdated = false;
		return MS::kSuccess;
	}

	MDagPath path;
	status = m_selList.getDagPath( 0, path );
	if( !status )
	{
		if( !m_nsSrc.length() )
			m_srcNsUpdated = false;
		return MS::kSuccess;
	}

	MFnDependencyNode fnNode( path.node() );
	MString strWorld = fnNode.name();

	int lengthStr = strWorld.length();
	MString strSub = strWorld.substring( lengthStr-9, lengthStr );

	if( strSub == "World_CTL" )
	{
		MString strNs = strWorld.substring( 0, lengthStr-10 );
		if( strNs != m_nsSrc )
		{
			m_srcNsUpdated = true;
			m_nsSrc = strNs;
		}
		m_srcMtxRequired = true;
	}

	m_ctlSetSrc.setAllEnable();

	return MS::kSuccess;
}



MStatus RetargetingCommand::argChk_setTrgWorldName( MArgDatabase& argData )
{
	MStatus status;

	int trgReplaced = argData.flagArgumentBool( flagTrgWorld[0], 0, &status );

	if( !status || !m_selList.length() )
	{
		m_trgNsUpdated = -1;
		return MS::kSuccess;
	}

	MDagPath path;
	status = m_selList.getDagPath( 0, path );

	if( !status )
	{
		m_trgNsUpdated = -1;
		return MS::kSuccess;
	}

	MFnDependencyNode fnNode( path.node() );
	MString strWorld = fnNode.name();

	int lengthStr = strWorld.length();
	MString strSub = strWorld.substring( lengthStr-9, lengthStr );

	if( strSub == "World_CTL" )
	{
		MString strNs = strWorld.substring( 0, lengthStr-10 );
		
		int existsNum = -1;
		for( int i=0; i< m_nsArrTrg.length(); i++ )
		{
			if( m_nsArrTrg[i] == strNs )
			{
				existsNum = i; break;
			}
		}
		
		if( existsNum == -1 )
		{
			m_nsArrTrg.append( strWorld.substring( 0, lengthStr-10 ) );
			CtlSet ctlSetNew;
			m_ctlSetArrTrgBase.append( ctlSetNew );
			m_trgNsUpdated = m_nsArrTrg.length()-1;
			m_trgMtxRequired = m_nsArrTrg.length()-1;
		}
		else
		{
			m_trgMtxRequired = existsNum;
		}
	}

	return MS::kSuccess;
}



MStatus RetargetingCommand::argChk_getSrcMtxInfo( MArgDatabase& argData )
{
	MStatus status;
	/*
	bool getValue1 = argData.flagArgumentBool( flagUpdSrcMtx[0], 0, &status );
	if( status )
		m_srcMtxRequired = getValue1;

	bool getValue2 = argData.flagArgumentBool( flagSourceUpdateRoot[0], 0, &status );
	if( status )
		m_srcRootRequired = getValue2;
	*/
	return MS::kSuccess;
}



MStatus RetargetingCommand::argChk_getTrgMtxInfo( MArgDatabase& argData )
{
	MStatus status;
	/*
	int getValue = argData.flagArgumentBool( flagUpdTrgMtx[0], 0, &status );
	if( status ) 
		m_trgMtxRequired = getValue;
	*/
	return status;
}



MStatus RetargetingCommand::argChk_updateEachWeight( MArgDatabase& argData )
{
	MStatus status;

	if( !m_selList.length() ) return MS::kSuccess;

	MObject oSelection;
	m_selList.getDependNode( 0, oSelection );
	MFnDependencyNode fnSelection = oSelection;

	MString strTarget = fnSelection.name();

	int indexTarget = -1;
	MString strSub = strTarget.substring( strTarget.length()-9, strTarget.length() );
	if( strSub == "World_CTL" )
	{
		MString strNs = strTarget.substring( 0, strTarget.length()-10 );
		for( int i=0; i<m_nsArrTrg.length(); i++ )
		{
			if( strNs == m_nsArrTrg[i] )
			{
				indexTarget = i;
				break;
			}
		}
	}
	if( indexTarget == -1 ) return MS::kSuccess;

	MString strPart; double weightPart;
	MString strCtl;  double weightCtl;
	argData.getFlagArgument( flagPartWeight[0], 0, strPart );
	argData.getFlagArgument( flagPartWeight[0], 1, weightPart );
	argData.getFlagArgument( flagCtlWeight[0], 0, strCtl );
	argData.getFlagArgument( flagCtlWeight[0], 1, weightCtl );
	
	m_weightSet.getCtlSet( &m_ctlSetArrTrgBase[ indexTarget ] );

	if( strPart.length() )
	{
		m_weightSet.setPart( strPart, weightPart );
	}

	if( strCtl.length() )
	{
		m_weightSet.setCtl( strCtl, weightCtl );
	}

	return MS::kSuccess;
}



MStatus RetargetingCommand::argChk_updateWeight( MArgDatabase& argData )
{
	MStatus status;

	double getValue;
	status = argData.getFlagArgument( flagWeight[0], 0, getValue );
	if( status )
		m_weight = getValue;

	return MS::kSuccess;
}



MStatus RetargetingCommand::argChk_setAble( MArgDatabase& argData )
{
	MStatus status;

	int getValue = argData.flagArgumentBool( flagRetarget[0], 0, &status );

	retargetMethod = retargetType::dragType;

	if( status ) 
	{
		m_setAble = true;
		if( getValue != 0 ) retargetMethod = retargetType::setType;
	}
	else
		m_setAble = false;

	double getCAnimValue;
	status = argData.getFlagArgument( flagRetargetAnim[0], 0, getCAnimValue );

	if( status )
	{
		m_setCAnimAble = true;
		m_cAnimFrame = getCAnimValue;
	}
	else
		m_setCAnimAble = false;

	return MS::kSuccess;
}



MStatus RetargetingCommand::argChk_flip( MArgDatabase& argData )
{
	MStatus status;

	bool value;
	status = argData.getFlagArgument( flagFlip[0], 0, value );
	if( status )
	{
		m_flipAble = value;
	}
	else
	{
		m_flipAble = false;
	}

	return MS::kSuccess;
}



MStatus RetargetingCommand::argChk_enable( MArgDatabase& argData )
{
	MStatus status;

	if( !m_selList.length() )
	{
		m_enableSet.getCtlSet( &m_ctlSetSrc );
	}
	else
	{
		int indexTarget = -1;

		MObject oSelection;
		m_selList.getDependNode( 0, oSelection );
		MFnDependencyNode fnSelection = oSelection;

		MString strTarget = fnSelection.name();

		MString strSub = strTarget.substring( strTarget.length()-9, strTarget.length() );
	
		if( strSub == "World_CTL" )
		{
			MString strNs = strTarget.substring( 0, strTarget.length()-10 );

			for( int i=0; i<m_nsArrTrg.length(); i++ )
			{
				if( strNs == m_nsArrTrg[i] )
				{
					indexTarget = i;
					break;
				}
			}
			if( indexTarget == -1 )
				m_enableSet.getCtlSet( &m_ctlSetSrc );
			else
				m_enableSet.getCtlSet( &m_ctlSetArrTrgBase[indexTarget] );
		}
		else
		{
			return MS::kFailure;
		}
	}

	MString namePart; bool partEnable;
	status = argData.getFlagArgument( flagEnablePart[0], 0, namePart );
	if( status )
	{
		status = argData.getFlagArgument( flagEnablePart[0], 1, partEnable );
		if( !status ) namePart = "";
		if( namePart.length() ) m_enableSet.enablePart( namePart, partEnable );
	}

	MString nameCtl; bool ctlEnable;
	status = argData.getFlagArgument( flagEnableCtl[0], 0, nameCtl );
	if( status )
	{
		status = argData.getFlagArgument( flagEnableCtl[0], 1, ctlEnable );
		if( !status ) nameCtl = "";
		if( nameCtl.length() ) m_enableSet.enableCtl( nameCtl, ctlEnable );
	}

	MString nameFollow; bool followEnable;
	status = argData.getFlagArgument( flagEnableFollow[0], 0, nameFollow );
	if( status )
	{
		status = argData.getFlagArgument( flagEnableFollow[0], 1, followEnable );
		if( !status ) nameFollow = "";
		if( nameFollow.length() ) m_enableSet.enableFollow( nameFollow, followEnable );
	}

	return MS::kSuccess;
}



MStatus RetargetingCommand::chk_matrixUpdate()
{
	MStatus status;

	if( m_srcNsUpdated )
	{
		status = m_ctlSetSrc.setBaseData( m_nsSrc, true );
		CHECK_MSTATUS_AND_RETURN_IT( status );
		status = m_ctlSetSrcFlip.setBaseData( m_nsSrc, true );
		CHECK_MSTATUS_AND_RETURN_IT( status );
		m_srcNsUpdated = false;
	}

	if( m_trgNsUpdated != -1 )
	{
		status = m_ctlSetArrTrgBase[ m_trgNsUpdated ].setBaseData( m_nsArrTrg[ m_trgNsUpdated ] );
		CHECK_MSTATUS_AND_RETURN_IT( status );
		m_trgNsUpdated = -1;
	}

	if( m_srcMtxRequired )
	{
		if( m_srcRootRequired )
		{
			m_ctlSetSrc.updateRootMatrix();
			m_ctlSetSrcFlip.updateRootMatrix();
		}
		m_ctlSetSrc.updateCtlMatrix();
		m_ctlSetSrcFlip.updateCtlMatrix();
		m_ctlSetSrcFlip.flip();
		m_srcMtxRequired = false;
	}

	if( m_trgMtxRequired != -1 )
	{
		m_ctlSetArrTrgBase[ m_trgMtxRequired ].updateRootMatrix();
		m_ctlSetArrTrgBase[ m_trgMtxRequired ].updateCtlMatrix();
		m_trgMtxRequired = -1;
	}

	return MS::kSuccess;
}



void RetargetingCommand::retargetPose()
{
	m_ctlSetArrTrg.setLength( m_ctlSetArrTrgBase.length() );

	for( int i=0; i< m_ctlSetArrTrg.length(); i++ )
	{
		m_ctlSetArrTrg[i] = m_ctlSetArrTrgBase[i];
		m_ctlSetArrTrg[i].updateCtlMatrix();

		if( m_flipAble )
			m_ctlSetArrTrg[i].connectSource( &m_ctlSetSrcFlip );
		else
			m_ctlSetArrTrg[i].connectSource( &m_ctlSetSrc );

		m_ctlSetArrTrg[i].connectBase( &m_ctlSetArrTrgBase[i] );
		m_ctlSetArrTrg[i].setRetargetValues();
		m_ctlSetArrTrg[i].retarget( m_weight );
	}
	m_setEdited = true;
}



MStatus RetargetingCommand::retargetCAnim()
{
	MStatus status;

	if( !m_fArrFrame.length() ) return MS::kSuccess;

	float beforeWeight = 1.0f;
	float afterWeight  = 0.0f;

	float startFrame = m_fArrFrame[0];
	float endFrame   = m_fArrFrame[ m_fArrFrame.length() -1 ];

	float floatRoofLength = fabs( endFrame-startFrame )+1;
	int   intRoofLength = floatRoofLength;
	if( floatRoofLength > intRoofLength )
		intRoofLength++;

	int indexReweight = 0;
	while( m_cAnimFrame > endFrame )
	{
		m_cAnimFrame -= (float)intRoofLength;
		indexReweight += 1;
	}

	int indexBefore = -1;
	int indexAfter  = -1;
	
	for( int i=0; i< m_fArrFrame.length(); i++ )
	{
		if( m_cAnimFrame >= m_fArrFrame[i] )
		{
			indexBefore = i;
			if( i == m_fArrFrame.length() )
			{
				indexBefore = 0;

				float afterValue = m_fArrFrame[0] - m_cAnimFrame + (float)intRoofLength;
				float beforeValue = m_cAnimFrame - m_fArrFrame[i];

				float sumValue = afterValue + beforeValue;

				beforeWeight = afterValue / sumValue;
				afterWeight  = beforeValue / sumValue;
			}
		}
		else
		{
			if( i == 0 ) break;
			indexAfter = i;

			float afterValue = m_fArrFrame[i] - m_cAnimFrame;
			float beforeValue = m_cAnimFrame - m_fArrFrame[i-1];

			float sumValue = afterValue + beforeValue;

			beforeWeight = afterValue / sumValue;
			afterWeight  = beforeValue / sumValue;
			break;
		}
	}

	if( m_cAnimFrame < 0 )
	{
		indexBefore  = endFrame;
		indexAfter   = startFrame;
		beforeWeight = -m_cAnimFrame;
		afterWeight  = 1.0-beforeWeight;
	}

	if( indexBefore < 0 ) return MS::kSuccess;
	if( indexAfter == -1 ) indexAfter = 0;

	CtlSet ctlSetNew;
	if( !m_flipAble )
		ctlSetNew.getBlend( m_ctlSetAnim[ indexBefore ],     m_ctlSetAnim[ indexAfter ],     beforeWeight, afterWeight );
	else
		ctlSetNew.getBlend( m_ctlSetAnimFlip[ indexBefore ], m_ctlSetAnimFlip[ indexAfter ], beforeWeight, afterWeight );

	m_ctlSetArrTrg.setLength( m_ctlSetArrTrgBase.length() );
	for( int i=0; i< m_ctlSetArrTrgBase.length(); i++ )
	{
		m_ctlSetArrTrg[i] = m_ctlSetArrTrgBase[i];
		m_ctlSetArrTrg[i].updateCtlMatrix();
		m_ctlSetArrTrg[i].connectSource( &ctlSetNew );
		m_ctlSetArrTrg[i].connectBase( &m_ctlSetArrTrgBase[i] );
		m_ctlSetArrTrg[i].setRetargetValues();
		m_ctlSetArrTrg[i].retarget( m_weight );
	}
	return MS::kSuccess;
}