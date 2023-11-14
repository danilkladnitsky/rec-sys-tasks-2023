import random


class SampleModel:
    def get_reco(user_id: int):
        return random.sample(range(0, 10), 10)
