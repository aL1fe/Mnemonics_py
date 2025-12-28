from sqlalchemy.ext.asyncio import AsyncSession
import random
from typing import Optional

from app.models.user import User
from app.models.article import Article
from app.models.user_article import UserArticle, UserArticle
from app.repositories.user_article_repo import UserArticleRepo


class UserArticleService:
    DEFAULT_WEIGHT = 10

    def __init__(self, user_article_repo: UserArticleRepo):
        self.user_article_repo = user_article_repo


    async def init_user_vocabulary(self, db: AsyncSession, user: User, article_list: list[Article]) -> None:
        '''
        Initializes the user's vocabulary with a given list of articles.  
        For each article, a "UserArticle" instance is created with a default weight,  
        and all instances are saved to the database in bulk.  
        This sets up the initial state of the user's learning progress for the articles.
        '''
        user_articles = [
            UserArticle(
                id = -1,  # Will be reassigned
                article=article,
                weight=self.DEFAULT_WEIGHT
            )
            for article in article_list
        ]
        await self.user_article_repo.bulk_create(db, user, user_articles)
           

    async def get_next_article(self, db: AsyncSession, user_id: int, last_article: Optional[Article]) -> Article:
        '''
        Returns a randomly selected article for the given user using weighted probability.
        Each article is selected proportionally to its weight, meaning articles with higher
        weight have a higher chance of being returned.
        The method retrieves the user's vocabulary from the database and performs a weighted random selection.
        '''
        user_vocabulary_orm = await self.user_article_repo.get_vocabulary(db, user_id)
        user_vocabulary = [UserArticle.model_validate(row, from_attributes=True) for row in user_vocabulary_orm]
        if last_article:
        # Exclude last article
            user_vocabulary = [user_article for user_article in user_vocabulary if user_article.article.id != last_article.id]
        total_weight = sum(user_article.weight for user_article in user_vocabulary)
        target_weight = random.randint(1, total_weight)
        # Random selection algorithm using weighted probability
        current_weight = 0
        for user_article in user_vocabulary:
            current_weight += user_article.weight
            if current_weight >= target_weight:
                return user_article.article
        raise RuntimeError("Failed to select article by weight")  # Fallback for static analyzers; logically unreachable
    

    async def update_weight(self, db: AsyncSession, user_id: int, artilce_id: int, delta: int):
        '''
        Updates the weight of a specific user-article relationship.
        The method applies the given delta value to the current weight of the article
        associated with the user, allowing the weight to be increased or decreased
        based on user learning progress.
        '''
        user_article = await self.user_article_repo.get(db, user_id, artilce_id)
        if user_article:
            weight = user_article.weight + delta
            weight = max(weight, 1)
            await self.user_article_repo.update_weight(db, user_article, weight)
