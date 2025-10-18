package com.yourname.blogwriter

import android.os.Bundle
import android.webkit.WebView
import android.webkit.WebViewClient
import android.webkit.WebSettings
import android.webkit.WebChromeClient
import android.view.View
import android.widget.ProgressBar
import androidx.appcompat.app.AppCompatActivity
import androidx.swiperefreshlayout.widget.SwipeRefreshLayout

/**
 * 블로그 글 작성기 Android 앱
 * Streamlit 웹앱을 WebView로 표시
 */
class MainActivity : AppCompatActivity() {
    
    private lateinit var webView: WebView
    private lateinit var progressBar: ProgressBar
    private lateinit var swipeRefreshLayout: SwipeRefreshLayout
    
    // ⚠️ 여기에 배포된 Streamlit 앱 URL을 입력하세요
    private val STREAMLIT_URL = "https://your-app.streamlit.app"
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        
        // View 초기화
        webView = findViewById(R.id.webview)
        progressBar = findViewById(R.id.progressBar)
        swipeRefreshLayout = findViewById(R.id.swipeRefreshLayout)
        
        setupWebView()
        setupSwipeRefresh()
        
        // Streamlit 앱 로드
        webView.loadUrl(STREAMLIT_URL)
    }
    
    /**
     * WebView 설정
     */
    private fun setupWebView() {
        webView.apply {
            // WebViewClient 설정
            webViewClient = object : WebViewClient() {
                override fun onPageFinished(view: WebView?, url: String?) {
                    super.onPageFinished(view, url)
                    progressBar.visibility = View.GONE
                    swipeRefreshLayout.isRefreshing = false
                }
                
                override fun shouldOverrideUrlLoading(view: WebView?, url: String?): Boolean {
                    return false // WebView에서 처리
                }
            }
            
            // WebChromeClient 설정 (로딩 진행률)
            webChromeClient = object : WebChromeClient() {
                override fun onProgressChanged(view: WebView?, newProgress: Int) {
                    super.onProgressChanged(view, newProgress)
                    if (newProgress < 100) {
                        progressBar.visibility = View.VISIBLE
                        progressBar.progress = newProgress
                    } else {
                        progressBar.visibility = View.GONE
                    }
                }
            }
            
            // WebSettings 설정
            settings.apply {
                // JavaScript 활성화 (Streamlit 필수)
                javaScriptEnabled = true
                
                // DOM Storage 활성화
                domStorageEnabled = true
                databaseEnabled = true
                
                // 캐시 설정
                cacheMode = WebSettings.LOAD_DEFAULT
                
                // Mixed Content 허용 (필요시)
                mixedContentMode = WebSettings.MIXED_CONTENT_ALWAYS_ALLOW
                
                // 확대/축소 기능
                setSupportZoom(true)
                builtInZoomControls = true
                displayZoomControls = false // 줌 컨트롤 숨김
                
                // 뷰포트 설정
                loadWithOverviewMode = true
                useWideViewPort = true
                
                // 텍스트 크기 조정
                textZoom = 100
                
                // 파일 접근 (필요시)
                allowFileAccess = true
                allowContentAccess = true
                
                // 추가 성능 설정
                setRenderPriority(WebSettings.RenderPriority.HIGH)
                setEnableSmoothTransition(true)
            }
        }
    }
    
    /**
     * 스와이프로 새로고침 설정
     */
    private fun setupSwipeRefresh() {
        swipeRefreshLayout.apply {
            setOnRefreshListener {
                webView.reload()
            }
            
            // 새로고침 색상 설정
            setColorSchemeResources(
                android.R.color.holo_blue_bright,
                android.R.color.holo_green_light,
                android.R.color.holo_orange_light,
                android.R.color.holo_red_light
            )
        }
    }
    
    /**
     * 뒤로가기 버튼 처리
     */
    override fun onBackPressed() {
        if (webView.canGoBack()) {
            webView.goBack()
        } else {
            super.onBackPressed()
        }
    }
    
    /**
     * WebView 상태 저장
     */
    override fun onSaveInstanceState(outState: Bundle) {
        super.onSaveInstanceState(outState)
        webView.saveState(outState)
    }
    
    /**
     * WebView 상태 복원
     */
    override fun onRestoreInstanceState(savedInstanceState: Bundle) {
        super.onRestoreInstanceState(savedInstanceState)
        webView.restoreState(savedInstanceState)
    }
    
    /**
     * 액티비티 일시정지 시
     */
    override fun onPause() {
        super.onPause()
        webView.onPause()
    }
    
    /**
     * 액티비티 재개 시
     */
    override fun onResume() {
        super.onResume()
        webView.onResume()
    }
    
    /**
     * 액티비티 종료 시
     */
    override fun onDestroy() {
        webView.destroy()
        super.onDestroy()
    }
}

