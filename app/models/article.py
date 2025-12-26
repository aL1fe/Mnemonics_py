from pydantic import BaseModel
from sqlalchemy import String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING, List

from app.database.base import Base, int_pk
if TYPE_CHECKING:
    from .user_article import UserArticleOrm
    from .user import UserOrm


class Article(BaseModel):
    id: int
    eng_word: str
    ukr_word: str


class ArticleOrm(Base):
    __tablename__ = "main_dictionary"

    id: Mapped[int_pk]
    eng_word: Mapped[str] = mapped_column(String(100))
    ukr_word: Mapped[str] = mapped_column(String(100))

    user_article_list: Mapped[List["UserArticleOrm"]] = relationship(back_populates="article")
    user_last_article_list: Mapped[List["UserOrm"]] = relationship(back_populates="last_article")


'''
-- MS SQL Server
CREATE TABLE main_dictionary(
	id INT IDENTITY(1,1) PRIMARY KEY,
	eng_word NVARCHAR(100) NOT NULL,
	ukr_word NVARCHAR(100) NOT NULL
);

INSERT INTO main_dictionary(eng_word, ukr_word) VALUES
('cat', N'кіт'), ('dog', N'собака'), ('mouse', N'миша');
'''
    