from flask import Flask, jsonify,render_template,redirect, send_from_directory,url_for,session,flash,request
from db import db
from model import AdminModel,ScoutModel,PlayerModel,ClubModel,PhotosModel,PriceTagModel,PlayerTestModel,VideoModel
import os
from flask_migrate import Migrate
from dotenv import load_dotenv
import uuid
import functools
from datetime import datetime
from werkzeug.utils import secure_filename
from sqlalchemy import and_
from dotenv import load_dotenv
from sendmail import ToSendMail
load_dotenv()


def create_app():


    app=Flask(__name__)
    app.secret_key='oBQ4GBTlzpSwE2OCGzRCGcXVANO9bsYZL_Cf3CSEXPs'
    app.config["SQLALCHEMY_DATABASE_URI"] =os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    migrate=Migrate(app,db)


    def login_required(route):
        @functools. wraps(route)
        def route_wrapper(*args, **kwargs):
            if not session.get('user'):
                return redirect(url_for("home"))
            return route(*args, **kwargs)
        return route_wrapper


    @app.errorhandler(404)
    def pageNoFound(error):
        return render_template('404page.html'), 404


    @app.route('/contractDocument/<string:testId>')
    @login_required
    def contractDocument(testId):
        test= PlayerTestModel.find_by_id(testId)
        return render_template('contractDocument.html',user=session.get('user'),profileP=session.get('profileP'),status=session.get('status'),c_email=session.get('email'),email='',player=test,testId=testId)
    

    @app.route('/adminUpdatePhoto/<string:email>', methods=['POST'])
    @login_required
    def adminUpdatePhoto(email):
        photo_file = request.files['photoFile']
        admin= AdminModel.find_by_id(email)
        filename = secure_filename(photo_file.filename)
        filename=admin.email+'.'+ filename.split('.')[-1]
        photo_file.save(os.path.join('./static/pictures/profile',filename))
        admin.picture=filename
        admin.save_to_db()
        session['profileP'] = filename
        return {"mesage":'done'}


    @app.route('/clubUpdatePhoto/<string:email>', methods=['POST'])
    @login_required
    def clubUpdatePhoto(email):
        photo_file = request.files['photoFile']
        club= ClubModel.find_by_id(email)
        filename = secure_filename(photo_file.filename)
        filename=club.email+'.'+ filename.split('.')[-1]
        photo_file.save(os.path.join('./static/pictures/profile',filename))
        club.picture=filename
        club.save_to_db()
        return {"mesage":'done'}


    @app.route('/playerUpdatePhoto/<string:email>', methods=['POST'])
    @login_required
    def playerUpdatePhoto(email):
        photo_file = request.files['photoFile']
        player= PlayerModel.find_by_id(email)
        filename = secure_filename(photo_file.filename)
        filename=player.email+'.'+ filename.split('.')[-1]
        photo_file.save(os.path.join('./static/pictures/profile',filename))
        player.picture=filename
        player.save_to_db()
        session['profileP'] = filename
        return {"mesage":'done'}


    @app.route('/scoutUpdatePhoto/<string:email>', methods=['POST'])
    @login_required
    def scoutUpdatePhoto(email):
        photo_file = request.files['photoFile']
        scout= ScoutModel.find_by_id(email)
        filename = secure_filename(photo_file.filename)
        filename=scout.email+'.'+ filename.split('.')[-1]
        photo_file.save(os.path.join('./static/pictures/profile',filename))
        scout.picture=filename
        scout.save_to_db()
        session['profileP'] = filename
        return {"mesage":'done'}


    @app.route('/playerGalley/<string:email>')
    @login_required
    def playerGalley(email):
        photos=PhotosModel.query.filter(PhotosModel.player_email==email).all()
        vid = VideoModel.query.filter(VideoModel.player_email == email).order_by(VideoModel.id.desc()).first()
        return render_template('playerGallery.html',email=email,user=session.get('user'),profileP=session.get('profileP'),photos=photos,status=session.get('status'),c_email=session.get('email'),vid=vid)


    @app.route('/activateScoutAC/<string:email>')
    @login_required
    def activateScoutAC(email):
        scout=ScoutModel.find_by_id(email)
        scout.isActivated= not scout.isActivated
        scout.save_to_db()
        return redirect(url_for('admin_allScout'))


    @app.route('/inactiveAccount')
    @login_required
    def inactiveAccount():
        return render_template('lockAccount.html',user=session.get('user'),profileP=session.get('profileP'))


    @app.route('/contractDownload/<string:testId>')
    def contractDownload(testId):
        test= PlayerTestModel.find_by_id(testId)
        return send_from_directory('./contract',f'{test.documentName}',as_attachment=True,download_name=f'{test.player.names} {test.createdDate}.zip')


    @app.route('/uploadContract/<string:testId>',methods=['POST','GET'])
    def uploadContract(testId):
        try:
            if 'file' in request.files:
                file = request.files['file']
                filename=f'{testId}.zip'
                file.save(os.path.join('./contract',filename))
                test= PlayerTestModel.find_by_id(testId)
                test.documentName=filename
                test.save_to_db()
                return jsonify({'message': 'File uploaded successfully'})
        except :
            return jsonify({'message': 'No file uploaded'})


    @app.route("/openCloseDeal/<string:testId>")
    @login_required
    def openCloseDeal(testId):

        test= PlayerTestModel.find_by_id(testId)
        test.status= not test.status
        test.save_to_db()
        return redirect(url_for('playerClubId',email=test.player_email))


    @app.route("/updatePlayerTest/<string:testId>",methods=['POST','GET'])
    @login_required    
    def updatePlayerTest(testId):

        test= PlayerTestModel.find_by_id(testId)
        if request.method== 'POST':
            test.medicalTest= request.form.get('medicalTest')
            test.physicalTest= request.form.get('physicalTest')
            test.testPass= False
            if request.form.get('testPass') =='true':
                test.testPass= True
            
            try:
                test.save_to_db()
                flash('Test is successfully saved')
            except :
                flash('unable to save test')

        return render_template('playerTest.html',testId=testId,user=session.get('user'),profileP=session.get('profileP'),test=test)


    @app.route('/player-deal-list')
    @login_required
    def PlayerDealList():
        tests= PlayerTestModel.query.filter(PlayerTestModel.player_email==session.get('email')).all()
        return render_template('playerDealList.html',user=session.get('user'),profileP=session.get('profileP'),tests=tests,email=session.get('email'))


    @app.route('/deal-list')
    @login_required
    def clubDealList():
        tests= PlayerTestModel.query.filter(PlayerTestModel.club_email==session.get('email')).all()
        return render_template('clubDealList.html',user=session.get('user'),profileP=session.get('profileP'),tests=tests)


    @app.route("/player-club-id/<string:email>",methods=['POST','GET'])
    @login_required
    def playerClubId(email):
        clubs=ClubModel.query.all()
        if request.method== 'POST':
            testP=PlayerTestModel()
            testP.testId=uuid.uuid4().hex
            testP.player_email=email
            testP.club_email=request.form.get('teamEmail')
            testP.createdDate=datetime.now()
            testP.scout_email=session.get('email')
            try:
                testP.save_to_db()
                flash('Deal session is successfully created')
            except:
                flash('Deal session is failed to create')

        tests= PlayerTestModel.query.filter(PlayerTestModel.player_email==email).all()
            
        return render_template('createDeal.html',email=email,clubs=clubs,user=session.get('user'),profileP=session.get('profileP'),tests=tests,c_email=session.get('email'))


    @app.route("/clubSendMail",methods=['POST'])
    def clubSendMail():
        data = request.get_json()
        email = data.get('email')
        player=PlayerModel.find_by_id(email)
        mymail=ToSendMail()
        mymail.send_simple_message(username=player.scout.names,teamname=session.get('user'),playername=player.names)
        response_data = {'message': 'Email received successfully'}
        return jsonify(response_data), 200


    @app.route('/club-update/<string:email>',methods=['POST','GET'])
    @login_required
    def update_club(email):
        club=ClubModel.find_by_id(email)
        if request.method== 'POST':
            club.clubName=request.form.get('clubName')
            club.motto=request.form.get('motto')
            club.mission=request.form.get('mission')
            club.vision=request.form.get('vision')
            club.description=request.form.get('desc')
            club.location=request.form.get('location')
            club.division=request.form.get('division')

            try:
                club.save_to_db()
                session['user']=club.clubName
                flash('Account is successfully Updated')
            except:
                flash('Sorry, Unable to Update Account')

        return render_template('clubUpdate.html',email=email,user=session.get('user'),profileP=session.get('profileP'),club=club,c_email=session.get('email'))


    @app.route('/admin-update/<string:email>',methods=['POST','GET'])
    @login_required
    def update_admin(email):
        admin=AdminModel.find_by_id(email)
        if request.method== 'POST':
            admin.names=request.form.get('names')
            admin.phone=request.form.get('phone')

            try:
                admin.save_to_db()
                session['user']=admin.names
                flash('Account is successfully Updated')
            except:
                flash('Sorry, Unable to Update Account') 
        return render_template('adminUpdate.html',email=email,user=session.get('user'),profileP=session.get('profileP'),admin=admin)



    @app.route('/scout-update/<string:email>',methods=['POST','GET'])
    @login_required
    def update_scout(email):
        scout=ScoutModel.find_by_id(email)
        if request.method== 'POST':
            scout.names=request.form.get('names')
            scout.phone=request.form.get('phone')
            scout.nationality = request.form.get('nationality')
            scout.birthdate = request.form.get('dob')
            scout.experience=request.form.get('experience')
            scout.description=request.form.get('description')

            try:
                scout.save_to_db()
                session['user']=scout.names
                flash('Account is successfully Updated')
            except:
                flash('Sorry, Unable to Update Account') 
        return render_template('scoutUpdate.html',email=email,user=session.get('user'),profileP=session.get('profileP'),scout=scout)


    @app.route('/playerUpdateInfo/<string:email>',methods=['POST','GET'])
    @login_required
    def playerupdate(email):

        player=PlayerModel.find_by_id(email)
        if request.method== 'POST':
            player.names=request.form.get('names')
            player.phone=request.form.get('phone')
            player.nationality = request.form.get('nationality')
            player.birthdate = request.form.get('dob')
            player.height=request.form.get('height')
            player.weight=request.form.get('weight')
            player.position=request.form.get('position')
            player.scout_email=request.form.get('scoutemail')

            try:
                ScoutModel.find_by_id(player.scout_email)
                player.save_to_db()
                session['user']=player.names
                flash('Account is successfully Updated')
            except:
                flash('Incorrect Scout email')

        return render_template('playerUpdate.html',email=email,user=session.get('user'),profileP=session.get('profileP'),player = player)
    

    @app.route('/availablePlayer')
    @login_required 
    def availablePlayer():
        player=PlayerModel.query.filter(and_(PlayerModel.isOnMarket==True,PlayerModel.isActivated==True)).all()
        return render_template('availblePlayer.html',user=session.get('user'),profileP=session.get('profileP'),status=session.get('status'),c_email=session.get('email'),players=player,playerAge=calculateAge,rmFloatPrice=rmFloatPrice)


    @app.route('/scout-player-info/<email>',methods=[ 'POST','GET'])
    @login_required
    def scoutPlayerInfo(email):
        player=PlayerModel.find_by_id(email)
        price=PriceTagModel.query.filter(PriceTagModel.playerEmail==email).first()
        if request.method=='POST':
            player.playerSince= request.form.get('playersince')
            player.nationalAppearance= request.form.get('national')
            player.clubAppearance= request.form.get('club')
            player.goals= request.form.get('goal')
            player.assist= request.form.get('assist')
            player.achievement= request.form.get('achieve')
            price.priceTag= request.form.get('priceTag')
            price.teamShare= request.form.get('teamShare')
            price.playerShare= request.form.get('playerShare')
            price.scoutShare= request.form.get('scoutShare')
            files=request.files.getlist('file')
            highLight= request.files.get('videoFile')

            try:

                if len(highLight.filename.split('.')) >=2:
                    vidname='{}{}.{}'.format(player.names,uuid.uuid4().hex,highLight.filename.split('.')[-1])
                    highLight.save(os.path.join('./static/video/',vidname))
                    vid=VideoModel()
                    vid.name=vidname
                    vid.player_email=email
                    vid.save_to_db()
                
                for file in files:
                    if len(file.filename.split('.')) <2:
                        continue
                    print(file)
                    photo=PhotosModel()
                    filename='{}{}.{}'.format(player.names,uuid.uuid4().hex,file.filename.split('.')[-1]) 
                    savephoto(file,filename)
                    photo.name=filename
                    photo.player_email=email
                    photo.save_to_db()
                price.save_to_db()
                player.save_to_db()
                flash('Information is saved')
            except:
                flash('Unable not save Information')
            
        return render_template('scout-player-info.html',user=session.get('user'),profileP=session.get('profileP'),email=email, player= player ,price=price,c_email=session.get('email'))

    def savephoto(file,filename):
        file.save(os.path.join('./static/pictures/posting',filename))

    @app.route('/scout-new-player')
    @login_required
    def scoutNewPlayer():
        player=PlayerModel.query.filter(and_(PlayerModel.isActivated==False,PlayerModel.scout_email==session.get('email'))).all()

        return render_template('scout-new-player.html',user=session.get('user'),profileP=session.get('profileP'),players=player,c_email=session.get('email'))


    @app.route('/admin-allPLayer')
    @login_required
    def admin_allPLayers():
        player=PlayerModel.query.filter(PlayerModel.isActivated==True).all()
        return render_template('admin_allPLayers.html',user=session.get('user'),profileP=session.get('profileP'),players=player,c_email=session.get('email'))
    

    @app.route('/admin-allScout')
    @login_required
    def admin_allScout():
        scout=ScoutModel.query.filter(ScoutModel.isActivated==True).all()
        return render_template('admin_allScout.html',user=session.get('user'),profileP=session.get('profileP'),scouts=scout,c_email=session.get('email'))


    @app.route('/admin-allClub')
    @login_required
    def admin_allClub():
        club=ClubModel.query.all()
        return render_template('admin_allClub.html',user=session.get('user'),profileP=session.get('profileP'),clubs=club,c_email=session.get('email'))


    @app.route('/playerInfo/<string:email>',methods=['POST','GET'])
    @login_required
    def playerInfo(email):
        player=PlayerModel.find_by_id(email)
        if request.method=='POST':
            player.isActivated=True
            player.save_to_db()
        return render_template('playerInfo.html',user=session.get('user'),profileP=session.get('profileP'),status=session.get('status'),email=email,player=player,c_email=session.get('email'))
    

    @app.route('/scoutInfo/<string:email>',methods=['POST','GET'])
    @login_required
    def scoutInfo(email):
        scout=ScoutModel.find_by_id(email)
        if request.method=='POST':
            scout.isActivated=True
            scout.save_to_db()
        return render_template('scoutInfo.html',user=session.get('user'),profileP=session.get('profileP'),email=email,scout=scout,c_email=session.get('email'))


    @app.route('/newRegistrations')
    @login_required
    def adminActivateAC():
        scout=ScoutModel.query.filter(ScoutModel.isActivated==False).all()
        player=PlayerModel.query.filter(PlayerModel.isActivated==False).all()

        return render_template('adminActivateAC.html',user=session.get('user'),profileP=session.get('profileP'),players=player,scouts=scout,c_email=session.get('email'))


    @app.route('/scoutPlayer')
    @login_required
    def scoutPlayer():
        
        player=PlayerModel.query.filter(and_(PlayerModel.isActivated==True,PlayerModel.scout_email== session.get('email') )).all()
        return render_template('scoutPlayerList.html',user=session.get('user'),profileP=session.get('profileP'),players=player,c_email=session.get('email'))
    

    @app.route('/marketStatus/<string:email>')
    @login_required
    def marketStatus(email):

        player=PlayerModel.find_by_id(email)
        player.isOnMarket= not player.isOnMarket
        player.save_to_db()
        return redirect(url_for('scoutPlayer'))

    
    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('home'))
    

    @app.route('/adminLogin',methods=['POST','GET'])
    def adminlogin():

        if session.get('user'):
            if session.get('status')=='admin':
                return redirect(url_for('adminActivateAC'))
            elif session.get('status')=='scout':
                return redirect(url_for('scoutNewPlayer'))
            elif session.get('status')=='player':
                return redirect(url_for('playerInfo',email=session.get('email')))
            elif session.get('status')=='club':
                return redirect(url_for('availablePlayer'))

        if request.method=='POST':
            email=request.form.get('email')
            password=request.form.get('password')
            try:
                admin=AdminModel.find_by_id(email)
                print('/========>>>>>')
                print(admin.email)
                print(password)
                print(admin.password)
                if admin.password==password:
                    session['email']=email
                    session['user']=admin.names
                    session['status']='admin'
                    session['profileP']=admin.picture
                    return redirect(url_for('adminActivateAC')) 
                flash('incorrect email or password')
            except:
                flash('incorrect email or password') 

        return render_template('adminlogin.html',user=session.get('user'))


    @app.route('/scoutlogin',methods=['POST','GET'])
    def scoutlogin():

        if session.get('user'):
            if session.get('status')=='admin':
                return redirect(url_for('adminActivateAC'))
            elif session.get('status')=='scout':
                return redirect(url_for('scoutNewPlayer'))
            elif session.get('status')=='player':
                return redirect(url_for('playerInfo',email=session.get('email')))
            elif session.get('status')=='club':
                return redirect(url_for('availablePlayer'))

        
        if request.method=='POST':
            email=request.form.get('email')
            password=request.form.get('password')
            try:
                scout=ScoutModel.find_by_id(email)
                if scout.password==password:
                    session['email']=email
                    session['user']=scout.names
                    session['status']='scout'
                    session['profileP']=scout.picture
                    if not scout.isActivated:
                        return redirect(url_for('inactiveAccount'))
                    return redirect(url_for('scoutNewPlayer'))
                flash('incorrect email or password')
            except:
                flash('incorrect email or password') 

        return render_template('scoutlogin.html',user=session.get('user'))
    

    @app.route('/playerlogin',methods=['POST','GET'])
    def playerLogin():

        if session.get('user'):
            if session.get('status')=='admin':
                return redirect(url_for('adminActivateAC'))
            elif session.get('status')=='scout':
                return redirect(url_for('scoutNewPlayer'))
            elif session.get('status')=='player':
                return redirect(url_for('playerInfo',email=session.get('email')))
            elif session.get('status')=='club':
                return redirect(url_for('availablePlayer'))
        
        if request.method=='POST':
            email=request.form.get('email')
            password=request.form.get('password')
            try:
                player=PlayerModel.find_by_id(email)
                if player.password==password:
                    session['email']=email
                    session['user']=player.names
                    session['status']='player'
                    session['profileP']=player.picture

                    if not player.isActivated:
                        return redirect(url_for('inactiveAccount'))
                    return redirect(url_for('playerInfo',email=email))
                flash('incorrect email or password')
            except:
                flash('incorrect email or password') 

        return render_template('playerlogin.html',user=session.get('user'))    


    @app.route('/clublogin',methods=['POST','GET'])
    def clublogin():

        if session.get('user'):
            if session.get('status')=='admin':
                return redirect(url_for('adminActivateAC'))
            elif session.get('status')=='scout':
                return redirect(url_for('scoutNewPlayer'))
            elif session.get('status')=='player':
                return redirect(url_for('playerInfo',email=session.get('email')))
            elif session.get('status')=='club':
                return redirect(url_for('availablePlayer'))
        
        if request.method=='POST':
            email=request.form.get('email')
            password=request.form.get('password')
            try:
                club=ClubModel.find_by_id(email)
                if club.password==password:
                    session['email']=email
                    session['user']=club.clubName
                    session['status']='club'
                    session['profileP']=club.picture
                    return redirect(url_for('availablePlayer'))
                flash('incorrect email or password')
            except:
                flash('incorrect email or password') 

        return render_template('clublogin.html',user=session.get('user'))


    @app.route('/')
    @app.route('/home')
    def home():
        # dm=AdminModel()
        # dm.email='admin@gmail.com'
        # dm.names='Aristide Isingizwe'
        # dm.password='admin123'
        # dm.phone='0781234567'
        # dm.save_to_db()

        return render_template('index.html')
    

    @app.route('/clubRegistration',methods=['GET','POST'])
    def clubRegistration():

        if request.method== 'POST':
            club=ClubModel()
            club.clubName=request.form.get('clubName')
            club.email=request.form.get('email')
            club.motto=request.form.get('motto')
            club.mission=request.form.get('mission')
            club.vision=request.form.get('vision')
            club.description=request.form.get('desc')
            club.location=request.form.get('location')
            club.division=request.form.get('division')
            club.password= request.form.get('password')
            file=request.files.get('file')

            try:
                filename = secure_filename(file.filename)
                filename=club.email+'.'+ filename.split('.')[1]
                file.save(os.path.join('./static/pictures/profile',filename))
                club.picture=filename
                club.save_to_db()
                flash('Account is successfully created')
            except:
                flash('Sorry, Unable to create Account')

        return render_template('clubRegistration.html',user=session.get('user'),profileP=session.get('profileP'))
    

    @app.route('/scoutRegistration',methods=['GET','POST'])
    def scoutReg():

        if request.method== 'POST':
            scout=ScoutModel()
            scout.names=request.form.get('names')
            scout.phone=request.form.get('phone')
            scout.email=request.form.get('email')
            scout.nationality = request.form.get('nationality')
            scout.birthdate = request.form.get('dob')
            scout.password=request.form.get('password')
            scout.experience=request.form.get('experience')
            scout.description=request.form.get('description')
            pass2code=request.form.get('password-confirm')
            file=request.files.get('picture')

            if pass2code != scout.password:
                flash('You typed different password')
                return render_template('scoutReg.html')
            try:
                filename = secure_filename(file.filename)
                filename=scout.email+'.'+ filename.split('.')[1]
                print(1111111111111111111111111)
                file.save(os.path.join('./static/pictures/profile',filename))
                print(22222222222222222222222222222)
                scout.picture=filename
                print(333333333333333333333333333333333333)
                scout.save_to_db()
                flash('Account is successfully created')
            except:
                flash('Sorry, Unable to create Account') 

        return render_template('scoutReg.html',user=session.get('user'))


    @app.route('/playerRegistration',methods=['GET','POST'])
    def playerReg():
        if request.method== 'POST':
            player=PlayerModel()
            player.names=request.form.get('names')
            player.phone=request.form.get('phone')
            player.email=request.form.get('email')
            player.nationality = request.form.get('nationality')
            player.birthdate = request.form.get('dob')
            player.password=request.form.get('password')
            player.height=request.form.get('height')
            player.weight=request.form.get('weight')
            player.position=request.form.get('position')
            player.scout_email=request.form.get('scoutemail')
            pass2code=request.form.get('password-confirm')
            file=request.files.get('picture')

            if pass2code != player.password:
                flash('You typed different password')
                return render_template('playerReg.html')
            try:
                ScoutModel.find_by_id(player.scout_email)
            except:
                flash('Incorrect Scout email')
                return render_template('playerReg.html')
            
            try:
                filename = secure_filename(file.filename)
                filename=player.email+'.'+ filename.split('.')[1]
                file.save(os.path.join('./static/pictures/profile',filename))
                player.picture=filename
                player.save_to_db()
                price=PriceTagModel()
                price.playerEmail=player.email
                price.save_to_db()
                flash('Account is successfully created')
            except:
                flash('Sorry, Unable to create Account') 

        return render_template('playerReg.html',user=session.get('user'))
    
    
    def calculateAge(playerBD):
        nowYear=datetime.now()
        return nowYear.year -playerBD.year
    
    def rmFloatPrice(price):
        return int(price)


    return app