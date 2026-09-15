#!/usr/bin/env python3
"""
Script de packaging du projet ChurnScope pour le livrable final.
Conforme au cahier des charges DPIA 1 - L'Ecole Multimedia.

Exemple d'utilisation :
    python scripts/package_submission.py --name "jouvence_martin" --classe "AIA01"
"""

import argparse
import os
import zipfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Liste des fichiers et dossiers indispensables selon le brief
REQUIRED_PATHS = [
    "README.md",
    "requirements.txt",
    "app.py",
    "data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv",
    "docs/01_analyse_preparation.md",
    "docs/02_apprentissage_modeles.md",
    "docs/03_validation_conclusion.md",
    "docs/presentation_dirigeants.md",
    "notebooks/01_exploration.ipynb",
    "notebooks/02_modelisation.ipynb",
    "notebooks/03_validation.ipynb",
    "src/export_model.py",
    "src/data/loader.py",
    "src/models/train.py",
    "src/monitoring/drift.py",
]


def verify_prerequisites():
    """Verifie la presence de tous les livrables obligatoires."""
    missing = []
    for rel_path in REQUIRED_PATHS:
        full_path = PROJECT_ROOT / rel_path
        if not full_path.exists():
            missing.append(rel_path)
    return missing


def create_zip_archive(name: str, classe: str, output_dir: Path) -> Path:
    """Cree une archive Zip propre contenant l'ensemble du projet."""
    clean_name = name.strip().lower().replace(" ", "_").replace("-", "_")
    clean_classe = classe.strip().upper().replace(" ", "")
    zip_filename = f"{clean_name}_projet3_{clean_classe}.zip"
    zip_filepath = output_dir / zip_filename

    print(f"Creation de l'archive : {zip_filepath}")

    with zipfile.ZipFile(zip_filepath, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(PROJECT_ROOT):
            # Filtrer les repertoires exclus
            dirs[:] = [
                d
                for d in dirs
                if not any(
                    pat in d
                    for pat in [
                        ".venv",
                        ".git",
                        "__pycache__",
                        ".pytest_cache",
                        ".ipynb_checkpoints",
                    ]
                )
            ]

            for file in files:
                if any(file.endswith(ext) for ext in [".pyc", ".zip"]):
                    continue
                file_path = Path(root) / file
                rel_path = file_path.relative_to(PROJECT_ROOT)
                zipf.write(file_path, arcname=str(rel_path))

    return zip_filepath


def main():
    parser = argparse.ArgumentParser(
        description="Generateur de livrable ZIP ChurnScope"
    )
    parser.add_argument(
        "--name", default="etudiant_dpia", help="Nom et prenom (ex: arthur_mensch)"
    )
    parser.add_argument("--classe", default="AIA01", help="Classe (ex: AIA01)")
    parser.add_argument(
        "--output-dir", default=str(PROJECT_ROOT), help="Dossier de destination"
    )
    args = parser.parse_args()

    print("Verification des livrables obligatoires...")
    missing = verify_prerequisites()
    if missing:
        print("Avertissement : Certains fichiers attendus sont absents :")
        for m in missing:
            print(f"   - {m}")
    else:
        print("Tous les fichiers obligatoires du brief sont presents !")

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    zip_path = create_zip_archive(args.name, args.classe, output_dir)

    size_mb = zip_path.stat().st_size / (1024 * 1024)
    print(f"Archive creee avec succes : {zip_path.name} ({size_mb:.2f} Mo)")
    print(f"Chemin complet : {zip_path}")


if __name__ == "__main__":
    main()
