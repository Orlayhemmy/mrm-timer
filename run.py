import os
from os.path import join, dirname
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI');
db = SQLAlchemy(app)

time_limit = 60

class TeamMember(db.Model):
    __tablename__ = 'team'
    id = db.Column(db.Integer, primary_key=True)
    membername = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<TeamMember %r>' % self.membername


@app.route('/')
def index():
    members = TeamMember.query.all()
    member_list = []
    for member in members:
        member_list.append({
            'id': member.id,
            'membername': member.membername
        })
  
    return render_template('index.html', team=member_list, timeLimit=time_limit)

@app.route('/add_member', methods=['POST'])
def member():
    if request.form['membername'] == '':
      return 'error'
    new_member = TeamMember(membername = request.form['membername'])
    db.session.add(new_member)
    db.session.commit()
    return index()

@app.route('/remove_member/<member_id>')
def remove_member(member_id):
    delete_member = TeamMember.query.filter_by(id = member_id).first()
    db.session.delete(delete_member)
    db.session.commit()
    return index() 

if __name__ == '__main__':
    app.run(debug=True)
