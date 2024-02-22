import os
import io
import json
import torch
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import torchvision.transforms as transforms
from datetime import datetime
from PIL import Image
from src.user.domain.exception import UserServiceError
from src.user.domain.errorcode import InsertImageError
from src.user.domain.entity import OriginImageInfo, FileInfo
from src.user.domain.util.local_file import (
    find_storage_path,
    create_folder_if_not_exists
    )


class InsertImageService:
    def __init__(self) -> None:
        self.width = 510
        self.height = 680
        self.threshold = 0.65

    def insert_image(self, origin_image: OriginImageInfo) -> FileInfo:
        # set unique id
        user_unique_id = self.__generated_uniqnue_id(origin_image.id)
        origin_image.id = user_unique_id

        # make unique id folder
        storage_path = find_storage_path()
        user_path = os.path.abspath(os.path.join(
            storage_path, origin_image.id
            ))
        create_folder_if_not_exists(user_path)

        # save file
        user_file = os.path.abspath(os.path.join(
            user_path, "origin_img.jpg"
            ))

        # resize image(510px * 680px)
        self.__resize_image(
            origin_image.image_file,
            user_file,
            self.width, self.height
        )

        # retrieval image
        similarity_image = self.__retrieval_image(user_file)
        if not similarity_image:
            raise UserServiceError(**InsertImageError.NonRetrievalImage.value)

        return FileInfo(unique_id=user_unique_id, path=user_file)

    @staticmethod
    def __generated_uniqnue_id(user_id: str):
        """Generate unique id according to API request."""
        id_prefix = user_id.split("@")[0]
        current_time = datetime.now()
        timestamp = current_time.strftime("%Y%m%d_%H%M%S")
        return f"{timestamp}_{id_prefix}"

    @staticmethod
    def __resize_image(
        image_bytes: bytes,
        user_file: str,
        width: int, height: int
    ):
        image = Image.open(io.BytesIO(image_bytes))
        resized_image = image.resize((width, height))
        resized_image.save(user_file)

    def __retrieval_image(
        self,
        user_file: str
    ):
        # load model and image
        model = self.__load_model()
        user_image_vector = self.__vectorize_image(user_file, model)
        similarities = self.__compute_similarity(user_image_vector)

        # Return exception if lower than threshold
        max_similarity = max(similarities.values())[0][0]
        if max_similarity < self.threshold:
            return ""
        return max(similarities, key=similarities.get)

    def __load_model(self):
        torch_path = self.__find_torch_path()
        model_file = os.path.abspath(os.path.join(
            torch_path, "resnet50_model.pth"))
        model = torch.load(model_file)
        return model

    def __vectorize_image(self, user_file: str, model: any):
        user_file_batch = self.__preprocess_image(user_file)
        model.eval()
        with torch.no_grad():
            feature_vector = model(user_file_batch)
        return feature_vector.squeeze()

    def __compute_similarity(self, user_image_vector: any):
        db_image_features = self.__load_vectorized_db_images()
        input_feature = user_image_vector.cpu().numpy()
        similarities = dict()

        for img_name, vec in db_image_features.items():
            feature = np.array(vec)
            similarity = cosine_similarity(input_feature.reshape(1, -1),
                                           feature.reshape(1, -1))
            similarities[img_name] = similarity
        return similarities

    def __load_vectorized_db_images(self):
        torch_path = self.__find_torch_path()
        json_file = os.path.abspath(os.path.join(
            torch_path, "image_dict.json"))
        with open(json_file, "r") as f:
            vectorized_db_images = json.load(f)
        return vectorized_db_images

    @staticmethod
    def __preprocess_image(user_file: str):
        if os.path.exists(user_file):
            image = Image.open(user_file)
            preprocess = transforms.Compose([
                transforms.Resize((512, 512)),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406],
                    std=[0.229, 0.224, 0.225])]
                    )
            image_rgb = image.convert("RGB")
            image_tensor = preprocess(image_rgb)
            return image_tensor.unsqueeze(0)

    @staticmethod
    def __find_torch_path():
        service_path = os.path.abspath(os.path.join(__file__, os.path.pardir))
        domain_path = os.path.abspath(os.path.join(
            service_path, os.path.pardir))
        user_path = os.path.abspath(os.path.join(domain_path, os.path.pardir))
        infra_path = os.path.abspath(os.path.join(user_path, "infra"))
        torch_path = os.path.abspath(os.path.join(infra_path, "torch"))
        return torch_path
