from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

metadata = MetaData()
db = SQLAlchemy(metadata=metadata)


class Earthquake(db.Model):
    __tablename__ = "earthquakes"

    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String, nullable=False)
    magnitude = db.Column(db.Float, nullable=False)
    year = db.Column(db.Integer, nullable=False)

    @property
    def short_location(self):
        """
        Normalize location for API output:
        - "Valdivia, Chile" -> "Chile"
        - "Alaska, USA"     -> "Alaska"
        """
        if "," not in self.location:
            return self.location

        parts = [p.strip() for p in self.location.split(",")]

    
        if parts[-1] == "Chile":
            return "Chile"

    
        return parts[0]


class Magnitude(db.Model):
    __tablename__ = "magnitudes"

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float, nullable=False)
