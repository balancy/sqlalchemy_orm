from db import Session
from db_models import Post, PostTagLink, Tag, User
from utils import fetch_posts_from_habr


def create_or_get_user(username):
    session = Session()

    user = session.query(User).filter_by(username=username).first()
    if not user:
        user = User(username=username)
        session.add(user)
        session.commit()

    user_id = user.id
    session.close()

    return user_id


def create_or_get_post(user_id, title, text):
    session = Session()

    post = session.query(Post).filter_by(title=title).first()
    if not post:
        post = Post(title=title, text=text, user_id=user_id)
        session.add(post)
        session.commit()

    post_id = post.id
    session.close()

    return post_id


def create_or_get_tag(title):
    session = Session()

    tag = session.query(Tag).filter_by(title=title).first()
    if not tag:
        tag = Tag(title=title)
        session.add(tag)
        session.commit()

    tag_id = tag.id
    session.close()

    return tag_id


def create_or_get_post_tag_link(post_id, tag_id):
    session = Session()

    post_tag_link = \
        session.query(PostTagLink) \
        .filter_by(post_id=post_id, tag_id=tag_id).first()

    if not post_tag_link:
        post_tag_link = PostTagLink(post_id=post_id, tag_id=tag_id)
        session.add(post_tag_link)
        session.commit()

    post_tag_link_id = post_tag_link.id
    session.close()

    return post_tag_link_id


def fill_db_with_data():
    for post in fetch_posts_from_habr():
        user_id = create_or_get_user(post["username"])
        post_id = create_or_get_post(user_id, post["title"], post["text"])
        for tag in post["tags"]:
            tag_id = create_or_get_tag(tag)
            create_or_get_post_tag_link(post_id, tag_id)


if __name__ == "__main__":
    fill_db_with_data()
