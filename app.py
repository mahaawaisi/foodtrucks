from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


app = Flask(__name__)


db_name = "foodtrucktest" # change name later
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///foodtrucktest.db' #here is where we can connect the database
db = SQLAlchemy(app)
CORS(app, resources={"*": {"origins": "http://localhost:3000"}})

# foodtrucktest.db
# come back to this, what is best practices for string max length

class Data(db.Model):
    locationId = db.Column(db.Integer, primary_key=True)
    Applicant = db.Column(db.String(500))
    FacilityType = db.Column(db.String(500))
    LocationDescription = db.Column(db.String(500))
    Address = db.Column(db.String(500))
    Status = db.Column(db.String(500))
    FoodItems = db.Column(db.String(500))
    X = db.Column(db.Float)
    Y = db.Column(db.Float)
    Latitude = db.Column(db.Float)
    Longitude = db.Column(db.Float)
    Location = db.Column(db.String(500))

try:
    with app.app_context():
        db.create_all()
except Exception as e:
    print(f"Error creating database tables: {e}")

@app.route('/test')
def test():
    print('in test')
    return jsonify({ "message": "Test route works!" })

@app.route('/data', methods=['GET'])
def get_data():
    print('HERE')
    data = Data.query.all()
    data_json = [{"locationid": d.locationId, "name": d.Applicant, "type": d.FacilityType, 
                  "locationDescription": d.LocationDescription, "address": d.Address,
                  "status": d.Status, "menu": d.FoodItems, "x_coordinate": d.X,
                  "y_coordinate": d.Y, "latitude": d.Latitude,
                  "longitude": d.Longitude, "coordinates": d.Location} for d in data]
    print('hi')
    return jsonify(data_json)

if __name__ == '__main__':
    print('Starting here')
    app.run(debug=True)