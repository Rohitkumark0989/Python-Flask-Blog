from flask import Flask,render_template,request,session,redirect,flash

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_migrate import Migrate
#from werkzeug import secure_filename
from werkzeug.utils import secure_filename
#from werkzeug.datastructures import  FileStorage
from dotenv import load_dotenv
load_dotenv()
import json
import os
import math
from datetime import datetime,date

with open('config.json','r') as c:
    params =json.load(c)["params"]


app = Flask(__name__)
app.secret_key = params['secret_key']
app.config['UPLOAD_FOLDER'] = params['upload_location']
app.config['PROFILE_FOLDER'] = params['profile_location']
app.config.update(
    MAIL_SERVER ='smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['gmail-user'],
    MAIL_PASSWORD = params['gmail-password']
)
mail =  Mail(app)

if os.getenv('FLASK_ENV') =='development':
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['production_uri']

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)
class Contacts(db.Model):
    """
    id,name,email,phone_num,msg,date
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    phone_num = db.Column(db.String(120), unique=True, nullable=False)
    msg = db.Column(db.String(120),  nullable=False)
    date = db.Column(db.String(12),  nullable=True)
    email = db.Column(db.String(20),  nullable=False)

class Posts(db.Model):
    """
    id,name,email,phone_num,msg,date
    """
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(120),  nullable=False)
    date = db.Column(db.String(120),  nullable=True)
    #date = db.Column(db.DateTime(),default=datetime.now())
    img_file = db.Column(db.String(120),  nullable=True,default='default.jpg')

class Users(db.Model):
    """
    id,name,email,phone_num,msg,date
    """
    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(80), nullable=False)
    l_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120),  nullable=False)
    password = db.Column(db.String(120),  nullable=False)
    date = db.Column(db.String(120),  nullable=True)
    profile_img = db.Column(db.String(120),  nullable=True,default='default.jpg')

@app.route("/")
def home():
    posts = Posts.query.filter_by().all()
    last = math.ceil(len(posts)/int(params['num_of_posts']))
    #[0:params['num_of_posts']]

    # Pagination logic
    page = request.args.get('page')
    if(not str(page).isnumeric()):
        page = 1
    page = int(page)
    posts = posts[(page-1)*int(params['num_of_posts']):(page-1)*int(params['num_of_posts'])+int(params['num_of_posts'])]
    if (page == 1):
        prev = "#"
        next = "/?page="+ str(page+1)
    elif (page == last):
        prev = "/?page=" + str(page - 1)
        next = "#"
    else:
        prev = "/?page=" + str(page - 1)
        next = "/?page=" + str(page + 1)


    return render_template("index.html",params=params,posts=posts,prev=prev, next=next)

@app.route("/admin", methods=['GET','POST'])
def admin():
    if ('user' in session and session['user'] == params['admin_user']):
        posts = Posts.query.all()
        return render_template('dashboard.html',params=params,posts = posts)

    if request.method == 'POST':
        # Redirect to admin panel
        username = request.form.get('username')
        password = request.form.get('password')
        if (username == params['admin_user'] and password == params['admin_password']):
            session['user'] = username
            posts = Posts.query.all()
            return render_template('dashboard.html',params=params,posts = posts)
    
    APP_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    TEMPLATE_PATH = os.path.join(APP_PATH, 'templates/')
    return render_template('admin/login.html', params=params)

    #return render_template('login.html',params=params)

@app.route("/about")
def about():
    return render_template('about.html',params=params)

@app.route("/post")
def post_detail():
    post = []
    return render_template('post.html',params=params,post=post)

@app.route("/post/<string:post_slug>", methods = ['GET'])
def post_route(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()
    return render_template('post.html',params=params,post=post)

@app.route("/edit/<string:sno>", methods = ['GET','POST'])
def edit(sno):

    if ('user' in session and session['user'] == params['admin_user']):
        if request.method == 'POST':
            box_title = request.form.get('title')
            slug = request.form.get('slug')
            content = request.form.get('content')
            img_file = request.form.get('img_file')
            date = datetime.today().strftime('%Y-%m-%d')
            if sno == '0':

                post = Posts(title=box_title,slug=slug,content=content,img_file=img_file,date=date)
                db.session.add(post)
                db.session.commit()
                return redirect('/edit/'+sno)
            else:

                post = Posts.query.filter_by(sno=sno).first()
                post.title = box_title
                post.slug = slug
                post.content = content
                post.img_file = img_file
                #post.date = date
                db.session.commit()
                return redirect('/edit/'+sno)
        post =  Posts.query.filter_by(sno=sno).first()

        if (post is not None):
              sno = sno
        else:
              sno = 0
        return render_template('edit.html',params=params,post=post,sno=sno)

@app.route("/contact", methods = ['GET','POST'])
def contact():
    if(request.method=='POST' ):
         ''' Add enetery to the DB'''
         name = request.form.get('name')
         email = request.form.get('email')
         phone = request.form.get('phone_num')
         message = request.form.get('msg')
         date = datetime.today().strftime('%Y-%m-%d')
         entery = Contacts(name=name,email=email,date=date,phone_num=phone,msg=message)
         db.session.add(entery)
         db.session.commit()
         mail.send_message('New message from blog' + name,
                           sender=email,
                           recipients= [params['gmail-user']],
                           body = message + "\n" + phone
                           )
    return render_template('contact.html',params=params)

@app.route("/bootstrap")
def bootstrap():
    return render_template('bootstrap.html')

@app.route("/uploader", methods = ['GET','POST'])
def uploader():
    if ('user' in session and session['user'] == params['admin_user']):
        if(request.method == 'POST'):
            f = request.files['file1']
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
            return "Uploaded successfully!"

@app.route("/delete/<string:sno>", methods = ['GET','POST'])
def delete(sno):
    if ('user' in session and session['user'] == params['admin_user']):
        post = Posts.query.filter_by(sno=sno).first()
        db.session.delete(post)
        db.session.commit()
    return redirect('/admin')

@app.route("/register", methods=['GET','POST'])
def register():
    """ Register Functionality """
    if(request.method=='POST' ):
         ''' Add new user data '''
         f_name = request.form.get('f_name')
         last_name = request.form.get('last_name')
         email = request.form.get('cus_email')
         password = request.form.get('password')
         date = datetime.today().strftime('%Y-%m-%d')
         encrypted_password = bcrypt.generate_password_hash(password).decode('utf-8')
         f = request.files['profile_pic']
         #f = request.form.file.data
         f.save(os.path.join(app.config['PROFILE_FOLDER'], secure_filename(f.filename)))
         entery = Users(f_name=f_name,l_name=last_name,email=email,password=encrypted_password,date=date,profile_img=f.filename)
         db.session.add(entery)
         db.session.commit()
         flash(f'User Registered Succesfully!')
         return redirect('/admin')

    return render_template('admin/register.html')

@app.route("/logout")
def logout():
    """ Logout Functionality """
    session.pop('user')
    return redirect('/admin')
def create_app():
    app = Flask(__name__)
if __name__=='__main__':
    app.run(debug=True)
