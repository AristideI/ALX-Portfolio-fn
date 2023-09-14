from db import db
from datetime import datetime

class VideoModel(db.Model):

    __tablename__='highLights'

    id = db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200),nullable=True)
    uploadDate=db.Column(db.Date,default=datetime.now())
    player_email=db.Column(db.String(100),db.ForeignKey('player.email'),nullable=True)

    player=db.relationship('PlayerModel',back_populates='videos')


    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id: int) -> "VideoModel":
        return cls.query.get_or_404(id)