from flask import Flask, jsonify, request, json
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from math import sin, cos, sqrt, atan2, radians

app = Flask(__name__)

db_name = "foodtrucktest" 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///foodtrucktest.db' 
db = SQLAlchemy(app)
CORS(app, resources={"*": {"origins": "http://localhost:3000"}})

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
    print(f"Error creating database table: {e}")

# Method: Calculate distance 
# Params: Truck lat/lon and User given lat/on
# Return: Distance in km between truck and user coordinates
def calculateDistance(truck_lat, truck_lon, user_lat, user_lon):
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
    return distance

# Method: Get data
# Return: First 5 closest trucks in 5km radius
@app.route('/data', methods=['GET'])
def get_data():
    user_lat = request.args.get("lat")
    user_lon = request.args.get("lon")

    # Tester lat and lon
    # user_lat =  37.802567414124184
    # user_lon = -122.4483553855345
    
    data = Data.query.all()
 
    filtered_data = []
    for truck in data:
        distance = calculateDistance(truck.Latitude, truck.Longitude, user_lat, user_lon)
        if(distance <= 5):
            filtered_data.append({"locationid": truck.locationId, "name": truck.Applicant, "type": truck.FacilityType,
                                 "locationDescription": truck.LocationDescription, "address": truck.Address,
                                 "status": truck.Status, "menu": truck.FoodItems, "x_coordinate": truck.X,
                                 "y_coordinate": truck.Y, "latitude": truck.Latitude,
                                 "longitude": truck.Longitude, "coordinates": truck.Location,
                                 "distance": distance})

    # Sort by distance and get first five trucks  
    sorted_data = sorted(filtered_data, key=lambda x: x["distance"])
    closest_trucks = sorted_data[:5]

    data_json = json.dumps(closest_trucks)
    return data_json

if __name__ == '__main__':
    app.run(debug=True)