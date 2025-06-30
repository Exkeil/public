from pydantic import BaseModel
from typing import Any, List, Optional


class APIResponse(BaseModel):
    action: str
    obj: str
    code: int
    action_id: str
    notifies: Optional[List[Any]] = None
    body: Optional[Any] = None
    list: Optional[List[dict]] = None
    total_count: Optional[int] = None


class AuthResponse(BaseModel):
    token: str
    domain_id: int
    user_id: int
    user_name: str
    user_login: str
    role_id: int
    role_name: str
    role_type: int
    domain_name: str