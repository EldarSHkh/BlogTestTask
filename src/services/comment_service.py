from src.database.repositories.comment_repository import CommentRepository
from src.api.dto import CommentDTO


class CommentNotFound(Exception):
    pass


class CommentService:
    def __init__(self, comment_repository: CommentRepository) -> None:
        self.comment_repository = comment_repository

    async def create_comment(self, *, author_id: int, post_id: int, text: str, parent_id: int = None) -> CommentDTO:
        comment = await self.comment_repository.add_comment(
            author_id=author_id,
            post_id=post_id,
            text=text,
            parent_id=parent_id
        )
        return CommentDTO.from_orm(comment)

    async def get_comment(self, *, comment_id: int) -> CommentDTO:
        comment = await self.comment_repository.get_comment(comment_id=comment_id)
        if comment:
            return CommentDTO.from_orm(comment)
        raise CommentNotFound

    async def delete_comment(self, *, author_id: int, comment_id: int) -> None:
        if not await self.comment_repository.delete_comment(comment_id=comment_id, author_id=author_id):
            raise CommentNotFound

    async def update_comment(self, *, author_id: int, comment_id: int, update_data: dict) -> CommentDTO:
        comment = await self.comment_repository.update_comment(
            comment_id=comment_id, author_id=author_id, update_data=update_data
        )
        if comment:
            return CommentDTO.from_orm(comment[0])
        raise CommentNotFound
