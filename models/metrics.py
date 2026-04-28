class Metrics:
    def __init__(self):
        self.entropy = 0.0
        self.avalanche_score = 0.0
        self.complexity_score = 0.0
        self.structure_score = 0.0
        self.key_score = 0.0

        # 🔥 MUST exist for ML scoring
        self.ind_score = 0.0

        self.final_score = 0.0