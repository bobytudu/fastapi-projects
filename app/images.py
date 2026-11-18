from dotenv import load_dotenv
from imagekitio import ImageKit
import os

load_dotenv()

imagekit = ImageKit(
    private_key=os.getenv("IMAGEKIT_PRIVATE_KEY"),
)
 
def upload_image(content, filename):
    try:
        result = imagekit.files.upload(
            file=content,
            file_name=filename,
            folder="/posts"
        )
        return result.url
    except Exception as e:
        print(f"Error uploading image: {e}")
        return None