from pathlib import Path

def load_all_texts(base_dir: str) -> str:
    base_path = Path(base_dir)
    filenames = ["parcours.md", "experiences.md", "competences.md", "contact.md", "projets.md"]
    
    content_list = []
    for filename in filenames:
        file_path = base_path / filename
        if file_path.exists():
            content_list.append(file_path.read_text(encoding="utf-8"))
        else:
            
            print(f"Avertissement : {filename} introuvable.")

    return "\n\n".join(content_list)