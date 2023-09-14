from db import db

class ClubModel(db.Model):

    __tablename__='club'

    email = db.Column(db.String(100),primary_key=True)
    clubName=db.Column(db.String(200),nullable=True)
    password = db.Column(db.String(150),nullable=True)
    motto = db.Column(db.String(500),nullable=True)
    mission = db.Column(db.String(500),nullable=True)
    vision=db.Column(db.String(500),nullable=True)
    description=db.Column(db.String(1000),nullable=True)
    location=db.Column(db.String(1000),nullable=True)
    division=db.Column(db.String(1000),nullable=True)
    picture=db.Column(db.String(100),default='avatar-1.png')

    playerTests= db.relationship('PlayerTestModel',back_populates='club',lazy="dynamic")

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, email: str) -> "ClubModel":
        return cls.query.get_or_404(email)


