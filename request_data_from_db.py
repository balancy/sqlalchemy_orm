from db import Session
from db_models import Post, Tag, User
from utils import output_posts_by_author, output_tags_by_post


def fetch_posts_by_author(username):
    posts = Session.query(User, Post).filter(
        User.username == username
    ).join(User.posts).all()

    return posts


def fetch_tags_by_post(title):
    tags = Session.query(Post, Tag).filter(
        Post.title == title
    ).join(Post.tags).all()

    return tags


if __name__ == "__main__":
    username = "denis-19"
    posts = fetch_posts_by_author(username)
    output_posts_by_author(username, posts)

    post_title = ("НАСА показало первое цветное изображение с вертолета "
                  "«Индженьюити»")
    tags = fetch_tags_by_post(post_title)
    output_tags_by_post(post_title, tags)
