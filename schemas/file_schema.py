from schemas import ma
from models.file import File

class FileSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = File

file_schema = FileSchema()
files_schema = FileSchema(many=True)
