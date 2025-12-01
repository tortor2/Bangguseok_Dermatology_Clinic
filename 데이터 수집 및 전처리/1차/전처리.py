


import json
import os

def process_jsonl_file(input_file_path, output_file_path):
    """
    JSONL 파일을 읽어 answer 값이 'N/A'인 줄은 삭제하고,
    'none'인 줄은 'no symptoms'로 수정한 후 새 파일에 저장합니다.
    """
    processed_lines = []
    skipped_count = 0
    modified_count = 0
    total_count = 0

    # 출력 디렉토리 확인 (필요한 경우 생성)
    output_dir = os.path.dirname(output_file_path)
    if output_dir and not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
        except OSError as e:
            print(f"❌ 오류: 출력 디렉토리를 생성할 수 없습니다: {output_dir}. 오류: {e}")
            return

    try:
        # 입력 파일을 읽기 모드로 열기
        with open(input_file_path, 'r', encoding='utf-8') as infile:
            print("⏳ 파일 읽기 및 처리 시작...")
            for line in infile:
                total_count += 1
                try:
                    # 각 줄을 JSON 객체로 로드
                    data = json.loads(line)

                    # 1. 'answer'가 'N/A'인 경우 건너뛰기 (삭제)
                    if data.get('answer') == 'N/A':
                        skipped_count += 1
                        continue

                    # 2. 'answer'가 'none'인 경우 'no symptoms'로 수정
                    if data.get('answer') == 'none':
                        data['answer'] = 'no symptoms'
                        modified_count += 1
                    
                    if data.get('answer') == 'None':
                        data['answer'] = 'no symptoms'
                        modified_count += 1

                    # 수정된 (또는 필터링을 통과한) 객체를 다시 문자열로 변환하여 리스트에 추가
                    # ensure_ascii=False 를 사용하여 한글이 깨지지 않도록 합니다.
                    processed_lines.append(json.dumps(data, ensure_ascii=False))

                except json.JSONDecodeError:
                    print(f"⚠️ 경고 (줄 {total_count}): 유효하지 않은 JSON 형식의 줄을 건너뜁니다: {line.strip()[:50]}...")
                except Exception as e:
                    print(f"❌ 처리 중 알 수 없는 오류 발생 (줄 {total_count}): {e} (줄 내용: {line.strip()[:50]}...)")


        # 수정된 라인들을 새 파일에 쓰기
        with open(output_file_path, 'w', encoding='utf-8') as outfile:
            for line in processed_lines:
                outfile.write(line + '\n')

        # 최종 통계 출력
        print("\n--- ✅ 처리 완료 ---")
        print(f"📚 입력 파일: {input_file_path}")
        print(f"💾 출력 파일: {output_file_path}")
        print(f"총 처리된 줄 수: {total_count}")
        print(f"'N/A'로 인해 **삭제된** 줄 수: {skipped_count}")
        print(f"'none'이 '**no symptoms**'로 **수정된** 줄 수: {modified_count}")
        print(f"최종 출력 파일에 저장된 줄 수: {len(processed_lines)}")


    except FileNotFoundError:
        print(f"❌ 심각한 오류: 입력 파일 경로를 찾을 수 없습니다: {input_file_path}")
    except Exception as e:
        print(f"❌ 파일 처리 중 예상치 못한 오류 발생: {e}")

# =========================================================================
# === 🚨 실행 부분: 이 두 줄만 실제 경로로 수정하시면 됩니다. ===
# =========================================================================

# 🎯 1. 9600줄 JSONL 파일의 정확한 경로를 여기에 입력하세요.
# 예시: 'C:/Users/PC/Desktop/original_data.jsonl'
INPUT_FILE_PATH = 'C:/Users/PC/Downloads/output_en.jsonl'  # <-- **실제 입력 JSONL 파일 경로로 변경하세요**
OUTPUT_FILE_PATH = 'C:/Users/PC/Downloads/llava_en.jsonl'

# 함수 실행
process_jsonl_file(INPUT_FILE_PATH, OUTPUT_FILE_PATH)