from pydantic import BaseModel, Field, model_validator

class GeoLocation(BaseModel):
    lat: float
    long: float

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
            "long": values["reclong"],
        }
        
        return values

def compute_average_mass(landings: list[MeteoriteLanding]) -> float:
    """
    Iterates through a list of meteorite landing objects, adds their masses together
    and returns that sum divided by the total number or landings

    Args:
        landings: A list of meteorite landing objects

    Returns:
        result: Average value.
    """
    total_mass = 0.
    for ml in landings:
        total_mass += ml.mass
    return (total_mass / len(landings))

def check_hemisphere(ml: MeteoriteLanding) -> str:
    """
    Given a meteorite landing's location (latitude and longitude in decimal notation),
    returns which hemispheres those coordinates land in.

    Args:
        ml: A MeteoriteLanding object

    Returns:
        location: Short string listing two hemispheres.
    """
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

def count_classes(landings: list[MeteoriteLanding]) -> dict[str, int]:
    """
    ???
    """
    classes_observed = {}
    for ml in landings:
        if ml.class_name not in classes_observed:
            classes_observed[ml.class_name] == 0

        classes_observed[ml.class_name] += 1
    return(classes_observed)