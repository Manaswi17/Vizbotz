# 📊 VizBotz - AI-Powered Data Visualizer 🚀

🔗 [Live Application Link](https://vizbotz.streamlit.app/)

---

## **Overview**
VizBotz is an interactive AI-powered data visualization web app built with **Streamlit** and integrated with **Google Gemini AI**.  
Users can upload CSV datasets, generate professional charts, and receive executive-style AI insights — all with a simple, user-friendly interface.

---

## **How to Run the Project**

### Prerequisites
- Python 3.12+
- pip package manager

### Steps to Run

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Manaswi17/Vizbotz.git
   ```

2. **Navigate to the project directory**:
   ```bash
   cd VizBotz
   ```

3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

4. **Activate the virtual environment**:
   - On **Windows**:
     ```bash
     .\venv\Scripts\activate
     ```
   - On **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

5. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

6. **Run the application**:
   ```bash
   streamlit run app.py
   ```

7. **Open your browser** and navigate to the URL provided by Streamlit.

---

## **Features Achieved**

- **Upload any CSV dataset** easily through the interface.
- **Generate dynamic visualizations**:
  - Bar Chart
  - Line Chart
  - Scatter Plot
  - Pie Chart
  - Box Plot
- **Auto-colored, interactive charts** using Vega-Lite.
- **AI-Powered Insights**:
  - Detects trends, outliers, and patterns
  - Summarized executive recommendations
- **Download AI insights** in JSON format.
- **Manual 'Generate' button** for clear user control.
- **Interactive tooltips** on graphs for better understanding.

---

## **Technical Achievements**

- Integrated **Google Gemini API** for AI-generated data insights.
- Built a responsive **Streamlit** web app for real-time interaction.
- Used **Vega-Lite** for creating high-quality, dynamic charts.
- Developed dynamic column selection for flexible plotting.
- Enabled **secure file handling** for user-uploaded datasets.
- Managed environment secrets securely using TOML configurations during deployment.

---

## **Design Achievements**

- Designed a **simple, professional UI** with minimal steps for user actions.
- Added **responsive layouts** for better experience across devices.
- Provided clear **error messages** when invalid operations are attempted.
- Implemented **easy-to-use selection dropdowns** for choosing graph types and columns.
- Ensured **separation between data uploading and chart generation** to maintain a clean workflow.

---

## **Tech Stack**

| Technology | Usage |
|:---|:---|
| Python 3.12 | Core programming language |
| Streamlit | Web application framework |
| Vega-Lite (via Altair) | Charting and visualization engine |
| Google Gemini API | AI-powered data insights |
| Pandas | Data manipulation and CSV handling |
| TOML | Secure secret management on cloud deployment |

---

## **Deployment**

- Hosted on **Streamlit Cloud**:  
🔗 [VizBotz Live Link](https://vizbotz.streamlit.app/)
- Secrets (e.g., GEMINI_API_KEY) are managed securely using platform-provided **Secrets Manager**.

---

## 📚 References
- [Google Gemini API Documentation](https://ai.google.dev/gemini-api/docs)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Altair + Vega-Lite Visualization Grammar](https://vega.github.io/vega-lite/)

