import random


class SampleModel:
    def get_reco(self, user_id: int):
        return random.sample(range(0, 10), 10)
