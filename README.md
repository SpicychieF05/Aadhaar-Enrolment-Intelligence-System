# Aadhaar Enrolment Intelligence System (AEIS)

![AEIS](https://img.shields.io/badge/AEIS-Government%20of%20India-blue)
![Status](https://img.shields.io/badge/Status-Production%20Ready-green)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Hackathon](https://img.shields.io/badge/UIDAI%20Hackathon-2026-orange)

## 🏆 Hackathon Information

**Event:** UIDAI Data Hackathon 2026  
**Team ID:** UIDAI_8374  
**Team Members:**
- [Chirantan Mallick](https://github.com/SpicychieF05/)
- [Akash Mondal](https://github.com/AkashMondal27)
- [Sahin Sultan](https://github.com/Sahin-sultan)
- [Piyal Baray](https://github.com/PiyalBaray)

---

## 🏛️ Overview

The **Aadhaar Enrolment Intelligence System (AEIS)** is a government-grade analytical web platform designed to analyze Aadhaar enrolment data at district and pincode levels. The system identifies trends, demographic patterns, seasonality, and anomalies, presenting insights through a user-friendly, accessible web dashboard.

### Key Features

- ✅ **Explainable Analytics**: Statistical analysis with full transparency
- ✅ **Anomaly Detection**: Z-score and rolling window methods
- ✅ **Interactive Dashboard**: Government-style UI with accessibility features
- ✅ **Data Visualization**: Comprehensive charts and graphs
- ✅ **Authentication System**: Login, signup, and password recovery
- ✅ **Export Capabilities**: CSV and PNG export functionality
- ✅ **Accessibility**: Font scaling, high contrast, keyboard navigation

## 📊 Dataset

**Source**: Real Aadhaar portal data from Birbhum District, West Bengal  
**Source Platform**: [Data.gov.in](https://www.data.gov.in)  
**Location**: `data/enrolment_dataset_birbhum.csv`

### Dataset Schema

| Column | Description |
|--------|-------------|
| date | Enrolment date (DD-MM-YYYY) |
| state | State name (West Bengal) |
| district | District name (Birbhum) |
| pincode | Postal code |
| age_0_5 | Enrolments for age 0-5 years |
| age_5_17 | Enrolments for age 5-17 years |
| age_18_greater | Enrolments for age 18+ years |

## 🏗️ System Architecture

### Technology Stack

**Frontend**:
- HTML5, CSS3, Vanilla JavaScript
- Government-style responsive design
- No frameworks (by specification)

**Backend**:
- Python 3.8+
- Flask web framework
- Statistical analysis with pandas, numpy, scipy
- Visualization with matplotlib, seaborn

**Data Processing**:
- pandas for data manipulation
- numpy for numerical operations
- scipy for statistical methods

## 📁 Directory Structure

```
project02/
│
├── backend/
│   ├── app.py                  # Flask REST API server
│   ├── data_loader.py          # Data loading and validation
│   ├── preprocessing.py        # Data preprocessing pipeline
│   ├── analysis.py             # Statistical analysis engine
│   ├── anomaly_model.py        # Explainable anomaly detection
│   ├── visualization.py        # Chart generation (base64)
│   └── config.py               # Configuration settings
│
├── data/
│   └── enrolment_dataset_birbhum.csv  # Official Birbhum district dataset
│
├── frontend/
│   ├── index.html              # Main analytics dashboard
│   ├── auth.html               # Authentication page
│   ├── styles.css              # Government-style dashboard CSS
│   ├── auth.css                # Authentication page CSS
│   ├── script.js               # Dashboard logic and API calls
│   └── auth.js                 # Authentication logic
│
├── README.md                   # Project documentation
├── requirements.txt            # Python dependencies
└── start_backend.bat           # Windows server startup script
```
│
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── AI_SPEC.md                  # System specification
```

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Edge)

### Step 1: Clone/Download the Project

```bash
cd D:\Aadhar-hackathon\project02
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Verify Dataset

Ensure the dataset is located at:
```
D:\Aadhar-hackathon\project02\data\enrolment_dataset_birbhum.csv
```

### Step 5: Start the Backend Server

```bash
cd backend
python app.py
```

Expected output:
```
Loading default dataset from: D:\Aadhar-hackathon\project02\data\enrolment_dataset_birbhum.csv
✓ Data loaded successfully: 2863 records
✓ Date range: 01-06-2025 to 09-09-2025
✓ Total enrolments: XXXXX

🚀 AEIS Backend starting on http://0.0.0.0:5000
```

### Step 6: Open the Frontend

1. Navigate to `frontend/` directory
2. Open `auth.html` in your web browser
3. Or use a local server:
   ```bash
   # Python built-in server
   cd frontend
   python -m http.server 8080
   ```
4. Access at `http://localhost:8080/auth.html`

## 🔐 Authentication

### Demo Credentials

For testing purposes, use these credentials:

- **User ID**: `admin`
- **Email**: `admin@aeis.gov.in`
- **Password**: `admin123`

### Features

- **Login**: Standard authentication
- **Sign Up**: OTP-based registration (demo OTP: `123456`)
- **Forgot Password**: Multi-step OTP verification (demo OTP: `123456`)

**Note**: In production, integrate with Supabase or government authentication system.

## 📈 Using the Dashboard

### 1. Load Data

**Option A: Default Dataset**
- Click "Load Default Data" to use the pre-configured Birbhum dataset

**Option B: Upload Custom Dataset**
- Click "Choose File" to upload your own CSV
- Must follow the required schema (see Dataset section)
- Click "Process Data" to analyze

### 2. Apply Filters

- **Date Range**: Filter by start and end dates
- **Pincode**: Select specific pincodes
- **Color Theme**: Default, high contrast, or print-friendly
- Click "Apply Filters" to update visualizations

### 3. View Analytics

The dashboard displays:
- **Summary Statistics**: Total enrolments, unique pincodes, averages
- **Daily Trends**: Line chart of enrolments over time
- **Age Distribution**: Bar and pie charts by age group
- **Geographic Analysis**: Top pincodes by volume
- **Temporal Patterns**: Monthly trends, day-of-week patterns
- **Age Over Time**: Stacked area chart

### 4. Detect Anomalies

- Click "Detect Anomalies" button
- View:
  - Statistical anomaly detection results
  - Visualization with highlighted anomalies
  - Detailed explanations for each anomaly
  - Methodology description

### 5. Export Data

- **Export Full Data**: Complete dataset as CSV
- **Export Summary**: Aggregated statistics as CSV
- **Export Charts**: Individual charts as PNG images

### 6. Accessibility Features

- **Font Size**: A+ / A- buttons to adjust text size
- **High Contrast**: Toggle for better visibility
- **Print Mode**: Optimized printing (Ctrl+P)
- **Keyboard Navigation**: Full keyboard support

## 🔍 Analytics Methodology

### Statistical Analysis

All analysis uses **explainable statistical methods**:

1. **Descriptive Statistics**: Mean, median, standard deviation, min/max
2. **Temporal Analysis**: Daily, weekly, monthly aggregations
3. **Geographic Analysis**: Pincode and district level insights
4. **Correlation Analysis**: Age group relationships

### Anomaly Detection

Two complementary methods:

1. **Z-Score Analysis**
   - Identifies days that deviate > 2.5 standard deviations from mean
   - Flags both high and low anomalies
   - Fully transparent and explainable

2. **Rolling Window Analysis**
   - Uses 7-day moving average and standard deviation
   - Compares each day to recent trends
   - Adapts to changing patterns

**No black-box ML models** - all methods are statistical and interpretable.

## 🎨 Design Philosophy

AEIS follows **government design standards**:

- ✅ Clean, professional appearance
- ✅ Navy blue primary color (#1e3a8a)
- ✅ White and light grey backgrounds
- ✅ No gradients or glassmorphism
- ✅ Subtle, purposeful animations
- ✅ High readability and accessibility
- ✅ Print-friendly layouts

## 🔧 API Endpoints

### Backend REST API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/load-default-data` | POST | Load default dataset |
| `/api/upload-data` | POST | Upload custom CSV |
| `/api/analyze` | POST | Run statistical analysis |
| `/api/detect-anomalies` | POST | Detect anomalies |
| `/api/visualizations` | POST | Generate charts |
| `/api/filters/pincodes` | GET | Get available pincodes |
| `/api/filters/date-range` | GET | Get date range |
| `/api/export/csv` | POST | Export data as CSV |

## 🧪 Testing

### Manual Testing Checklist

- [ ] Backend starts without errors
- [ ] Default data loads successfully
- [ ] Authentication pages work (login, signup, forgot password)
- [ ] Dashboard loads after login
- [ ] All visualizations render correctly
- [ ] Filters apply and update charts
- [ ] Anomaly detection runs successfully
- [ ] Export functions work (CSV and PNG)
- [ ] Accessibility features function properly
- [ ] Responsive design works on different screen sizes

### Test with Sample Queries

1. Load default data → View all analytics
2. Filter by date range (e.g., September 2025)
3. Filter by specific pincode (e.g., 731123)
4. Run anomaly detection
5. Export summary CSV
6. Export individual charts

## 🐛 Troubleshooting

### Backend Issues

**Error: "Data file not found"**
- Ensure CSV is at correct path: `data/enrolment_dataset_birbhum.csv`
- Check file permissions

**Error: "Module not found"**
- Run `pip install -r requirements.txt`
- Verify virtual environment is activated

**Port already in use**
- Change PORT in `backend/config.py`
- Or stop process using port 5000

### Frontend Issues

**"Failed to connect to backend"**
- Ensure backend is running on port 5000
- Check browser console for CORS errors
- Verify API_BASE_URL in `script.js`

**Charts not displaying**
- Check browser console for errors
- Ensure matplotlib backend is set to 'Agg'
- Verify visualization.py imports correctly

**Authentication not working**
- Check sessionStorage in browser DevTools
- Verify demo credentials match those in `auth.js`

---

## 👥 Team

**UIDAI Data Hackathon 2026**  
**Team ID:** UIDAI_8374

### Team Members:
- **[Chirantan Mallick](https://github.com/SpicychieF05/)** - Full Stack Developer
- **[Akash Mondal](https://github.com/AkashMondal27)** - Backend Developer
- **[Sahin Sultan](https://github.com/Sahin-sultan)** - Data Analyst
- **[Piyal Baray](https://github.com/PiyalBaray)** - Frontend Developer

---

## 🙏 Acknowledgments

- **Event**: UIDAI Data Hackathon 2026
- **Data Source**: [Data.gov.in](https://www.data.gov.in)
- **Organization**: UIDAI (Unique Identification Authority of India)
- **Dataset**: Official Aadhaar enrolment data from Birbhum District, West Bengal

---

## 📝 License

Government of India | Unique Identification Authority of India  
Developed for UIDAI Data Hackathon 2026

---

**Developed and validated using official Birbhum (West Bengal) Aadhaar datasets via Data.gov.in**

&copy; 2026 Government of India | Unique Identification Authority of India
