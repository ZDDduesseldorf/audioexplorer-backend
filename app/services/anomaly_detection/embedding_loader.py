import json
import os


class EmbeddingLoader:
    def __init__(self, directory):
        self.directory = directory

    def load_embeddings(self):

        embeddings = []

        for file_name in os.listdir(self.directory):
            if file_name.endswith(".json"):
                path = os.path.join(self.directory, file_name)

                with open(path, "r") as f:
                    data = json.load(f)

                    embeddings.append(data["vector"])

        return embeddings
