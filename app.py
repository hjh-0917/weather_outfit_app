from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# ✅ OpenWeatherMap API 키 (Render에서 환경변수 OR 로컬에서 직접 변수)
API_KEY = os.environ.get("OPENWEATHER_API_KEY", "여기에_임시_API키_넣기")

# ✅ 한글 도시명 → 영어 도시명 변환
korean_to_english = {
    "서울": "Seoul",
    "부산": "Busan",
    "대구": "Daegu",
    "인천": "Incheon",
    "광주": "Gwangju",
    "대전": "Daejeon",
    "울산": "Ulsan",
    "세종": "Sejong",
    "경기": "Gyeonggi-do",
    "강원": "Gangwon-do",
    "충북": "Chungcheongbuk-do",
    "충남": "Chungcheongnam-do",
    "전북": "Jeollabuk-do",
    "전남": "Jeollanam-do",
    "경북": "Gyeongsangbuk-do",
    "경남": "Gyeongsangnam-do",
    "제주": "Jeju"
}

# ✅ 기온별 코디 추천 함수 (GPT 없이 구현)
def get_outfit_suggestion(temp, weather_desc):
    if temp >= 27:
        return "오늘은 정말 덥네요! 시원한 반팔 티셔츠와 린넨 반바지를 추천해요."
    elif 20 <= temp < 27:
        return "따뜻한 날씨예요. 얇은 긴팔 티셔츠와 면바지를 입으면 좋아요."
    elif 10 <= temp < 20:
        return "선선하네요. 가벼운 자켓과 니트를 매치해보세요."
    else:
        return "추운 날씨예요! 두꺼운 코트와 목도리로 따뜻하게 준비하세요."

@app.route("/", methods=["GET", "POST"])
def index():
    weather_info = None
    outfit_suggestion = None

    if request.method == "POST":
        city_kor = request.form.get("city")  # 사용자가 입력한 도시명
        city_eng = korean_to_english.get(city_kor)

        if not city_eng:
            weather_info = f"지원하지 않는 도시명입니다: {city_kor}"
        else:
            # ✅ 날씨 API 호출
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city_eng}&appid={API_KEY}&units=metric&lang=kr"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                temp = data['main']['temp']
                desc = data['weather'][0]['description']

                # ✅ 날씨 정보 문구
                weather_info = f"{city_kor}({city_eng})의 현재 온도는 {temp}°C, 날씨는 '{desc}'입니다."

                # ✅ 기온 기반 코디 추천
                outfit_suggestion = get_outfit_suggestion(temp, desc)
            else:
                weather_info = "날씨 정보를 불러오는데 실패했습니다. API 키와 도시명을 확인하세요."

    return render_template("index.html", weather=weather_info, outfit=outfit_suggestion)

# ✅ Render 배포용 (0.0.0.0 + 동적 PORT)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
