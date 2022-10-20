from fastapi import Request, HTTPException, status


def check_is_owner(owner_id: int, request: Request) -> None:
    if request.state.user.user_id != owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        