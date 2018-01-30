from app import app, db
from flask import render_template, flash, redirect, request, url_for, session, make_response
from app.forms import RegisterForm, LoginForm, AddTaskForm
from flask_login import current_user, login_user, login_required
from app.models import Users, TaskList
from datetime import datetime

@app.route('/')
@app.route('/home')
def home():
	user = {'username': 'rushi'}
	return render_template('home.html')

# RegisterForm
@app.route('/register', methods=['GET'])
def register_get():
	form = RegisterForm()
	return render_template('register.html', form = form)


@app.route('/register', methods=['POST'])
def register_post():
	form = RegisterForm(request.form)

	# Get the values from the form
	if form.validate():
		# TODO: use managers and don't put logic in views
		name = form.name.data 
		email = form.email.data
		username = form.username.data
		password = form.password.data

		user = Users(name=name, email=email, username=username)
		user.set_password(password)
		db.session.add(user)
		db.session.commit()

		flash("You are now registered and can login", "success")

		return redirect(url_for('login_get'))

	flash("Check the values", "danger")
	return render_template("register.html", form=form)

# LoginForm
@app.route('/login', methods=['GET'])
def login_get():
	if current_user.is_authenticated:
		return redirect(url_for('userhome'))
	form = LoginForm()
	return render_template('login.html', form=form)

@app.route('/login', methods=['POST'])
def login_post():
	if current_user.is_authenticated:
		return redirect(url_for('userhome'))

	form = LoginForm(request.form)
	if form.validate():
		# Get form fields
		username = form.username.data
		password = form.password.data
		
		# Get details from database
		user = Users.query.filter_by(username=username).first()
		
		# Check for username and password
		if user is None or not user.check_password(password):
			flash("User doesnt exist or password is incorrect")
			return redirect(url_for('login_get'))
		else:
			login_user(user)								# Authentication of User
			session['user_id'] = user.id
			return redirect('userhome')
		

# User Home Page
@app.route('/userhome')
@login_required
def userhome():
	# Get the tasks to homepage
	# Retreive data
	tasks = current_user.tasks.all()
	print(tasks)
	
	if len(tasks) > 0 :
		# return render_template('userhome.html', tasks = tasks)
		response = make_response(render_template('userhome.html', tasks = tasks))
		response.headers['Last-Modified'] = datetime.now()
		response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
		response.headers['Pragma'] = 'no-cache'
		response.headers['Expires'] = '-1'
		return response
	else:
		response = make_response(render_template('userhome.html'))
		response.headers['Last-Modified'] = datetime.now()
		response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
		response.headers['Pragma'] = 'no-cache'
		response.headers['Expires'] = '-1'
		return response
	# Close cursor
	cur.close()

# Add Task
@app.route('/addTask', methods = ['GET'])
@login_required
def addTask_get():
	form = AddTaskForm()
	return render_template('addTask.html', form=form)

@app.route('/addTask', methods = ['POST'])
@login_required
def addTask_post():
	form = AddTaskForm(request.form)
	if form.validate():
		form = AddTaskForm(request.form)	
		# Get Task Details
		title = form.title.data
		body = form.body.data
		status = False

		# Insert tasks into database
		task = TaskList(title=title, body=body, status=status, user_id=current_user.id)
		db.session.add(task)
		db.session.commit()
		
		flash("Task added successfully", "success")
		return redirect(url_for('userhome'))

	return render_template('addTask.html', form=form)

# Edit task
@app.route('/editTask/<string:id>', methods = ['GET'])
@login_required
def editTask_get(id):
	# Get data
	task = TaskList.query.filter_by(id=id).first()
	
	if task is not None and task.is_own_task(task.user_id):
		return render_template('editTask.html', task=task)
	else :
		flash("The task doesnot belong to you", "danger")
		return redirect(url_for('userhome'))

@app.route('/editTask/<string:id>', methods = ['POST'])
@login_required
def editTask_post(id):
	# Get data
	task = TaskList.query.filter_by(id=id).first()
	
	# Get Task Details
	task.title = request.form['title']
	task.body = request.form['body']
	task.status = False

	db.session.add(task)
	db.session.commit()

	flash("Task Updated successfully", "success")

	return redirect(url_for('userhome'))

# Delete Task
@app.route('/deleteTask/<string:id>', methods=['POST'])
@login_required
def deleteTask(id):
	task = TaskList.query.filter_by(id=id).first()
	db.session.delete(task)
	db.session.commit()

	flash("Deleted succesfully ", "danger")
	return redirect(url_for('userhome'))

# Status Of Task
@app.route('/statusOfTask/<string:status>/<string:id>', methods = ['POST'])
@login_required
def statusOfTask(status,id):

	if status == 'False':
		status = True
	else:
		status = False
	
	task = TaskList.query.filter_by(id=id).first()
	task.status = status
	db.session.add(task)
	db.session.commit()

	flash("Status changed succesfully ", "success")
	return redirect(url_for('userhome'))	


# Logout
@app.route('/logout')
@login_required
def logout():
	session.clear();
	flash("You are logged out")
	return redirect(url_for('login_get'))



















