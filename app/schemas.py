from pydantic import BaseModel, HttpUrl
from typing import Dict, Any

class DetectRequest(BaseModel):
    url: HttpUrl

class DetectResponse(BaseModel):
    url: HttpUrl
    technologies: Dict[str, Any]