# import openai
# from django.conf import settings
# import json

# GPT_API_KEY = settings.GPT_API_KEY
# # GPT API Key 설정
# openai.api_key = GPT_API_KEY


# def get_tmdb_keywords(vision_keywords, tmdb_keywords):
#     # OpenAI ChatCompletion API 호출
#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",  # 3.5 버전 사용
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant."},
#             {
#                 "role": "user",
#                 "content": (
#                     "Given these keywords extracted from an image: "
#                     f"{vision_keywords}, match them strictly to the most relevant keywords "
#                     "from this TMDB keyword list: "
#                     f"{tmdb_keywords}. "
#                     "Only return keywords that exist in the TMDB keyword list. "
#                     "Each result must be an object in the format: "
#                     '[{"name": "keyword_name", "id": keyword_id}, ...]. '
#                     "Do not include keywords that are not in the TMDB list. "
#                     "Ensure the response is valid JSON, contains only matched objects from the TMDB list, "
#                     "and is consistent in structure. Do not include any other text or explanations in the output."
#                 ),
#             },
#         ],
#     )
#     # 응답에서 필요한 데이터 추출
#     matched_keywords_json = response['choices'][0]['message']['content']

#     # JSON 문자열을 Python 객체로 변환
#     matched_keywords = json.loads(matched_keywords_json)

#     # Python 객체 (리스트) 반환
#     return matched_keywords

import openai
from django.conf import settings
import json
from sentence_transformers import SentenceTransformer, util
import numpy as np

GPT_API_KEY = settings.GPT_API_KEY
# GPT API Key 설정
openai.api_key = GPT_API_KEY

# SentenceTransformer 모델 로드
model = SentenceTransformer('all-MiniLM-L6-v2')  # 효율적인 임베딩 모델

# def get_tmdb_keywords(vision_keywords, tmdb_keywords, min_count=10):
#     """
#     Vision 키워드와 TMDB 키워드를 매칭하여 최소 10개 이상 반환.
#     """
#     try:
#         # GPT API 호출
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",  # 3.5 버전 사용
#             messages=[
#                 {"role": "system", "content": "You are a helpful assistant."},
#                 {
#                     "role": "user",
#                     "content": (
#                         "Given these keywords extracted from an image: "
#                         f"{vision_keywords}, match them strictly to the most relevant keywords "
#                         "from this TMDB keyword list: "
#                         f"{tmdb_keywords}. "
#                         "Only return keywords that exist in the TMDB keyword list. "
#                         "Each result must be an object in the format: "
#                         '[{"name": "keyword_name", "id": keyword_id}, ...]. '
#                         "Do not include keywords that are not in the TMDB list. "
#                         "Ensure the response is valid JSON, contains only matched objects from the TMDB list, "
#                         "and is consistent in structure. Do not include any other text or explanations in the output."
#                     ),
#                 },
#             ],
#         )

#         # 응답 처리
#         matched_keywords_json = response['choices'][0]['message']['content']
#         matched_keywords = json.loads(matched_keywords_json)  # JSON 문자열 -> Python 객체 변환

#         # 키워드가 10개 미만일 경우 추가 보충
#         if len(matched_keywords) < min_count:
#             print(f"Fewer than {min_count} keywords found. Adding additional closest matches...")
#             additional_keywords = find_closest_matches(
#                 vision_keywords, tmdb_keywords, min_count - len(matched_keywords)
#             )
#             matched_keywords.extend(additional_keywords)

#         # 최종 반환 (중복 제거 및 최대 min_count 개)
#         unique_keywords = {kw['id']: kw for kw in matched_keywords}.values()  # 중복 제거
#         return list(unique_keywords)[:min_count]

#     except json.JSONDecodeError as e:
#         # JSON 디코딩 실패 시 에러 처리
#         print(f"JSON Decode Error: {e}")
#         return []
#     except Exception as e:
#         # 기타 예외 처리
#         print(f"Error: {e}")
#         return []

# def find_closest_matches(vision_keywords, tmdb_keywords, count):
#     """
#     Vision 키워드와 의미적으로 가장 유사한 TMDB 키워드를 보충.
#     """
#     # 1. 키워드 텍스트만 추출
#     vision_texts = [kw.lower() for kw in vision_keywords]
#     tmdb_texts = [kw["name"].lower() for kw in tmdb_keywords]

#     # 2. 텍스트 임베딩 생성
#     vision_embeddings = model.encode(vision_texts, convert_to_tensor=True)
#     tmdb_embeddings = model.encode(tmdb_texts, convert_to_tensor=True)

#     # 3. 코사인 유사도 계산
#     similarity_matrix = util.cos_sim(vision_embeddings, tmdb_embeddings).cpu().numpy()

#     # 4. 유사도 기준 상위 키워드 추출
#     closest_matches = []
#     for i, vision_kw in enumerate(vision_texts):
#         # 유사도 기준 상위 TMDB 키워드 선택
#         sorted_indices = np.argsort(-similarity_matrix[i])  # 유사도 내림차순 정렬
#         for idx in sorted_indices:
#             if len(closest_matches) >= count:  # 요청된 개수 충족 시 중단
#                 break
#             tmdb_kw = tmdb_keywords[idx]
#             if tmdb_kw not in closest_matches:  # 중복 제거
#                 closest_matches.append(tmdb_kw)

#     # 결과 반환
#     return closest_matches[:count]

def get_tmdb_keywords(vision_keywords, tmdb_keywords, min_count=5):
    """
    Vision 키워드와 TMDB 키워드를 매칭하여 최소 10개 이상 반환.
    """
    try:
        # GPT API 호출
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # 3.5 버전 사용
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": (
                        "Given these keywords extracted from an image: "
                        f"{vision_keywords}, match them strictly to the most relevant keywords "
                        "from this TMDB keyword list: "
                        f"{tmdb_keywords}. "
                        "Only return keywords that exist in the TMDB keyword list. "
                        "Each result must be an object in the format: "
                        '[{"name": "keyword_name", "id": keyword_id}, ...]. '
                        "Do not include keywords that are not in the TMDB list. "
                        "Ensure the response is valid JSON, contains only matched objects from the TMDB list, "
                        "and is consistent in structure. Do not include any other text or explanations in the output."
                    ),
                },
            ],
        )

        # GPT 응답 처리
        matched_keywords_json = response['choices'][0]['message']['content']
        matched_keywords = json.loads(matched_keywords_json)  # JSON 문자열 -> Python 객체 변환

        # GPT 응답에서 TMDB 키워드 리스트로 필터링
        matched_keywords = [
            kw for kw in matched_keywords
            if any(tmdb_kw["id"] == kw["id"] for tmdb_kw in tmdb_keywords)
        ]

        # 키워드가 10개 미만일 경우 추가 보충
        if len(matched_keywords) < min_count:
            print(f"Fewer than {min_count} keywords found. Adding additional closest matches...")
            additional_keywords = find_closest_matches(
                vision_keywords, tmdb_keywords, min_count - len(matched_keywords)
            )
            matched_keywords.extend(additional_keywords)

        # 최종 반환 (중복 제거 및 최대 min_count 개)
        unique_keywords = {kw['id']: kw for kw in matched_keywords}.values()  # 중복 제거
        print('//////unique', unique_keywords)
        return list(unique_keywords)[:min_count]

    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []

def find_closest_matches(vision_keywords, tmdb_keywords, count):
    """
    Vision 키워드와 의미적으로 가장 유사한 TMDB 키워드를 보충.
    """
    # 1. 키워드 텍스트만 추출
    vision_texts = [kw.lower() for kw in vision_keywords]
    tmdb_texts = [kw["name"].lower() for kw in tmdb_keywords]

    # 2. 텍스트 임베딩 생성
    vision_embeddings = model.encode(vision_texts, convert_to_tensor=True)
    tmdb_embeddings = model.encode(tmdb_texts, convert_to_tensor=True)

    # 3. 코사인 유사도 계산
    similarity_matrix = util.cos_sim(vision_embeddings, tmdb_embeddings).cpu().numpy()

    # 4. 유사도 기준 상위 키워드 추출
    closest_matches = []
    for i, vision_kw in enumerate(vision_texts):
        sorted_indices = np.argsort(-similarity_matrix[i])  # 유사도 내림차순 정렬
        for idx in sorted_indices:
            if len(closest_matches) >= count:
                break
            tmdb_kw = tmdb_keywords[idx]
            if tmdb_kw not in closest_matches:  # 중복 제거
                closest_matches.append(tmdb_kw)
    print('/////closets', closest_matches)
    return closest_matches[:count]

