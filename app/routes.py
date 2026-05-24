from flask import Blueprint, request, jsonify,render_template
import dashaflow
from app.calculators.constants import RASHI_MAP
from app.calculators.engines import chart_class

api_bp = Blueprint('api', __name__)

@api_bp.route('/', methods=['GET'])
def start_chart():
    return render_template('index.html', result=None)

@api_bp.route('/chart', methods=['POST'])
def handle_form_submission():
    # Flask reads standard HTML form elements via request.form
    birth_data = {
        "dob": request.form.get('dob'),
        "time": request.form.get('time'),
        "lat": float(request.form.get('lat', 0)),
        "lon": float(request.form.get('lon', 0)),
        "timezone": request.form.get('timezone', 'Asia/Kolkata')
    }
    
    try:
        chart = chart_class(birth_data)
        d1_data = chart.d1
        # Pass your compiled object directly straight into your newly minted design layout
        return render_template('d1.html', result=d1_data)
    
    except Exception as e:
        return f"Calculation failed: {str(e)}", 500