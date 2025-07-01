import os
import json
from models import Patient
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError("Clé API OpenAI manquante dans le fichier .env")

client = OpenAI(api_key=api_key)

def ask_gpt(patient: Patient):
    prompt = (
        "Tu es un assistant médical. Évalue le risque de diabète (faible/moyen/élevé) "
        "en te basant sur les données suivantes :\n\n"
        f"{patient.to_prompt()}\n"
        "Donne une réponse structurée :\n- Risque estimé\n- Explication"
    )

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()

def run():
    with open("data.json", "r", encoding="utf-8") as f:
        patients_data = json.load(f)

    for entry in patients_data:
        try:
            patient = Patient(**entry)
            print(f"\n🧑‍⚕️ Analyse du patient {patient.name} :")
            result = ask_gpt(patient)
            print(result)
        except Exception as e:
            print(f"Erreur avec le patient {entry.get('name', 'inconnu')} : {e}")

if __name__ == "__main__":
    run()
