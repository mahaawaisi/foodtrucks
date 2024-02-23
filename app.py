from flask import Flask, jsonify, request, json
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from math import sin, cos, sqrt, atan2, radians


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

# I guess you could display the distance 
def calculateDistance(truck_lat, truck_lon, user_lat, user_lon):
    # Approximate radius of earth in km
    R = 6373.0
    lat1 = radians(float(user_lat))
    lon1 = radians(float(user_lon))
    lat2 = radians(truck_lat)
    lon2 = radians(truck_lon)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    # if the distance is more than 5km then give back otherwise don't
    return distance


# This method gets the 5 closest trucks based on users location
@app.route('/data', methods=['GET'])
def get_data():
    user_lat = request.args.get("lat")
    user_lon = request.args.get("long")

    user_lat =  37.802567414124184
    user_lon = -122.4483553855345

    data = Data.query.all()
 
     # okay come back to this and filter by 5 closest trucks
    filtered_data = []
    for truck in data:
        distance = calculateDistance(truck.Latitude, truck.Longitude, user_lat, user_lon)
        if(distance <= 5):
            filtered_data.append({"locationid": truck.locationId, "name": truck.Applicant, "type": truck.FacilityType,
                                 "locationDescription": truck.LocationDescription, "address": truck.Address,
                                 "status": truck.Status, "menu": truck.FoodItems, "x_coordinate": truck.X,
                                 "y_coordinate": truck.Y, "latitude": truck.Latitude,
                                 "longitude": truck.Longitude, "coordinates": truck.Location})
            print('more than 5 km')
            print(f"Truck {truck.locationId} is within 5km ({distance} km away)")

    data_json = json.dumps(filtered_data)
    return jsonify(data_json)


# only do this if you finish
# Get the trucks in radius distance
@app.route('/data', methods=['GET'])
def get_trucks_radius():
    radius = request.args.get("radius")




if __name__ == '__main__':
    print('Starting here')
    app.run(debug=True)