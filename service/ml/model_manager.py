from service.ml.sample_model.model import SampleModel
from enum import Enum


class Models(str, Enum):
    SAMPLE_MODEL = 'sample_model'


def get_model_by_name(name: str, user_id: int):
    model_name = name.lower()

    if (model_name == Models.SAMPLE_MODEL):
        return SampleModel

    return None
