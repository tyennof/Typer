from typing import Optional
import typer
from pathlib import Path

app = typer.Typer()

# 'run' nom de la commande définie grace au décorateur
@app.command('run')
def main(extension: str,
         directory: Optional[str] = typer.Argument(None, help="Dossier dans lequel chercher."),
         delete: bool = typer.Option(False, help="Supprime les fichiers trouvés.")):
    """
    Affiche les fichiers trouvés avec l'extension donnée.

    """

    # Vérification de l'existence du paramètre de répertoire sinon répertoire courant
    if directory:
        directory = Path(directory)
    else:
        directory = Path.cwd()

    # Si paramètre du répertoire donné, vérification de l'existence de ce répertoire
    if not directory.exists():
        typer.secho(f"Le dossier '{directory}' n'existe pas.", fg=typer.colors.RED)
        raise typer.Exit()

    # Parcours du répertoire en fonction de l'extension donnée
    files = directory.rglob(f"*.{extension}")

    if delete:
        typer.confirm("Voulez-vous vraiment supprimer tous les fichiers supprimés ?", abort=True)
        with typer.progressbar(files) as progress:
            for file in progress:
                file.unlink()
                typer.secho(f"Suppression du fichier {file}.", fg=typer.colors.RED)
    else:
        typer.secho(f"Fichier trouvés avec l'extension {extension}:", bg=typer.colors.BLUE, fg=typer.colors.BRIGHT_WHITE)
        for file in files:
            typer.secho(file)

# Contrairement à 'run', on ne spécifie pas de nom après 'command' donc on utilise le nom de la fonction par défaut
@app.command()
def search(extension: str):
    """Chercher les fichiers avec l'extension donnée."""
    main(extension=extension, directory=None, delete=False)

@app.command()
def delete(extension: str):
    """Supprimer les fichiers avec l'extension donnée."""
    main(extension=extension, directory=None, delete=True)


if __name__ == "__main__":
    app()