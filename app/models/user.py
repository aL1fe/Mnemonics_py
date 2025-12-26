from pydantic import BaseModel
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING, Optional, List

from app.database.base import Base, int_pk
from .user_article import UserArticle
from .article import Article
if TYPE_CHECKING:
    from .user_article import UserArticleOrm
    from .article import ArticleOrm


class User(BaseModel):
    id: int
    telegram_user_id: int
    telegram_user_name: Optional[str]
    telegram_first_name: Optional[str]
    telegram_last_name: Optional[str]
    is_sync: bool = True
    last_article: Optional[Article]
    user_article_list: list[UserArticle]


class UserOrm(Base):
    __tablename__ = "users"

    id: Mapped[int_pk]    
    telegram_user_id: Mapped[int] = mapped_column(unique=True)
    telegram_user_name: Mapped[Optional[str]] = mapped_column(String(100))
    telegram_first_name: Mapped[Optional[str]] = mapped_column(String(100))
    telegram_last_name: Mapped[Optional[str]] = mapped_column(String(100))
    is_sync: Mapped[bool] = mapped_column(default=True)

    last_article_id: Mapped[Optional[int]] = mapped_column(ForeignKey("main_dictionary.id"), nullable=True)
    last_article: Mapped[Optional["ArticleOrm"]] = relationship(back_populates="user_last_article_list")

    user_article_list: Mapped[List["UserArticleOrm"]] = relationship(back_populates="user")
    

'''
-- MS SQL Server
CREATE TABLE users(
	id INT IDENTITY(1,1) PRIMARY KEY,
	telegram_user_id INT NOT NULL,
	telegram_user_name NVARCHAR(100) NULL,
	telegram_first_name NVARCHAR(100) NULL,
	telegram_last_name NVARCHAR(100) NULL,
	is_sync BIT NOT NULL DEFAULT 1,
	last_article_id INT NULL,	
	CONSTRAINT uq_telegram_user_id UNIQUE (telegram_user_id),
	CONSTRAINT FK_users_article
        FOREIGN KEY (last_article_id) REFERENCES main_dictionary(id)
);

INSERT INTO users (
    telegram_user_id,
    telegram_user_name,
    telegram_first_name,
    telegram_last_name,
    is_sync,
    last_article_id
) VALUES
(123456789, N'ivan_telegram', N'Иван', N'Иванов', 1, 1),
(987654321, N'maria_telegram', N'Мария', N'Петрова', 1, 3);
'''
