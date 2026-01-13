from pydantic import BaseModel, Field, model_validator
    

class GeoLocation(BaseModel):
    lat: float
    lon: float

class MeteoriteLanding(BaseModel):
    name: str
    id: int
    mass: int = Field(alias="mass (g)")
    location: GeoLocation
    class_name: str = Field(alias="recclass")

    @model_validator(mode="before")
    @classmethod
    def preprocess_inputs(cls, values: dict) -> dict:
        values = {
            ...values,
            "id": int(values["id"]),
            "mass (g)": int(float(values["mass (g)"])),
            "location": GeoLocation(
                lat=float(values["reclat"]),
                lon=float(values["reclong"])
            )
        }
        return values