from dataclasses import dataclass
from typing import Any, Dict

@dataclass
class NextInitializedTickWithinOneWordResult:
  tickNext: int
  initialized: bool

  @staticmethod
  def fromCall (data: Dict[str, Any]) -> 'NextInitializedTickWithinOneWordResult':
    return NextInitializedTickWithinOneWordResult (
      int(data['tickNext'], 0),
      bool(int(data['unlocked'], 0))
    )

  def __repr__(self) -> str:
    return str(self.__dict__)