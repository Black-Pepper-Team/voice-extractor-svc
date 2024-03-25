import peewee
from typing import List

db = peewee.PostgresqlDatabase('voice', user='voice', password='voice', host='localhost', port=5432)

class BaseModel(peewee.Model):
    class Meta:
        database = db


class Claim(BaseModel):
    id = peewee.PrimaryKeyField()
    metadata = peewee.TextField()
    vector = peewee.TextField()
    pk = peewee.TextField()
    user_id = peewee.TextField()
    claim_id = peewee.TextField(null=True)
    is_submitted = peewee.BooleanField()

def migrate_up() -> None:
    """
    The basic version of database migration
    """
    with db:
        db.create_tables([Claim])
        
def migrate_down() -> None:
    """
    Migrate down operation with dropping all tables
    """
    with db:
        db.drop_tables([Claim])
        
def select_all_claims() -> List[Claim]:
    """
    Selects all claims from the database
    """
    
    return [claim for claim in Claim.select().dicts()]