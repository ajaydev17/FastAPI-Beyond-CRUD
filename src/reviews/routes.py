from fastapi import APIRouter, Depends, status
from src.db.models import User
from src.reviews.schemas import ReviewCreateSchema, ReviewViewSchema
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.reviews.service import ReviewService
from src.auth.dependencies import get_current_user

# create the router
review_router = APIRouter()

# create the review service instance
review_service = ReviewService()

# creating a book review
@review_router.post(
    '/book/{book_uid}',
    response_model=ReviewViewSchema,
    status_code=status.HTTP_201_CREATED,
)
async def add_book_review(
        book_uid: str,
        review_data: ReviewCreateSchema,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session)
) -> ReviewViewSchema:
    review = await review_service.add_review_to_book(
        user_email=current_user.email,
        book_uid=book_uid,
        review_data=review_data,
        session=session
    )

    return review
