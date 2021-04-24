from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    func,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import backref, relationship


from db import Base


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
