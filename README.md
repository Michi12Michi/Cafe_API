# Cafe_API

A Python3/Flask/SQLAlchemy REST API which is designed to store data about Cafes all around the world.
Every Cafe entry has the following non-null properties:
    id, integer, primary key
    name, string(250) (unique)
    map_url, string(500)
    img_url, string(500)
    location, string(250)
    seats, string(250) 
    has_toilet, boolean
    has_wifi, boolean
    has_sockets, boolean
    can_take_calls, boolean
    coffee_price, string(250)
    
Routes and methods are the following:
-GET /random                                               allows to draw a random cafe from the database and to access to all of its properties;
-GET /all                                                  allows to draw all cafes and to access to all of their properties;
-GET /search[loc required]                                 allows to search for all of the cafes in a particular location;
-POST /add [all properties required]                       allows to add a new cafe to the database;
-PATCH /update-price/id [id and coffee-price required]     allows to update coffee_price of a specific cafe;
-DELETE /delete/id [id required]                           allows to delete a specific cafe from the database.
