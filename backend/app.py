"""
Flask Backend for Aadhaar Enrolment Intelligence System (AEIS)
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import traceback

from config import HOST, PORT, DEBUG, CORS_ORIGINS, DEFAULT_CSV_PATH
from data_loader import load_data, validate_uploaded_file, get_data_info
from preprocessing import preprocess_data, filter_by_date_range, filter_by_pincode
from analysis import run_full_analysis
from anomaly_model import run_anomaly_detection
from visualization import generate_all_visualizations

app = Flask(__name__)
CORS(app, origins=CORS_ORIGINS)

# Global data store (in production, use proper database)
current_data = None


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'AEIS Backend',
        'version': '1.0.0'
    })


@app.route('/api/load-default-data', methods=['POST'])
def load_default_data():
    """Load and process the default dataset"""
    global current_data
    
    try:
        # Load data
        df = load_data(DEFAULT_CSV_PATH)
        
        # Preprocess
        df = preprocess_data(df)
        
        # Store globally
        current_data = df
        
        # Get basic info
        info = get_data_info(df)
        
        return jsonify({
            'success': True,
            'message': 'Data loaded and preprocessed successfully',
            'data_info': info
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error loading data: {str(e)}',
            'traceback': traceback.format_exc()
        }), 500


@app.route('/api/upload-data', methods=['POST'])
def upload_data():
    """Handle CSV file upload"""
    global current_data
    
    if 'file' not in request.files:
        return jsonify({
            'success': False,
            'message': 'No file provided'
        }), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({
            'success': False,
            'message': 'No file selected'
        }), 400
    
    try:
        # Save temporarily
        temp_path = os.path.join('data', 'temp_upload.csv')
        os.makedirs('data', exist_ok=True)
        file.save(temp_path)
        
        # Validate and load
        success, message, df, info = validate_uploaded_file(temp_path)
        
        if not success:
            return jsonify({
                'success': False,
                'message': message
            }), 400
        
        # Preprocess
        df = preprocess_data(df)
        current_data = df
        
        # Clean up temp file
        os.remove(temp_path)
        
        return jsonify({
            'success': True,
            'message': 'File uploaded and processed successfully',
            'data_info': info
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error processing upload: {str(e)}',
            'traceback': traceback.format_exc()
        }), 500


@app.route('/api/analyze', methods=['POST'])
def analyze_data():
    """Run full analysis on current data"""
    global current_data
    
    if current_data is None:
        return jsonify({
            'success': False,
            'message': 'No data loaded. Please load data first.'
        }), 400
    
    try:
        # Get filter parameters
        params = request.json or {}
        start_date = params.get('start_date')
        end_date = params.get('end_date')
        pincodes = params.get('pincodes')
        
        # Apply filters
        df = current_data.copy()
        if start_date or end_date:
            df = filter_by_date_range(df, start_date, end_date)
        if pincodes:
            df = filter_by_pincode(df, pincodes)
        
        # Run analysis
        analysis_results = run_full_analysis(df)
        
        return jsonify({
            'success': True,
            'analysis': analysis_results
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error during analysis: {str(e)}',
            'traceback': traceback.format_exc()
        }), 500


@app.route('/api/detect-anomalies', methods=['POST'])
def detect_anomalies():
    """Run anomaly detection on current data"""
    global current_data
    
    if current_data is None:
        return jsonify({
            'success': False,
            'message': 'No data loaded. Please load data first.'
        }), 400
    
    try:
        # Get filter parameters
        params = request.json or {}
        start_date = params.get('start_date')
        end_date = params.get('end_date')
        
        # Apply filters
        df = current_data.copy()
        if start_date or end_date:
            df = filter_by_date_range(df, start_date, end_date)
        
        # Run anomaly detection
        anomaly_results = run_anomaly_detection(df)
        
        return jsonify({
            'success': True,
            'anomalies': anomaly_results
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error during anomaly detection: {str(e)}',
            'traceback': traceback.format_exc()
        }), 500


@app.route('/api/visualizations', methods=['POST'])
def generate_visualizations():
    """Generate all visualizations"""
    global current_data
    
    if current_data is None:
        return jsonify({
            'success': False,
            'message': 'No data loaded. Please load data first.'
        }), 400
    
    try:
        # Get parameters
        params = request.json or {}
        start_date = params.get('start_date')
        end_date = params.get('end_date')
        pincodes = params.get('pincodes')
        color_theme = params.get('color_theme', 'default')
        include_anomalies = params.get('include_anomalies', False)
        
        # Apply filters
        df = current_data.copy()
        if start_date or end_date:
            df = filter_by_date_range(df, start_date, end_date)
        if pincodes:
            df = filter_by_pincode(df, pincodes)
        
        # Generate anomaly data if requested
        anomaly_data = None
        if include_anomalies:
            anomaly_data = run_anomaly_detection(df)
        
        # Generate visualizations
        charts = generate_all_visualizations(df, anomaly_data, color_theme)
        
        return jsonify({
            'success': True,
            'visualizations': charts
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error generating visualizations: {str(e)}',
            'traceback': traceback.format_exc()
        }), 500


@app.route('/api/filters/pincodes', methods=['GET'])
def get_pincodes():
    """Get list of available pincodes"""
    global current_data
    
    if current_data is None:
        return jsonify({
            'success': False,
            'message': 'No data loaded'
        }), 400
    
    pincodes = sorted(current_data['pincode'].unique().tolist())
    return jsonify({
        'success': True,
        'pincodes': pincodes
    })


@app.route('/api/filters/date-range', methods=['GET'])
def get_date_range():
    """Get available date range"""
    global current_data
    
    if current_data is None:
        return jsonify({
            'success': False,
            'message': 'No data loaded'
        }), 400
    
    return jsonify({
        'success': True,
        'date_range': {
            'min': current_data['date'].min().strftime('%Y-%m-%d'),
            'max': current_data['date'].max().strftime('%Y-%m-%d')
        }
    })


@app.route('/api/export/csv', methods=['POST'])
def export_csv():
    """Export current analysis as CSV"""
    global current_data
    
    if current_data is None:
        return jsonify({
            'success': False,
            'message': 'No data loaded'
        }), 400
    
    try:
        params = request.json or {}
        export_type = params.get('type', 'full')  # 'full', 'summary', 'anomalies'
        
        # Generate CSV based on type
        # This is a simplified version - expand as needed
        csv_data = current_data.to_csv(index=False)
        
        return jsonify({
            'success': True,
            'csv_data': csv_data,
            'filename': f'aeis_export_{export_type}.csv'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error exporting data: {str(e)}'
        }), 500


if __name__ == '__main__':
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    # Auto-load default data on startup
    try:
        df = load_data(DEFAULT_CSV_PATH)
        df = preprocess_data(df)
        current_data = df
    except Exception as e:
        pass
    
    app.run(host=HOST, port=PORT, debug=DEBUG)
