# src/comments/controller.py

from fastapi import APIRouter, Depends, status, Request

# --- Proje İçi Gerekli Modüller ---
from . import models as comment_models
from . import service as comment_service
from src.auth.service import get_current_user_dependency
from src.entities.user import User as UserEntity
from src.rate_limiter import limiter, get_token_user

router = APIRouter()


@router.post(
    "",
    response_model=comment_models.CommentResponse,
    status_code=status.HTTP_201_CREATED
)
@limiter.limit("100/hour", key_func=get_token_user)
async def create_new_comment_for_event(
        event_id: int,
        comment: comment_models.CommentCreate,
        request: Request,
        current_user: UserEntity = Depends(get_current_user_dependency)
):
    """
    Belirli bir etkinliğe yeni bir yorum ekler.
    Yorum metni zorunludur, emoji ve dosya ekleri opsiyoneldir.
    """
    created_comment_doc = await comment_service.create_comment(
        event_id=event_id,
        comment_data=comment,  # Artık comment nesnesinin tamamını gönderiyoruz
        author=current_user
    )

    return created_comment_doc