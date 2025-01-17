from flask import Blueprint, render_template, request, redirect, url_for, flash
import pickle
import os
import numpy as np
from cache import cache

bp = Blueprint("predict", __name__, url_prefix="/predict")

# Load the models
model_paths = {
    'length': 'best_model_fish_length_(cm).pkl',
    'weight': 'best_model_fish_weight_(g).pkl',
    'quality': 'best_model_water_quality_score.pkl'
}

models = {}
for key, path in model_paths.items():
    if os.path.exists(path):
        with open(path, 'rb') as model_file:
            models[key] = pickle.load(model_file)
    else:
        models[key] = None

def get_water_quality_category(fish_health_condition_factor):
    if fish_health_condition_factor < 0.8:
        return 'poor'
    elif 0.8 <= fish_health_condition_factor < 1.0:
        return 'fair'
    elif 1.0 <= fish_health_condition_factor < 1.2:
        return 'normal'
    elif 1.2 <= fish_health_condition_factor < 1.4:
        return 'good'
    else:
        print(fish_health_condition_factor)
        print(fish_health_condition_factor < 0.8)
        print(type(fish_health_condition_factor))
        return 'excellent'

@bp.route('/', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            temperature = float(request.form['temperature'])
            turbidity = float(request.form['turbidity'])
            dissolved_oxygen = float(request.form['dissolved_oxygen'])
            ph = float(request.form['ph'])
            ammonia = float(request.form['ammonia'])
            nitrate = float(request.form['nitrate'])

            # Validate the input values
            if not (20 <= temperature <= 35):
                raise ValueError("Temperature must be between 20 and 35°C")
            if not (0 <= turbidity <= 100):
                raise ValueError("Turbidity must be between 0 and 100 NTU")
            if not (0 <= dissolved_oxygen <= 20):
                raise ValueError("Dissolved Oxygen must be between 0 and 20 mg/L")
            if not (1 <= ph <= 14):
                raise ValueError("pH must be between 1 and 14")
            if not (0 <= ammonia <= 1):
                raise ValueError("Ammonia must be between 0 and 1 mg/L")
            if not (1 <= nitrate <= 100):
                raise ValueError("Nitrate must be between 1 and 100 mg/L")

            # Prepare the data for prediction
            input_data = [[temperature, turbidity, dissolved_oxygen, ph, ammonia, nitrate]]

            # Make predictions
            fish_length = models['length'].predict(input_data)[0] if models['length'] else "Model not available"
            fish_weight = models['weight'].predict(input_data)[0] if models['weight'] else "Model not available"
            water_quality = models['quality'].predict(input_data)[0] if models['quality'] else "Model not available"

            if isinstance(fish_length, (np.float32, float)) and isinstance(fish_weight, (np.float32, float)):
                fish_condition_factor = (100 * fish_weight) / (fish_length ** 3)
            else:
                fish_condition_factor = "Cannot compute"

            # Get water quality category
            if isinstance(fish_condition_factor, (np.float32, float)):
                water_quality_category = get_water_quality_category(fish_condition_factor)
            else:
                water_quality_category = "Cannot determine"

            predictions = {
                'length': fish_length,
                'weight': fish_weight,
                'quality': water_quality,
                'quality_category': water_quality_category
            }

            return render_template(
                'pages/smart_cultivation_system/predict.html',
                predictions=predictions,
                fish_condition_factor=fish_condition_factor
            )
        except ValueError as e:
            flash(str(e))
            return redirect(url_for('predict.predict'))
    return render_template('pages/smart_cultivation_system/predict.html', predictions=None, fish_condition_factor=None)
