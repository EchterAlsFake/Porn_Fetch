package me.echteralsfake.pornfetch

import android.os.Handler
import android.os.Looper
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.getValue
import androidx.compose.runtime.setValue

/**
 * Python will call ProgressBridge.onProgress(current, total)
 * where current/total are segment counts (not bytes).
 */
object ProgressBridge {

    private val mainHandler = Handler(Looper.getMainLooper())

    // Compose state: UI will automatically recompose when these change.
    var current by mutableStateOf(0L)
        private set

    var total by mutableStateOf(0L)
        private set

    @JvmStatic
    fun reset() {
        mainHandler.post {
            current = 0L
            total = 0L
        }
    }

    @JvmStatic
    fun onProgress(cur: Long, tot: Long) {
        // IMPORTANT: update Compose state on the MAIN THREAD only
        mainHandler.post {
            current = cur
            total = tot
        }
    }
}
