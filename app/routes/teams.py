from fastapi import APIRouter
from app.services.teams_utils import create_teams_meeting

router = APIRouter()

@router.post("/create-teams-meeting")
def create_meeting():
    join_url = create_teams_meeting()
    if join_url:
        return {"join_url": join_url}
    else:
        return {"error": "Failed to create meeting"}
