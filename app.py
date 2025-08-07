from flask import Flask, render_template, request
import requests
import os
import random

app = Flask(__name__)

API_KEY = os.environ.get("OPENWEATHER_API_KEY", "여기에_임시_API키_넣기")

korean_to_english = {
    "서울": "Seoul", "부산": "Busan", "대구": "Daegu",
    "인천": "Incheon", "광주": "Gwangju", "대전": "Daejeon",
    "울산": "Ulsan", "세종": "Sejong", "경기": "Gyeonggi-do",
    "강원": "Gangwon-do", "충북": "Chungcheongbuk-do", "충남": "Chungcheongnam-do",
    "전북": "Jeollabuk-do", "전남": "Jeollanam-do", "경북": "Gyeongsangbuk-do",
    "경남": "Gyeongsangnam-do", "제주": "Jeju"
}

def get_age_group(age):
    if age < 20:
        return "10대"
    elif age < 30:
        return "20대"
    elif age < 40:
        return "30대"
    else:
        return "40대 이상"

def get_outfit_suggestions(temp, gender, age_group):
    suggestions = []

    if gender == "남성":
        if age_group == "10대":
            if temp >= 27:
                suggestions = [
                    "그래픽 반팔티 + 카고 반바지 + 운동화 + 볼캡",
                    "루즈핏 나시 + 농구 반바지 + 샌들 + 체인 목걸이"
                ]
            elif temp >= 20:
                suggestions = [
                    "얇은 후드티 + 데님 팬츠 + 운동화",
                    "셔츠 + 면바지 + 캔버스화"
                ]
            elif temp >= 10:
                suggestions = [
                    "니트 + 조거 팬츠 + 아노락",
                    "맨투맨 + 청바지 + 운동화"
                ]
            else:
                suggestions = [
                    "패딩 + 기모 후드 + 트레이닝 팬츠 + 방한 부츠",
                    "울 코트 + 니트 + 기모 슬랙스 + 머플러"
                ]
        elif age_group == "20대":
            if temp >= 27:
                suggestions = [
                    "오버핏 셔츠 + 반바지 + 로퍼 + 선글라스",
                    "린넨 셋업 + 슬리퍼 + 팔찌"
                ]
            elif temp >= 20:
                suggestions = [
                    "청자켓 + 반팔티 + 치노 팬츠 + 캔버스화",
                    "맨투맨 + 슬랙스 + 스니커즈"
                ]
            elif temp >= 10:
                suggestions = [
                    "트렌치 코트 + 니트 + 청바지 + 첼시부츠",
                    "가디건 + 면바지 + 더비 슈즈"
                ]
            else:
                suggestions = [
                    "패딩 + 히트텍 + 니트 + 기모 슬랙스 + 목도리",
                    "무스탕 + 후드티 + 데님 팬츠 + 방한화"
                ]
        # 나중에 30대, 40대 이상 추가 가능
    elif gender == "여성":
        if age_group == "10대":
            if temp >= 27:
                suggestions = [
                    "크롭티 + 플리츠 스커트 + 운동화 + 볼캡",
                    "나시 + 와이드 팬츠 + 샌들 + 목걸이"
                ]
            elif temp >= 20:
                suggestions = [
                    "셔츠 + 반바지 + 운동화",
                    "긴팔 티 + 데님 스커트 + 캔버스화"
                ]
            elif temp >= 10:
                suggestions = [
                    "후드 집업 + 조거팬츠 + 운동화",
                    "가디건 + 플레어 팬츠 + 플랫 슈즈"
                ]
            else:
                suggestions = [
                    "패딩 + 기모 맨투맨 + 레깅스 + 롱부츠",
                    "롱코트 + 니트 + 슬랙스 + 머플러"
                ]
        elif age_group == "20대":
            if temp >= 27:
                suggestions = [
                    "크롭 블라우스 + 하이웨스트 반바지 + 샌들 + 에코백",
                    "민소매 원피스 + 샌들 + 햇빛차단모자"
                ]
            elif temp >= 20:
                suggestions = [
                    "린넨 셋업 + 플랫슈즈 + 미니백",
                    "셔츠 원피스 + 스니커즈 + 팔찌"
                ]
            elif temp >= 10:
                suggestions = [
                    "트렌치코트 + 원피스 + 앵클부츠",
                    "니트 + 슬랙스 + 로퍼 + 숄더백"
                ]
            else:
                suggestions = [
                    "숏패딩 + 기모 니트 + 팬츠 + 워커",
                    "롱코트 + 터틀넥 + 울 팬츠 + 부츠"
                ]

    return random.choice(suggestions) if suggestions else "기본적인 편안한 옷차림을 추천해요."

@app.route("/", methods=["GET", "POST"])
def index():
    weather_info = None
    outfit_suggestion = None

    if request.method == "POST":
        city_kor = request.form.get("city")
        gender = request.form.get("gender")
        age_str = request.form.get("age")

        # 입력값 검증
        if not age_str.isdigit():
            outfit_suggestion = "나이는 숫자로 입력해주세요."
        else:
            age = int(age_str)
            city_eng = korean_to_english.get(city_kor)

            if not city_eng:
                weather_info = f"지원하지 않는 도시명입니다: {city_kor}"
            else:
                url = f"http://api.openweathermap.org/data/2.5/weather?q={city_eng}&appid={API_KEY}&units=metric&lang=kr"
                response = requests.get(url)

                if response.status_code == 200:
                    data = response.json()
                    temp = data['main']['temp']
                    desc = data['weather'][0]['description']

                    weather_info = f"{city_kor}({city_eng})의 현재 온도는 {temp}°C, 날씨는 '{desc}'입니다."
                    age_group = get_age_group(age)
                    outfit_suggestion = get_outfit_suggestions(temp, gender, age_group)
                else:
                    weather_info = "날씨 정보를 불러오는데 실패했습니다."

    return render_template("index.html", weather=weather_info, outfit=outfit_suggestion)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
