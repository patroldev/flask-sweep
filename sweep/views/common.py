"""
File: common.py
Purpose: UI routes for the app
"""
import csv
try:
    import StringIO
except ImportError:
    from io import StringIO

from flask import render_template, redirect, url_for, request, Blueprint, send_file
from sweep import db
from sweep.models import Locations, Patrollers, Activity
from datetime import datetime

common = Blueprint('common', __name__)


@common.route("/")
@common.route("/index.html")
def main():
    active_patrollers = Activity.active_patrollers()
    return render_template("index.html",
                           Patrollers=Patrollers.query.all(),
                           Locations=Locations.query.order_by(Locations.name),
                           active_patrollers=active_patrollers)


@common.route("/patrollers.html")
def edit_patrollers():
    return render_template("patrollers.html", Patrollers=Patrollers.query.all())


@common.route("/locations.html")
def edit_locations():
    return render_template("locations.html", Locations=Locations.query.order_by(Locations.name))


@common.route("/update_patrollers", methods=["POST"])
def update_patrollers():
    if request.form['button'] == 'update':
        if request.form['patroller-select'] == "new-patroller":
            p = Patrollers(name=request.form['patroller-name'],
                           status=request.form['status'])
        else:
            p = Patrollers.query.filter_by(name=request.form['patroller-select'])
            if len(request.form['patroller-name']) > 0:
                p.name = request.form['patroller-name']
            p.status = request.form['status']
        db.session.add(p)
        db.session.commit()
    elif request.form['button'] == 'delete':
        if request.form['patroller-select'] != "new-patroller":
            p = Patrollers.get(Patrollers.name == request.form['patroller-select'])
            db.session.delete(p)
            db.session.commit()
    else:
        return "Error posting data. Please report this issue to the developer."
    return redirect(url_for("common.edit_patrollers"))


@common.route("/update_locations", methods=["POST"])
def update_locations():
    if request.form['button'] == 'update':
        if request.form['select-location'] == "new-location":
            l = Locations(name=request.form['location-name'])
        else:
            l = Locations.get(Locations.name == request.form['select-location'])
            if len(request.form['location-name']) > 0:
                l.name = request.form['location-name']
        db.session.add(l)
        db.session.commit()
    elif request.form['button'] == 'delete':
        if request.form['select-location'] != "new-location":
            l = Locations.get(Locations.name == request.form['select-location'])
            db.session.delete(l)
            db.session.commit()
    else:
        return "Error posting data. Please report this issue to the developer."
    return redirect(url_for("common.edit_locations"))


@common.route("/activity", methods=["POST"])
def update_activity():
    patroller_id = request.form.get("patroller-id", None)
    location_name = request.form.get("location-name", None)
    leader = request.form.get("is_leader", False)
    is_leader = bool(leader)

    if request.form['button'] == 'sign-in':
        p = Patrollers.query.filter_by(id=patroller_id).first()
        l = Locations.query.filter_by(name=location_name).first()
        a = Activity(patroller=p, location=l,
                     is_leader=is_leader, signon=datetime.now())
    elif request.form['button'] == 'sign-out':
        p = Patrollers.query.filter_by(id=patroller_id).first()
        a = Activity.query.filter(Activity.patroller == p, Activity.signoff == None).first()
        a.signoff = datetime.now()
    db.session.add(a)
    db.session.commit()
    return redirect("/index.html")


@common.route("/reports.html")
def reports():
    return render_template("reports.html", patrollers=Patrollers.query.order_by(Patrollers.name))


@common.route("/generate_report", methods=['POST'])
def generate_report():
    r = request.form.copy()
    if r['select-patroller'] == "all_patrollers":
        a = Activity.query.filter(Activity.signon >= r['start'], Activity.signoff <= r['end'])
    else:
        p = Patrollers.query.filter(name=r['select-patroller']).first()
        a = Activity.query.filter(Activity.patroller == p, Activity.signon >= r['start'], Activity.signoff <= r['end'])
    data = [activity.to_dict() for activity in a]
    if not data:
        return 204
    writer = StringIO.StringIO()
    csv_writer = csv.DictWriter(writer,
                                fieldnames=['id', 'patroller', 'location', 'is_leader',
                                            'signon', 'signoff', 'hours'])
    csv_writer.writeheader()
    csv_writer.writerows(data)
    writer.seek(0)
    return send_file(writer, attachment_filename='{0}.csv'.format(r['report-name']),
                     as_attachment=True)
