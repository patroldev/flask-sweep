"""
File: models.py
Purpose: database definitions for SQLAlchemy
"""
from collections import defaultdict

from sweep import db


class Patrollers(db.Model):
    __table_name__ = 'patrollers'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(144))
    status = db.Column(db.String(144))

    def __repr__(self):
        return '<Patroller(name=\'{0}\')>'.format(self.name)

    def to_json(self):
        return {'id': self.id, 'name': self.name, 'status': self.status}


class Locations(db.Model):
    __table_name__ = 'locations'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(144))

    def __repr__(self):
        return '<Location(name=\'{0}\')>'.format(self.name)

    def to_json(self):
        return {'id': self.id, 'name': self.name}


class Activity(db.Model):
    __table_name__ = 'activity'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patroller_id = db.Column(db.Integer,
                             db.ForeignKey(
                                 'patrollers.id',
                                 ondelete='CASCADE'),
                             nullable=False)
    location_id = db.Column(db.Integer,
                            db.ForeignKey(
                                'locations.id',
                                ondelete='CASCADE'),
                            nullable=False)
    patroller = db.relationship('Patrollers', backref=db.backref("patrollers"))
    location = db.relationship('Locations', backref=db.backref("locations"))
    is_leader = db.Column(db.Boolean, default=False)
    signon = db.Column(db.DateTime, default=None)
    signoff = db.Column(db.DateTime, default=None)

    def __repr__(self):
        return '<Activity(Patroller=\'{0}\'), Location=\'{1}\'>'.format(self.patroller.name, self.location.name)

    @classmethod
    def active_patrollers(cls):
        """
        Returns dictionary of active patrollers

            Args:
                None

            Returns:
                Dictionary
        """
        x = defaultdict(list)
        for activity in cls.query.filter_by(signoff=None):
            x[activity.location.name].append(activity.patroller)
        return x

    def to_dict(self):
        """ Serializes Activity Object to dictionary

            Args:
                None

            Returns:
                Dictionary

        """
        activity = dict()
        activity['id'] = self.id
        activity['patroller'] = self.patroller.name
        activity['location'] = self.location.name
        activity['signon'] = self.signon.strftime("%Y-%m-%d %H:%M:%S")
        activity['signoff'] = self.signoff.strftime("%Y-%m-%d %H:%M:%S")
        if self.signon and self.signoff:
            activity['hours'] = str(self.signoff - self.signon)
        return activity
