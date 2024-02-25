import os
import io
import grpc
from src.admin.domain.util import find_storage_path
from src.user.adapter.grpc import stream_pb2, stream_pb2_grpc
from src.admin.domain.entity import OriginImageInfo
from src.admin.domain.exception import AdminServiceError
from src.admin.domain.errorcode import GeneratedContentsError
from PIL import Image


class GeneratedContentService:
    def __init__(self) -> None:
        self.width = 510
        self.height = 680
        self.threshold = 0.7

    async def generated_content(
            self,
            origin_image_info: OriginImageInfo
    ) -> any:
        # file path
        storage_path = find_storage_path()
        resize_image = os.path.abspath(os.path.join(storage_path, origin_image_info.image_name))
        if os.path.exists(resize_image):
            raise AdminServiceError(**GeneratedContentsError.AlreadyExistenceImage.value)

        # resize image
        self.__resize_image(
            origin_image_info.image_file,
            resize_image,
            self.width, self.height
        )

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

    @staticmethod
    def __resize_image(
        image_bytes: bytes,
        user_file: str,
        width: int, height: int
    ):
        image = Image.open(io.BytesIO(image_bytes))
        image = image.convert("RGB")
        resized_image = image.resize((width, height))
        resized_image.save(user_file)
