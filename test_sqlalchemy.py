from db import Session
from db_models import Post, User
from request_data_from_db import fetch_posts_by_author, fetch_tags_by_post


class TestRequestDataFromDb:
    def test_fetch_posts_by_author(self):
        username = Session.query(User).first().username
        posts = fetch_posts_by_author(username)
        usernames_in_result = list(set(post[0].username for post in posts))

        Session.close()

        assert username == usernames_in_result[0] and len(posts)

    def test_fetch_tags_by_post(self):
        title = Session.query(Post).first().title
        tags = fetch_tags_by_post(title)
        posts_in_result = list(set(tag[0].title for tag in tags))

        Session.close()

        assert title == posts_in_result[0] and len(tags)
