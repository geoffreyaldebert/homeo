import openai
import pandas as pd
from datetime import datetime
import random
import os
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow


import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from requests import HTTPError

load_dotenv()

secret_auth = os.getenv("AUTHS")
if secret_auth:
    with open('secrets.json', 'w') as token:
        token.write(secret_auth)

token_auth = os.getenv("AUTHT")
if token_auth:
    with open('token.json', 'w') as token:
        token.write(token_auth)

# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/gmail.send",
]

def generate_and_send():
    openai.api_key = os.getenv("SECRET_OAI")

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'secrets.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        mail = ""

        today = datetime.today().strftime("%Y-%m-%d")

        d1 = datetime.strptime(today, "%Y-%m-%d")

        vie = pd.read_csv("vie.csv", dtype=str)
        phrase = ""
        delta = 100000
        deltabis = None
        for index, row in vie.iterrows():
            d2 = datetime.strptime(row["date"], "%Y-%m-%d")
            if delta > abs((d2 - d1).days):
                delta = abs((d2 - d1).days)
                deltabis = (d2 - d1).days
                phrase = row["phrase"]

        if deltabis > 0:
            modif = "dans"
            modif2 = "c'est"
        else:
            modif = "il y a"
            modif2 = "c'était"
            
        intro = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"Ecris une phrase d'introduction à un mail saluant Arthur et en le tutoyant. Arthur est médecin et est très enthousiaste sur le domaine de l'homéopathie. Tu peux ajouter un peu de contexte vis-à-vis de ce qu'il est en train de vivre en ce moment, à savoir : {modif} {delta} jours, {modif2} {phrase}. Place toi depuis le point de vue de trois docteurs en homéopathie dont on ne dira pas les noms. Ne signe pas la phrase.",
            max_tokens=1000,
        )

        generated_text = intro.choices[0].text
        print(generated_text)

        mail += generated_text
        mail += "\n\nComme toutes les semaines, tu reçois ci-dessous le Top 3 des articles dont on parle le plus dans le domaine de l'homéopathie en ce moment. N'hésite pas à nous faire des retours."


        maladies = [
            "Grippe",
            "Rhume",
            "Diabète de type 1",
            "Diabète de type 2",
            "Hypertension artérielle",
            "Asthme",
            "Cancer du poumon",
            "Cancer du sein",
            "Cancer de la prostate",
            "Cancer du côlon",
            "VIH/SIDA",
            "Maladie d'Alzheimer",
            "Maladie de Parkinson",
            "Sclérose en plaques",
            "Fibromyalgie",
            "Polyarthrite rhumatoïde",
            "Maladie de Crohn",
            "Rectocolite hémorragique",
            "Sclérose latérale amyotrophique (SLA)",
            "Maladie cœliaque",
            "Anémie",
            "Leucémie",
            "Lupus érythémateux systémique",
            "Hémophilie",
            "Thrombose veineuse profonde (TVP)",
            "Embolie pulmonaire",
            "Maladie coronarienne",
            "Insuffisance cardiaque",
            "Accident vasculaire cérébral (AVC)",
            "Fibrillation auriculaire",
            "Maladie de Raynaud",
            "Fibrose kystique",
            "Hypothyroïdie",
            "Hyperthyroïdie",
            "Glaucome",
            "Cataracte",
            "Dépression",
            "Anxiété",
            "Trouble bipolaire",
            "Trouble obsessionnel compulsif (TOC)",
            "Schizophrénie",
            "Trouble de stress post-traumatique (TSPT)",
            "Trouble de l'alimentation",
            "Syndrome du côlon irritable (SCI)",
            "Endométriose",
            "Syndrome des ovaires polykystiques (SOPK)",
            "Fibromes utérins",
            "Candidose",
            "Herpès",
            "Chlamydia",
            "Gonorrhée",
            "Syphilis",
            "Infection à papillomavirus humain (HPV)",
            "Hépatite B",
            "Hépatite C",
            "Paludisme",
            "Dengue",
            "Zika",
            "Chikungunya",
            "Ebola",
            "Maladie de Lyme",
            "Maladie du sommeil",
            "Choléra",
            "Tuberculose",
            "Méningite",
            "Malaria",
            "Fièvre jaune",
            "Leishmaniose",
            "Hypothyroïdie",
            "Hyperthyroïdie",
            "Obésité",
            "Anorexie mentale",
            "Boulimie",
            "Trouble du comportement alimentaire non spécifié (TCAN)",
            "Diabulimie",
            "Apnée du sommeil",
            "Insomnie",
            "Narcolepsie",
            "Syndrome des jambes sans repos (SJSR)",
            "Maladie d'Addison",
            "Maladie de Cushing",
            "Diabète insipide",
            "Glaucome",
            "DMLA (Dégénérescence maculaire liée à l'âge)",
            "Glaucome",
            "Cataracte",
            "Conjonctivite",
            "Kératite",
            "Migraine",
            "Céphalée de tension",
            "Cluster headache",
            "Fibromyalgie",
            "Spondylarthrite ankylosante",
        ]

        maladie1 = random.choice(maladies)
        maladie2 = random.choice(maladies)
        maladie3 = random.choice(maladies)

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"Ecris-moi 3 résumés d'articles fictifs sur l'homéopathie. Chaque article doit parler d'une plante ou d'un fruit miracle qui peut soigner une maladie. Sois varié dans le choix des remèdes. Pour l'article 1, il s'agit de soigner la maladie '{maladie1}'. Pour l'article 2, soigner la malaide '{maladie2}'. Pour l'article 3, la maladie '{maladie3}'",
            max_tokens=2000,
        )

        generated_text = response.choices[0].text
        print(generated_text)

        mail += generated_text
        mail += "\n\nBien à toi et à la semaine prochaine !\n\nDr MDG, GA et VR"
        mail += ""
        
        mail = "<html><head></head><body><p>" + mail.replace("\n", "</p><p>") + "</p></body></html>"

        print(mail)

        service = build('gmail', 'v1', credentials=creds)
                    
        message = MIMEMultipart('alternative')
        message['to'] = f'{os.getenv("RECIPIENTS")}'
        message['bcc'] = f'{os.getenv("CCIRECIPIENTS")}'
        #message['to'] = os.getenv("RECIPIENT1")
        message['subject'] = f'Reminder Spectacles - {str(today)}'
        part1 = MIMEText(mail, 'html')
        #part2 = MIMEText(mail, 'html')
        message.attach(part1)
        # message.attach(part2)
        create_message = {
            'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()
        }
        message = (service.users().messages().send(userId="me", body=create_message).execute())

    except HTTPError as error:
        print(F'An error occurred: {error}')
        message = None

    os.remove("secrets.json")
    os.remove("token.json")

if __name__ == '__main__':
    generate_and_send()
