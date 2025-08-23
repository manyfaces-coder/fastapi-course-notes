# Выполняем запросы к БД
import asyncio

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import db_helper, User, Profile, Post


async def create_user(session: AsyncSession, username: str):
    user = User(username=username)
    session.add(user)
    await session.commit()
    print(f"User: {user}")
    return user


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    # result: Result = await session.execute(stmt)
    # user: User | None = result.scalar_one_or_none() # не уверены, что пользователь существует
    # если уверены, что пользователь существует
    # user: User | None = result.scalar_one() # если пользователя нет, получим исключение
    # альтернатива без result
    user: User | None = await session.scalar(stmt)
    print("found user", username, user)
    return user


async def create_user_profile(
    session: AsyncSession,
    user_id: int,
    first_name: str | None = None,
    last_name: str | None = None,
) -> Profile:
    profile = Profile(
        user_id=user_id,
        first_name=first_name,
        last_name=last_name,
    )
    session.add(profile)
    await session.commit()
    return profile


async def show_users_with_profiles(session: AsyncSession):
    stmt = select(User).options(joinedload(User.profile)).order_by(User.id)
    # первый вариант
    # result: Result = await session.execute(stmt)
    # users = result.scalars()
    # второй вариант
    users = await session.scalars(stmt)
    for user in users:
        print(user)
        print(user.profile.first_name)


async def create_posts(
    session: AsyncSession,
    user_id: int,
    *posts_titles: str,
) -> list[Post]:
    posts = [Post(title=title, user_id=user_id) for title in posts_titles]
    session.add_all(posts)
    await session.commit()
    print(f"posts: {posts}")
    return posts


async def get_users_with_posts(
    session: AsyncSession,
):
    # stmt = select(User).options(joinedload(User.posts)).order_by(User.id) # вместо этого можно использовать:
    # selectinload, он используется для связей "ко многим"
    stmt = select(User).options(selectinload(User.posts)).order_by(User.id)
    # получаем пользователей через session.scalars
    # users = await session.scalars(stmt)
    # получаем пользователей через result
    result: Result = await session.execute(stmt)
    # users = result.unique().scalars()
    # если использовать selectinload, то можно обойтись без unique()
    users = result.unique().scalars()

    # если через session.scalars, то делаем так:
    # for user in users.unique():
    # если через result, то делаем так:
    for user in users:
        print("**" * 10)
        print(user)
        for post in user.posts:
            print("-", post)


async def get_users_with_posts_and_profiles(
    session: AsyncSession,
):
    stmt = (
        select(User)
        .options(
            joinedload(User.profile),
            selectinload(User.posts),
        )
        .order_by(User.id)
    )
    users = await session.scalars(stmt)

    for user in users:  # type: User
        print("**" * 10)
        print(
            user, user.profile and user.profile.first_name
        )  # and проверит, если профиль пустой, то ничего не выведет
        for post in user.posts:
            print("-", post)


async def get_posts_wits_authors(session: AsyncSession):
    stmt = select(Post).options(joinedload(Post.user)).order_by(Post.id)
    posts = await session.scalars(stmt)

    for post in posts:  # type: Post
        print("post", post)
        print("author", post.user)


async def get_profiles_with_users_users_with_posts(session: AsyncSession):
    stmt = (
        select(Profile)
        .join(Profile.user)
        .options(
            joinedload(Profile.user).selectinload(User.posts),
        )
        .where(User.username == "Ivan")
        .order_by(Profile.id)
    )

    profiles = await session.scalars(stmt)

    for profile in profiles:
        print(profile.first_name, profile.user)
        print(profile.user.posts)


async def main():
    async with db_helper.session_factory() as session:
        # создаем пользователей
        # await create_user(session=session, username="Ivan")
        # await create_user(session=session, username="Bob")

        # # ищем пользователей по username
        user_ivan = await get_user_by_username(session=session, username="Ivan")
        user_aleks = await get_user_by_username(session=session, username="Aleks")
        # await get_user_by_username(session=session, username="Test")

        # создание профилей для пользователей
        # await create_user_profile(
        #     session=session,
        #     user_id=user_ivan.id,
        #     first_name="Ivan",
        # )
        # await create_user_profile(
        #     session=session,
        #     user_id=user_aleks.id,
        #     first_name="Aleks",
        #     last_name="Che",
        # )
        # await show_users_with_profiles(session=session)

        # await create_posts(
        #     session,
        #     user_ivan.id,
        #     "FastApi edc",
        #     "sqlalchemy first lesson",
        # )
        # await create_posts(
        #     session,
        #     user_aleks.id,
        #     "Python 3.11",
        #     "Virtualenv",
        # )
        # await get_users_with_posts(session=session)

        # await get_posts_wits_authors(session=session)

        # await get_users_with_posts_and_profiles(session=session)

        await get_profiles_with_users_users_with_posts(session=session)


if __name__ == "__main__":
    asyncio.run(main())
