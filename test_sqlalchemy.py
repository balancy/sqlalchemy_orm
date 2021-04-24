from request_data_from_db import fetch_posts_by_author, fetch_tags_by_post


class TestRequestDataFromDb:
    def test_fetch_posts_by_author(self):
        username = "denis-19"
        posts = fetch_posts_by_author(username)
        usernames_in_result = list(set(post[0].username for post in posts))

        if usernames_in_result:
            assert username == usernames_in_result[0] and len(posts)
        else:
            assert not len(posts)

    def test_fetch_tags_by_post(self):
        title = ("НАСА показало первое цветное изображение с вертолета "
                 "«Индженьюити»")
        tags = fetch_tags_by_post(title)
        posts_in_result = list(set(tag[0].title for tag in tags))

        if posts_in_result:
            assert title == posts_in_result[0] and len(tags)
        else:
            assert not len(tags)
