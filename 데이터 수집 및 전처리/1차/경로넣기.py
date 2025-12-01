import json
import os

# 원본 JSON 경로
input_path = "C:/Users/PC/Downloads/dataset/merged_data.json"
# 수정된 JSON 저장 경로
output_path = "C:/Users/PC/Downloads/dataset/processed_blip.json"

# 기준 경로
base_path = "/content/drive/MyDrive/dataset"

# JSON 파일 불러오기 (UTF-8로 읽기)
with open(input_path, "r", encoding="cp949", errors="ignore") as f:
    data = json.load(f)

# image 키 값 절대경로로 변경
for item in data:
    img_path = item.get("image")
    if img_path:
        # 이미 절대경로가 아니면 base_path 붙이기
        if not os.path.isabs(img_path):
            # 파일 이름만 남기고 base_path/images/파일.png 형태로 조합
            filename = os.path.basename(img_path)
            item["image"] = os.path.join(base_path, "images", filename)

# 저장
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"✅ image 키 절대경로로 변환 완료! 저장 위치: {output_path}")
