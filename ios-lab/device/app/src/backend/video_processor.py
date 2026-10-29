"""Asynchronous video-iterator preparation for the desktop frontend."""
from __future__ import annotations

import asyncio
from contextlib import aclosing
from datetime import datetime
from pathlib import Path
import re
from typing import AsyncGenerator, AsyncIterator
import uuid

from base_api.modules.errors import (
    AccessDeniedError,
    BotProtectionDetected,
    ChallengeMathError,
    DataNotLoadedError,
    RateLimitError,
    SecurityAbort,
)
from src.shared.logging_setup import configure_app_logging
from pornhub_api.modules.errors import GifPendingReview, VideoDisabled
from PySide6.QtCore import QObject, Signal

from src.backend import clients
from src.backend.config import __version__, app_settings
from src.backend.download_manager import DownloadManager, VideoFilters, VideoObject
from src.backend.helper_functions import make_debug_log
from src.shared.error_reporting import report_exception
from src.shared.download_options import title_template, video_output_path
from src.shared.errors import (
    AppBotBlocked,
    AppNetworkError,
    AppNotFoundError,
    safe_api_call,
)


class ProcessVideos(QObject):
    error_signal = Signal(str)

    """
    This class is responsible for processing the videos in the background, loading the data, adjusting paths and
    handling errors
    """

    def __init__(self, iterator: AsyncGenerator, custom_path_options: str, video_filters: VideoFilters,
                 download_manager: DownloadManager, reverse_videos: bool, stop_flag: asyncio.Event,
                 origin_iterator_url: str | None = None, origin_iterator_name: str | None = None) -> None:
        super().__init__()
        video_filters.validate()
        title_template(custom_path_options)
        self.iterator = iterator
        self.custom_path_options = custom_path_options
        self.download_manager = download_manager
        self.reverse_videos = reverse_videos
        self.stop_flag = stop_flag
        self.video_filters = video_filters
        self.origin_iterator_url = origin_iterator_url
        self.origin_iterator_name = origin_iterator_name
        self.max_attempts = app_settings.retries
        self.output_path = app_settings.output_path
        self.result_limit = app_settings.result_limit
        self.logger = configure_app_logging(logger_name="Porn Fetch - [ProcesVideos]", log_file="PornFetch.log",
                                            level=app_settings.log_level_map.get(app_settings.log_level, "INFO"))

    @staticmethod
    async def reverse_iterator(iterator: AsyncIterator):
        videos = []
        async for video in iterator:
            videos.append(video)  # This is very stupid, please don't use this „feature"!

        return reversed(videos)

    def process_filter(self, filters: VideoFilters, attributes: VideoObject) -> bool:
        # 1. Duration Filters
        if filters.duration_minimum is not None or filters.duration_maximum is not None:
            if attributes.length is None:
                return False
            if filters.duration_minimum is not None and attributes.length < filters.duration_minimum:
                return False
            if filters.duration_maximum is not None and attributes.length > filters.duration_maximum:
                return False

        # 2. Regex Filters
        if filters.author_regex:
            if not re.search(filters.author_regex, attributes.author, re.IGNORECASE):
                return False

        if filters.title_regex:
            if not re.search(filters.title_regex, attributes.title, re.IGNORECASE):
                return False

        if filters.tags_regex:
            # Fails immediately if the video has no tags to match against
            if not attributes.tags:
                return False
            pattern = re.compile(filters.tags_regex, re.IGNORECASE)
            # Passes if at least one tag matches the regex
            if not any(pattern.search(tag) for tag in attributes.tags):
                return False

        # 3. Quality Filters (Evaluated based on the highest available quality)
        if filters.quality_minimum or filters.quality_maximum:
            if not attributes.qualities:
                return False
            max_quality = self._get_max_quality(attributes.qualities)

            if filters.quality_minimum:
                min_q = self._parse_quality(filters.quality_minimum)
                if max_quality < min_q:
                    return False

            if filters.quality_maximum:
                max_q = self._parse_quality(filters.quality_maximum)
                if max_quality > max_q:
                    return False

        # 4. Date Filters
        if filters.published_after:
            if attributes.publish_date is None:
                return False
            after_date = datetime.fromisoformat(filters.published_after).date()
            pub_date = attributes.publish_date.date()
            if pub_date < after_date:
                return False

        if filters.published_before:
            if attributes.publish_date is None:
                return False
            before_date = datetime.fromisoformat(filters.published_before).date()
            pub_date = attributes.publish_date.date()
            if pub_date > before_date:
                return False

        # If it survives all the checks, all applied filters are True!
        return True

    @staticmethod
    def _parse_quality(quality_str: str | int) -> int:
        """Read resolution labels, with 4K represented by its 2160 vertical pixels."""
        if not quality_str:
            return 0

        return VideoFilters.quality_value(quality_str)

    def _get_max_quality(self, qualities: list[str | int]) -> int:
        """Finds the highest resolution available in the list of qualities."""
        if not qualities:
            return 0
        parsed_qualities = [self._parse_quality(q) for q in qualities]
        return max(parsed_qualities)

    @staticmethod
    async def process_single_video(video_object: str | clients.AllowedVideoType) -> tuple[
        clients.AllowedVideoType, VideoObject]:
        video = await clients.get_video(video_object)
        video_attributes = await clients.load_video_attributes(video=video)
        return video, video_attributes

    def create_output_path(self, video_attributes: VideoObject, index: int, user_pattern: str) -> Path:
        return video_output_path(video_attributes, index, user_pattern, self.output_path)

    async def start_processing(self):
        self.logger.info("Starting Processing of Iterator!")

        if self.reverse_videos:
            self.iterator = self.reverse_iterator(self.iterator)

        async with aclosing(self.iterator) as iterator:
            idx = 0
            examined = 0
            async for video in iterator:
                idx += 1
                if self.stop_flag.is_set():
                    return
                if idx < max(1, self.video_filters.start_index):
                    continue
                if self.video_filters.end_index and idx > self.video_filters.end_index:
                    break
                print(f"Processing: {video} {idx}")
                video_url = getattr(video, "url", str(video))
                if self.result_limit is not None and examined >= self.result_limit:
                    break
                examined += 1

                last_error = None  # Keeps track of the
                last_exception = None

                if self.stop_flag.is_set():
                    return  # User hit the abort button

                if app_settings.processing_delay:
                    await asyncio.sleep(float(app_settings.processing_delay))
                    if self.stop_flag.is_set():
                        return

                try:
                    self.logger.debug(f"Current Index: {idx}")
                    video, video_object = await safe_api_call(self.process_single_video, video)
                    print(f"Video: {video}")

                    self.logger.info("Checking Filters...")
                    if self.process_filter(self.video_filters, video_object):
                        identifier = uuid.uuid4().hex
                        self.logger.info(f"Successfully received Video! [Identifier ->: {identifier}]")
                        output_path = self.create_output_path(video_object, idx, self.custom_path_options)

                        quality = app_settings.mappings_quality.get(int(app_settings.quality))
                        quality = quality if quality in video_object.qualities else (video_object.qualities[0] if video_object.qualities else "best")

                        video_object.output_path = output_path
                        video_object.identifier = identifier
                        video_object.index = idx
                        video_object.selected_quality = quality
                        video_object.source_video = video
                        video_object.origin_iterator_url = self.origin_iterator_url
                        video_object.origin_iterator_name = self.origin_iterator_name

                        self.download_manager.add_video(video_object)

                # General Errors
                except AppNetworkError as e:
                    last_exception = e
                    last_error = make_debug_log(e=e, video_url=video_url, function="start_processing", user_message="""
                    A network error happened, I'll try retrying...""")
                    continue  # Maybe it solves by itself ;)

                except AppNotFoundError as e:
                    last_exception = e
                    last_error = make_debug_log(e=e, video_url=video_url, function="start_processing", user_message="""
                    I was trying to access a website, but turns out, it doesn't exist. Please verify if you entered
                    the correct URL.
    
                    If you are sure you did, please report this issue
                    """)

                    break  # If the resource is not there, it won't magically appear lmao

                except (VideoDisabled, GifPendingReview) as e:
                    last_exception = e
                    last_error = make_debug_log(e=e, video_url=video_url, function="start_processing", user_message="""
                    The Video / GIF seems to be disabled or pending a review! It can't be downloaded (yet) :(
                    """)
                    break

                except (SecurityAbort, ChallengeMathError, ChallengeMathError) as e:
                    last_exception = e
                    last_error = make_debug_log(e=e, video_url=video_url, function="start_processing", user_message="""
                    An error occurred while solving a challenge from PornHub, please report this immediately, I need to 
                    fix this quickly!""")
                    break

                except RateLimitError as e:
                    last_exception = e
                    last_error = make_debug_log(e=e, video_url=video_url, function="start_processing", user_message="""
                    You got rate limited by the server. I have already tried solving this, which didn't work. 
                    Please use a (different) proxy or VPN.""")
                    break

                except DataNotLoadedError as e:
                    last_exception = e
                    last_error = make_debug_log(e=e, video_url=video_url, function="start_processing", user_message=f"""
                    If you see this I fucked up developing my API packages and you should immediately open an issue on 
                    GitHub lol""")
                    break

                except (AccessDeniedError, BotProtectionDetected, AppBotBlocked) as e:
                    last_exception = e
                    last_error = make_debug_log(e=e, video_url=video_url, function="start_processing", user_message="""
                    The website denied access, probably because it detected you as a bot. Please report this, as I probably
                    need to update the headers. 
                    """)

                except Exception as e:
                    last_exception = e
                    self.logger.error(f"UNHANDLED EXCEPTION in start_processing: {e}", exc_info=True)
                    last_error = make_debug_log(e=e, video_url=video_url, function="start_processing", user_message="An unexpected error occurred.")
                    break

                finally:
                    if last_exception is not None:
                        report_id = await report_exception(
                            last_exception,
                            operation="prepare scraped video",
                            location="ProcessVideos.start_processing",
                            context={
                                "video_url": video_url,
                                "origin_url": self.origin_iterator_url,
                                "video_index": idx,
                            },
                            enabled=app_settings.enable_logging,
                            version=__version__,
                        )
                        if last_error is not None:
                            last_error = f"{last_error.rstrip()}\n\nError ID: {report_id}"
                    if last_error is not None:
                        self.error_signal.emit(last_error)
