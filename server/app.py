# server/app.py
#!/usr/bin/env python3

#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate
from models import db, Earthquake

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


# Create tables + seed safely for tests
with app.app_context():
    db.create_all()

    if Earthquake.query.count() == 0:
        db.session.add_all([
            Earthquake(location="Chile", magnitude=9.5, year=1960),
            Earthquake(location="Alaska", magnitude=9.2, year=1964),
            Earthquake(location="Haiti", magnitude=8.0, year=2010),
        ])
        db.session.commit()


@app.route("/earthquakes/<int:id>", methods=["GET"])
def earthquake_by_id(id):
    quake = db.session.get(Earthquake, id)

    if quake is None:
        return make_response(
            {"message": f"Earthquake {id} not found."},
            404
        )

    return make_response(
        {
            "id": quake.id,
            "magnitude": quake.magnitude,
            "location": quake.short_location,
            "year": quake.year,
        },
        200,
    )


@app.route("/earthquakes/magnitude/<float:magnitude>", methods=["GET"])
def earthquakes_by_magnitude(magnitude):
    quakes = (
        Earthquake.query
        .filter(Earthquake.magnitude >= magnitude)
        .order_by(Earthquake.magnitude.desc())
        .all()
    )

    return make_response(
        {
            "count": len(quakes),
            "quakes": [
                {
                    "id": q.id,
                    "magnitude": q.magnitude,
                    "location": q.short_location,
                    "year": q.year,
                }
                for q in quakes
            ],
        },
        200,
    )


if __name__ == "__main__":
    app.run(port=5555, debug=True)
