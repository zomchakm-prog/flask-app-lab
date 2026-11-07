from datetime import datetime
from app import db

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    posted = db.Column(db.DateTime, default=datetime.utcnow)
    category = db.Column(
        db.Enum('news', 'publication', 'tech', 'other', name='category_enum'),
        default='other',
        nullable=False
    )
    
     
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    author = db.Column(db.String(20), default='Anonymous', nullable=False)

    def __repr__(self):
        return f"<Post(title={self.title})>"