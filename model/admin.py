from db import db

class AdminModel(db.Model):

    __tablename__='admin_table'

    email=db.Column(db.String(100),primary_key=True)
    names=db.Column(db.String(100),nullable=True)
    phone=db.Column(db.String(100),nullable=True)
    password=db.Column(db.String(100),nullable=True)
    picture=db.Column(db.String(100),default='avatar-1.png')

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, email: str) -> "AdminModel":
        return cls.query.get_or_404(email)
