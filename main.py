import os
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from typing import List
import traceback

from visual_data import audio_data
from convert_audio import convert_audio_file

app = FastAPI(title="Audio Codec Testing Platform")

UPLOAD_FOLDER = "converted_files"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def read_index():
    if os.path.exists("templates/webapp.html"):
        with open("templates/webapp.html", "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Audio codec tester</h1><p>Webapp not found</p>"


@app.post("/convert")
async def convert_audio(
    file: UploadFile = File(...),
    codecs: List[str] = Form(default=["mp3", "flac", "ogg", "wav"])
):
    try:
        input_path = os.path.join(UPLOAD_FOLDER, file.filename)

        contents = await file.read()
        with open(input_path, "wb") as f:
            f.write(contents)

        base_name = os.path.splitext(file.filename)[0]

        original_info = audio_data(input_path)
        original_size_kb = round(os.path.getsize(input_path) / 1024, 2)
        original_bitrate = original_info.get('bitrate', '1411')

        download_links = convert_audio_file(
            input_path=input_path,
            output_folder=UPLOAD_FOLDER,
            base_filename=base_name,
            selected_codecs=codecs
        )

        return {
            "original": {
                "name": file.filename,
                "size_kb": original_size_kb,
                "duration": original_info["duration"],
                "sample_rate": original_info["sample_rate"],
                "bitrate": original_bitrate
            },
            "links": download_links
        }

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, filename=filename)
    raise HTTPException(status_code=404, detail="File not found")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)