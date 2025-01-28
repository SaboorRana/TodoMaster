from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import request
from flask import redirect
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MOTIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(200),nullable=False)
    desc = db.Column(db.String(600),nullable=False)
    date_created = db.Column(db.DateTime,default = datetime.utcnow)

    def __repr__(self):
        return f"{self.sno} - {self.title}"

@app.route("/",methods=['Get','POST'])
def hello_world():
    if request.method=='POST':
        tit = request.form.get('title')
        des = request.form.get('desc')
        todo = Todo(title=tit,desc=des)
        db.session.add(todo)
        db.session.commit()
    todo_show = Todo.query.all()
    return render_template('index.html',todo_show = todo_show)

@app.route("/About")
def about():
    return render_template('about.html')

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get('query')
    if query:
        results = Todo.query.filter(
            (Todo.title.ilike(f"%{query}%")) | (Todo.desc.ilike(f"%{query}%"))
        ).all()
    else:
        results = []  
    return render_template('search.html', todos=results, query=query)
@app.route("/update/<int:sno>",methods=['GET','POST'])
def update(sno):
   if request.method=='POST':
        title = request.form.get('title')
        desc = request.form.get('desc')
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.commit()
        return redirect('/')
   todo = Todo.query.filter_by(sno=sno).first()
   return render_template('update.html',todo = todo) 
@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    if todo:
        db.session.delete(todo)  
        db.session.commit() 
    return redirect('/') 

if __name__=="__main__":
    app.run(debug=True,port=8000)