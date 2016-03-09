import datetime
from flask import Blueprint, render_template, request, redirect, url_for, abort, views
from app.core.json import json_respon, jsonify
from app.core.db import db
from models import Hotels, Country, Province, City
from sqlalchemy.exc import IntegrityError
from flask.ext.login import login_required, current_user

hotel_views = Blueprint('hotel', __name__, template_folder='../templates')

#LIST HOTEL
class Hotel(views.MethodView):
    def get(self):
        hotels = Hotels.query.all()
        data = [dict(href= url_for('.hotel', id=hotel.id),
                     hotel_id=hotel.name)
                     for hotel in hotels]
        return json_respon(data=data)
    def delete(self):
        hotels = Hotels.query.all()
        try:
            [db.session.delete(Hotels.query.get(hotel.id)) for hotel in hotels]
            db.session.commit()
        except IntegrityError as e:
            return json_respon(code=400,
                               msg=e.message)
hotel_view = Hotel.as_view('hotel')
hotel_views.add_url_rule('/hotel', view_func=hotel_view, methods=["GET", "DELETE"])

class HotelDetail(views.MethodView):
    #DETAIL SINGLE HOTEL
    def get(self, id):
        hotel = Hotels.query.get(id)
        if not hotel:
            return abort(404)
        data = dict(name = hotel.name,
                    address = hotel.address,
                    zipcode = hotel.zipcode,
                    country = hotel.country.country,
                    province = hotel.province.province,
                    city = hotel.city.city)
        return json_respon(data=data)
    #UPDATE single hotel
    @login_required
    def put(self, id):
        hotel = Hotels.query.get(id)
        if not hotel:
            return abort(404)
        try:
            hotel.name = request.args.get('name', hotel.name)
            hotel.address = request.args.get('address', hotel.address)
            hotel.zipcode = request.args.get('zipcode', hotel.zipcode)
            hotel.country = request.args.get('country', hotel.country)
            hotel.province = request.args.get('province', hotel.province)
            hotel.city = request.args.get('city', hotel.city)
            db.session.commit()
        except IntegrityError as e:
            return json_respon(code=400,
                               msg=e.message)
        return json_respon(msg="hotel update succesfully")
    #DELETE SINGLE HOTEL
    @login_required
    def delete(self, id):
        hotel = Hotels.query.get(id)
        try:
            db.session.delete(hotel)
            db.session.commit()
        except IntegrityError as e:
            return json_respon(code=400,
                               msg=e.message)
        return json_respon(msg="hotel deleted succesfully")
hotel_view = HotelDetail.as_view('hotel_detail')
hotel_views.add_url_rule('/hotel/<int:id>', view_func=hotel_view, methods=["GET", "PUT", "DELETE"])

#CREATE A NEW HOTEL
class NewHotel(views.MethodView):
    def post(self):
        countries = Country.query.all()
        provincies = Province.query.all()
        cities = City.query.all()

        name = request.args.get('name', None)
        address = request.args.get('address', None)
        zipcode = request.args.get('zipcode', None)
        country = request.args.get('country', None)
        province = request.args.get('province', None)
        city = request.args.get('city', None)
        hotel = Hotels(name, address, zipcode, city, province, country)
        try:
            db.session.add(hotel)
            db.session.commit()
        except IntegrityError as e:
            return json_respon(code=400,
                               msg=e.message)
        return json_respon(msg="Hotel submitted successfully.")
#user_view = login_required(NewHotel.as_view('new_hotel'))
hotel_view = login_required(NewHotel.as_view('new_hotel'))
hotel_views.add_url_rule('/hotel/new_hotel', view_func=hotel_view, methods=["POST"])
