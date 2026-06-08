class AnomalyResult:

    def __init__(
        self,
        embedding_index,
        algorithm,
        raw_score,
        normalized_score
    ):

        self.embedding_index = embedding_index

        self.algorithm = algorithm

        self.raw_score = raw_score

        self.normalized_score = normalized_score

    def to_dict(self):

        return {
            "embedding_index": self.embedding_index,
            "algorithm": self.algorithm,
            "raw_score": self.raw_score,
            "normalized_score": self.normalized_score
        }

    def __str__(self):

        return (
            f"{self.algorithm} | "
            f"Embedding {self.embedding_index} | "
            f"{self.normalized_score:.2f}%"
        )