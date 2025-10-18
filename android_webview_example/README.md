# 📱 Android WebView 앱 예제 코드

이 폴더에는 Streamlit 블로그 글 작성기를 Android 앱으로 만들기 위한 예제 코드가 들어있습니다.

## 📁 파일 설명

### 1. `MainActivity.kt`
- 메인 액티비티 코드
- WebView 설정 및 Streamlit 앱 로드
- 뒤로가기, 새로고침 등 기능 구현

### 2. `activity_main.xml`
- 메인 액티비티 레이아웃
- WebView와 ProgressBar 포함

### 3. `AndroidManifest.xml`
- 앱 권한 설정 (인터넷, 파일 접근 등)
- 액티비티 설정

### 4. `build.gradle`
- 앱 빌드 설정
- 필요한 라이브러리 의존성

### 5. `network_security_config.xml`
- 네트워크 보안 설정
- HTTP/HTTPS 허용 설정

## 🚀 사용 방법

1. **Android Studio에서 새 프로젝트 생성**
   - Empty Activity 선택

2. **이 폴더의 파일들을 프로젝트에 복사**
   - `MainActivity.kt` → `app/src/main/java/com/yourname/blogwriter/`
   - `activity_main.xml` → `app/src/main/res/layout/`
   - `AndroidManifest.xml` → `app/src/main/`
   - `build.gradle` → `app/`
   - `network_security_config.xml` → `app/src/main/res/xml/` (폴더 생성 필요)

3. **MainActivity.kt 수정**
   ```kotlin
   private val STREAMLIT_URL = "https://your-app.streamlit.app"
   ```
   → 배포된 Streamlit 앱 URL로 변경

4. **패키지 이름 변경**
   - `com.yourname.blogwriter` → 원하는 패키지명으로 변경

5. **빌드 및 실행**
   - Run 버튼 클릭 또는 Shift + F10

## ⚙️ 커스터마이징

### 앱 이름 변경
`app/src/main/res/values/strings.xml`:
```xml
<string name="app_name">블로그 글 작성기</string>
```

### 앱 아이콘 변경
1. `res 우클릭 → New → Image Asset`
2. 아이콘 이미지 선택

### 스플래시 스크린 추가
`themes.xml`에 스플래시 테마 추가

### 오류 페이지 커스터마이징
`MainActivity.kt`의 `WebViewClient`에서 `onReceivedError` 구현

## 🔧 문제 해결

### 앱이 로드되지 않는 경우
1. 인터넷 권한 확인
2. Streamlit URL이 올바른지 확인
3. `usesCleartextTraffic="true"` 설정 확인

### WebView가 비어있는 경우
1. JavaScript 활성화 확인
2. DOM Storage 활성화 확인

### 파일 업로드가 안 되는 경우
1. 파일 접근 권한 확인
2. `ValueCallback` 구현 필요 (고급)

## 📦 APK 생성

1. **Build → Generate Signed Bundle / APK**
2. **APK 선택**
3. 키스토어 생성 (처음인 경우)
4. **release** 선택
5. APK 파일 생성 완료!

위치: `app/release/app-release.apk`

## 🌟 추가 기능 아이디어

- [ ] 오프라인 모드
- [ ] 푸시 알림
- [ ] 다크 모드 지원
- [ ] 파일 업로드 지원
- [ ] 앱 내 브라우저 열기
- [ ] 공유 기능

## 📞 도움말

- Android 공식 문서: https://developer.android.com
- Kotlin 가이드: https://kotlinlang.org/docs/home.html
- WebView 가이드: https://developer.android.com/guide/webapps/webview

