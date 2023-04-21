from sqlalchemy import JSON, Column, Integer, String, LargeBinary, Text
from sqlalchemy.orm import relationship
from database.database import Base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import TypeDecorator, LargeBinary
import zlib
class CompressedText(TypeDecorator):
    impl = LargeBinary

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = zlib.compress(value.encode('utf-8'))
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = zlib.decompress(value).decode('utf-8')
        return value


class Workspace(Base):
    __tablename__ = "workspaces"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True)
    tags = Column(JSON,nullable=True)
    mapUrl = Column(Text)
    objects = relationship("Object", back_populates="workspace", cascade='save-update')
    
