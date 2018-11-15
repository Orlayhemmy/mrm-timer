import json
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://drclaerh:kEACdRfROUl9xtjcGBBbpnMQtUlSSYXK@stampy.db.elephantsql.com:5432/drclaerh'
db = SQLAlchemy(app)

team = ['Olusola Oseni', 'Onuchukwu Chika', 'Taiwo Sunday']

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
  
  return render_template('index.html', team=member_list)

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
