import pytest
from datetime import datetime, timezone
from src.api.dto import CommentDTO
from src.helpers.comment_processor import remove_duplicates_comments



def test_comment_processor() -> None:
    comment_3 = CommentDTO(
        id=3,
        post_id=1,
        author_id=2,
        parent_id=None,
        text="qwerty",
        created_at=datetime.now(tz=timezone.utc)
    )
    comment_2 = CommentDTO(
        id=2,
        post_id=1,
        author_id=2,
        parent_id=1,
        text="qwerty",
        created_at=datetime.now(tz=timezone.utc)
    )
    comment_1 = CommentDTO(
        id=1,
        post_id=1,
        author_id=1,
        parent_id=None,
        text="qwerty",
        replies=[comment_2],
        created_at=datetime.now(tz=timezone.utc)
    )

    raw_comments = [comment_1, comment_2, comment_3]
    expected_result = [comment_1, comment_3]
    assert raw_comments != expected_result
    result_comments = remove_duplicates_comments(raw_comments)
    assert result_comments == expected_result



