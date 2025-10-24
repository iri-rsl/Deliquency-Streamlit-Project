# cleaning, normalization, feature engineering
import pandas as pd
import numpy as np

# --------------------------------------------------------------
# Necessary data
# --------------------------------------------------------------

REGIONS = {
    'Auvergne-Rhône-Alpes': ['01', '03', '07', '15', '26', '38', '42', '43', '63', '69', '73', '74'],
    'Bourgogne-Franche-Comté': ['21', '25', '39', '58', '70', '71', '89', '90'],
    'Bretagne': ['35', '22', '56', '29'],
    'Centre-Val de Loire': ['18', '28', '36', '37', '41', '45'],
    'Corse': ['2A', '2B'],
    'Grand Est': ['08', '10', '51', '52', '54', '55', '57', '67', '68', '88'],
    'Guadeloupe': ['971'],
    'Guyane': ['973'],
    'Hauts-de-France': ['02', '59', '60', '62', '80'],
    'Île-de-France': ['75', '77', '78', '91', '92', '93', '94', '95'],
    'La Réunion': ['974'],
    'Martinique': ['972'],
    'Mayotte': ['976'], 
    'Normandie': ['14', '27', '50', '61', '76'],
    'Nouvelle-Aquitaine': ['16', '17', '19', '23', '24', '33', '40', '47', '64', '79', '86', '87'],
    'Occitanie': ['09', '11', '12', '30', '31', '32', '34', '46', '48', '65', '66', '81', '82'],
    'Pays de la Loire': ['44', '49', '53', '72', '85'],
    'Provence-Alpes-Côte d\'Azur': ['04', '05', '06', '13', '83', '84'],
}

DEPARTMENTS = {
    '01': 'Ain', 
    '02': 'Aisne', 
    '03': 'Allier', 
    '04': 'Alpes-de-Haute-Provence', 
    '05': 'Hautes-Alpes',
    '06': 'Alpes-Maritimes', 
    '07': 'Ardèche', 
    '08': 'Ardennes', 
    '09': 'Ariège', 
    '10': 'Aube', 
    '11': 'Aude',
    '12': 'Aveyron', 
    '13': 'Bouches-du-Rhône', 
    '14': 'Calvados', 
    '15': 'Cantal', 
    '16': 'Charente',
    '17': 'Charente-Maritime', 
    '18': 'Cher', 
    '19': 'Corrèze', 
    '2A': 'Corse-du-Sud', 
    '2B': 'Haute-Corse',
    '21': 'Côte-d\'Or', 
    '22': 'Côtes-d\'Armor', 
    '23': 'Creuse', 
    '24': 'Dordogne', 
    '25': 'Doubs', 
    '26': 'Drôme',
    '27': 'Eure', 
    '28': 'Eure-et-Loir', 
    '29': 'Finistère', 
    '30': 'Gard', 
    '31': 'Haute-Garonne', 
    '32': 'Gers',
    '33': 'Gironde', 
    '34': 'Hérault', 
    '35': 'Ille-et-Vilaine', 
    '36': 'Indre', 
    '37': 'Indre-et-Loire',
    '38': 'Isère', 
    '39': 'Jura', 
    '40': 'Landes', 
    '41': 'Loir-et-Cher', 
    '42': 'Loire', 
    '43': 'Haute-Loire',
    '44': 'Loire-Atlantique', 
    '45': 'Loiret', 
    '46': 'Lot', 
    '47': 'Lot-et-Garonne', 
    '48': 'Lozère',
    '49': 'Maine-et-Loire', 
    '50': 'Manche', 
    '51': 'Marne', 
    '52': 'Haute-Marne', 
    '53': 'Mayenne',
    '54': 'Meurthe-et-Moselle', 
    '55': 'Meuse', 
    '56': 'Morbihan', 
    '57': 'Moselle', 
    '58': 'Nièvre', 
    '59': 'Nord',
    '60': 'Oise', 
    '61': 'Orne', 
    '62': 'Pas-de-Calais', 
    '63': 'Puy-de-Dôme', 
    '64': 'Pyrénées-Atlantiques',
    '65': 'Hautes-Pyrénées', 
    '66': 'Pyrénées-Orientales', 
    '67': 'Bas-Rhin', 
    '68': 'Haut-Rhin', 
    '69': 'Rhône',
    '70': 'Haute-Saône', 
    '71': 'Saône-et-Loire', 
    '72': 'Sarthe', 
    '73': 'Savoie', 
    '74': 'Haute-Savoie',
    '75': 'Paris', 
    '76': 'Seine-Maritime', 
    '77': 'Seine-et-Marne', 
    '78': 'Yvelines', 
    '79': 'Deux-Sèvres',
    '80': 'Somme', 
    '81': 'Tarn', 
    '82': 'Tarn-et-Garonne', 
    '83': 'Var', 
    '84': 'Vaucluse', 
    '85': 'Vendée',
    '86': 'Vienne', 
    '87': 'Haute-Vienne', 
    '88': 'Vosges', 
    '89': 'Yonne', 
    '90': 'Territoire de Belfort',
    '91': 'Essonne', 
    '92': 'Hauts-de-Seine', 
    '93': 'Seine-Saint-Denis', 
    '94': 'Val-de-Marne', 
    '95': 'Val-d\'Oise',
    '971': 'Guadeloupe', 
    '972': 'Martinique', 
    '973': 'Guyane', 
    '974': 'La Réunion', 
    '976': 'Mayotte',
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
        'Code_departement': 'Code_departement',
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

def add_department_names(data):
    """
    Add department names using the DEPARTMENTS dictionary.
    """
    data_copy = data.copy()
    data_copy['Code_departement'] = data_copy['Code_departement'].apply(lambda x: str(x).zfill(2))
    # Add department names
    data_copy['Departement_name'] = data_copy['Code_departement'].map(DEPARTMENTS)
    return data_copy

def add_region_names(data):
    """
    Add region names using the REGIONS dictionary.
    """
    data_copy = data.copy()
    data_copy['Code_departement'] = data_copy['Code_departement'].apply(lambda x: str(x).zfill(2))
    
    # Create reverse mapping from department code to region
    dept_to_region = {}
    for region, departments in REGIONS.items():
        for dept in departments:
            dept_to_region[dept] = region
    
    # Add region names
    data_copy['Region_name'] = data_copy['Code_departement'].map(dept_to_region)
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
    # Add region names
    data_cleaned = add_region_names(data_cleaned)

    # Feature engineering
    return data_cleaned
