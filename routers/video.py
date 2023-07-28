from fastapi import APIRouter, Response




router = APIRouter(tags=["Video"], prefix="/video")



@router.route('/feed')
def video_feed():
    return Response((), media_type='multipart/x-mixed-replace; boundary=frame')