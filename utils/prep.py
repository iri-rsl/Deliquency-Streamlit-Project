# cleaning, normalization, feature engineering
import pandas as pd
import numpy as np

# --------------------------------------------------------------
# Necessary data
# --------------------------------------------------------------

REGION_COORDINATES = {
    1: {"name": "Guadeloupe", "lat": 16.2650, "lon": -61.5510},
    2: {"name": "Martinique", "lat": 14.6415, "lon": -61.0242},
    3: {"name": "Guyane", "lat": 3.9339, "lon": -53.1258},
    4: {"name": "La Réunion", "lat": -21.1151, "lon": 55.5364},
    6: {"name": "Mayotte", "lat": -12.8275, "lon": 45.1662},
    11: {"name": "Île-de-France", "lat": 48.8566, "lon": 2.3522},
    24: {"name": "Centre-Val de Loire", "lat": 47.7516, "lon": 1.6751},
    27: {"name": "Bourgogne-Franche-Comté", "lat": 47.2805, "lon": 4.9994},
    28: {"name": "Normandie", "lat": 49.1829, "lon": -0.3707},
    32: {"name": "Hauts-de-France", "lat": 50.4801, "lon": 2.7937},
    44: {"name": "Grand Est", "lat": 48.7002, "lon": 6.1878},
    52: {"name": "Pays de la Loire", "lat": 47.7633, "lon": -0.3299},
    53: {"name": "Bretagne", "lat": 48.2020, "lon": -2.9326},
    75: {"name": "Nouvelle-Aquitaine", "lat": 45.7640, "lon": 0.8191},
    76: {"name": "Occitanie", "lat": 43.9334, "lon": 2.1592},
    84: {"name": "Auvergne-Rhône-Alpes", "lat": 45.7640, "lon": 4.8357},
    93: {"name": "Provence-Alpes-Côte d'Azur", "lat": 43.9352, "lon": 6.0679},
    94: {"name": "Corse", "lat": 42.0396, "lon": 9.0129}
}

DEPARTMENT_COORDINATES = {
    # Metropolitan France
    "01": {"name": "Ain", "lat": 46.2044, "lon": 5.2265},
    "02": {"name": "Aisne", "lat": 49.5708, "lon": 3.6180},
    "03": {"name": "Allier", "lat": 46.5664, "lon": 3.3428},
    "04": {"name": "Alpes-de-Haute-Provence", "lat": 44.0936, "lon": 6.2360},
    "05": {"name": "Hautes-Alpes", "lat": 44.6616, "lon": 6.0820},
    "06": {"name": "Alpes-Maritimes", "lat": 43.7102, "lon": 7.2620},
    "07": {"name": "Ardèche", "lat": 44.7342, "lon": 4.3348},
    "08": {"name": "Ardennes", "lat": 49.7662, "lon": 4.7166},
    "09": {"name": "Ariège", "lat": 42.9637, "lon": 1.6020},
    "10": {"name": "Aube", "lat": 48.2973, "lon": 4.0781},
    "11": {"name": "Aude", "lat": 43.2044, "lon": 2.3508},
    "12": {"name": "Aveyron", "lat": 44.3518, "lon": 2.5757},
    "13": {"name": "Bouches-du-Rhône", "lat": 43.5283, "lon": 5.4497},
    "14": {"name": "Calvados", "lat": 49.1829, "lon": -0.3707},
    "15": {"name": "Cantal", "lat": 45.0347, "lon": 2.4441},
    "16": {"name": "Charente", "lat": 45.6500, "lon": 0.1500},
    "17": {"name": "Charente-Maritime", "lat": 45.7484, "lon": -0.7488},
    "18": {"name": "Cher", "lat": 47.0814, "lon": 2.3988},
    "19": {"name": "Corrèze", "lat": 45.3005, "lon": 2.0404},
    "2A": {"name": "Corse-du-Sud", "lat": 41.9267, "lon": 8.7369},
    "2B": {"name": "Haute-Corse", "lat": 42.4067, "lon": 9.1500},
    "21": {"name": "Côte-d'Or", "lat": 47.3220, "lon": 4.8632},
    "22": {"name": "Côtes-d'Armor", "lat": 48.5110, "lon": -2.7900},
    "23": {"name": "Creuse", "lat": 46.1635, "lon": 2.0339},
    "24": {"name": "Dordogne", "lat": 45.1848, "lon": 0.7218},
    "25": {"name": "Doubs", "lat": 47.2378, "lon": 6.0241},
    "26": {"name": "Drôme", "lat": 44.7311, "lon": 5.0449},
    "27": {"name": "Eure", "lat": 49.0237, "lon": 1.1857},
    "28": {"name": "Eure-et-Loir", "lat": 48.4469, "lon": 1.4884},
    "29": {"name": "Finistère", "lat": 48.2020, "lon": -4.2000},
    "30": {"name": "Gard", "lat": 43.8374, "lon": 4.3601},
    "31": {"name": "Haute-Garonne", "lat": 43.6047, "lon": 1.4442},
    "32": {"name": "Gers", "lat": 43.6465, "lon": 0.5864},
    "33": {"name": "Gironde", "lat": 44.8378, "lon": -0.5792},
    "34": {"name": "Hérault", "lat": 43.6109, "lon": 3.8763},
    "35": {"name": "Ille-et-Vilaine", "lat": 48.1173, "lon": -1.6778},
    "36": {"name": "Indre", "lat": 46.8083, "lon": 1.6906},
    "37": {"name": "Indre-et-Loire", "lat": 47.3941, "lon": 0.6848},
    "38": {"name": "Isère", "lat": 45.1885, "lon": 5.7245},
    "39": {"name": "Jura", "lat": 46.6794, "lon": 5.9044},
    "40": {"name": "Landes", "lat": 44.0061, "lon": -0.7311},
    "41": {"name": "Loir-et-Cher", "lat": 47.5906, "lon": 1.3359},
    "42": {"name": "Loire", "lat": 45.4397, "lon": 4.3872},
    "43": {"name": "Haute-Loire", "lat": 45.0438, "lon": 3.8845},
    "44": {"name": "Loire-Atlantique", "lat": 47.2184, "lon": -1.5536},
    "45": {"name": "Loiret", "lat": 47.9022, "lon": 2.1387},
    "46": {"name": "Lot", "lat": 44.4478, "lon": 1.4411},
    "47": {"name": "Lot-et-Garonne", "lat": 44.2013, "lon": 0.6156},
    "48": {"name": "Lozère", "lat": 44.5177, "lon": 3.4993},
    "49": {"name": "Maine-et-Loire", "lat": 47.4739, "lon": -0.5540},
    "50": {"name": "Manche", "lat": 49.1158, "lon": -1.3067},
    "51": {"name": "Marne", "lat": 48.9560, "lon": 4.3668},
    "52": {"name": "Haute-Marne", "lat": 48.1102, "lon": 5.4906},
    "53": {"name": "Mayenne", "lat": 48.3067, "lon": -0.6156},
    "54": {"name": "Meurthe-et-Moselle", "lat": 48.6921, "lon": 6.1844},
    "55": {"name": "Meuse", "lat": 49.1302, "lon": 5.3916},
    "56": {"name": "Morbihan", "lat": 47.7467, "lon": -2.8540},
    "57": {"name": "Moselle", "lat": 49.1193, "lon": 6.1757},
    "58": {"name": "Nièvre", "lat": 47.2167, "lon": 3.5333},
    "59": {"name": "Nord", "lat": 50.6292, "lon": 3.0573},
    "60": {"name": "Oise", "lat": 49.4169, "lon": 2.8260},
    "61": {"name": "Orne", "lat": 48.6499, "lon": 0.0927},
    "62": {"name": "Pas-de-Calais", "lat": 50.4958, "lon": 2.5377},
    "63": {"name": "Puy-de-Dôme", "lat": 45.7797, "lon": 3.0863},
    "64": {"name": "Pyrénées-Atlantiques", "lat": 43.2951, "lon": -0.3707},
    "65": {"name": "Hautes-Pyrénées", "lat": 43.2333, "lon": 0.0833},
    "66": {"name": "Pyrénées-Orientales", "lat": 42.6887, "lon": 2.8948},
    "67": {"name": "Bas-Rhin", "lat": 48.5734, "lon": 7.7521},
    "68": {"name": "Haut-Rhin", "lat": 47.7516, "lon": 7.3353},
    "69": {"name": "Rhône", "lat": 45.7640, "lon": 4.8357},
    "70": {"name": "Haute-Saône", "lat": 47.6131, "lon": 6.1561},
    "71": {"name": "Saône-et-Loire", "lat": 46.7837, "lon": 4.8570},
    "72": {"name": "Sarthe", "lat": 48.0077, "lon": 0.1996},
    "73": {"name": "Savoie", "lat": 45.5646, "lon": 6.5615},
    "74": {"name": "Haute-Savoie", "lat": 46.0638, "lon": 6.6821},
    "75": {"name": "Paris", "lat": 48.8566, "lon": 2.3522},
    "76": {"name": "Seine-Maritime", "lat": 49.4431, "lon": 1.0993},
    "77": {"name": "Seine-et-Marne", "lat": 48.8411, "lon": 2.9956},
    "78": {"name": "Yvelines", "lat": 48.8014, "lon": 2.1301},
    "79": {"name": "Deux-Sèvres", "lat": 46.3230, "lon": -0.4646},
    "80": {"name": "Somme", "lat": 49.9167, "lon": 2.2833},
    "81": {"name": "Tarn", "lat": 43.9297, "lon": 2.1481},
    "82": {"name": "Tarn-et-Garonne", "lat": 44.0151, "lon": 1.3555},
    "83": {"name": "Var", "lat": 43.4675, "lon": 6.2377},
    "84": {"name": "Vaucluse", "lat": 44.0520, "lon": 5.0469},
    "85": {"name": "Vendée", "lat": 46.6704, "lon": -1.4269},
    "86": {"name": "Vienne", "lat": 46.5802, "lon": 0.3404},
    "87": {"name": "Haute-Vienne", "lat": 45.8315, "lon": 1.2578},
    "88": {"name": "Vosges", "lat": 48.1732, "lon": 6.4511},
    "89": {"name": "Yonne", "lat": 47.7979, "lon": 3.5681},
    "90": {"name": "Territoire de Belfort", "lat": 47.6378, "lon": 6.8628},
    "91": {"name": "Essonne", "lat": 48.6301, "lon": 2.4478},
    "92": {"name": "Hauts-de-Seine", "lat": 48.8414, "lon": 2.2699},
    "93": {"name": "Seine-Saint-Denis", "lat": 48.9356, "lon": 2.4539},
    "94": {"name": "Val-de-Marne", "lat": 48.7907, "lon": 2.4475},
    "95": {"name": "Val-d'Oise", "lat": 49.0510, "lon": 2.1034},
    
    # DOM-TOM
    "971": {"name": "Guadeloupe", "lat": 16.2650, "lon": -61.5510},
    "972": {"name": "Martinique", "lat": 14.6415, "lon": -61.0242},
    "973": {"name": "Guyane", "lat": 3.9339, "lon": -53.1258},
    "974": {"name": "La Réunion", "lat": -21.1151, "lon": 55.5364},
    "976": {"name": "Mayotte", "lat": -12.8275, "lon": 45.1662},
}

# --------------------------------------------------------------
# Cleaning functions
# --------------------------------------------------------------
def rename_columns(data):
    """
    Rename columns to English for consistency.
    """
    data_copy = data.copy()
    data_copy = data_copy.rename(columns={
        'Code_region': 'Code_region',
        'Code_departement': 'Code_department',
        'annee': 'year',
        'indicateur': 'crime_type',
        'unite_de_compte': 'entity_involved',
        'nombre': 'amount',
        'taux_pour_mille': 'rate_per_1000',
        'insee_pop': 'population',
        'insee_pop_millesime': 'population_year',
        'insee_log': 'housing',
        'insee_log_millesime': 'housing_year',
    })
    return data_copy

def convert_rate_to_numeric(data):
    """
    Convert 'rate_per_1000' column from French format (comma decimal) to numeric float.
    """
    data_copy = data.copy()
    data_copy['rate_per_1000'] = data_copy['rate_per_1000'].str.replace(',', '.').astype(float)
    return data_copy

def add_region_names(data):
    """
    Add region names using the REGIONS dictionary.
    """
    data_copy = data.copy()
    data_copy['Region_name'] = data_copy['Code_region'].map(lambda x: REGION_COORDINATES.get(x, {}).get("name", "Unknown"))
    return data_copy

def add_region_coordinates(data):
    """
    Add region coordinates using the REGION_COORDINATES dictionary.
    """
    data_copy = data.copy()
    data_copy['Region_lat'] = data_copy['Code_region'].map(lambda x: REGION_COORDINATES.get(x, {"lat": None})['lat'])
    data_copy['Region_lon'] = data_copy['Code_region'].map(lambda x: REGION_COORDINATES.get(x, {"lon": None})['lon'])
    return data_copy

def add_department_names(data):
    """
    Add department names using the DEPARTMENT_COORDINATES dictionary.
    """
    data_copy = data.copy()
    data_copy['Department_name'] = data_copy['Code_department'].map(lambda x: DEPARTMENT_COORDINATES.get(x, {}).get("name", "Unknown"))
    return data_copy

def add_department_coordinates(data):
    """
    Add department coordinates using the DEPARTMENT_COORDINATES dictionary.
    """
    data_copy = data.copy()
    data_copy['Department_lat'] = data_copy['Code_department'].map(lambda x: DEPARTMENT_COORDINATES.get(x, {"lat": None})['lat'])
    data_copy['Department_lon'] = data_copy['Code_department'].map(lambda x: DEPARTMENT_COORDINATES.get(x, {"lon": None})['lon'])
    return data_copy    

def check_missing_data(data):
    """
    Analyze missing data in the dataset.
    """
    missing = data.isna().mean().reset_index()
    missing.columns = ['column', 'missing_fraction']
    return missing.sort_values('missing_fraction', ascending=False)

def check_duplicates(data):
    """
    Check for duplicate rows in the dataset.
    """
    return data.duplicated().sum()
def clean_data(data):
    """
    Main function to clean and prepare the delinquency data.
    """
    # Convert taux_pour_mille to numeric
    data_cleaned = rename_columns(data)
    data_cleaned = convert_rate_to_numeric(data_cleaned)
    
    if check_duplicates(data_cleaned) > 0:
        data_cleaned = data_cleaned.drop_duplicates().reset_index(drop=True)    
    
    # Add department names
    data_cleaned = add_department_names(data_cleaned)
    data_cleaned = add_department_coordinates(data_cleaned)
    # Add region names
    data_cleaned = add_region_names(data_cleaned)
    data_cleaned = add_region_coordinates(data_cleaned)

    # Feature engineering
    return data_cleaned
