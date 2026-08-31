from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile, HTTPException, status

from app.core.config import settings


class FileService:
    UPLOAD_DIR = Path("uploads/documents")

    async def save(self, file: UploadFile) -> str:
        self.UPLOAD_DIR.mkdir(
            parents=True,
            exist_ok=True
        )
        extension = Path(file.filename).suffix

        if extension not in settings.allowed_file_extensions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported file type: {extension}",
            )

        filename = f"{uuid4()}{extension}"
        file_path = self.UPLOAD_DIR / filename

        size = 0

        with file_path.open("wb") as buffer:
            while chunk := await file.read(1024 * 1024):
                size += len(chunk)

                if size > settings.max_file_size:
                    file_path.unlink(missing_ok=True)

                    raise HTTPException(
                        status_code=status.HTTP_413_CONTENT_TOO_LARGE,
                        detail="File is too large"
                    )
                buffer.write(chunk)

        return str(file_path)

