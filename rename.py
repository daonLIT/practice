import json
from pathlib import Path

# 1) JSON 파일과 실제 파일들이 들어있는 디렉터리 경로 설정
JSON_PATH  = Path("pap2025_41989_false_auto_v2.json")  
FILES_DIR  = Path(r'C:\projects\pdf\get_name')
OUTPUT_DIR = Path(r'C:\projects\pdf\rename')

# 2) 출력 디렉터리 만들기
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 3) JSON 로드 & mapping 생성 (basename → file_hash)
with JSON_PATH.open(encoding="utf-8") as f:
    records = json.load(f)

mapping = {
    Path(rec["downloaded_file_path"]).name: rec["file_hash"]
    for rec in records
}

# 4) 디렉터리 순회하며 리네임 + 이동
for file_path in FILES_DIR.iterdir():
    if not file_path.is_file():
        continue

    for orig_basename, file_hash in mapping.items():
        if orig_basename in file_path.name:
            new_name = f"{file_hash}{file_path.suffix}"
            dest_path = OUTPUT_DIR / new_name
            try:
                file_path.rename(dest_path)
                print(f"✔️  {file_path.name} → {new_name}")
            except Exception as e:
                print(f"❌  오류({file_path.name}): {e}")
            break
    else:
        print(f"⚠️  매칭 없음: {file_path.name}")
