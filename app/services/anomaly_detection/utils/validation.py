



# Wir validieren die Embeddings, die zur Analyse gebracht werden 

def validate_embeddings(embeddings):

    if embeddings is None:
        raise ValueError("Embeddings cannot be None")

    if len(embeddings) == 0:
        raise ValueError("Embeddings cannot be empty")

    if not isinstance(embeddings, list):
        raise TypeError("Embeddings must be a list")

    for embedding in embeddings:

        if not isinstance(embedding, list):
            raise TypeError("Each embedding must be a list")

        if len(embedding) == 0:
            raise ValueError("Embedding vector cannot be empty")

        for value in embedding:
            if not isinstance(value, (int, float)):
                raise TypeError(
                    "Embedding values must be numeric"
                )