"""Bounded async iteration with cooperative worker cleanup."""
from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import aclosing
from typing import TypeVar, cast

T = TypeVar("T")
R = TypeVar("R")


async def run_workers(
    items: AsyncIterator[T], operation: Callable[[T], Awaitable[None]], concurrency: int,
) -> None:
    """Apply an operation with bounded buffering; await all workers on exit."""
    count = max(1, concurrency)
    queue = asyncio.Queue(maxsize=count)
    sentinel = object()

    async def produce() -> None:
        async with aclosing(items):
            async for item in items:
                await queue.put(item)
        for _ in range(count):
            await queue.put(sentinel)

    async def consume() -> None:
        while True:
            item = await queue.get()
            if item is sentinel:
                return
            await operation(item)
            # CLI download handlers may consume cancellation to persist pause state.
            if asyncio.current_task().cancelling():
                return

    tasks = [asyncio.create_task(produce())]
    tasks.extend(asyncio.create_task(consume()) for _ in range(count))
    try:
        await asyncio.gather(*tasks)
    finally:
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)


async def bounded_map(
    items: list[T], operation: Callable[[T], Awaitable[R]], concurrency: int,
) -> list[R]:
    """Preserve input order without creating one task per item."""
    results: list[R | None] = [None] * len(items)

    async def indexed_items():
        for index, item in enumerate(items):
            yield index, item

    async def dispatch(indexed) -> None:
        index, item = indexed
        results[index] = await operation(item)

    await run_workers(indexed_items(), dispatch, concurrency)
    return cast(list[R], results)
