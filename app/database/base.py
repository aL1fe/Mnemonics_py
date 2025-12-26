from sqlalchemy.orm import DeclarativeBase, mapped_column
from typing_extensions import Annotated
import sqlalchemy as sa


int_pk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]

str_128 = Annotated[str, 128]
class Base(DeclarativeBase):
    type_annotation_map = {
        str_128: sa.String(128)
    }
