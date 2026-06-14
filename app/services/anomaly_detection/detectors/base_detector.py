from abc import ABC, abstractmethod


class BaseDetector(ABC):
    @abstractmethod
    def fit_predict(self, embeddings):
        pass
