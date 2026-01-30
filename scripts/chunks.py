import os
from pathlib import Path
from dotenv import load_dotenv
from upstash_vector import Index, Vector

load_dotenv()
index = Index.from_env()

def run_ingestion():
    """
    C'est ma fonction pour nettoyer et envoyer mes données vers Upstash. 
    Elle va chercher tous les fichiers .md dans mon dossier 'data' et les découper 
    proprement grâce aux balises '##'. Pour chaque morceau, je crée un vecteur 
    avec un ID unique et je garde le titre et le nom du fichier en métadonnées. 
    À la fin, ça envoie tout d'un coup vers la base de données vectorielle pour 
    que mon IA puisse faire des recherches précises par section.
    """
    # Dossier où se trouvent les fichiers : parcours.md, experience.md ...
    data_path = Path("data")
    vectors = []

    # Vérification si le dossier existe
    if not data_path.exists():
        print("Le dossier 'data' n'existe pas.")
        return

    for file_path in data_path.glob("*.md"):
        print(f"Lecture de : {file_path.name}")
        content = file_path.read_text(encoding="utf-8")
        
        # Découpage par section ##
        sections = content.split("##")
        
        for i, section in enumerate(sections):
            section = section.strip()
            if not section:
                continue
            
            lines = section.splitlines()
            titre = lines[0].strip() # Titre après le ##
            corps = "\n".join(lines[1:]).strip()
            
            # On prépare l'ID 
            vector_id = f"{file_path.stem}-{i}"
            
            # Texte complet que l'IA va lire
            texte_pour_ia = f"SECTION: {titre}\n{corps if corps else titre}"
            
            vectors.append(Vector(
                id=vector_id,
                data=texte_pour_ia,
                metadata={
                    "title": titre,
                    "source": file_path.name
                }
            ))

    if vectors:
        print(f"Envoi de {len(vectors)} sections vers Upstash...")
        index.upsert(vectors=vectors)
        print("Terminé ! Les données sont en ligne.")
    else:
        print("Aucun contenu trouvé dans les fichiers .md.")

if __name__ == "__main__":

    run_ingestion()

