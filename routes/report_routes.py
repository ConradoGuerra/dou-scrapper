from flask import Blueprint
from service.create_report import create_report

report_bp = Blueprint('report_bp', __name__)

@report_bp.route('/')
def home():
    return create_report()
