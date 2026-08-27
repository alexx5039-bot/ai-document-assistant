from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile



class FileService:
    UPLOAD_DIR = Path("uploads/documents")

    async def save(self, file: UploadFile) -> str:
        self.UPLOAD_DIR.mkdir(
            parents=True,
            exist_ok=True
        )
        extension = Path(file.filename).suffix
        filename = f"{uuid4()}{extension}"
        file_path = self.UPLOAD_DIR / filename
        content = await file.read()
        file_path.write_bytes(content)

        return str(file_path)