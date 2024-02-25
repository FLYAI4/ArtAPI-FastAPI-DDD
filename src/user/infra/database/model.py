from src.shared_kernel.infra.database.model import Base
from sqlalchemy import Column, Integer, String, Boolean


class Review(Base):
    __tablename__ = 'user_content_review'

    seq = Column(Integer, primary_key=True)
    id = Column(String(500), nullable=False)
    image_name = Column(String(500), nullable=False)
    like_status = Column(Boolean, nullable=False, default=False)
    review_content = Column(String(500), nullable=False)
