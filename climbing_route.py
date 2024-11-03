from dataclasses import dataclass


@dataclass
class ClimbingRoute:
    route_id: int
    user_id: int
    name: str
    grade: str
