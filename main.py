import aiofiles
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from storage import MediaStorage
from MediaSplit import MediaStorageSplit


app = FastAPI(title="Media Storage Microservice")
media_storage = MediaStorageSplit()


@app.post("/upload")
async def upload_media(file: UploadFile = File(...)):
    """
    Endpoint to upload media content (photo, video, music)
    Returns media ID and metadata
    """
    media_id, media_info = await media_storage.save_media(file, file.content_type)
    return {
        "media_id": media_id,
        "metadata": media_info
    }

@app.post("/split/{media_id}")
async def split_media(media_id: str, chunk_size: int = 1000) -> list[str]:
    """
    Endpoint to split media into chunks
    """

    chunks = await media_storage.split_media(media_id, chunk_size)
    return chunks

@app.get("/media/{media_id}")
async def get_media(media_id: str):
    """
    Endpoint to retrieve media file or metadata
    """
    media_info = media_storage.get_media_info(media_id)
    if not media_info:
        raise HTTPException(status_code=404, detail="Media not found")

    return FileResponse(media_info['path'], 
    media_type=media_info['content_type'], 
    filename=media_info['original_name'])

@app.delete("/media/{media_id}")
async def delete_media(media_id: str):
    """
    Endpoint to delete media by ID
    """
    success = media_storage.delete_media(media_id)
    if not success:
        raise HTTPException(status_code=404, detail="Media not found")

    return JSONResponse(content={"message": "Media deleted successfully"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8001)