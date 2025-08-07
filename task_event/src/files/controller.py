# src/files/controller.py

from fastapi import APIRouter, UploadFile, File, Request, HTTPException, status
import shutil  # Dosya işlemleri için
import os

router = APIRouter()

# Yüklenen dosyaların kaydedileceği klasör
UPLOAD_DIRECTORY = "static/uploads"


@router.post("/upload")
async def upload_file(request: Request, file: UploadFile = File(...)):
    # Klasörün var olduğundan emin ol
    os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

    file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)

    # Dosyayı diske kaydet
    try:
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Dosya kaydedilemedi: {e}")

    # Dosyanın erişilebilir URL'ini oluştur
    # request.base_url -> http://127.0.0.1:8005/
    file_url = f"{request.base_url}{file_location.replace(os.path.sep, '/')}"

    return {"filename": file.filename, "url": file_url}