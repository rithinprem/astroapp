from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
from app.calculators.engines import chart_class

api_bp = Blueprint('api', __name__)

@api_bp.route('/', methods=['GET'])
def start_chart():
    return render_template('index.html', result=None)

# 1. POST ROUTE: Only processes the incoming form data and redirects
@api_bp.route('/chart', methods=['POST'])
def handle_form_submission():
    birth_data = {
        "dob": request.form.get('dob'),
        "time": request.form.get('time'),
        "lat": float(request.form.get('lat', 0)),
        "lon": float(request.form.get('lon', 0)),
        "timezone": request.form.get('timezone', 'Asia/Kolkata')
    }
    session['birth_data'] = birth_data  # Store the birth data safely in user's session
    
    # Redirect to the clean GET route of this same blueprint
    return redirect(url_for('api.show_d1_chart'))

# 2. GET ROUTE for D1: Safely renders the D1 chart page
@api_bp.route('/chart', methods=['GET'])
def show_d1_chart():
    birth_data = session.get('birth_data')
    
    # Safety Check: Redirect to form index if session expired or doesn't exist
    if not birth_data:
        return redirect(url_for('api.start_chart'))
        
    try:
        chart = chart_class(birth_data)
        d1_data = chart.d1_chart_engine()
        return render_template('d1.html', result=d1_data)
    except Exception as e:
        return f"Calculation failed: {str(e)}", 500
    
# 3. GET ROUTE for D9: Safely renders the D9 chart page
@api_bp.route('/d9', methods=['GET'])
def d9_chart():
    birth_data = session.get('birth_data')
    
    # Safety Check: Redirect to form index if session doesn't exist
    if not birth_data:
        return redirect(url_for('api.start_chart'))
        
    try:
        chart = chart_class(birth_data)
        d9_data = chart.d9_chart_engine()
        return render_template('d9.html', result=d9_data)
    except Exception as e:
        return f"Calculation failed: {str(e)}", 500