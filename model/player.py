from db import db

class PlayerModel(db.Model):

    __tablename__='player'

    email = db.Column(db.String(100),primary_key=True)
    names=db.Column(db.String(200),nullable=True)
    phone = db.Column(db.String(15),nullable=True)
    password = db.Column(db.String(150),nullable=True)
    nationality=db.Column(db.String(100),nullable=True)
    birthdate=db.Column(db.Date,nullable=True)
    picture=db.Column(db.String(100),default='avatar-1.png')
    position=db.Column(db.String(100),nullable=True)
    height=db.Column(db.String(5),nullable=True)
    weight=db.Column(db.String(5),nullable=True)
    playerSince=db.Column(db.String(5000),nullable=True)
    nationalAppearance=db.Column(db.String(5),nullable=True)
    clubAppearance=db.Column(db.String(5),nullable=True)
    goals=db.Column(db.String(5),nullable=True)
    assist=db.Column(db.String(5),nullable=True)
    highLight=db.Column(db.String(2000),nullable=True)
    achievement=db.Column(db.String(5000),nullable=True)
    scout_email=db.Column(db.String(100),db.ForeignKey('scout.email'),nullable=True)
    isActivated=db.Column(db.Boolean,default=False)
    isOnMarket=db.Column(db.Boolean,default=False)
    

    scout=db.relationship('ScoutModel',back_populates='players')
    photos=db.relationship('PhotosModel',back_populates='player',lazy="dynamic")
    videos=db.relationship('VideoModel',back_populates='player',lazy="dynamic")
    priceTags= db.relationship('PriceTagModel',back_populates='player',lazy="dynamic")
    playerTests= db.relationship('PlayerTestModel',back_populates='player',lazy="dynamic")


    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()


    @classmethod
    def find_by_id(cls, email: str) -> "PlayerModel":
        return cls.query.get_or_404(email)
