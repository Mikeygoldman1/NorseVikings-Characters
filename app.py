from flask import Flask, render_template,request 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
import os 


app = Flask(__name__)
uri = os.getenv("DATABASE_URL")  # default to None if not set
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
# set the connection string -- use the local connection if uri is None
app.config['SQLALCHEMY_DATABASE_URI'] = uri or 'postgresql://mikeygoldman1:Kolov1@localhost/vikings_norsemen_characters'
db = SQLAlchemy(app)

class Table1(db.Model):
    __tablename__ = 'norsemen'
    id = db.Column(db.Integer, primary_key=True)
    img_url = db.Column(db.String(2048))
    character_description = db.Column(db.Text)
    actor_name = db.Column(db.String(255))
    actor_description = db.Column(db.Text)
    

class Table2(db.Model):
    __tablename__ = 'viking'
    id = db.Column(db.Integer, primary_key=True)
    img_url = db.Column(db.String(2048))
    character_name = db.Column(db.String(255))
    character_description = db.Column(db.Text)
    actor_name = db.Column(db.String(255))
    actor_description = db.Column(db.Text)
    

@app.route('/', methods=['GET', 'POST'])
def index():
    norsemen_data = Table1.query.all()
    viking_data = Table2.query.all()

    # for row in norsemen_data:
    #     if row.actor_name is None:
    #         row.actor_name = row.character_description

    # for row in viking_data:
    #     if row.actor_name is None:
    #         row.actor_name = row.character_name
    
    if request.method == 'POST':
        table_search = request.form.get('table_search')
        actor_search = request.form.get('actor_search')

        if table_search:
            if table_search.lower() == 'norsemen':
                norsemen_data = Table1.query.all()
                viking_data = []
            elif table_search.lower() == 'viking':
                viking_data = Table2.query.all()
                norsemen_data = []
        elif actor_search:
            norsemen_data = Table1.query.filter(Table1.actor_name.contains(actor_search)).all()
            viking_data = Table2.query.filter(Table2.actor_name.contains(actor_search)).all()

    return render_template('index.html', norsemen_data=norsemen_data, viking_data=viking_data)
    

@app.route('/actor/<string:table>/<int:id>')
def actor(table, id):
    if table.lower() == 'norsemen':
        actor = Table1.query.get(id)
        return render_template('norsemen_actor.html', actor=actor)
    else:
        actor = Table2.query.get(id)
        return render_template('viking_actor.html', actor=actor)




if __name__ == '__main__':
    app.run(debug=True)
