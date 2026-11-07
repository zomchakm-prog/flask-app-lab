import unittest
from app import app, db
from app.posts.models import Post

class PostTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False  # Вимикаємо CSRF для коректного проходження тестів форми
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_post(self):
        with self.app.app_context():
            response = self.client.post("/posts/create", data={
                "title": "My first post",
                "content": "This is TDD!",
                "category": "news",
                "is_active": True,
                "publish_date": "2026-11-07T20:00"
            }, follow_redirects=True)
            
            self.assertEqual(response.status_code, 200)

            post = db.session.query(Post).filter_by(title="My first post").first()
            self.assertIsNotNone(post)
            self.assertEqual(post.content, "This is TDD!")

    def test_get_posts(self):
        response = self.client.get("/posts/")
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()