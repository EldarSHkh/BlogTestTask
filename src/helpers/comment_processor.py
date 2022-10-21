from src.api.dto import CommentDTO


def remove_duplicates_comments(comments: list[CommentDTO]) -> list[CommentDTO]:
    unique_comments = []
    for comment in comments:
        if comment.parent_id is None:
            unique_comments.append(comment)
    return unique_comments
