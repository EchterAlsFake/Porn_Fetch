from __future__ import annotations
"""
This file is used for entirely testing the backend of Porn Fetch and verifying
that all sites work and return consistent data.
"""

import asyncio

from dataclasses import dataclass
from src.backend.download_manager import VideoFilters
from PySide6.QtTest import QAbstractItemModelTester, QSignalSpy

ALLOWED_QUALITIES = {144, 240, 250, 360, 480, 540, 720, 1080, 1440, 2160}

def normalize_quality(value) -> int | None:
    """
    Accepts normal representations such as:
        1080
        "1080"
        "1080p"

    Rejects things such as:
        "best"
        "half"
        "worst"
        "1920"
        "860"
        "1080p60"
        None
    """

    if isinstance(value, int):
        return value

    if not isinstance(value, str):
        return None

    value = value.strip().lower()

    if value.endswith("p"):
        value = value[:-1]

    if not value.isdigit():
        return None

    return int(value)

def validate_qualities(available_qualities) -> list[int]:
    if not isinstance(available_qualities, (list, tuple)):
        raise AssertionError(
            "availableQualities is not a list/tuple: "
            f"{available_qualities!r}"
        )

    if not available_qualities:
        raise AssertionError(
            "No qualities were created"
        )

    normalized = []

    for raw_quality in available_qualities:
        quality = normalize_quality(raw_quality)

        if quality is None:
            raise AssertionError(
                f"Invalid quality value: {raw_quality!r}"
            )

        if quality not in ALLOWED_QUALITIES:
            raise AssertionError(
                f"Unsupported quality {raw_quality!r} "
                f"(normalized to {quality})"
            )

        normalized.append(quality)

    return normalized

@dataclass(frozen=True, slots=True)
class WebsiteTest:
    name: str
    url: str
    require_author: bool = True


TESTS = [
    WebsiteTest(
        name="PornHub",
        url="https://www.pornhub.com/view_video.php?viewkey=67bd0f66a8fce",
    ),
    WebsiteTest(
        name="XHamster",
        url="https://xhamster.com/videos/yoga-instructor-guides-us-during-hardcore-sex-xhLLvCd",
    ),
    WebsiteTest(
        name="XNXX",
        url="https://www.xnxx.com/video-i60z5ca/als_der_stiefbruder_amara_der_heissen_kleinen_schwester_ihr_tagebuch_findet_weiss_er_dass_es_der_weg_zu_ihrer_sussen_muschi_ist._sieh_zu_wie_sie_seinen_schwanz_bis_zu_einem_gesicht_voller_sperma_lutscht_und_fickt_nur_um_sie_dreckig_zu_halten"
    ),
    WebsiteTest(
        name="xvideos",
        url="https://de.xvideos.com/video.omtdluc3e5f/52563166/0/my_slutty_stepsister_was_getting_ready_for_a_date_but_i_sto_p_d_her_and_fucked_her_myself"
    ),
    WebsiteTest(
        name="eporner",
        url="https://www.eporner.com/video-DwpUUJacHxs/jewelry-process-in-the-making/"
    ),
    WebsiteTest(
        name="spankbang",
        url="https://spankbang.com/a4u5v/video/dogfart+from+parking+war+to+hardcore+fuck+adira+allure+vs+monster+neighbor+cock"
    ),
    WebsiteTest(
        name="youporn",
        url="https://www.youporn.com/watch/196323191/"
    ),
    WebsiteTest(
        name="beeg",
        url="https://beeg.com/-0785353135636417"
    ),
    WebsiteTest(
        name="redtube",
        url="https://de.redtube.com/191071081"
    ),
    WebsiteTest(
        name="thumbzilla",
        url="https://www.thumbzilla.com/watch/264561861/"
    ),
    WebsiteTest(
        name="tube8",
        url="https://www.tube8.com/porn-video/264330411/"
    ),
    WebsiteTest(
        name="xfreehd",
        url="https://beta.xfreehd.com/video/1060341/camilla-cream-cumsters"
    ),
    WebsiteTest(
        name="porntrex",
        url="https://www.porntrex.com/video/3002169/gaia-on-top-anal-creampie"
    )

    # This contains all websites to test for the single URL mode
]


async def test_url(
    backend,
    model,
    test: WebsiteTest,
    timeout: float = 60.0,
) -> dict:
    before = model.rowCount()

    # This verifies the actual Qt model notification as well.
    rows_inserted_spy = QSignalSpy(model.rowsInserted)

    try:
        await asyncio.wait_for(
            backend._process_single_url(
                url=test.url,
                custom_options="",
                filters=VideoFilters(),
            ),
            timeout=timeout,
        )

    except TimeoutError:
        raise AssertionError(
            f"Timed out after {timeout:.0f}s"
        )

    after = model.rowCount()

    if after <= before:
        raise AssertionError(
            "Processing finished, but no row was added"
        )

    if rows_inserted_spy.count() < 1:
        raise AssertionError(
            "Model changed without emitting rowsInserted"
        )

    # Inspect only rows created by this URL.
    for row in range(before, after):
        index = model.index(row, 0)

        job_id = model.data(index, model.JobIdRole)
        title = model.data(index, model.TitleRole)
        author = model.data(index, model.AuthorRole)

        available_qualities = model.data(
            index,
            model.AvailableQualitiesRole,
        )

        selected_quality = model.data(
            index,
            model.SelectedQualityRole,
        )

        if not isinstance(title, str) or not title.strip():
            continue

        if test.require_author:
            if not isinstance(author, str) or not author.strip():
                continue

        if not str(job_id).strip():
            continue

        normalized_qualities = validate_qualities(
            available_qualities
        )

        normalized_selected = normalize_quality(
            selected_quality
        )

        if normalized_selected is None:
            raise AssertionError(
                f"Row {row}: invalid selected quality: "
                f"{selected_quality!r}"
            )

        if normalized_selected not in ALLOWED_QUALITIES:
            raise AssertionError(
                f"Row {row}: selected quality "
                f"{selected_quality!r} is unsupported"
            )

        if normalized_selected not in normalized_qualities:
            raise AssertionError(
                f"Row {row}: selected quality "
                f"{selected_quality!r} is not present in "
                f"available qualities {available_qualities!r}"
            )

        return {
            "row": row,
            "job_id": job_id,
            "title": title,
            "author": author,
            "qualities": normalized_qualities,
            "selected_quality": normalized_selected,
        }

    raise AssertionError(
        "A row was created, but it did not contain valid metadata"
    )

async def run_smoke_tests(backend, model) -> int:
    # Let Qt continuously sanity-check your model while we're testing.
    model_tester = QAbstractItemModelTester(
        model,
        QAbstractItemModelTester.FailureReportingMode.Warning,
    )

    passed = 0
    failed = 0

    print()
    print("=" * 72)
    print(" LIVE WEBSITE SMOKE TESTS")
    print("=" * 72)

    for number, test in enumerate(TESTS, start=1):
        prefix = f"[{number:02d}/{len(TESTS):02d}] {test.name}"

        try:
            result = await test_url(
                backend=backend,
                model=model,
                test=test,
            )

        except Exception as exc:
            failed += 1

            print(f"{prefix:<35} FAIL")
            print(f"      {exc}")

        else:
            passed += 1

            print(f"{prefix:<35} PASS")
            print(f"      title : {result['title']!r}")
            print(f"      author: {result['author']!r}")
            print(f"      qualities : {result['qualities']}")
            print(f"      selected  : {result['selected_quality']}")

    print()
    print("=" * 72)
    print(
        f"{passed} passed | "
        f"{failed} failed | "
        f"{len(TESTS)} total"
    )

    print("=" * 72)

    # Keep model_tester alive until everything has finished.
    del model_tester

    return 0 if failed == 0 else 1