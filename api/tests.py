from django.test import TestCase


# Create your tests here.
@pytest.mark.django_db
class TestBlogSchema(TestCase):

    def setUp(self):
        self.client = Client(schema)
        self.blog = mixer.blend(Blog)

    def test_single_blog_query(self):
        response = self.client.execute(single_blog_query, variables={"id": self.blog.id})
        response_blog = response.get("data").get("blog")
        assert response_blog["id"] == str(self.blog.id)

    def test_blog_list_query(self):
        mixer.blend(Blog)
        mixer.blend(Blog)

        response = self.client.execute(blog_list_query)
        blogs = response.get("data").get("blogs")
        ok = response.get("data").get("ok")

        assert len(blogs)

    def test_create_blog(self):
        author = mixer.blend(Author)
        payload = {
            "title": "How to test GraphQL with pytest",
            "authorId": author.id,
            "body": "This is the example of functional testing.",
        }

        response = self.client.execute(create_blog_mutation, variables={"input": payload})
        blog = response.get("data").get("createBlog").get("blog")
        title = blog.get("title")
        assert title == payload["title"]

    def test_update_blog(self):
        payload = {
            "id": self.blog.id,
            "title": "How to test GraphQL update mutation with pytest"
        }

        response = self.client.execute(update_blog_mutation, variables={"input": payload})

        response_blog = response.get("data").get("updateBlog").get("blog")
        title = response_blog.get("title")
        assert title == payload["title"]
        assert title != self.blog.title

    def test_delete_blog(self):
        payload = {
            "id": self.blog.id
        }
        response = self.client.execute(delete_blog_mutation, variables={"input": payload})
        ok = response.get("data").get("deleteBlog").get("ok")
        assert ok
