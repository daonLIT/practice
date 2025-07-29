import os
import shutil

# 1) 원본이 모여 있는 최상위 디렉토리
root_dir = r"C:/projects/pdf/pap_extraction0"

# 2) 추출한 파일을 저장할 디렉토리 (존재하지 않으면 자동 생성)
target_dir = r'/pdf/get_name'
os.makedirs(target_dir, exist_ok=True)

# 3) root_dir 안의 모든 하위 폴더 순회
for sub in os.listdir(root_dir):
    sub_path = os.path.join(root_dir, sub)
    if not os.path.isdir(sub_path):
        continue

    # 4) 하위 폴더 중 'original' 폴더 경로
    orig_path = os.path.join(sub_path, 'original')
    if not os.path.isdir(orig_path):
        print(f"'{sub}' 폴더에 original 폴더가 없습니다.")
        continue

    # 5) original 폴더 내 모든 파일 목록 수집
    files = [f for f in os.listdir(orig_path)
             if os.path.isfile(os.path.join(orig_path, f))]
    if not files:
        print(f"'{sub}/original' 폴더에 파일이 없습니다.")
        continue

    # 6) 각 파일을 target_dir로 복사
    for fname in files:
        src_file = os.path.join(orig_path, fname)
        # 파일명 충돌 방지를 위해 서브폴더명을 prefix로 붙임
        dst_file = os.path.join(target_dir, f"{sub}_{fname}")
        shutil.copy2(src_file, dst_file)
        print(f"복사: {src_file} → {dst_file}")
