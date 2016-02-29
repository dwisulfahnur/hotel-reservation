import datetime
from flask import Blueprint, request, views
from app.core.json import json_respon
from models import Reservation
from flask.ext.login import login_required, current_user

reservation_views = Blueprint('reservation', __name__, template_folder='../templates')

#LIST ALL RESERVATION
class ReservationHistory(views.MethodView):
    def get(self):
        reservations = Reservation.query.all()
        data = [dict(id = reservation.id,
                     reservation_user = reservation.user.fullname,
                     code = reservation.code,
                     checkin_date = reservation.checkin_date,
                     checkout_date = reservation.checkout_date,
                     room_number = reservation.room_number,
                     adult = reservation.adult,
                     amount = reservation.amount,
                     night = reservation.night,
                     status = reservation.status,
                     checkin_status = reservation.checkin_status,
                     checkout_status = reservation.checkout_status)
                     for reservation in Reservation.query.all()]
        return json_respon(data=data)
reservation_views.add_url_rule('/reservation', view_func=ReservationHistory.as_view('reservation'))

#DETAIL RESERVATION
class ReservationDetail(views.MethodView):
    #Show detail of reservation
    def get(self, id):
        reservation = Reservation.query.get(id)
        if not reservation:
            return abort(404)
        data = dict(id = reservation.id,
                    reservation_user = reservation.user.fullname,
                    code = reservation.code,
                    checkin_date = reservation.checkin_date,
                    checkout_date = reservation.checkout_date,
                    room_number = reservation.room_number,
                    adult = reservation.adult,
                    amount = reservation.amount,
                    night = reservation.night,
                    status = reservation.status,
                    checkin_status = reservation.checkin_status,
                    checkout_status = reservation.checkout_status)
        return json_respon(data=data)
    #Update detail of reservation
    def put(self, id):
        reservation = Reservation.query.get(id)
        if not reservation:
            return abort(404)
        try:
            reservation.id = request.args.get(id = reservation.id)
            reservation.user.fullname = request.args.get(reservation_user = reservation.user)
            reservation.code = request.args.get(code = reservation.code)
            reservation.checkin.date = request.args.get(checkin_date = reservation.checkin_date)
            reservation.checkout.date = request.args.get(checkout_date = reservation.checkout_date)
            reservation.room_number = request.args.get(room_number = reservation.room_number)
            reservation.adult = request.args.get(adult = reservation.adult)
            reservation.amount = request.args.get(amount = reservation.amount)
            reservation.night = request.args.get(night = reservation.night)
            reservation.status = request.args.get(status = reservation.status)
            reservation.checkin_status = request.args.get(checkin_status = reservation.checkin_status)
            reservation.checkout_status = request.args.get(checkout_status = reservation.checkout_status)
            db.session.commit()
        except IntegrityError as e:
            return json_respon(code=400,
                               msg=e.message)
        return json_respon(msg="Reservation updated succesfully")

    #Delete one reservation
    def delete(self, id):
        reservation = Reservation.query.get(id)
        if not reservation:
            return abort(404)
        try:
            db.session.delete(reservation)
            db.session.commit()
        except IntegrityError as e:
            return json_respon(code=400,
                               msg=e.message)
        return json_respon(msg="Reservation deleted succesfully")
reservation_view = login_required(ReservationDetail.as_view('reservation_detail'))
reservation_views.add_url_rule('/reservation/<int:id>', view_func=reservation_view, methods=["GET", "PUT", "DELETE"])
