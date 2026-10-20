from pydantic import BaseModel, Field


class score(BaseModel):
    rank: int
    score: int = Field(ge=0)
    name: str


class high_score(BaseModel):
    scores: list[score]


class High:
    def __init__(self, path_name: str):
        self.path = path_name

    def load_highscore(self):
        with open(self.path, "r+") as f:
            data = f.read()

        check_data = high_score.model_validate(data)
        return check_data
