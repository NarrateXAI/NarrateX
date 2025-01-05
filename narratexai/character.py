from pydantic import BaseModel
from typing import Dict, List, Optional


from pydantic import BaseModel
from typing import Dict, List, Optional


class CharacterLore(BaseModel):
    character_name: str
    identity: Dict
    background: Dict
    personality: Dict
    skills: Dict
    relationships: Dict
    motivations: Dict
    key_events: Dict
    setting_connection: Dict
    storyline_and_missions: Dict
    locations: List

class Locations(BaseModel):
  locations: List
