from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional

@dataclass
class Template:
    """Basic prompt template data model."""
    id: str
    type: str
    name: str
    content: str
    parent_id: Optional[str] = None
    description: Optional[str] = None
    variables: List[str] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)
    version: str = "1.0.0"
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    is_active: bool = True
