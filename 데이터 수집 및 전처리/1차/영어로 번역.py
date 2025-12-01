import json
import os

# 파일 경로 설정
INPUT_FILENAME = "C:/Users/PC/Downloads/output.jsonl"  # 이전 단계에서 생성된 평탄화된 JSONL 파일
OUTPUT_FILENAME = "C:/Users/PC/Downloads/output_en.jsonl" # 최종 영어 번역본 JSONL 파일

# --- 변환 규칙 딕셔너리 ---
TRANSLATION_MAP = {
    # 1. 질환명 및 상태 (Answer)
    "건선": "Psoriasis",
    "아토피": "Atopic Dermatitis",
    "여드름": "Acne",
    "정상": "Normal",
    "주사": "Rosacea",
    "지루": "Seborrheic Dermatitis",
    "N/A": "N/A", # N/A는 그대로 유지 (또는 "Not Applicable"로 변경 가능)
    "none": "none", # none은 그대로 유지 (또는 "None"으로 변경 가능)
    
    # 2. 질문 템플릿 (Question)
    "이 이미지에서 어떤 질환이 보이나요?": "What skin disease is visible in this image?",
    "이 이미지는 신체 어느 부위인가요?": "What part of the body is this image of?",
    "이 이미지에서 어떤 증상이 나타나나요?": "What symptoms are visible in this image?",
    "이 질환에 대해 설명해주세요.": "Describe this disease.",
    
    # 3. 답변 상세 설명 (Answer)
    "얼굴": "Face",
    "머리": "Head",
    "해당없음": "None",
    "두피, 눈썹, 코입주름 등 피지분비가 있는 곳을 따라 발생하는 염증성 피부질환":
        "An inflammatory skin condition that occurs along areas with high sebum secretion, such as the scalp, eyebrows, and nasolabial folds.",
    "얼굴의 가운데 부위에 발생하는 지속적인 홍반이 특징인 염증성 피부질환":
        "An inflammatory skin condition characterized by persistent redness (erythema) occurring in the central area of the face.",
    "면포와 구진, 농포, 결절 등으로 나타나는 피지선과 모낭의 만성질환":
        "A chronic disease of the sebaceous glands and hair follicles, presenting as comedones, papules, pustules, and nodules.",
    "심한 가려움을 동반하는 만성 습진의 일종":
        "A type of chronic eczema accompanied by severe itching.",
    "인설이 쌓인 붉은 구진이나 판으로 나타나는 염증성 피부질환":
        "An inflammatory skin condition that presents as red papules or plaques covered with scales."
}
# 'none'과 'N/A'는 그대로 두는 것이 일반적이므로 맵에 추가했습니다.
# "N/A"나 "none"이 파일에서 한글 문자열로 되어있다면, 위에 "해당없음"처럼 한글명을 추가해야 합니다.

def translate_jsonl_fields(input_filepath, output_filepath, translation_map):
    """
    JSONL 파일을 읽어 'question'과 'answer' 필드의 한글 값을 
    제공된 맵에 따라 영어로 변환하고 새 파일에 저장합니다.
    """
    if not os.path.exists(input_filepath):
        print(f"❌ 오류: 입력 파일을 찾을 수 없습니다. 경로를 확인해주세요: {input_filepath}")
        return

    translated_count = 0
    
    try:
        with open(input_filepath, 'r', encoding='utf-8') as infile, \
             open(output_filepath, 'w', encoding='utf-8') as outfile:
            
            for line in infile:
                if line.strip():
                    try:
                        record = json.loads(line.strip())
                        
                        # 1. 'question' 필드 번역
                        korean_q = record.get("question")
                        if korean_q in translation_map:
                            record["question"] = translation_map[korean_q]
                        
                        # 2. 'answer' 필드 번역
                        korean_a = record.get("answer")
                        if korean_a in translation_map:
                            record["answer"] = translation_map[korean_a]
                        
                        # 3. 번역된 객체를 새 JSONL 파일에 쓰기
                        outfile.write(json.dumps(record, ensure_ascii=False) + '\n')
                        translated_count += 1
                        
                    except json.JSONDecodeError as e:
                        print(f"❌ 오류: JSON 디코딩 오류. 해당 줄을 건너뜁니다: {e}")
                        continue
        
        print(f"✅ 번역 완료! 총 {translated_count}개의 객체가 '{output_filepath}'에 성공적으로 저장되었습니다.")

    except Exception as e:
        print(f"❌ 예상치 못한 오류 발생: {e}")

# 함수 실행
translate_jsonl_fields(INPUT_FILENAME, OUTPUT_FILENAME, TRANSLATION_MAP)