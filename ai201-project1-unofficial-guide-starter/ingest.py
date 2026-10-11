import os

DATA_DIR = "documents"
MIN_CHUNK_LENGTH = 50


def load_and_chunk_documents():
    chunks = []

    for filename in sorted(os.listdir(DATA_DIR)):
        if not filename.endswith(".txt"):
            continue

        filepath = os.path.join(DATA_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            raw_text = f.read()

        # Split into blocks by blank lines
        blocks = [b for b in raw_text.split("\n\n")]

        # Filter blocks: remove very short chunks and header-like lines
        merged = []
        for i, block in enumerate(blocks):
            block = block.strip()
            # Filter out very short chunks and header lines
            if len(block) < MIN_CHUNK_LENGTH:
                continue
            if block.startswith("Professor:") or block.startswith("Overall"):
                continue
            merged.append(block)

        for idx, chunk in enumerate(merged):
            chunks.append({
                "source": filename,
                "chunk_index": idx,
                "text": chunk
            })

    return chunks


if __name__ == "__main__":
    chunks = load_and_chunk_documents()
    print(f"Total chunks: {len(chunks)}")
    print()
    for i, ch in enumerate(chunks[:5]):
        print("---- SAMPLE", i + 1, "from", ch["source"]) 
        print(ch["text"]) 
        print()
