from db import db

class PlayerTestModel(db.Model):

    __tablename__='playerTest'

    testId=db.Column(db.String(200),primary_key=True)
    medicalTest=db.Column(db.String(3),default='0')
    physicalTest=db.Column(db.String(3),default='0')
    testPass=db.Column(db.Boolean,default=False)
    player_email=db.Column(db.String(100),db.ForeignKey('player.email'),nullable=True)
    club_email=db.Column(db.String(100),db.ForeignKey('club.email'),nullable=True)
    createdDate=db.Column(db.Date,nullable=True)
    scout_email=db.Column(db.String(100),db.ForeignKey('scout.email'),nullable=True)
    status=db.Column(db.Boolean,default=True)
    documentName=db.Column(db.String(100),nullable=True)

    player=db.relationship('PlayerModel',back_populates='playerTests')
    club=db.relationship('ClubModel',back_populates='playerTests')
    scout=db.relationship('ScoutModel',back_populates='playerTests')

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, testId: str) -> "PlayerTestModel":
        return cls.query.get_or_404(testId)