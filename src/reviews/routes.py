from fastapi import APIRouter, Depends, status
from src.db.models import User
from src.reviews.schemas import ReviewCreateSchema, ReviewViewSchema
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.reviews.service import ReviewService
from src.auth.dependencies import get_current_user, RoleChecker
from typing import List
from src.errors import ReviewNotFound

# create the router
review_router = APIRouter()

# create the review service instance
review_service = ReviewService()

# role checker instance
admin_role_checker = RoleChecker(['admin'])
user_role_checker = RoleChecker(['user', 'admin'])

# get all reviews
@review_router.get(
    '/',
    response_model=List[ReviewViewSchema],
    dependencies=[admin_role_checker],
    status_code=status.HTTP_200_OK,
)
async def get_all_reviews(
        session: AsyncSession = Depends(get_session)
) -> List[ReviewViewSchema]:
    reviews = await review_service.get_all_reviews(session=session)

    return reviews

# get a review by id
@review_router.get(
    '/{review_id}',
    response_model=ReviewViewSchema,
    status_code=status.HTTP_200_OK,
)
async def get_review_by_id(
        review_id: str,
        session: AsyncSession = Depends(get_session)
) -> ReviewViewSchema:
    review = await review_service.get_review(review_id=review_id, session=session)

    if not review:
        raise ReviewNotFound()

    return review

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

@review_router.delete(
    '/{review_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[user_role_checker],
)
async def delete_review(
        review_id: str,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session)
) -> None:
    await review_service.delete_review_from_book(
        review_id=review_id,
        user_email=current_user.email,
        session=session
    )

    return None
