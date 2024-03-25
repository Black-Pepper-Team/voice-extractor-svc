# API + CLI imports
import typer
from typing_extensions import Annotated
from pathlib import Path

# Internal imports
import src.api.main as api
from src.model.claim import Claim, db

app = typer.Typer(help="Face recognition API for the Black Pepper Team")

# --- Debugging commands ---

@app.command()
def run_api() -> None:
    """Runs the service API"""
    
    api.run_api()
    
@app.command()
def migrate_up() -> None:
    """
    Migrates the database up
    """

    try:
        claim_db.migrate_up()
        print('Database migrated up')
    except Exception as e:
        logging.error(f'Error while migrating up: {e}')
    
@app.command()
def migrate_down() -> None:
    """
    Migrates the database down
    """
    
    try:
        claim_db.migrate_down()
        print('Database migrated down')
    except Exception as e:
        logging.error(f'Error while migrating down: {e}')
    

if __name__ == '__main__':
    app()
    