from src.database.repositories.post_repository import PostRepository
from src.api.dto import PostDTO


class PostNotFound(Exception):
    pass


class PostService:
    def __init__(self, post_repository: PostRepository) -> None:
        self.user_repository = post_repository

    async def create_post(self, *, author_id: int, title: str, text: str) -> PostDTO:
        post = await self.user_repository.add_post(author_id=author_id, title=title, text=text)
        return PostDTO.from_orm(post)

    async def get_post_by_id(self, *, post_id: int) -> PostDTO:
        post = await self.user_repository.get_post_by_id(post_id=post_id)
        return PostDTO.from_orm(post)

    async def delete_post(self, *, author_id: int, post_id: int) -> None:
        if not await self.user_repository.delete_post(post_id=post_id, author_id=author_id):
            raise PostNotFound

    async def update_post(self, *, author_id: int, post_id: int, update_data: dict) -> PostDTO:
        post = await self.user_repository.update_post(post_id=post_id, author_id=author_id, update_data=update_data)
        if post:
            return PostDTO.from_orm(post[0])
        raise PostNotFound
