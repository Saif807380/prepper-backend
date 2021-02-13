from fastapi import HTTPException, status

plan_already_exists_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Plan already exists",
)
