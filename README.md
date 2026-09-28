# 🧠 Parkinson's Disease Speech Detection System

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.x-lightgrey.svg)](https://flask.palletsprojects.com/)
[![React](https://img.shields.io/badge/React-19-61dafb.svg)](https://react.dev/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.3%2B-orange.svg)](https://scikit-learn.org/)
[![pyAudioAnalysis](https://img.shields.io/badge/pyAudioAnalysis-0.3%2B-green.svg)](https://github.com/tyiannak/pyAudioAnalysis)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An end-to-end, non-invasive screening platform designed to assist in early detection of **Parkinson's Disease (PD)** using acoustic voice analysis and machine learning. 

Parkinson's disease frequently impairs vocal function—often years before significant motor symptoms manifest—causing vocal tremor, dysphonic variation, reduced loudness, and pitch instability. This application provides an intuitive three-step web interface to capture voice samples (via microphone or file upload), extract key acoustic parameters using short-time Fourier feature extraction, classify the audio via a trained Machine Learning model, and display immediate risk scores along with nearby specialist medical recommendations.

---

## 📑 Table of Contents

- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Tech Stack](#-tech-stack)
- [Project Directory Structure](#-project-directory-structure)
- [Acoustic Analysis & ML Pipeline](#-acoustic-analysis--ml-pipeline)
- [API Reference](#-api-reference)
- [Installation & Getting Started](#-installation--getting-started)
  - [Prerequisites](#prerequisites)
  - [1. Backend Setup](#1-backend-setup)
  - [2. Frontend Setup](#2-frontend-setup)
- [Application Workflow](#-application-workflow)
- [Demo vs Full ML Mode](#-demo-vs-full-ml-mode)
- [Medical Disclaimer](#-medical-disclaimer)

---

## ✨ Key Features

- **Intuitive 3-Step Guided Workflow**:
  1. **Patient Information**: Captures patient metadata (Name, Age, Gender).
  2. **Voice Capture**: Dual-mode input via live in-browser microphone recording or audio file upload (`.wav`, `.mp3`).
  3. **Diagnostic Report**: Dynamic risk evaluation score, clinical interpretation, and healthcare guidance.
- **Acoustic Feature Extraction**: Extracts 19 short-time acoustic voice features (pitch, jitter, shimmer, spectral characteristics) using `pyAudioAnalysis`.
- **Pretrained Machine Learning Classification**: Fast inference utilizing a trained Scikit-Learn classification model (`model_parkinson.pkl`).
- **In-Browser Audio Recording**: High-fidelity voice sampling leveraging the Web Audio API and `MediaRecorder` API with live timer and audio playback.
- **Hospital Referral Recommendations**: Automatically suggests nearby neurological treatment centers and hospitals (customized for Pune region, e.g., Ruby Hall Clinic, Jehangir Hospital, Sahyadri Super Speciality Hospital) if elevated risk is detected.
- **Auditing & History Tracking**: Records screening sessions with client IP, timestamp, and test results via SQLAlchemy ORM.
- **Fully Responsive & Fluid UI**: Modern design featuring fluid typography (`clamp()`), step progress indicators, interactive cards, and zero horizontal overflow across desktop and mobile screens.

---

## 🏗️ System Architecture

```mermaid
flowchart TD
    subgraph Client["Frontend (React 19)"]
        A["Step 1: Patient Information Form"] --> B["Step 2: Voice Input (Mic / Upload)"]
        B --> C["Axios POST /upload or /upload-demo"]
        G["Step 3: Risk Assessment & Hospital Referral"]
    end

    subgraph Server["Backend (Flask REST API)"]
        C --> D["Flask Routes (routes.py)"]
        D --> E{"Mode Selection"}
        E -->|"Production ML"| F1["Asynchronous Diagnose Thread"]
        E -->|"Demo Mode"| F2["Simulated Prediction Thread"]
    end

    subgraph Pipeline["Acoustic Analysis & Machine Learning"]
        F1 --> H["Read Audio (pyAudioAnalysis)"]
        H --> I["Short-time Feature Extraction (50ms window / 25ms step)"]
        I --> J["19 Acoustic Parameters Sliced"]
        J --> K["Feature Scaling (StandardScaler)"]
        K --> L["Model Inference (model_parkinson.pkl)"]
        L --> M["Binary / Risk Output"]
    end

    subgraph Persistence["Database (SQLAlchemy)"]
        M --> DB[("file_results (IP, Timestamp, Result)")]
        F2 --> DB
    end

    M -.->|JSON Response| G
    F2 -.->|JSON Response| G
```

---

## 🛠️ Tech Stack

### **Frontend**
| Technology | Description |
|---|---|
| **React 19** | Component-driven UI library for fast, reactive rendering |
| **React Router v7** | Single Page Application (SPA) client-side routing |
| **Axios** | Promise-based HTTP client for API communication |
| **Web Audio API / MediaRecorder** | In-browser audio streaming and live voice sample recording |
| **Modern CSS3** | Fluid layouts (`clamp()`), animated spinners, responsive step-indicators |

### **Backend**
| Technology | Description |
|---|---|
| **Python 3.8+** | Primary server-side programming language |
| **Flask (v2.x / v1.x)** | Lightweight WSGI web application framework |
| **Flask-CORS** | Cross-Origin Resource Sharing handling for React frontend |
| **Flask-SQLAlchemy** | Object Relational Mapper (ORM) for persistent data storage |
| **Werkzeug** | Secure file handling (`secure_filename`) and WSGI utilities |
| **Gunicorn** | Production-ready WSGI HTTP server |

### **Machine Learning & Audio Processing**
| Technology | Description |
|---|---|
| **Scikit-Learn** | Pre-trained classifier pipeline and feature normalization (`StandardScaler`) |
| **pyAudioAnalysis** | Feature extraction, short-time Fourier audio analysis |
| **NumPy & SciPy** | Multi-dimensional array manipulation and mathematical operations |
| **pydub & eyeD3** | Audio manipulation, format conversions, and audio metadata extraction |

### **Database & Deployment**
| Technology | Description |
|---|---|
| **SQLAlchemy Engine** | Database abstraction layer supporting PostgreSQL or SQLite |
| **Procfile** | Heroku / PaaS web process configuration |

---

## 📁 Project Directory Structure

```text
parkinson_speech/
├── README.md                           # Main project documentation
├── parkinsons-backend/                 # Flask Backend & Machine Learning Engine
│   ├── app.py                          # Flask application factory, CORS, and DB config
│   ├── routes.py                       # REST API route handlers and thread managers
│   ├── models.py                       # SQLAlchemy database models (file_results)
│   ├── Procfile                        # Deployment process definition for Gunicorn
│   ├── requirements.txt                # Legacy dependencies specification
│   ├── requirements-new.txt            # Modern dependency specifications (Python 3.8+)
│   ├── .gitignore                      # Git ignored files for backend
│   └── Parkinson/                      # ML Inference and Audio Signal Processing Module
│       ├── __init__.py                 # Python package marker
│       ├── audio_analyzer.py           # pyAudioAnalysis audio reading & feature extraction
│       ├── ParkinsonCheck.py           # Model loading, feature preprocessing & prediction
│       └── model_parkinson.pkl         # Pretrained Parkinson detection classification model
│
└── parkinsons-frontend/                # React 19 Client Application
    ├── package.json                    # NPM dependencies, scripts, and build metadata
    ├── package-lock.json               # Locked dependency tree
    ├── README.md                       # React template reference
    ├── .gitignore                      # Git ignored files for frontend
    ├── public/                         # Static assets & HTML template
    │   ├── index.html                  # HTML entry point
    │   ├── favicon.ico                 # Web favicon
    │   ├── manifest.json               # Web application manifest
    │   └── robots.txt                  # Search crawler configuration
    └── src/                            # Application source code
        ├── index.js                    # React DOM entry point
        ├── index.css                   # Global baseline CSS styles
        ├── App.js                      # Root component & Route configuration
        ├── App.css                     # Component design, cards, and fluid media queries
        ├── setupTests.js               # Test environment configuration
        ├── reportWebVitals.js          # Performance metric tracking
        └── pages/                      # Application route pages
            ├── FormPage.js             # Step 1: Patient details input form
            ├── VoiceInputPage.js       # Step 2: Microphone recorder & file upload interface
            └── ResultPage.js           # Step 3: Screening outcome & hospital recommendations
```

---

## 🔬 Acoustic Analysis & ML Pipeline

The voice diagnosis pipeline utilizes acoustic feature extraction to detect subtle vocal markers characteristic of early-stage Parkinson's disease:

1. **Audio Ingestion**: Audio files (`.wav` format) are received via multipart file upload or microphone capture.
2. **Short-Time Feature Extraction**:
   - Audio is read using `pyAudioAnalysis.audioBasicIO.readAudioFile`.
   - `audioFeatureExtraction.stFeatureExtraction` applies short-time windowing:
     - **Window Size**: 50 ms ($0.050 \times F_s$)
     - **Step Size**: 25 ms ($0.025 \times F_s$)
3. **Feature Slicing**:
   - The first **19 acoustic feature parameters** are extracted, encompassing fundamental frequency (pitch), energy, zero crossing rate, spectral roll-off, spectral flux, and related voice tremor metrics.
4. **Standardization & Preprocessing**:
   - Extracted features are standardized using `StandardScaler` to match the statistical distribution of the training dataset.
   - Sliced parameters are reshaped to `(-1, 19)` dimensions.
5. **Classification**:
   - The serialized Scikit-Learn classifier (`model_parkinson.pkl`) executes inference and yields the prediction result.

---

## 📡 API Reference

The backend exposes RESTful endpoints for screening and data management:

### 1. `POST /upload`
Submits an audio file for full machine learning analysis.
- **Request Format**: `multipart/form-data`
- **Body Parameter**: `file` (Binary audio file, `.wav`)
- **Processing**: Triggers an asynchronous diagnostic background thread.
- **Response**: `upload done` (HTTP 200)

### 2. `POST /upload-demo`
Submits an audio file for rapid demonstration mode (does not require external C++ audio dependencies).
- **Request Format**: `multipart/form-data`
- **Body Parameter**: `file` (Binary audio file)
- **Response**: `upload done` (HTTP 200)

### 3. `GET /done`
Polls whether the background audio diagnostic thread has finished processing.
- **Response**: `"true"` or `"false"` (HTTP 200)

### 4. `GET /getresult`
Retrieves the screening outcome once processing completes.
- **Response**:
```json
{
  "Parkinson": 1
}
```

### 5. `GET /history`
Retrieves previous screening records matching the requester's IP address.
- **Response**:
```json
{
  "file_results": [
    {
      "filename": "sample_recording.wav",
      "Parkinson": 0
    }
  ]
}
```

### 6. `GET /`
Health check / Home route.
- **Response**: `"Apmycure Homepage"` (HTTP 200)

---

## 🚀 Installation & Getting Started

### Prerequisites

Ensure you have the following installed on your machine:
- **Node.js** (v16.0.0 or higher) and **npm**
- **Python** (v3.8 or higher)
- **Git**
- *(Optional for full audio analysis)*: C++ build tools and `ffmpeg` (for `pyAudioAnalysis` and audio decoding)

---

### 1. Backend Setup

1. **Navigate to the backend directory**:
   ```bash
   cd parkinsons-backend
   ```

2. **Create and activate a virtual environment**:
   - **Windows**:
     ```powershell
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - **macOS / Linux**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install Python dependencies**:
   ```bash
   pip install -r requirements-new.txt
   ```
   > [!TIP]
   > For modern Python versions (3.8 - 3.11), use `requirements-new.txt`. For legacy environments, use `requirements.txt`.

4. **Set the Database URL environment variable**:
   - **Windows (PowerShell)**:
     ```powershell
     $env:DATABASE_URL="sqlite:///parkinsons.db"
     ```
   - **Windows (Command Prompt)**:
     ```cmd
     set DATABASE_URL=sqlite:///parkinsons.db
     ```
   - **macOS / Linux**:
     ```bash
     export DATABASE_URL="sqlite:///parkinsons.db"
     ```
   *(You may also specify a PostgreSQL URI, e.g. `postgresql://user:pass@localhost:5432/parkinson_db`)*

5. **Start the Flask server**:
   ```bash
   python app.py
   ```
   The backend server will run at `http://localhost:5000`.

---

### 2. Frontend Setup

1. **Open a new terminal and navigate to the frontend directory**:
   ```bash
   cd parkinsons-frontend
   ```

2. **Install npm dependencies**:
   ```bash
   npm install
   ```

3. **Start the React development server**:
   ```bash
   npm start
   ```
   The application will open automatically in your browser at `http://localhost:3000`.

---

## 🔄 Application Workflow

```text
[ Step 1: Patient Info ] ──> [ Step 2: Voice Input ] ──> [ Step 3: Diagnostic Report ]
      (Name, Age, Sex)          (Live Mic or .WAV)           (Risk Score & Hospitals)
```

1. **Step 1: Patient Details** (`/`):
   - Enter full name, age, and gender.
   - Click **"Next: Voice Input"**.
2. **Step 2: Voice Sample Collection** (`/voice`):
   - **Option A**: Click **"Start Recording"**, speak a sustained phonation (e.g. holding the vowel sound `/a/` or `/o/` steadily for a few seconds), and click **"Stop Recording"**. Listen to the recording preview.
   - **Option B**: Click **"Choose File"** to upload an existing `.wav` or `.mp3` sample.
   - Click **"Analyze Voice"**.
3. **Step 3: Diagnostic Result** (`/result`):
   - Review the calculated risk score percentage.
   - **Low Risk**: Displays positive wellness feedback.
   - **High Risk**: Displays high-risk indicator and provides verified details for nearby neurological care centers (Ruby Hall Clinic, Jehangir Hospital, Sahyadri Super Speciality Hospital).

---

## ⚡ Demo vs Full ML Mode

The application supports two operating modes to accommodate different hardware and deployment environments:

- **Demo Mode (`/upload-demo`)**:
  - Enabled by default in the frontend interface.
  - Simulates clinical screening and returns risk probabilities without requiring audio driver compilation or heavyweight scientific packages.
  - Ideal for rapid UI evaluation, demonstrations, and environments where `pyAudioAnalysis` C++ compilation is unavailable.
- **Full Production ML Mode (`/upload`)**:
  - Executes real-time feature extraction on incoming audio using `pyAudioAnalysis`.
  - Runs inference on `model_parkinson.pkl`.
  - Switch the API endpoint in [VoiceInputPage.js](file:///d:/parkinson-speech/parkinson_speech/parkinsons-frontend/src/pages/VoiceInputPage.js) from `/upload-demo` to `/upload` when deploying to production with all audio codecs installed.

---

## ⚠️ Medical Disclaimer

> [!IMPORTANT]
> **This software is an experimental screening tool and research proof-of-concept.**
> It is **not** an FDA-approved medical diagnostic device and should **never** replace professional medical advice, clinical examination, or neurological evaluation by a certified physician or healthcare provider. Anyone experiencing tremors, vocal changes, or motor difficulties should promptly seek professional medical counsel.

---

## 📄 License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
