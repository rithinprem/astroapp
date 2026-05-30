from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
from app.calculators.engines import chart_class
from app.db import load_db  # Import the MongoDB client from db.py

api_bp = Blueprint('api', __name__)

@api_bp.route('/', methods=['GET'])
def start_chart():
    return render_template('index.html', result=None)

# 1. POST ROUTE: Only processes the incoming form data and redirects
@api_bp.route('/chart', methods=['POST'])
def handle_form_submission():
    birth_data = {
        "full_name": request.form.get('fullname'),
        "dob": request.form.get('dob'),
        "time": request.form.get('time'),
        "lat": float(request.form.get('lat', 0)),
        "lon": float(request.form.get('lon', 0)),
        "timezone": request.form.get('timezone', 'Asia/Kolkata')
    }

    session['birth_data'] = birth_data  # Store the birth data safely in user's session

    birth_data_copy = birth_data.copy()  # Create a copy to avoid modifying the session data
    client = load_db()
    db = client['astroapp']
    users = db['astroapp_people']
    id = birth_data_copy['dob']+birth_data_copy['time']
    birth_data_copy['id'] = id
    users.create_index([("id", 1)], unique=True)
    try:
        users.insert_one(birth_data_copy)
    except:
        pass  # Ignore duplicate key errors for simplicity
    
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
        birth_data.pop('full_name', None)  # Remove full_name from birth_data before processing
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
        birth_data.pop('full_name', None)  # Remove full_name from birth_data before processing
        chart = chart_class(birth_data)
        d9_data = chart.d9_chart_engine()
        return render_template('d9.html', result=d9_data)
    except Exception as e:
        return f"Calculation failed: {str(e)}", 500

# 4. GET ROUTE for D30: Safely renders the D30 chart page
@api_bp.route('/d30', methods=['GET'])
def d30_chart():
    birth_data = session.get('birth_data')
    
    # Safety Check: Redirect to form index if session doesn't exist
    if not birth_data:
        return redirect(url_for('api.start_chart'))
        
    try:
        birth_data.pop('full_name', None)  # Remove full_name from birth_data before processing
        chart = chart_class(birth_data)
        d30_data = chart.d30_chart_engine()
        return render_template('d30.html', result=d30_data)
    except Exception as e:
        return f"Calculation failed: {str(e)}", 500
    

@api_bp.route('/d7', methods=['GET'])
def d7_chart():
    birth_data = session.get('birth_data')
    
    # Safety Check: Redirect to form index if session doesn't exist
    if not birth_data:
        return redirect(url_for('api.start_chart'))
        
    try:
        birth_data.pop('full_name', None)  # Remove full_name from birth_data before processing
        chart = chart_class(birth_data)
        d7_data = chart.d7_chart_engine()
        return render_template('d7.html', result=d7_data)
    except Exception as e:
        return f"Calculation failed: {str(e)}", 500

@api_bp.route('/d4', methods=['GET'])
def d4_chart():
    birth_data = session.get('birth_data')
    
    # Safety Check: Redirect to form index if session doesn't exist
    if not birth_data:
        return redirect(url_for('api.start_chart'))
        
    try:
        birth_data.pop('full_name', None)  # Remove full_name from birth_data before processing
        chart = chart_class(birth_data)
        d4_data = chart.d4_chart_engine()
        return render_template('d4.html', result=d4_data)
    except Exception as e:
        return f"Calculation failed: {str(e)}", 500


@api_bp.route('/get_saved_people', methods=['GET'])
def get_saved_people():
    client = load_db()
    db = client['astroapp']
    users = db['astroapp_people']
    data = []
    for doc in users.find({}):
        doc.pop('_id')
        data.append(doc)
    return jsonify(data)