#include "CreateJointContext.h"


MStatus CreateJointContext::getSelection( MDagPathArray& geometry )
{
    MStatus status;

    MSelectionList selectionList;
    MGlobal::getActiveSelectionList( selectionList );

    // Get the shape nodes
    MItSelectionList itList( selectionList );
    MDagPath pathNode;
    unsigned int numShapes;

    for ( ; !itList.isDone(); itList.next() )
    {
        status = itList.getDagPath( pathNode );
        CHECK_MSTATUS_AND_RETURN_IT( status );
        numShapes = pathNode.childCount();
        for ( unsigned int i = 0; i < numShapes; ++i )
        {
            status = pathNode.push( pathNode.child( i ) );
            CHECK_MSTATUS_AND_RETURN_IT( status );

            if ( pathNode.node().hasFn( MFn::kMesh ) )
            {
                MFnDagNode fnDag( pathNode );
                if ( !fnDag.isIntermediateObject() )
                {
                    geometry.append( MDagPath( pathNode ) );
                }
            }
            pathNode.pop();
        }
    }

    return MS::kSuccess;
}


MStatus CreateJointContext::getMeshIntersection( int x, int y, MPointArray& pointArr )
{
    MStatus status;

    MPoint nearClip;
    MPoint farClip;
    m_view.viewToWorld( x, y, nearClip, farClip );
    MVector rayDirection = (farClip - nearClip).normal();
    MFloatPoint raySource, hitPoint;
    raySource.setCast( nearClip );
    float intersectionDistance = 0.0f;
    MIntArray hitFace, hitTriangle;
    MFloatArray hitBary1, hitBary2;
    bool initialClosestIntersection = true;
    float minIntersectionDistance = 0.0f;

	MFloatPointArray intersectionPoints;
	MFloatArray      intersectionDists;

	m_closeGeoIndex = -1;
	MPoint pointClosest = farClip;
	MPoint pointSecondClosest;

    for ( unsigned int i = 0; i < m_geometry.length(); ++i )
    {
        MFnMesh fnMesh( m_geometry[i], &status );
        CHECK_MSTATUS_AND_RETURN_IT( status );

		if ( fnMesh.allIntersections( raySource,
                rayDirection, NULL, NULL, false, MSpace::kWorld,
                1000.0f, false, NULL, false, intersectionPoints, &intersectionDists,
                &hitFace, &hitTriangle,
                &hitBary1, &hitBary2,
                0.00001f, &status ) )
        {
			bool getClosest = false;
            int closestIndex = 0;
			int secondClostIndex = 0;
			for( unsigned int j=0; j< intersectionPoints.length(); j++ )
			{
				if( nearClip.distanceTo( pointClosest ) > nearClip.distanceTo( intersectionPoints[j] ) )
				{
					pointClosest = intersectionPoints[j];
					m_closeGeoIndex = i;
					getClosest = true;
					closestIndex = j;
				}
			}
			if( getClosest )
			{
				if( intersectionPoints.length() > 1 )
				{
					pointSecondClosest = farClip;
					for( unsigned int j=0; j< intersectionPoints.length(); j++ )
					{
						if( j == closestIndex ) continue;
						if( nearClip.distanceTo( pointSecondClosest ) > nearClip.distanceTo( intersectionPoints[j] ) )
						{
							pointSecondClosest = intersectionPoints[j];
							secondClostIndex = j;
						}
					}
				}
				else
				{
					pointSecondClosest = pointClosest;
				}
				pointArr.setLength( 2 );
				pointArr[0] = pointClosest;
				pointArr[1] = pointSecondClosest;
			}
        }
		else
		{
			intersectionPoints.clear();
		}
    }

    return MS::kSuccess;
}


MPoint CreateJointContext::getCenterPoint( const MPointArray& pointArr )
{
	MVector point( 0,0,0 );
	for( unsigned int i=0; i< pointArr.length(); i++ )
	{
		point += pointArr[i];
	}
	point /= pointArr.length();

	return point;
}


MStatus CreateJointContext::setUpdateCondition( const MSelectionList& beforeList,
	                                            const MSelectionList& afterList,
												const MPoint worldPosition )
{
	MStatus status;

	bool beforeExists = false;

	MDagPath pathBefore, pathAfter;
	MObject  oBefore, oAfter;

	beforeList.getDependNode( 0, oBefore );
	MFnTransform tBefore = oBefore;
	tBefore.getPath( pathBefore );
	if( oBefore.apiType() == MFn::kJoint )
	{
		beforeExists = true;
	}

	afterList.getDependNode( 1, oAfter );
	MFnTransform tAfter = oAfter;
	tAfter.getPath( pathAfter );

	if( beforeExists )
	{
		MMatrix invParent = pathBefore.exclusiveMatrixInverse();
		MMatrix mtxBefore = pathBefore.inclusiveMatrix();
		MMatrix mtxAfter  = pathAfter.inclusiveMatrix();

		MVector aimVector = worldPosition - MVector( mtxBefore[3] );
		MVector upVector( mtxBefore[1] );
		MVector biVector = aimVector ^ upVector;

		double doubleListMtx[4][4] = 
		{ aimVector.x, aimVector.y, aimVector.z, 0,
		  upVector.x,  upVector.y,  upVector.z,  0,
		  biVector.x,  biVector.y,  biVector.z,  0,
		  0,0,0,1 };

		MMatrix mtxEditBefore( doubleListMtx );
		MMatrix mtxEditBeforeLocal = mtxEditBefore * invParent;

		MTransformationMatrix trMtx = mtxEditBeforeLocal;

		tBefore.setRotation( trMtx.eulerRotation() );
		tBefore.addChild( tAfter.object() );

		MMatrix invBefore = pathAfter.exclusiveMatrixInverse();
		tAfter.setTranslation( worldPosition * invBefore, MSpace::kTransform );
	}
	else
	{
		tAfter.setTranslation( worldPosition, MSpace::kTransform );
	}

	return MS::kSuccess;
}