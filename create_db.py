from db import Base, engine

from db_models import Post, PostTagLink, Tag, User


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
