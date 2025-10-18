# 📱 안드로이드 앱 배포 가이드

Streamlit 블로그 글 작성기를 안드로이드 앱으로 배포하는 방법을 단계별로 안내합니다.

## 🎯 배포 방법 3가지

### 방법 1: PWA (Progressive Web App) - 가장 간단 ⭐ 추천
### 방법 2: Android WebView 앱 - 네이티브 앱 경험
### 방법 3: Python 네이티브 앱 - 고급

---

## 🌟 방법 1: PWA (Progressive Web App) - 가장 간단

PWA는 웹사이트를 앱처럼 설치할 수 있게 해줍니다. 별도의 앱 개발 없이 가능합니다!

### 📋 Step 1: Streamlit 앱을 클라우드에 배포

#### 옵션 A: Streamlit Cloud (무료, 가장 쉬움)

1. **GitHub에 코드 업로드**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/your-username/blog-writer.git
   git push -u origin main
   ```

2. **Streamlit Cloud 배포**
   - https://streamlit.io/cloud 접속
   - GitHub 계정으로 로그인
   - "New app" 클릭
   - 레포지토리 선택
   - 앱 자동 배포! (URL: `https://your-app.streamlit.app`)

#### 옵션 B: Heroku (무료/유료)

```bash
# Heroku CLI 설치 후
heroku login
heroku create your-blog-writer
git push heroku main
```

#### 옵션 C: AWS, Google Cloud, Azure 등

### 📋 Step 2: PWA 기능 추가

PWA manifest 파일을 생성하여 앱처럼 설치 가능하게 만듭니다.

**장점:**
- ✅ 별도 개발 불필요
- ✅ 배포 심사 불필요
- ✅ 자동 업데이트
- ✅ 크로스 플랫폼 (Android, iOS, Desktop)

**단점:**
- ❌ Google Play Store에 등록 불가
- ❌ 일부 네이티브 기능 제한

**사용 방법:**
1. 배포된 웹사이트 접속
2. Chrome에서 "메뉴 → 앱 설치" 또는 "홈 화면에 추가"
3. 앱처럼 사용!

---

## 📱 방법 2: Android WebView 앱 - 네이티브 앱 경험

Streamlit 앱을 Android WebView로 래핑하여 네이티브 앱처럼 만듭니다.

### 📋 필수 준비물

1. **Android Studio** 설치 (https://developer.android.com/studio)
2. **Streamlit 앱이 배포된 URL** (예: https://your-app.streamlit.app)

### 📋 Step 1: Android Studio 프로젝트 생성

1. Android Studio 실행
2. "New Project" → "Empty Activity" 선택
3. 프로젝트 정보 입력:
   - Name: `BlogWriter`
   - Package name: `com.yourname.blogwriter`
   - Language: `Kotlin` (또는 Java)
   - Minimum SDK: `API 24 (Android 7.0)`

### 📋 Step 2: 필요한 권한 추가

**app/src/main/AndroidManifest.xml** 수정:

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    
    <!-- 인터넷 권한 추가 -->
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    
    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.BlogWriter"
        android:usesCleartextTraffic="true">
        
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:configChanges="orientation|screenSize">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
```

### 📋 Step 3: MainActivity 코드 작성

**app/src/main/java/com/yourname/blogwriter/MainActivity.kt**:

```kotlin
package com.yourname.blogwriter

import android.os.Bundle
import android.webkit.WebView
import android.webkit.WebViewClient
import android.webkit.WebSettings
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {
    
    private lateinit var webView: WebView
    
    // 여기에 배포된 Streamlit 앱 URL 입력
    private val STREAMLIT_URL = "https://your-app.streamlit.app"
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        
        webView = findViewById(R.id.webview)
        
        // WebView 설정
        webView.apply {
            webViewClient = WebViewClient()
            
            settings.apply {
                javaScriptEnabled = true
                domStorageEnabled = true
                databaseEnabled = true
                cacheMode = WebSettings.LOAD_DEFAULT
                mixedContentMode = WebSettings.MIXED_CONTENT_ALWAYS_ALLOW
                
                // 확대/축소 기능
                setSupportZoom(true)
                builtInZoomControls = true
                displayZoomControls = false
                
                // 추가 설정
                loadWithOverviewMode = true
                useWideViewPort = true
            }
            
            // Streamlit 앱 로드
            loadUrl(STREAMLIT_URL)
        }
    }
    
    // 뒤로가기 버튼 처리
    override fun onBackPressed() {
        if (webView.canGoBack()) {
            webView.goBack()
        } else {
            super.onBackPressed()
        }
    }
}
```

### 📋 Step 4: Layout 파일 작성

**app/src/main/res/layout/activity_main.xml**:

```xml
<?xml version="1.0" encoding="utf-8"?>
<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <WebView
        android:id="@+id/webview"
        android:layout_width="match_parent"
        android:layout_height="match_parent" />

</RelativeLayout>
```

### 📋 Step 5: 앱 아이콘 변경

1. `res/mipmap` 폴더에 아이콘 이미지 추가
2. Android Studio의 Image Asset Studio 사용:
   - `res 우클릭 → New → Image Asset`
   - 아이콘 이미지 선택 및 생성

### 📋 Step 6: 빌드 및 테스트

1. **에뮬레이터 또는 실제 기기 연결**
2. **Run** 버튼 클릭 (또는 Shift + F10)
3. 앱이 설치되고 실행됩니다!

### 📋 Step 7: APK 생성 (배포용)

1. **Build → Generate Signed Bundle / APK**
2. **APK 선택**
3. 키스토어 생성 (처음인 경우):
   - `Create new...` 클릭
   - 정보 입력 및 저장
4. **release** 선택
5. **Finish** 클릭
6. APK 파일이 생성됩니다! (`app/release/app-release.apk`)

---

## 🏪 Google Play Store 배포

### 📋 Step 1: Google Play Console 계정 생성

1. https://play.google.com/console 접속
2. 계정 생성 (일회성 등록비 $25)

### 📋 Step 2: 앱 생성

1. "앱 만들기" 클릭
2. 앱 정보 입력:
   - 앱 이름
   - 기본 언어
   - 앱/게임 선택
   - 무료/유료 선택

### 📋 Step 3: 스토어 등록 정보 작성

필요한 항목:
- ✅ 앱 설명 (간단, 상세)
- ✅ 스크린샷 (최소 2개)
- ✅ 아이콘 (512x512px)
- ✅ 기능 그래픽 (1024x500px)
- ✅ 개인정보처리방침 URL
- ✅ 콘텐츠 등급 설정

### 📋 Step 4: 앱 번들(AAB) 업로드

1. Android Studio에서 **App Bundle** 생성:
   - `Build → Generate Signed Bundle / APK`
   - `Android App Bundle` 선택
2. Play Console에 업로드
3. 심사 요청

### 📋 Step 5: 심사 및 출시

- 심사 기간: 보통 1~3일
- 승인 후 전 세계 배포!

---

## 🐍 방법 3: Python 네이티브 앱

### Kivy 사용 (고급 사용자용)

Python 코드를 네이티브 Android 앱으로 변환합니다.

**장점:**
- ✅ Python 코드 재사용
- ✅ 완전한 네이티브 앱

**단점:**
- ❌ Streamlit을 Kivy로 재작성 필요
- ❌ 복잡한 설정
- ❌ 많은 시간 소요

**추천하지 않음**: Streamlit 앱의 경우 방법 1 또는 2가 훨씬 효율적입니다.

---

## 🎯 추천 방법 요약

### 초보자 또는 빠른 배포:
→ **방법 1 (PWA)** 사용
- Streamlit Cloud에 배포
- 사용자가 "홈 화면에 추가"로 설치
- 개발 시간: 30분

### 정식 앱 스토어 배포:
→ **방법 2 (WebView 앱)** 사용
- Android Studio로 WebView 앱 생성
- Play Store에 배포
- 개발 시간: 2~3시간

---

## 💡 추가 팁

### 1. 오프라인 지원
- Service Worker 추가로 오프라인 캐싱 가능
- 하지만 LLM API는 인터넷 필요

### 2. 푸시 알림
- Firebase Cloud Messaging 통합
- 새 기능 알림 등

### 3. 앱 업데이트
- PWA: 자동 업데이트
- WebView: 서버 코드만 업데이트하면 앱도 자동 업데이트
- 네이티브 앱: Play Store에 새 버전 업로드 필요

### 4. 성능 최적화
- 이미지 최적화
- 캐싱 활용
- API 응답 시간 개선

---

## 📞 도움이 필요하신가요?

- Android Studio 공식 문서: https://developer.android.com/docs
- Streamlit Community: https://discuss.streamlit.io/
- Google Play Console 도움말: https://support.google.com/googleplay/android-developer

---

## ✅ 체크리스트

배포 전 확인사항:

- [ ] Streamlit 앱이 정상 작동하는가?
- [ ] API 키가 안전하게 관리되는가?
- [ ] 모든 기기에서 테스트했는가?
- [ ] 개인정보처리방침을 작성했는가?
- [ ] 앱 아이콘과 스크린샷을 준비했는가?
- [ ] 에러 처리가 잘 되어있는가?
- [ ] 앱 설명을 작성했는가?

---

**행운을 빕니다! 🚀**

