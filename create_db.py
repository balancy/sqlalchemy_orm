from datetime import datetime
from sqlalchemy import (
    Boolean,
    create_engine,
    Column,
    DateTime,
    ForeignKey,
    func,
    Integer,
    String,
    Table,
    Text,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session

from config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base(bind=engine)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


association_table = Table(
    'post_tag', Base.metadata,
    Column('posts_id', Integer, ForeignKey('posts.id')),
    Column('tags_id', Integer, ForeignKey('tags.id'))
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(
        String(32), unique=True, nullable=False, default="", server_default=""
    )
    is_admin = Column(
        Boolean, nullable=False, default=False, server_default="0"
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
    title = Column(String(90), nullable=False, default="", server_default="")
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
        "Tag", secondary="post_tag", back_populates="posts"
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
        "Post", secondary="post_tag", back_populates="tags"
    )

    def __str__(self):
        return f"{self.__class__.__name__} <{self.title}>"

    def __repr__(self):
        return str(self)


def main():
    Base.metadata.create_all()


if __name__ == "__main__":
    main()
