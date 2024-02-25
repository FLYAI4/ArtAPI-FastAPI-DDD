from src.shared_kernel.infra.database.model import Base
from sqlalchemy import Column, Integer, String, BINARY


class Content(Base):
    __tablename__ = 'generated_content'

    seq = Column(Integer, primary_key=True)
    image_name = Column(String(500), nullable=False, unique=True)
    origin_image = Column(BINARY, nullable=False)
    audio_content = Column(BINARY, nullable=False)
    video_content = Column(BINARY, nullable=False)
