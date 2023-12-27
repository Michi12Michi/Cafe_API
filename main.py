from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy()
db.init_app(app)

# Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)
    
    def to_dict(self):
    	dictionary = {}
    	for column in self.__table__.columns:
    		dictionary[column.name] = getattr(self, column.name)
    	return dictionary

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("index.html")

# HTTP GET - Read Record
@app.get("/random")
def random_cafe():
	''' Returns a JSON random Cafe from db'''
	result = db.session.execute(db.select(Cafe))
	all_cafes = result.scalars().all()
	random_cafe = random.choice(all_cafes)
	return jsonify(cafe=random_cafe.to_dict())

@app.get("/all")
def all_cafes():
	''' Returns a JSON all Cafe from db'''
	result = db.session.execute(db.select(Cafe))
	all_cafes = result.scalars().all()
	return jsonify([cafe.to_dict() for cafe in all_cafes])

@app.get("/search")
def search_cafe():
	''' Returns a JSON location-specific Cafe from db'''
	loc = request.args.get("loc")
	cafes_result = db.session.execute(db.select(Cafe).where(Cafe.location == loc))
	cafes_list = cafes_result.scalars().all()
	if cafes_list:
		return jsonify([cafe.to_dict() for cafe in cafes_list])
	else:
		return jsonify(error={"Not Found": f"Sorry, we don't have cafes in {loc}"}), 404

# HTTP POST - Create Record
@app.post("/add")
def add():
	new_cafe = Cafe(
    	name = request.form.get("name"),
    	map_url = request.form.get("map_url"),
    	img_url = request.form.get("img_url"),
    	location = request.form.get("location"),
    	seats = request.form.get("seats"),
    	has_toilet = bool(request.form.get("has_toilet")),
    	has_wifi = bool(request.form.get("has_wifi")),
    	has_sockets = bool(request.form.get("has_sockets")),
    	can_take_calls = bool(request.form.get("can_take_calls")),
    	coffee_price = request.form.get("coffee_price"),
	)
	db.session.add(new_cafe)
	db.session.commit()
	return jsonify(response={"Success": "Successfully added the new cafe!"}), 200

# HTTP PATCH - Update Record
@app.patch("/update-price/<int:cafe_id>")
def update_price(cafe_id):
	new_price = request.args.get("coffee_price")
	coffee = db.get_or_404(Cafe, cafe_id)
	if coffee:
		coffee.coffee_price = new_price
		db.session.commit()
		return jsonify(response={"Success": "Successfully updated the price!"}), 200
	else:
		return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404

# HTTP DELETE - Delete Record
@app.delete("/delete/<int:cafe_id>")
def delete_coffee(cafe_id):
	api_key = request.args.get("api-key")
	if api_key and api_key == "TopSecretAPIKey": # 😂️😂️😂️😂️
		coffee = db.get_or_404(Cafe, cafe_id)
		db.session.delete(coffee)
		db.session.commit()
		return jsonify(response={"Success": "Successfully deleted the cafe!"}), 200
	else:
		return jsonify(error={"Error": "Unauthorized to delete"}), 403

if __name__ == '__main__':
    app.run(debug=True)
