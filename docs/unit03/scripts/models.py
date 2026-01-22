from pydantic import BaseModel, Field, model_validator


class MeteoriteLanding(BaseModel):
    name: str
    id: int
    mass: int = Field(alias="mass (g)")
    class_name: str = Field(alias="recclass")
    location: GeoLocation

    @model_validator(mode="before")
    @classmethod
    def preprocess_inputs(cls, values):
        values["location"] = {
            "lat": values["reclat"],
            "lon": values["reclong"],
        }
    return values

class GeoLocation(BaseModel):
    lat: float
    lon: float

def compute_average_mass(landings: list[MeteoriteLandings]) -> float:
        total_mass = 0.
        for ml in landings:
            total_mass += ml.mass
        return (total_mass / len(landings))

def check_hemisphere(ml: MeteoriteLanding) -> str:
    location = ''
    if (ml.location.lat > 0):
        location = 'Northern'
    else:
        location = 'Southern'
    if (ml.location.long > 0):
        location = f'{location} & Eastern'
    else:
        location = f'{location} & Western'
    return(location)