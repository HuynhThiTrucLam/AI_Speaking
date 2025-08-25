import os
from typing import Optional

import cloudinary
import cloudinary.uploader


class CloudinaryUploader:
    def __init__(self,
                 cloud_name: Optional[str] = None,
                 api_key: Optional[str] = None,
                 api_secret: Optional[str] = None):
        cloudinary.config(
            cloud_name=cloud_name or os.getenv('CLOUDINARY_CLOUD_NAME'),
            api_key=api_key or os.getenv('CLOUDINARY_API_KEY'),
            api_secret=api_secret or os.getenv('CLOUDINARY_API_SECRET')
        )

    def upload_file(self, file_path: str, folder: str = "AISpeaker", resource_type: str = "video") -> str:
        """
        Upload an audio file. Cloudinary treats many audio formats under resource_type "video".
        Returns the public URL.
        """
        result = cloudinary.uploader.upload(
            file_path,
            folder=folder,
            resource_type=resource_type
        )
        return result.get('secure_url') or result.get('url')


