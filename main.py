import requests
import json

# URL de l'API
url = "https://civiweb-api-prd.azurewebsites.net/api/Offers/search"

# Données de la requête (payload)
data = {
    "limit": 200,
    "skip": 0,
    "sort": ["0"],
    "activitySectorId": [],
    "missionsTypesIds": [],
    "missionsDurations": [],
    "gerographicZones": ["4"],
    "countriesIds": ["90"],
    "studiesLevelId": [],
    "companiesSizes": [],
    "specializationsIds": [],
    "entreprisesIds": [0],
    "missionStartDate": None,
    "query": None
}

# En-têtes de la requête
headers = {
    'Accept-Language': 'fr',
    'Content-Type': 'application/json',
    'Origin': 'https://mon-vie-via.businessfrance.fr'
}

# Cookies
cookies = {
    'ARRAffinity': '72bb2a684c17669bf3902a995c7b7cc53f2219f43eb6deb5805493078234f236',
    'ARRAffinitySameSite': '72bb2a684c17669bf3902a995c7b7cc53f2219f43eb6deb5805493078234f236'
}

# Envoi de la requête POST
response = requests.post(url, headers=headers, cookies=cookies, json=data)
fileSearch = response.json()

# Vérification du statut de la requête
if response.status_code == 200:
    # Enregistrer la réponse dans un fichier JSON
    with open('response.json', 'w', encoding='utf-8') as f:
        json.dump(fileSearch, f, ensure_ascii=False, indent=4)
    print("La réponse a été enregistrée dans 'response.json'.")
else:
    print(f"Erreur {response.status_code}: Impossible de récupérer les données.")

# Vérification que 'result' est bien présent dans la réponse
if 'result' in fileSearch:
    value = fileSearch['result']
    print("\nListe des offres :\n")
    for element in value:
        # Affichage des informations : nom de l'organisation, titre de la mission
        print("Orga : ", element['organizationName']," | Ville : ", element['cityName'],"\nMission : ", element['missionTitle'],"\nDebut : ",element['missionStartDate'])
        
        # Récupérer les spécialisations pour chaque offre
        specializations = element.get('specializations', [])
        
        # Vérifier si des spécialisations existent
        if specializations:
            print("Spécialisations :")
            for spec in specializations:
                specialization_label = spec.get("specializationLabel", "Non spécifié")
                specialization_label_en = spec.get("specializationLabelEn", "Non spécifié")
                print(f"- {specialization_label} ({specialization_label_en})")
                
        else:
            print("Aucune spécialisation pour cette offre.")
        print('\n')
else:
    print("'result' n'a pas été trouvé dans la réponse.")
