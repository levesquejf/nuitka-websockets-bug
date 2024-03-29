import asyncio
import gc
import objgraph
import websockets

from concurrent.futures import CancelledError


async def hello(text):
    uri = "wss://echo.websocket.org"
    async with websockets.connect(uri) as ws:

        reader_task = asyncio.ensure_future(reader(ws))
        writer_task = asyncio.ensure_future(writer(ws, text))
        await asyncio.wait(
            [reader_task, writer_task], return_when=asyncio.FIRST_COMPLETED,
        )

        for task in (reader_task, writer_task):
            if not task.done():
                task.cancel()
            try:
                await task
            except CancelledError:
                pass


async def reader(ws):
    while True:
        r = await ws.recv()
        print(f"{r}")


async def writer(ws, text):
    await ws.send(text)
    await asyncio.sleep(0.5)


async def run():
    await hello(f"Test")

    print("Objects before loop")
    gc.collect()
    obj_start = len(gc.get_objects())
    objgraph.show_growth(shortnames=False)

    for i in range(0, 20):
        await hello(f"Test {i}")

    print("\n\nObjects after loop")
    gc.collect()
    obj_end = len(gc.get_objects())
    objgraph.show_growth(shortnames=False)

    print(f"\nObjects Count Diff: {obj_end - obj_start}")

    for t in asyncio.Task.all_tasks():
        print(t)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())


if __name__ == "__main__":
    main()
