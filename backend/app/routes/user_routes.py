from fastapi import APIRouter, HTTPException, Query
from app.core.database import user_collection

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/profile")
async def get_user_profile(email: str = Query(...)):
    user = await user_collection.find_one({"email": email})

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Remove sensitive fields
    user["_id"] = str(user["_id"])
    user.pop("hashed_password", None)

    return user
