from sanic import Sanic,Blueprint
from data_ins import data_collection

# urls for the file
login = Blueprint(name = "twad_insertation", url_prefix="/zogx_test")

#child url
login.add_route(data_collection.user_details,"/user--details",methods=["POST"])

login.add_route(data_collection.user_login,"/user-login",methods=["POST"])

login.add_route(data_collection.password_reset,"/password-reset",methods=["POST"])

login.add_route(data_collection.forgot_password,"/forgot-password",methods=["POST"])

login.add_route(data_collection.otp_verfiy,"/otp_verfiy",methods=["POST"])