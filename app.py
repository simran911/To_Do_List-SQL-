from datetime import datetime
from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    done = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)

    def __init__(self, content):
        self.content = content
        self.done = False
        self.created_at = datetime.utcnow()
        self.completed_at = None

    def __repr__(self) -> str:
        return '<Content %s>' % self.content

# Create the database tables within an application context
with app.app_context():
    db.create_all()

@app.route('/')
def task_list():
    tasks = Task.query.all()
    return render_template('list.html', tasks=tasks)

@app.route('/task', methods=['POST'])
def add_task():
    content = request.form['content']
    if not content:
        return 'Error'
    
    task = Task(content)
    db.session.add(task)
    db.session.commit()
    return redirect('/')

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return redirect('/')
    
    db.session.delete(task)
    db.session.commit()
    return redirect('/')

@app.route('/done/<int:task_id>')
def resolve_task(task_id):
    task = Task.query.get(task_id)

    if not task:
        return redirect('/')
    
    task.done = not task.done
    if task.done:
        task.completed_at = datetime.utcnow()
    else:
        task.completed_at = None

    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
