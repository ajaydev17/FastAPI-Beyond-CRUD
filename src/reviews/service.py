from src.db.models import Review
from src.auth.service import UserService
from src.books.service import BookService
from sqlmodel.ext.asyncio.session import AsyncSession
from src.reviews.schemas import ReviewCreateSchema, ReviewViewSchema
from fastapi.exceptions import HTTPException
from fastapi import status
from src.errors import UserNotFound, BookNotFound
from sqlmodel import select, desc
from typing import List

# create a service to manage books and users
user_service = UserService()
book_service = BookService()


class ReviewService:

    async def add_review_to_book(
            self,
            user_email: str,
            book_uid: str,
            review_data: ReviewCreateSchema,
            session: AsyncSession,
    ) -> dict:
        try:
            book = await book_service.get_book(
                book_uid=book_uid,
                session=session
            )

            if not book:
                raise BookNotFound()

            user = await user_service.get_user_by_email(
                email=user_email,
                session=session
            )

            if not user:
                raise UserNotFound()

            review_dict = review_data.model_dump()
            review = Review(
                **review_dict
            )

            review.user = user
            review.book = book

            session.add(review)
            await session.commit()

            return review
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to add review to book: {str(e)}"
            )

    async def get_review(
            self,
            review_id: int,
            session: AsyncSession
    ) -> ReviewViewSchema:
        statement = select(Review).order_by(desc(Review.created_at))
        reviews = await session.exec(statement)
        return reviews.first()

    async def get_all_reviews(
            self,
            session: AsyncSession
    ) -> List[ReviewViewSchema]:
        statement = select(Review).order_by(desc(Review.created_at))
        reviews = await session.exec(statement)
        return reviews.all()

    async def delete_review_from_book(
            self,
            review_id: str,
            user_email: str,
            session: AsyncSession
    ) -> None:
        user = await user_service.get_user_by_email(user_email, session)

        review = self.get_review(review_id, session)

        if not review or review.user != user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Review not found or not owned by user"
            )

        await session.delete(review)
        await session.commit()

