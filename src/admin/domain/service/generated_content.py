import os
import io
import grpc
import time
from src.admin.domain.util import find_storage_path
from src.user.adapter.grpc import stream_pb2, stream_pb2_grpc
from src.admin.domain.entity import OriginImageInfo
from src.admin.domain.exception import AdminServiceError
from src.admin.domain.errorcode import GeneratedContentsError
from PIL import Image


class GeneratedContentService:
    _IMAGE_WIDTH: int = 510
    _IMAGE_HEIGHT: int = 680

    async def generated_content(
            self,
            origin_image_info: OriginImageInfo
    ) -> any:
        # file path
        storage_path = find_storage_path()
        resize_image = os.path.abspath(os.path.join(storage_path, origin_image_info.image_name))

        # created generated content
        # gif, text content, coord content, tts
        options = [('grpc.max_receive_message_length', 50 * 1024 * 1024)]
        with grpc.insecure_channel('localhost:50051', options=options) as channel:
            stub = stream_pb2_grpc.StreamServiceStub(channel)
            with open(resize_image, "rb") as f:
                request = stream_pb2.Request(
                    image=f.read(),
                    id=origin_image_info.image_name
                )
            responses = stub.GeneratedContentStream(request)
            flag = False
            for response in responses:
                if response.tag == "finish":
                    flag = True
                    time.sleep(1)
                    break
                yield response
            if flag:
                channel.close()

    async def delete_resize_image(
            self,
            origin_image_info: OriginImageInfo
    ) -> OriginImageInfo:
        # delete file
        storage_path = find_storage_path()
        resize_image = os.path.abspath(os.path.join(storage_path, origin_image_info.image_name))
        if os.path.exists(resize_image):
            os.remove(resize_image)
        return origin_image_info

    def resize_image(
        self,
        origin_image_info: OriginImageInfo,
    ):
        # file path
        storage_path = find_storage_path()
        resize_image = os.path.abspath(os.path.join(storage_path, origin_image_info.image_name))

        if os.path.exists(resize_image):
            raise AdminServiceError(**GeneratedContentsError.AlreadyExistenceImage.value)

        image = Image.open(io.BytesIO(origin_image_info.image_file))
        image = image.convert("RGB")
        resized_image = image.resize(
            (GeneratedContentService._IMAGE_WIDTH, GeneratedContentService._IMAGE_HEIGHT))
        resized_image.save(resize_image)

        return resize_image
