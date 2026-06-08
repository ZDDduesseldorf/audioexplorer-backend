import json
import os
import random

OUTPUT_DIR = "data/embeddings"

os.makedirs(OUTPUT_DIR, exist_ok=True)

VECTOR_SIZE = 128
NUMBER_OF_FILES = 50

for i in range(1, NUMBER_OF_FILES + 1):
    vector = [round(random.uniform(-3, 3), 4) for _ in range(VECTOR_SIZE)]

    data = {
        "id": f"embedding_{i:03}",
        "vector": vector
    }

    file_path = os.path.join(
        OUTPUT_DIR,
        f"embedding_{i:03}.json"
    )

    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

print(f"{NUMBER_OF_FILES} embeddings generated.")