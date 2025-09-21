from fastapi import FastAPI
import uvicorn
from lw_orch import lw_orch_router

app = FastAPI()

app.include_router(lw_orch_router.router)

@app.get("/")
def welcome():
    return {"message": "Welcome to the API"}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)