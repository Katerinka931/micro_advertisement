from app.database import db


class Advertisement(db.Model):
    __tablename__ = 'advertisement'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Integer, nullable=True)
    phone = db.Column(db.Text, nullable=False)

    # photo = db.Column(db.Text, nullable=False)

    def __init__(self, title, description, price, phone):
        self.title = title
        self.description = description
        self.price = price
        self.phone = phone

    def dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'phone': self.phone
        }

    def __repr__(self):
        return f'<Advertisement\n Title: {self.title} \nDescription: {self.description} \nPrice: {self.price} \nPhone: {self.phone}>'
