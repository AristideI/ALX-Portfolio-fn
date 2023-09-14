from db import db

class ScoutModel(db.Model):

    __tablename__='scout'

    email = db.Column(db.String(100),primary_key=True)
    names=db.Column(db.String(200),nullable=True)
    phone = db.Column(db.String(15),nullable=True)
    password = db.Column(db.String(150),nullable=True)
    nationality=db.Column(db.String(100),nullable=True)
    birthdate=db.Column(db.Date,nullable=True)
    picture=db.Column(db.String(100),default='avatar-1.png')
    experience=db.Column(db.String(1000),nullable=True)
    description=db.Column(db.String(1000),nullable=True)
    isActivated=db.Column(db.Boolean,default=False)


    players=db.relationship('PlayerModel',back_populates='scout',lazy="dynamic")
    playerTests=db.relationship('PlayerTestModel',back_populates='scout',lazy="dynamic")


    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, email: str) -> "ScoutModel":
        return cls.query.get_or_404(email)


