import openslide
import numpy as np
import cv2
import os
import uuid
from storage import MediaStorage


class MediaStorageSplit(MediaStorage):
    async def split_media(self, media_id: str, chunk_size: int = 1000) -> list[str]:
        media_info = self.get_media_info(media_id)
        if media_info is None:
            raise ValueError(f"Media {media_id} not found")

        if not media_info["original_name"].lower().endswith(".svs"):
            raise ValueError(f"Media {media_id} is not an svs")

        media_path = media_info["path"]
        slide = openslide.open_slide(media_path)
        width, height = slide.level_dimensions[0]

        chunks = []
        for y in range(0, height, chunk_size):
            for x in range(0, width, chunk_size):
                region_width = min(chunk_size, width - x)
                region_height = min(chunk_size, height - y)
                region = slide.read_region((x, y), 0, (region_width, region_height))
                region_np = np.array(region)[:, :, :3]  # Exclude alpha channel
                region_bgr = cv2.cvtColor(region_np, cv2.COLOR_RGBA2BGR)
                chunk_filename = f"{uuid.uuid4()}.png"
                chunk_path = os.path.join(self.base_path, media_path["filename"][:-4], chunk_filename)
                cv2.imwrite(chunk_path, region_bgr)

                # Store metadata
                media_info = {
                    "filename": chunk_filename,
                    "original_name": f"{chunk_filename}_{y}_{x}.jpeg" ,
                    "content_type": "image/jpeg",
                    "path": chunk_path,
                    "size": os.path.getsize(chunk_path)
                }
                media_id = chunk_filename
                self.media_registry[media_id] = media_info
                self.save_media_registry()

                chunks.append(chunk_filename)


        return chunks