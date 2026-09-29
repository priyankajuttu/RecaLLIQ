from dataclasses import dataclass
from typing import List, Optional

@dataclass
class ClientInfo:
    name: str
    industry: str
    deal_value: float
    stakeholders: List[str]
    account_manager: str

@dataclass
class Interaction:
    id: str
    date: str
    type: str
    summary: str
    content: str
    participants: List[str]
    key_facts: List[str]

@dataclass
class Commitment:
    description: str
    owner: str
    date: str
    status: str  # OPEN/DONE/OVERDUE

@dataclass
class PreferenceChange:
    attribute: str
    old_value: str
    new_value: str
    date: str
    context: str
