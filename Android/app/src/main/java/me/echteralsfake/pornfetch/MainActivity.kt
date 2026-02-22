package me.echteralsfake.pornfetch

import android.content.ContentValues
import android.content.Context
import android.os.Build
import android.os.Bundle
import android.provider.MediaStore
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.Info
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material3.*
import androidx.compose.material3.adaptive.navigationsuite.NavigationSuiteScaffold
import androidx.compose.runtime.*
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.tooling.preview.PreviewScreenSizes
import androidx.compose.ui.unit.dp
import androidx.core.splashscreen.SplashScreen.Companion.installSplashScreen
import com.chaquo.python.PyException
import com.chaquo.python.PyObject
import com.chaquo.python.Python
import com.chaquo.python.android.AndroidPlatform
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import me.echteralsfake.pornfetch.ui.theme.PornFetchTheme
import java.io.File

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
        quality: String = "best",
        path: String
    ) {
        // This function does not return a value.
        // It will throw an exception on failure, which is caught by the caller.
        module.callAttr("download_android", url, quality, path)
    }
}

/**
 * Safely gets a string attribute from a Python object by calling Python's built-in `getattr`.
 * This is a robust way to access attributes on an object like a dataclass instance.
 */
fun getPyAttrString(pyObj: PyObject, key: String): String? {
    return try {
        val builtins = Python.getInstance().getModule("builtins")
        val attr = builtins.callAttr("getattr", pyObj, key)

        val s = attr?.toString()?.trim('"')
        if (s.isNullOrEmpty() || s == "None") {
            null
        } else {
            s
        }
    } catch (e: PyException) {
        // Attribute does not exist or another Python error occurred.
        null
    }
}

/**
 * Moves a file from app-private storage to the public MediaStore (Gallery).
 * @return The public path for display, or null on failure.
 */
fun moveVideoToGallery(context: Context, sourcePath: String): String? {
    val sourceFile = File(sourcePath)
    if (!sourceFile.exists()) {
        return null
    }

    val displayName = sourceFile.name
    val mimeType = "video/mp4" // Assuming MP4. A more robust solution might probe the file.
    val collection = MediaStore.Video.Media.EXTERNAL_CONTENT_URI

    val contentValues = ContentValues().apply {
        put(MediaStore.MediaColumns.DISPLAY_NAME, displayName)
        put(MediaStore.MediaColumns.MIME_TYPE, mimeType)
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            // Scoped storage: save to a specific sub-directory in Videos.
            put(MediaStore.MediaColumns.RELATIVE_PATH, "Movies/PornFetch")
            put(MediaStore.MediaColumns.IS_PENDING, 1)
        }
    }

    val resolver = context.contentResolver
    val uri = resolver.insert(collection, contentValues)

    uri?.let { newUri ->
        try {
            resolver.openOutputStream(newUri)?.use { outputStream ->
                sourceFile.inputStream().use { inputStream ->
                    inputStream.copyTo(outputStream)
                }
            }

            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
                contentValues.clear()
                contentValues.put(MediaStore.MediaColumns.IS_PENDING, 0)
                resolver.update(newUri, contentValues, null, null)
            }

            sourceFile.delete() // Clean up the original file.
            return if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
                "Movies/PornFetch/$displayName"
            } else {
                // On older versions, we don't have a clean relative path.
                "Gallery (Videos)"
            }
        } catch (e: Exception) {
            // If copy fails, delete the incomplete MediaStore entry.
            resolver.delete(newUri, null, null)
            return null
        }
    }

    return null
}


class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        installSplashScreen()

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

    // App-private folder (no permissions needed for this staging area)
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
                statusText = "Starting..."
                ProgressBridge.reset()

                scope.launch {
                    try {
                        statusText = "Getting video info..."
                        val downloadedFilePath = withContext(Dispatchers.IO) {
                            PornFetchPython.refreshClients()

                            val video = PornFetchPython.checkVideo(url)
                            val attributes = PornFetchPython.loadVideoAttributes(video)
                            val title = getPyAttrString(attributes, "title") // Correctly get attribute
                                ?: "video_${System.currentTimeMillis()}" // Fallback title

                            // Sanitize title to create a valid filename
                            val sanitizedTitle = title.replace(Regex("[^a-zA-Z0-9._-]"), "_").take(100)
                            val filename = "$sanitizedTitle.mp4"
                            val targetFile = File(downloadDir, filename)

                            statusText = "Downloading..."
                            PornFetchPython.downloadWithProgress(
                                url = url,
                                quality = "best",
                                path = targetFile.absolutePath // Pass the full, explicit file path
                            )

                            // If we get here, the download is presumed successful. Return the path for the next step.
                            targetFile.absolutePath
                        }

                        statusText = "Download complete, moving to gallery..."
                        val galleryPath = withContext(Dispatchers.IO) {
                            moveVideoToGallery(context, downloadedFilePath)
                        }

                        statusText = if (galleryPath != null) {
                            "✅ Download finished!\nSaved to: $galleryPath"
                        } else {
                            "⚠️ Download finished, but failed to move to gallery. File is in app's private folder."
                        }

                    } catch (e: Exception) {
                        // This will catch errors from Python (e.g., invalid URL) or file operations.
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
