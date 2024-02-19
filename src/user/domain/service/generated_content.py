import os
import grpc
from src.user.adapter.grpc import stream_pb2, stream_pb2_grpc
from src.user.domain.entity import GeneratedIdInfo
from src.user.domain.util.local_file import find_storage_path


class GeneratedContentService:
    def create_generated_content(self, user_id_info: GeneratedIdInfo):
        # load image from local
        origin_file = self.__find_user_origin_image(user_id_info.generated_id)

        # create generate content
        # gif, text content, coord content
        text_content, coord_content = self.__request_create_content_grpc(
            user_id_info.generated_id, origin_file
        )
        return text_content, coord_content

        # save mongodb -> text, coord DB 저장

        # save posgreSQL

    @staticmethod
    def __find_user_origin_image(generated_id: str) -> str:
        storage_path = find_storage_path()
        user_path = os.path.abspath(os.path.join(storage_path, generated_id))
        origin_file = os.path.abspath(os.path.join(user_path, "origin_img.jpg"))
        return origin_file

    @staticmethod
    def __request_create_content_grpc(generated_id: str, origin_file: str):
        options = [('grpc.max_receive_message_length', 10 * 1024 * 1024)]
        with grpc.insecure_channel('localhost:50051', options=options) as channel:
            stub = stream_pb2_grpc.StreamServiceStub(channel)
            with open(origin_file, "rb") as f:
                request = stream_pb2.Request(
                    image=f.read(),
                    id=generated_id
                )
            responses = stub.GeneratedContentStream(request)
            flag = False
            for response in responses:
                if response.tag == "content":
                    text_content = response.data
                if response.tag == "coord":
                    coord_content = response.data
                if response.tag == "finish":
                    flag = True
                    break
            if flag:
                channel.close()
                # yield f"{response.tag}: {response.data}\n".encode()
        return text_content, coord_content
