from dataclasses import dataclass
from typing import Optional, TypeVar

T = TypeVar('T')

@dataclass
class ResponseDto:
    message: Optional[str] = None
    error: Optional[str] = None
    body: Optional[T] = None