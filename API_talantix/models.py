from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

@dataclass
class APIResponse:
    code: int
    message: Optional[str]
    body: Dict[str, Any]
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'APIResponse':
        return cls(
            code=data.get('code', 0),
            message=data.get('message'),
            body=data.get('body', {})
        )

@dataclass
class APIRecord:
    id: str
    object_type: str
    is_system: bool
    data: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    
    @classmethod
    def from_raw_data(cls, raw_data: Dict[str, Any], object_type: str, is_system: bool) -> 'APIRecord':
        now = datetime.now()
        return cls(
            id=str(raw_data.get('id', '')),
            object_type=object_type,
            is_system=is_system,
            data=raw_data,
            created_at=now,
            updated_at=now
        )

@dataclass
class APIRequest:
    action: str
    obj: str
    action_id: str
    params: Dict[str, Any]
    limit: Optional[int] = None
    offset: Optional[int] = None
    filter_: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        request = {
            'action': self.action,
            'obj': self.obj,
            'action_id': self.action_id,
            'params': self.params
        }
        
        if self.limit is not None:
            request['limit'] = self.limit
            
        if self.offset is not None:
            request['offset'] = self.offset
            
        if self.filter_ is not None:
            request['filter'] = self.filter_
            
        return request 