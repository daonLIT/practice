import json
from pathlib import Path

def check_hash_files(json_path: Path, hash_dir: Path):
    # JSON 로드
    with json_path.open(encoding='utf-8') as f:
        records = json.load(f)

    # 존재하지 않는 해시값 수집용
    missing_hashes = []

    # 디렉토리 경로가 유효한지 확인
    if not hash_dir.is_dir():
        raise NotADirectoryError(f"{hash_dir!r} is not a directory")

    for rec in records:
        file_hash = rec.get('file_hash')
        if not file_hash:
            continue  # 해시값이 없는 레코드는 건너뜀

        # 확장자를 모르거나 여러 확장자(.pdf, .hwp 등)가 섞여 있으면 glob 으로 처리
        matches = list(hash_dir.glob(f"{file_hash}.*"))
        if not matches:
            missing_hashes.append(file_hash)

    # 결과 출력
    if missing_hashes:
        print("다음 해시값에 해당하는 파일을 찾을 수 없습니다:")
        for h in missing_hashes:
            print("  -", h)
    else:
        print("모든 file_hash 값에 해당하는 파일이 디렉토리에 존재합니다.")

if __name__ == "__main__":
    # JSON 파일 경로
    json_path = Path("C:/projects/pdf/pap2025_41989_false_auto_v2.json")
    # 해시값 파일들이 저장된 디렉토리
    hash_dir = Path("C:/projects/pdf/rename")

    check_hash_files(json_path, hash_dir)
