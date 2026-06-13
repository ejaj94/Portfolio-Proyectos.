package com.example.logleveentregador

import android.os.Bundle
import android.view.ViewGroup
import android.webkit.WebView
import android.webkit.WebViewClient
import android.webkit.GeolocationPermissions
import android.webkit.WebChromeClient
import android.webkit.WebSettings
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.ui.Modifier
import androidx.compose.ui.viewinterop.AndroidView
import com.example.logleveentregador.theme.LogleveEntregadorTheme
import androidx.core.app.ActivityCompat
import android.Manifest
import android.content.pm.PackageManager

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        // Request Location Permissions for maps and GPS tracking
        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this, arrayOf(Manifest.permission.ACCESS_FINE_LOCATION, Manifest.permission.ACCESS_COARSE_LOCATION), 1)
        }

        enableEdgeToEdge()
        setContent {
            LogleveEntregadorTheme {
                Surface(modifier = Modifier.fillMaxSize(), color = MaterialTheme.colorScheme.background) {
                    AndroidView(
                        factory = { context ->
                            WebView(context).apply {
                                layoutParams = ViewGroup.LayoutParams(
                                    ViewGroup.LayoutParams.MATCH_PARENT,
                                    ViewGroup.LayoutParams.MATCH_PARENT
                                )
                                webViewClient = object : WebViewClient() {
                                    override fun shouldOverrideUrlLoading(view: WebView?, request: android.webkit.WebResourceRequest?): Boolean {
                                        val url = request?.url?.toString() ?: ""
                                        view?.loadUrl(url)
                                        return true
                                    }
                                }
                                webChromeClient = object : WebChromeClient() {
                                    override fun onGeolocationPermissionsShowPrompt(
                                        origin: String?,
                                        callback: GeolocationPermissions.Callback?
                                    ) {
                                        callback?.invoke(origin, true, false)
                                    }
                                }
                                settings.javaScriptEnabled = true
                                settings.domStorageEnabled = true
                                settings.setGeolocationEnabled(true)
                                settings.mixedContentMode = WebSettings.MIXED_CONTENT_ALWAYS_ALLOW
                                
                                loadUrl("https://logleve-delivery.azurewebsites.net/apps/courier")
                            }
                        },
                        modifier = Modifier.fillMaxSize()
                    )
                }
            }
        }
    }
}

