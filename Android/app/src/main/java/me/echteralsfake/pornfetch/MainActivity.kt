package me.echteralsfake.pornfetch
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import kotlinx.coroutines.withContext
import com.chaquo.python.Python
import com.chaquo.python.PyObject
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.Info
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.material3.adaptive.navigationsuite.NavigationSuiteScaffold
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.tooling.preview.PreviewScreenSizes
import com.chaquo.python.android.AndroidPlatform
import me.echteralsfake.pornfetch.ui.theme.PornFetchTheme


object PornFetchPython {

    private val module: PyObject by lazy {
        Python.getInstance().getModule("clients")
    }

    fun refreshClients(enableKillSwitch: Boolean = false) {
        module.callAttr("refresh_clients", enableKillSwitch)
    }

    fun checkVideo(url: String): PyObject {
        return module.callAttr("check_video", url)
    }

    fun loadVideoAttributes(video: PyObject): PyObject {
        return module.callAttr("load_video_attributes", video)
    }

    fun downloadWithProgress(
        url: String,
        downloader: String = "threaded",
        quality: String = "best",
        path: String
    ): Boolean {
        val result = module.callAttr("download_android", url, downloader, quality, path)
        return result.toJava(Boolean::class.java)
    }
} // ✅ <-- THIS closes the object properly


fun pyDictString(dict: PyObject, key: String): String? {
    val v = dict.asMap()[PyObject.fromJava(key)] ?: return null
    val s = v.toString().trim('"')
    return if (s == "None") null else s
}

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {

        if (!Python.isStarted()) {
            Python.start(AndroidPlatform(this))
        }

        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            PornFetchTheme {
                PornFetchApp()
            }
        }
    }
}

@PreviewScreenSizes
@Composable
fun PornFetchApp() {
    var currentDestination by rememberSaveable { mutableStateOf(AppDestinations.HOME) }

    NavigationSuiteScaffold(
        navigationSuiteItems = {
            AppDestinations.entries.forEach {
                item(
                    icon = { Icon(it.icon, contentDescription = it.label) },
                    label = { Text(it.label) },
                    selected = it == currentDestination,
                    onClick = { currentDestination = it }
                )
            }
        }
    ) {
        when (currentDestination) {
            AppDestinations.HOME -> HomeScreen()
            AppDestinations.SETTINGS -> Text("Settings screen (later)")
            AppDestinations.INFO -> Text("Credits screen (later)")
        }
    }
}

enum class AppDestinations(
    val label: String,
    val icon: ImageVector,
) {
    HOME("Home", Icons.Default.Home),
    SETTINGS("Settings", Icons.Default.Settings),
    INFO("Credits", Icons.Default.Info),
}

@Composable
fun HomeScreen() {
        var url by remember { mutableStateOf("") }
        var statusText by remember { mutableStateOf("Paste a URL and press Download.") }
        var isDownloading by remember { mutableStateOf(false) }

        val scope = rememberCoroutineScope()
        val context = LocalContext.current

        // App-private folder (no permissions needed)
        val downloadDir =
            context.getExternalFilesDir(null)?.absolutePath
                ?: context.filesDir.absolutePath

        // Progress from the bridge (segments)
        val current = ProgressBridge.current
        val total = ProgressBridge.total

        val fraction =
            if (total > 0) (current.toFloat() / total.toFloat()).coerceIn(0f, 1f) else 0f

        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp)
        ) {
            Text("Download test", style = MaterialTheme.typography.titleLarge)

            Spacer(modifier = Modifier.height(12.dp))

            OutlinedTextField(
                value = url,
                onValueChange = { url = it },
                modifier = Modifier.fillMaxWidth(),
                label = { Text("Video URL") },
                singleLine = true
            )

            Spacer(modifier = Modifier.height(12.dp))

            Button(
                enabled = url.isNotBlank() && !isDownloading,
                onClick = {
                    isDownloading = true
                    statusText = "Starting download..."
                    ProgressBridge.reset()

                    scope.launch {
                        try {
                            val ok = withContext(Dispatchers.IO) {
                                PornFetchPython.refreshClients()

                                // "quality" and "downloader" depend on your APIs
                                PornFetchPython.downloadWithProgress(
                                    url = url,
                                    downloader = "threaded",
                                    quality = "best",
                                    path = downloadDir
                                )
                            }

                            statusText = if (ok) {
                                "✅ Download finished!\nSaved in:\n$downloadDir"
                            } else {
                                "❌ Download failed / unsupported URL."
                            }
                        } catch (e: Exception) {
                            statusText = "❌ Error:\n${e.message}"
                        } finally {
                            isDownloading = false
                        }
                    }
                }
            ) {
                Text(if (isDownloading) "Downloading..." else "Download")
            }

            Spacer(modifier = Modifier.height(16.dp))

            Text("Progress: $current / $total segments (${(fraction * 100).toInt()}%)")

            LinearProgressIndicator(
                progress = fraction,
                modifier = Modifier.fillMaxWidth()
            )

            Spacer(modifier = Modifier.height(16.dp))

            Card(modifier = Modifier.fillMaxWidth()) {
                Text(
                    text = statusText,
                    modifier = Modifier.padding(16.dp),
                    style = MaterialTheme.typography.bodyLarge
                )
            }
        }
    }
