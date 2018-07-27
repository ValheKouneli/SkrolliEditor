from application import db

class Article(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
   date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
   
   name = db.Column(db.String(144), nullable=False)
   writer = db.Column(db.String(144), nullable=True)
   ready = db.Column(db.Boolean, nullable=False)

   editor_in_charge = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=True)
   created_by = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

   def __init__(self, name):
      self.name = name
      self.ready = False
