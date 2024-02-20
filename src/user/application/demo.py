import os
import time
from src.user.adapter.rest.request import GeneratedContentRequest


class UserCommandDemo:
    def __init__(self) -> None:
        application_path = os.path.abspath(os.path.join(__file__, os.path.pardir))
        user_path = os.path.abspath(os.path.join(application_path, os.path.pardir))
        domain_path = os.path.abspath(os.path.join(user_path, "domain"))
        self.demo_path = os.path.abspath(os.path.join(domain_path, "demo"))

    async def demo_generate_content(
            self, id: str, requset: GeneratedContentRequest
    ):
        # gif 파일은 바로 전달
        gif_file = os.path.abspath(os.path.join(self.demo_path, "loading.gif"))
        with open(gif_file, "rb") as f:
            content = f.read()
            yield f"gif: {content}\n".encode()
        # 10초 대기 후 완료 메시지 전달
        time.sleep(10)
        yield f"finish: {requset.generated_id}\n".encode()

    def get_demo_text_content():
        # text_content, audio_content
        text_content = "이 그림은 자연주의와 약간의 인상주의 스타일로 그려진 회화로 보입니다. 이 작품은 전통에서 비롯되었지만, 더 현대적이고 편안한 붓질과 순간을 포착하는 데 관심을 가진 점이 특징입니다. 매체는 캔버스 위에 오일 또는 아크릴 페인트로 보이며, 이는 텍스처와 빛이 표면에서 반사하는 방식에서 나타납니다. 스타일은 약간 단순화되어 있으며, 넓은 색상 영역이 하늘, 초목, 나무의 수직 형태를 구분합니다. 영향을 준 요소로는 인상주의의 측면과 조화와 세부 사항에 대한 더 현대적이고 간소화된 접근법이 포함될 수 있습니다."
        pass

    def get_demo_coord_content():
        coord_content = '"나무" : { "좌표"  : [55, 75, 455, 390], "내용" : "스타일은 약간 단순화되어 있으며, 넓은 색상 영역이 하늘, 초목, 나무의 수직 형태를 구분합니다. 그림은 눈길을 위로 끌어올리는 높고 가느다란 포플러 나무들이 지배하는 풍경을 그립니다. 작가는 나무의 수직선과 하늘과 필드의 수평선 사이의 대조를 이용합니다." } '
        pass

    def get_demo_video_content():
        # video demo content 추가(나무 사진으로)
        pass
