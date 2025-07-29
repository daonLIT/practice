import win32com.client
import win32gui, win32con, threading, time
import os


# 팝업 감시 & 닫기 함수sdfd
def _close_security_dialog():
    # 창 제목이 OS 언어 설정에 따라 다를 수 있으니,
    # 실제 뜨는 경고창 제목을 확인해서 바꿔 주세요.
    title = "보안 경고"
    while True:
        hwnd = win32gui.FindWindow(None, title)
        if hwnd:
            # [확인] 버튼 ID가 1번인 경우가 많습니다.
            # 혹 다르면 Spy++ 등으로 확인 후 WM_COMMAND 파라미터를 조정하세요.
            win32gui.PostMessage(hwnd, win32con.WM_COMMAND, 1, 0)
            break
        time.sleep(0.05)

def convert_hwp_to_pdf(hwp_path: str, output_pdf_path: str):
    try:
        # 1) 팝업 닫기 스레드 스타트
        t = threading.Thread(target=_close_security_dialog, daemon=True)
        t.start()

        hwp = win32com.client.gencache.EnsureDispatch("HWPFrame.HwpObject")
        hwp.RegisterModule("FilePathCheckDLL", "FileAuto")

        if not hwp.Open(hwp_path):
            print(f"[❌] 파일 열기 실패: {hwp_path}")
            return
        
        hwp.XHwpWindows.Item(0).Visible = False
        
        hwp.SaveAs(output_pdf_path, "PDF")
        print(f"[✅] 변환 성공: {os.path.basename(hwp_path)} → {os.path.basename(output_pdf_path)}")
    except Exception as e:
        print(f"[❌] 변환 실패: {hwp_path} | 오류: {e}")
    finally:
        try:
            hwp.Quit()
        except:
            pass

def batch_convert_hwp_to_pdf(input_folder: str, output_folder: str):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    hwp_files = [f for f in os.listdir(input_folder) if f.lower().endswith((".hwp", ".hwpx"))]

    if not hwp_files:
        print("[⚠️] 변환할 파일이 없습니다.")
        return

    # 변환 대상 필터링: 이미 PDF가 있는지 확인
    remaining_files = []
    for file in hwp_files:
        filename_wo_ext = os.path.splitext(file)[0]
        output_path = os.path.join(output_folder, filename_wo_ext + ".pdf")

        if not os.path.exists(output_path):  # PDF가 없으면 변환 대상
            remaining_files.append(file)

    print(f"[🔄] 총 {len(remaining_files)}개의 파일을 변환합니다...\n")

    for file in remaining_files:
        input_path = os.path.join(input_folder, file)
        filename_wo_ext = os.path.splitext(file)[0]
        output_path = os.path.join(output_folder, filename_wo_ext + ".pdf")
        convert_hwp_to_pdf(input_path, output_path)

    print("\n[🏁] 모든 파일 변환 완료.")


# ✅ 사용자 맞춤 경로로 실행
if __name__ == "__main__":
    input_dir = r"C:\projects\pdf\rename"
    output_dir = r"C:\projects\pdf\get_pdfs"
    batch_convert_hwp_to_pdf(input_dir, output_dir)
        