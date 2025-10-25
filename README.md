# Delinquency Data Visualization Dashboard

## Description

Can also find the link to the dashboard [here](https://deliquency-app-project-hgiwuyfbum4ebrfsrhd4fx.streamlit.app/) !
This Streamlit-based dashboard provides comprehensive analysis and visualization of French delinquency data from the national police and gendarmerie. The application offers interactive visualizations to explore crime patterns across French departments and regions, including temporal trends, geographic distributions, and demographic correlations.

### Key Features
- 📊 **Interactive KPIs**: Overview metrics with dynamic filtering
- 🗺️ **Geographic Analysis**: Regional and departmental crime mapping with Folium
- 📈 **Temporal Trends**: Year-over-year crime pattern analysis
- 🏛️ **Regional Deep Dive**: Detailed analysis for specific regions
- 👥 **Demographic Correlations**: Crime patterns vs population and housing data
- ⚠️ **Severity Analysis**: Crime hotspot identification and severity scoring
- 🔍 **Entity Analysis**: Breakdown by victim, perpetrator, vehicle, and infraction records

## Project Structure

```
Deliquency-Streamlit-Project/
├── app.py                      # Main Streamlit application
├── data/
│   └── delinquency.csv        # Processed crime dataset
├── sections/
│   ├── conclusion.py          # Conclusion and summary section
│   ├── deep_drives.py         # Regional analysis section
│   ├── intro.py              # Introduction and overview
│   ├── overview.py           # KPI dashboard section
│   └── technical.py          # Technical analysis section
├── utils/
│   ├── io.py                 # Data loading utilities
│   ├── prep.py               # Data preprocessing functions
│   ├── viz.py                # Visualization functions
│   └── preparing_data.ipynb  # Data preparation notebook
├── assets/                   # Static assets (images, etc.)
├── requirements.txt          # Python dependencies
└── README.md                # Project documentation
```

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/iri-rsl/Deliquency-Streamlit-Project.git
   cd Deliquency-Streamlit-Project
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Access the dashboard**
   Open your browser and navigate to `http://localhost:8501` if it doesn't open automatically.

### Dependencies

The main packages used in this project:
- `streamlit` - Web application framework
- `pandas` - Data manipulation and analysis
- `plotly` - Interactive visualizations
- `folium` - Geographic mapping
- `streamlit-folium` - Folium integration for Streamlit

## Usage

### Navigation
The dashboard is organized into several sections accessible via the sidebar:

1. **Introduction** - Project overview and data description
2. **Overview** - Key performance indicators and filtering options
3. **Deep Drives** - Regional analysis with detailed insights
4. **Technical Analysis** - Advanced analytics and correlations
5. **Conclusion** - Summary and key findings

### Architecture
- **Frontend**: Streamlit for web interface
- **Data Processing**: Pandas for data manipulation
- **Visualizations**: Plotly for interactive charts, Folium for maps
- **Caching**: Streamlit's built-in caching for performance optimization

### Performance Optimizations
- Data caching for faster load times
- Efficient filtering mechanisms
- Lazy loading of visualizations
- Responsive design for various screen sizes

## License

This project is developed for educational purposes as part of the Data Visualization course at EFREI.

## Resources
- **Dataset Source**: [data.gouv.fr](https://www.data.gouv.fr/datasets/bases-statistiques-communale-departementale-et-regionale-de-la-delinquance-enregistree-par-la-police-et-la-gendarmerie-nationales/#/resources/93438d99-b493-499c-b39f-7de46fa58669)
- **Python code for departmental/regional data**: [GitHub Repository](https://gist.github.com/mlorant/b4d7bb6f96c47776c8082cf7af44ad95)


## Acknowledgments

- EFREI Paris - Data Visualization Course
- French Ministry of Interior for providing open crime data
- Streamlit community for excellent documentation and examples 

