import os
import grpc
from src.user.adapter.grpc import stream_pb2, stream_pb2_grpc
from src.user.domain.entity import GeneratedIdInfo, GeneratedContent
from src.user.domain.util.local_file import find_storage_path


class GeneratedContentService:
    async def create_generated_content(
            self, user_id_info: GeneratedIdInfo
    ) -> any:
        # load image from local
        origin_file = self.__find_user_origin_image(user_id_info.generated_id)

        # create generate content
        # gif, text content, coord content, tts
        options = [('grpc.max_receive_message_length', 50 * 1024 * 1024)]
        with grpc.insecure_channel('localhost:50051', options=options) as channel:
            stub = stream_pb2_grpc.StreamServiceStub(channel)
            with open(origin_file, "rb") as f:
                request = stream_pb2.Request(
                    image=f.read(),
                    id=user_id_info.generated_id
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

    async def save_audio_content_to_local(
            self, user_id_info: GeneratedIdInfo,
            audio_content: GeneratedContent
    ):
        user_path = os.path.abspath(os.path.join(
             find_storage_path(),
             user_id_info.generated_id
            ))
        audio_file = os.path.abspath(os.path.join(user_path, "main.mp3"))
        with open(audio_file, "wb") as f:
            f.write(audio_content.content)

    @staticmethod
    def __find_user_origin_image(generated_id: str) -> str:
        storage_path = find_storage_path()
        user_path = os.path.abspath(os.path.join(storage_path, generated_id))
        origin_file = os.path.abspath(os.path.join(user_path, "origin_img.jpg"))
        return origin_file
