import requests
import json
from dotenv import load_dotenv
import os
import yagmail

load_dotenv()
mdp = os.getenv("MDP")
url = os.getenv("URL")
email = os.getenv("EMAIL")
receiver = os.getenv("TO")
ARRAffinity = os.getenv("ARRAffinity")
ARRAffinitySameSite = os.getenv("ARRAffinitySameSite")



# Connexion
yag = yagmail.SMTP(email, mdp)





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
    'ARRAffinity': ARRAffinity,
    'ARRAffinitySameSite': ARRAffinitySameSite
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

# Construction du contenu de l'email
email_content = "Liste des offres :\n\n"

# Vérification que 'result' est bien présent dans la réponse
if 'result' in fileSearch:
    specializations_list = []
    value = fileSearch['result']
    print("\nListe des offres :\n")
    for element in value:
        # Affichage des informations : nom de l'organisation, titre de la mission
        print("Orga : ", element['organizationName']," | Ville : ", element['cityName'],"\nMission : ", element['missionTitle'],"\nDebut : ",element['missionStartDate'])
        # Mise à jour du dictionnaire package avec les informations de l'élément
        package = {
            "Organisation": element['organizationName'],
            "Ville": element['cityName'],
            "Mission": element['missionTitle'],
            "Debut": element['missionStartDate'],
            "Specialisations": []
        }
        
        # Récupérer les spécialisations pour chaque offre
        specializations = element.get('specializations', [])
        
        # Vérifier si des spécialisations existent
        if specializations:
            
            print("Spécialisations :")
            for spec in specializations:
                specialization_label = spec.get("specializationLabel", "Non spécifié")
                specialization_label_en = spec.get("specializationLabelEn", "Non spécifié")
                print(f"- {specialization_label} ({specialization_label_en})")
                package["Specialisations"].append(f"{specialization_label}")
        else :
            package["Specialisations"] = "Aucune spécialisation pour cette offre."
            print("Aucune spécialisation pour cette offre.")    
        print('\n')
        email_content += f"<p><b>Orga :</b> <span style='color:blue;'>{package['Organisation']}</span> | <b>Ville :</b> <span style='color:green;'>{package['Ville']}</span><br>"
        email_content += f"Mission :  {package['Mission']}\n"
        email_content += f"Debut :  {package['Debut']}\n"
        email_content += "Spécialisations :\n"
        for spec in package["Specialisations"]:
            email_content += f"- {spec}\n"
        email_content += "\n\n"
else:
    print("'result' n'a pas été trouvé dans la réponse.")

print('\n')
print('\n')
print('\n')
print(email_content)


with open('temp.txt', 'w', encoding='utf-8') as f1:
    f1.write(email_content)
    f1.close()
with open('response.txt', 'r', encoding='utf-8') as f, open('temp.txt', 'r', encoding='utf-8') as ff:
    r=f.read()
    temp=ff.read()
    if r != temp:
        f.close()
        print("Les fichiers sont différents, remplacement du fichier 'temp.txt' par 'response.txt'.")
        with open('response.txt', 'w', encoding='utf-8') as fff:
            fff.write(temp)
        # Envoi de l'email
        try:
            yag.send(
                to=receiver,
                subject="Sujet de l'email",
                contents=email_content,
            )
            print("Email envoyé avec succès.")
        except Exception as e:
            print(f"Erreur : {e}")
    else:
        print("Les fichiers sont identiques.")
    