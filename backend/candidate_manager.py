# Candidate manager and duplicate detection module

import hashlib


def get_resume_hash(file_bytes):
    # Compute SHA-256 hash of resume bytes to detect exact file duplicates
    return hashlib.sha256(file_bytes).hexdigest()


def detect_duplicates(uploaded_files):
    # Detect duplicate uploaded resumes by filename and file hash
    unique_files = []
    seen_hashes = set()
    duplicates_found = []

    for uf in uploaded_files:
        file_bytes = uf.getvalue()
        file_hash = get_resume_hash(file_bytes)

        if file_hash in seen_hashes:
            duplicates_found.append(uf.name)
        else:
            seen_hashes.add(file_hash)
            unique_files.append(uf)

    return unique_files, duplicates_found

