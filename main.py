from datetime import datetime

from bs4 import BeautifulSoup
import requests
from sqlalchemy import (
    Boolean,
    create_engine,
    Column,
    DateTime,
    ForeignKey,
    func,
    Integer,
    String,
    Text,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    backref,
    relationship,
    sessionmaker,
    scoped_session,
)

from config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base(bind=engine)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(
        String(32),
        unique=True,
        nullable=False,
        default="",
        server_default="",
    )
    is_admin = Column(
        Boolean,
        nullable=False,
        default=False,
        server_default="0",
    )
    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        server_default=func.now()
    )

    posts = relationship("Post", back_populates="user")

    def __str__(self):
        return f"{self.__class__.__name__} <{self.username}>"

    def __repr__(self):
        return str(self)


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(
        String(90),
        nullable=False,
        default="",
        server_default="",
    )
    published_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        server_default=func.now()
    )
    text = Column(Text, nullable=True, default="", server_default="")

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship(User, back_populates="posts")
    tags = relationship(
        "Tag", secondary="post_tag_links",
    )

    def __str__(self):
        return f"{self.__class__.__name__} <{self.title}>"

    def __repr__(self):
        return str(self)


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False, default="", server_default="")
    posts = relationship(
        "Post", secondary="post_tag_links",
    )

    def __str__(self):
        return f"{self.__class__.__name__} <{self.title}>"

    def __repr__(self):
        return str(self)


class PostTagLink(Base):
    __tablename__ = "post_tag_links"

    id = Column(Integer, primary_key=True)
    post_id = Column('post_id', Integer, ForeignKey('posts.id'))
    tag_id = Column('tag_id', Integer, ForeignKey('tags.id'))

    post = relationship(
        Post,
        backref=backref("post_tag_links", cascade="all, delete-orphan")
    )
    tag = relationship(
        Tag,
        backref=backref("post_tag_links", cascade="all, delete-orphan")
    )


def create_db():
    Base.metadata.create_all()


def fetch_posts_from_habr():
    url = "https://habr.com/ru/news/"
    response = requests.get(url)
    response.raise_for_status()

    parsed_html = BeautifulSoup(response.text, "lxml")
    all_html_news = parsed_html.select(".posts_list .post")

    news_set = []
    for post in all_html_news:
        news_set.append({
            "title": post.select_one(".post__title a").text,
            "text": post.select_one(".post__text").text.strip(),
            "username": post.select_one(".post__meta .user-info").text.strip(),
            "tags": [elm.text for elm in post.select(".post__hubs .inline-list__item_hub a")]
        })

    return news_set


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

    post_tag_link = session.query(PostTagLink).filter_by(post_id=post_id, tag_id=tag_id).first()
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
            post_tag_id = create_or_get_post_tag_link(post_id, tag_id)


if __name__ == "__main__":
    # create_db()
    fill_db_with_data()

