# EAF Base API: AI Agent Documentation

**Target Audience:** AI Coding Agents, Copilots, and LLM-assisted developers.

## 1. Module Overview
`eaf_base_api` is a foundational Python library designed by EchterAlsFake. It serves as the core engine for various media scraping and API wrapper projects. It provides a robust, centralized set of tools for:
- Advanced HTTP networking (with proxy support, retries, and rate-limit handling).
- Intelligent HTTP caching.
- HLS / M3U8 stream parsing and concurrent downloading.
- Declarative, source-aware dataclass models for media objects.
- Concurrent, multi-stage web scraping and item extraction.

Whenever you are working on a codebase that depends on `eaf_base_api`, you must follow the conventions defined by this library rather than implementing custom HTTP clients, scrapers, or caching mechanisms.

## 2. Core Components

### `BaseCore` (Networking & Caching Engine)
The `BaseCore` class is the central HTTP client and session manager. It is built on top of `curl_cffi` to mimic real browser TLS/JA3 fingerprints.

**Key Features:**
- **Lifecycle Management:** Always use `BaseCore` as an asynchronous context manager to ensure proper cleanup of the connection pool (e.g., `async with BaseCore() as core:`).
- **Caching Policies (`CachePolicy`):** Supports precise cache control:
  - `CachePolicy.USE`: Read from cache if fresh, otherwise fetch and write.
  - `CachePolicy.REFRESH`: Force fetch and overwrite cache.
  - `CachePolicy.BYPASS`: Skip cache entirely (neither read nor write).
- **Auto-Retries:** Transparently retries idempotent requests upon network failures.
- **Methods to use:** `core.request()`, `core.fetch_text()`, `core.fetch_bytes()`.

### `RuntimeConfig` (Configuration Container)
`RuntimeConfig` holds the configuration settings used by `BaseCore` and other library components. It allows customization of HTTP parameters, caching rules, retries, and concurrency. 

**Key Configuration Categories:**
- **Caching:** Adjust memory limits and time-to-live for cached responses (`response_cache_size_bytes`, `response_cache_ttl`).
- **Networking:** Control connection parameters like `timeout`, `proxy`, `impersonation` (e.g., `"chrome"`), and `http_version`.
- **Retries:** Customize exponential backoff on network failures (`request_attempts`, `request_retry_initial_delay`, `request_multiplier`).
- **Concurrency:** Limit parallel tasks during scraping and downloading (`videos_concurrency`, `pages_concurrency`, `max_workers_download`).

**How to configure `BaseCore`:**
By default, `BaseCore` falls back to the global singleton `config` from `base_api.modules.config` (e.g., `from base_api import config`). To apply custom settings, pass a custom `RuntimeConfig` object when instantiating `BaseCore`:

```python
from base_api.modules.config import RuntimeConfig
from base_api import BaseCore

my_config = RuntimeConfig()
my_config.request_attempts = 10
my_config.proxy = "http://my-proxy.local:8080"
my_config.impersonation = "safari"

async with BaseCore(configuration=my_config) as core:
    # All requests via this core use my_config settings
    await core.fetch_text("https://example.com")
```

### `BaseMedia` & `media_field` (Lazy-Loaded Data Models)
`BaseMedia` provides a powerful schema for building data models (using standard `dataclass`) where fields might need to be lazily fetched from different remote endpoints (sources).

**Key Features:**
- **`media_field(*sources)`:** Use this function instead of `dataclasses.field()` when defining attributes. It declares which sources (e.g., "html", "api") can provide data for that attribute. The first source listed is the highest priority.
- **`loader_methods` Dictionary:** Subclasses must define `loader_methods` as a class variable, mapping each source name (like `"html"`) to the name of an async instance method (like `"_load_html"`).
- **Atomic Updates:** Loader methods must return a `dict` containing the loaded fields. `BaseMedia` will automatically validate the mapping and apply it to the model. Do NOT mutate the model properties directly inside loader methods.
- **Loading Data:** Callers use `await video.load_fields("title")` or `await video.load_sources("api")` to fetch data. An unresolved field raises `DataNotLoadedError`.

**Example:**
```python
@dataclass(kw_only=True, slots=True)
class Video(BaseMedia):
    title: str | None = media_field("html", "api")
    
    loader_methods: ClassVar[dict[str, str]] = {
        "html": "_load_html",
    }

    async def _load_html(self) -> dict[str, object]:
        data = await self.core.fetch_text(self.url)
        return {"title": "Parsed Title"} # Return a dict, do not set self.title directly
```

### `Helper` & `ScrapeStream` (Concurrent Scraping)
`Helper` is an advanced, concurrent, two-stage scraper pipeline. It fetches paginated listings, extracts dictionaries of item data, and converts them into `BaseMedia` objects.

**Key Features:**
- **Task Sets:** It manages bounded `asyncio` task sets dynamically without heavy `TaskGroup` overhead.
- **Result Ordering:**
  - `ResultOrder.COMPLETION` (Default): Yields parsed items as fast as possible, ignoring original page order.
  - `ResultOrder.ORIGINAL`: Buffers results to yield them in the exact order they appeared on the target pages.
- **Usage:** Create a stream using `helper.iterator()`, and iterate over it inside an `async with` block to guarantee task cleanup. Results are yielded as `ScrapeResult` objects, where you check `result.succeeded` and use `result.unwrap()`.

## 3. Best Practices & Rules for AI Agents

1. **Do not reinvent the wheel:** If a script needs to fetch web content, parse HLS, or scrape data, check if `BaseCore` or `Helper` can do it natively.
2. **Never leave `BaseCore` unclosed:** Use `async with BaseCore() as core:` or explicitly call `await core.close()`. Failing to do so causes unclosed socket warnings.
3. **Data Mutation:** Do not assign values directly to lazily loaded fields in a `BaseMedia` dataclass. Provide the data through the `dict` returned by the configured loader method.
4. **Imports:** Standard components are exposed in `base_api.__init__.py`. Import from `base_api` directly (e.g., `from base_api import BaseCore, BaseMedia, media_field, Helper`).
5. **No `BaseMedia.load()`:** Version 4 removed legacy `.load(api=...)` methods. You must use source-aware media fields and loaders as described above.
