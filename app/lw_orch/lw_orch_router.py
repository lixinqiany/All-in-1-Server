from fastapi import APIRouter

router = APIRouter(
    prefix="/api/v1/orchestrator",
    tags=["lw_orch"]
)

@router.get("/")
def welcome2lw_orch():
    return {"status": "success",
            "message": "Welcome to the LightWAN Orch API"}