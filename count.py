import json
from pathlib import Path

def count_missing_hash_files(json_path: Path, hash_dir: Path) -> int:
    # JSON 로드
    with json_path.open(encoding='utf-8') as f:
        records = json.load(f)

    missing_hashes = []

    if not hash_dir.is_dir():
        raise NotADirectoryError(f"{hash_dir!r} is not a directory")

    for rec in records:
        file_hash = rec.get('file_hash')
        if not file_hash:
            continue

        # 확장자에 상관없이 매칭
        if not any(hash_dir.glob(f"{file_hash}.*")):
            missing_hashes.append(file_hash)

    return len(missing_hashes)

if __name__ == "__main__":
    json_path = Path("/projects/pdf/pap2025_41989_false_auto_v2.json")
    hash_dir  = Path("/projects/pdf/rename")

    missing_count = count_missing_hash_files(json_path, hash_dir)
    print(missing_count)
