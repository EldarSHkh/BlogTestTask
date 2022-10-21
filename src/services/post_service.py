from src.database.repositories.post_repository import PostRepository
from src.api.dto import PostDTO
from src.helpers.comment_processor import remove_duplicates_comments


class PostNotFound(Exception):
    pass


class PostService:
    def __init__(self, post_repository: PostRepository) -> None:
        self.post_repository = post_repository

    async def create_post(self, *, author_id: int, title: str, text: str) -> PostDTO:
        post = await self.post_repository.add_post(
            author_id=author_id, title=title, text=text
        )
        return PostDTO.from_orm(post)

    async def get_post_by_id(self, *, post_id: int) -> PostDTO:
        post = await self.post_repository.get_post_by_id(post_id=post_id)
        if post:
            post = PostDTO.from_orm(post)
            comments = remove_duplicates_comments(post.comments)
            post.comments = comments
            return post
        raise PostNotFound

    async def delete_post(self, *, author_id: int, post_id: int) -> None:
        if not await self.post_repository.delete_post(
            post_id=post_id, author_id=author_id
        ):
            raise PostNotFound

    async def update_post(
        self, *, author_id: int, post_id: int, update_data: dict
    ) -> PostDTO:
        post = await self.post_repository.update_post(
            post_id=post_id, author_id=author_id, update_data=update_data
        )
        if post:
            return PostDTO.from_orm(post[0])
        raise PostNotFound
