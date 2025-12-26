from pydantic import BaseModel
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING

from app.database.base import Base, int_pk
from .article import Article
if TYPE_CHECKING:
    from .article import ArticleOrm
    from .user import UserOrm


class UserArticle(BaseModel):
    id: int
    article: Article
    weight: int


class UserArticleOrm(Base):
    __tablename__ = "user_articles"

    id: Mapped[int_pk]    
    weight: Mapped[int]

    article_id: Mapped[int] = mapped_column(ForeignKey("main_dictionary.id"))
    article: Mapped["ArticleOrm"] = relationship(back_populates="user_article_list")

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["UserOrm"] = relationship(back_populates="user_article_list")


'''
-- MS SQL Server
CREATE TABLE user_articles(
	id INT IDENTITY(1,1) PRIMARY KEY,
	article_id INT NOT NULL,
	user_id INT NOT NULL,
	[weight] INT NOT NULL,
	CONSTRAINT FK_user_articles_article
        FOREIGN KEY (article_id) REFERENCES main_dictionary(id),
	CONSTRAINT FK_user_articles_user
        FOREIGN KEY (user_id) REFERENCES users(id)
);

INSERT INTO user_articles(article_id, user_id, [weight]) VALUES
(1, 1, 10),
(2, 1, 20),
(3, 1, 30),
(1, 2, 15),
(2, 2, 25),
(3, 2, 35);
'''
