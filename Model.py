from pydantic import BaseModel, Field

class Patient(BaseModel):
    name: str
    age: int = Field(..., ge=0, description="Âge du patient en années")
    weight: float = Field(..., gt=0, description="Poids en kg")
    height: float = Field(..., gt=0, description="Taille en mètres")
    has_diabetes_family_history: bool

    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)

    def to_prompt(self) -> str:
        return (
            f"Nom : {self.name}\n"
            f"Âge : {self.age}\n"
            f"Poids : {self.weight} kg\n"
            f"Taille : {self.height} m\n"
            f"IMC : {self.bmi()}\n"
            f"Antécédents familiaux de diabète : {'Oui' if self.has_diabetes_family_history else 'Non'}\n"
        )
