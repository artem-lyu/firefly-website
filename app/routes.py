from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, send_from_directory
from flask.templating import render_template_string
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import EditProfileFormEmployee, LoginForm, PostFormEmployer, RegistrationForm, EditProfileForm, \
    EmptyForm, PostForm, RegistrationFormEmployee, RegistrationFormEmployer, ResetPasswordRequestForm, ResetPasswordForm, ResumeForm, MessageForm
from app.models import Employee, Employer, User, Post, Message, Notification
from app.email import send_password_reset_email
from werkzeug.utils import secure_filename
import os
import json
from flask import jsonify


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    if current_user.is_employer:
        return redirect(url_for('index_employer'))
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title='Home',
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)

@app.route('/job_apply', methods=["POST"])
@login_required
def job_apply():
    flash("You have successfully applied for this job!")
    user = Employee.query.filter_by(username=current_user.username).first()
    current_post = Post.query.filter_by()
    user.number_jobs += 1
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/like/<int:post_id>/<action>')
@login_required
def like_action(post_id, action):
    post = Post.query.filter_by(id=post_id).first_or_404()
    post_author = User.query.filter_by(id=post.user_id).first()
    firefly_id = User.query.filter_by(id=3).first()
    if action == 'like':
        current_user.like_post(post)
        db.session.commit()
        flash("You successfully have applied for this job!")
        msg = Message(author=firefly_id, recipient=post_author, body="Someone has applied for your job! Their profile: Fireflycharity.artem-lyu.github.io/user/{}".format(current_user.username))
        db.session.add(msg)
        post_author.add_notification('unread_message_count', post_author.new_messages())
        db.session.commit()
    return redirect(request.referrer)

@app.route("/index/employer", methods = ["GET", "POST"])
@login_required
def index_employer():
    form = PostFormEmployer()
    if form.validate_on_submit():
        post = Post(position_title=form.position_title.data, author= current_user, contact_phone = form.contact_phone.data, physical_address = form.physical_address.data, body = form.body.data)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('explore'))
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index_employer.html', title='Home', form=form,
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url) 

@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title='Explore', posts=posts.items,
                           next_url=next_url, prev_url=prev_url)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.employee.data:
        return redirect(url_for('register_employee'))
    elif form.employer.data:
        return redirect(url_for('register_employer'))
    return render_template('register.html', title='Register', form=form)

@app.route('/register/employee', methods = ['GET','POST'])
def register_employee():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationFormEmployee()
    if form.validate_on_submit():
        user = Employee(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        user.date_birth = form.date_birth.data
        user.location = form.location.data
        user.home_address = form.home_address.data
        user.name = form.name.data
        user.contact_phone = form.contact_phone.data
        user.official_id = form.official_id.data
        user.number_jobs = 0
        user.is_employer = False
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register_employee.html', title='Register', form=form)

@app.route('/register/employer', methods = ['GET','POST'])
def register_employer():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationFormEmployer()
    if form.validate_on_submit():
        user = Employer(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        user.legal_person_name = form.legal_person_name.data
        user.legal_person_phone = form.legal_person_phone.data
        user.physical_address = form.physical_address.data
        user.name = form.name.data
        user.contact_phone = form.contact_phone.data
        user.official_id = form.official_id.data
        user.is_employer = True
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register_employee.html', title='Register', form=form)

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)

@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    filename = 'resume_' + filename + '.pdf'
    return send_from_directory(directory=uploads, path=filename)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    form = EmptyForm()
    return render_template('user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url, form=form)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        if form.upload_resume.data:
            return redirect(url_for('upload_resume'))
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)

@app.route('/edit_profile/employee', methods = ['GET', 'POST'])
@login_required
def edit_profile_employee():
    form = EditProfileFormEmployee(current_user.username)
    if form.validate_on_submit():
        if form.upload_resume.data:
            return redirect(url_for('upload_resume'))
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        current_user.home_address = form.home_address.data
        current_user.date_birth = form.date_birth.data
        current_user.location = form.location.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile_employee'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile_employee.html', title='Edit Profile',
                           form=form)
        

@app.route('/edit_profile/upload_resume', methods=['GET','POST'])
@login_required
def upload_resume():
    form = ResumeForm()
    if form.validate_on_submit():
        filename = secure_filename(form.resume.data.filename)
        form.resume.data.save('app/uploads/' +  'resume_' + current_user.username + '.pdf')
        current_user.resume_path = 'app/uploads/' +  'resume_' + current_user.username + '.pdf'
        flash('Your resume has been uploaded.')
        return redirect(url_for('edit_profile'))
    return render_template('upload_resume.html', title = 'Upload Resume', form=form)

@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash('You are following {}!'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))


@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash('You are not following {}.'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))

@app.route('/messages')
@login_required
def messages():
    current_user.last_message_read_time = datetime.utcnow()
    current_user.add_notification('unread_message_count', 0)
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    messages = current_user.messages_received.order_by(
        Message.timestamp.desc()).paginate(
            page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('messages', page=messages.next_num) \
        if messages.has_next else None
    prev_url = url_for('messages', page=messages.prev_num) \
        if messages.has_prev else None
    return render_template('messages.html', messages=messages.items,
                           next_url=next_url, prev_url=prev_url)


@app.route('/notifications')
@login_required
def notifications():
    since = request.args.get('since', 0.0, type=float)
    notifications = current_user.notifications.filter(
        Notification.timestamp > since).order_by(Notification.timestamp.asc())
    return jsonify([{
        'name': n.name,
        'data': n.get_data(),
        'timestamp': n.timestamp
    } for n in notifications])

@app.route('/send_message/<recipient>', methods=['GET', 'POST'])
@login_required
def send_message(recipient):
    user = User.query.filter_by(username=recipient).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(author=current_user, recipient=user,
                      body=form.message.data)
        db.session.add(msg)
        user.add_notification('unread_message_count', user.new_messages())
        db.session.commit()
        flash('Your message has been sent.')
        return redirect(url_for('user', username=recipient))
    return render_template('send_message.html', title='Send Message',
                           form=form, recipient=recipient)

