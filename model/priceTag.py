from db import db

class PriceTagModel(db.Model):

    __tablename__='priceTag'

    tagId=db.Column(db.Integer,primary_key=True)
    priceTag=db.Column(db.Float,default=0)
    scoutShare=db.Column(db.Float,default=0)
    playerShare=db.Column(db.Float,default=0)
    teamShare=db.Column(db.Float,default=0)
    playerEmail=db.Column(db.String(100),db.ForeignKey('player.email'),unique=True,nullable=False)
    
    player=db.relationship('PlayerModel',back_populates='priceTags')


    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()


    @classmethod
    def find_by_id(cls, tagId) -> "PriceTagModel":
        return cls.query.get_or_404(tagId)