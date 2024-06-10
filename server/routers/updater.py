from fastapi import APIRouter
import httpx

router = APIRouter()


@router.get("/updater")
async def fetch_updates():
    url = (
        "https://github.com/automators-com/tweaked/releases/latest/download/latest.json"
    )

    async with httpx.AsyncClient(follow_redirects=True) as client:
        response = await client.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Failed to fetch updates"}
