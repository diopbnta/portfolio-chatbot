import asyncio
from agents import Agent, Runner, function_tool
from upstash_vector import Index
from dotenv import load_dotenv

# 1. Configuration
load_dotenv()
index = Index.from_env()

# 2. L'Outil de recherche (Tool)
@function_tool
def consulter_dossier_alioune(recherche: str) -> str:
    """
    Recherche des informations dans le portfolio d'Alioune DIOP.
    À utiliser pour : Nom, Prénom, Contact, BUT Science des Données, 
    Expérience McDonald's, Stage BOA, Compétences Python/SQL.
    """
    # On récupère les 6 meilleurs morceaux pour avoir une vue complète
    resultats = index.query(data=recherche, top_k=6, include_metadata=True)
    
    if not resultats:
        return "Je n'ai pas trouvé d'information spécifique à ce sujet dans mon dossier."
    
    # Construction de la réponse pour l'agent avec tes titres (metadata['title'])
    contexte = "Voici les éléments de mon parcours trouvés :\n"
    for r in resultats:
        titre = r.metadata.get('title', 'Information')
        contexte += f"\n[SECTION : {titre}]\n{r.data}\n"
    
    return contexte

# 3. Configuration de l'Agent
async def main():
    # Instructions personnalisées pour qu'il soit TON porte-parole
    consignes = """
    Tu es Alioune DIOP, étudiant en BUT Science des Données à Niort (EMS).
    Tu es un assistant professionnel qui répond au nom d'Alioune.

    RÈGLES DE RÉPONSE :
    1. Réponds toujours en utilisant "Je" (ex: "Je m'appelle Alioune DIOP", "J'ai travaillé chez McDonald's").
    2. Pour CHAQUE question, utilise l'outil 'consulter_dossier_alioune' avec des mots-clés simples.
    3. Si on te pose une question sur tes compétences, utilise les sections 'Langages', 'Outils' et 'Bases de données'.
    4. Sois poli, déterminé et professionnel, comme dans ta section 'À propos'.
    5. Réponds exclusivement en français.
    """

    mon_agent = Agent(
        name="Alioune AI",
        model="gpt-4.1-nano", # Modèle de ton cours
        tools=[consulter_dossier_alioune],
        instructions=consignes
    )

    # 4. Exécution (Le Runner)
    # Tu peux changer la question ici pour tester
    question = "Comment te présenterais-tu lors d'un entretien pour un stage en data science ?"
    
    print(f"Alioune AI analyse la question : {question}...")
    
    resultat = await Runner.run(mon_agent, question)
    
    print("\n" + "="*50)
    print("RÉPONSE D'ALIOUNE :")
    print(resultat.final_output)
    print("="*50)

if __name__ == "__main__":
    asyncio.run(main())