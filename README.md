Issue tracked at [Nuitka/#xxx](https://github.com/Nuitka/Nuitka/issues/xxx) and [Websockets/#669](https://github.com/aaugustin/websockets/issues/699).

This repo reproduces a bug causing memory leaks when using `Websockets` >= 8.0 with `Nuitka`. When the `reader()` task is cancelled, the `WebSocketCommonProtocol.close_connection()`, `WebSocketCommonProtocol.keepalive_ping()` and `WebSocketCommonProtocol.transfer_data()` tasks are still present in the `asyncio.Task.all_tasks()` even if `gc.collect()` is run manually. The issue only occurs when the code is compiled with nuitka. It can be easily reproduced using Docker containers.

This bug is present with both Python 3.6.9 and 3.7.5 (tested with Nuitka 0.6.5).

### Running on Linux (Docker) with native Python 3.7.5

```
# ./run-native.sh
( ... docker building the image ... )

Task 0
Task 1
( ... up to Task 19 ... )

<Task pending coro=<run() running at main.py:44> cb=[_run_until_complete_cb() at /usr/local/lib/python3.7/asyncio/base_events.py:153]>
```

### Running on Linux (Docker), compiled with Nuitka 0.6.5 on Python 3.7.5

```
# ./run-nuitka.sh
( ... docker building the image ... )

Task 0
Task 1
( ... up to Task 19 ... )

( ... A lot of WS tasks are present ... )
<Task finished coro=<WebSocketCommonProtocol.close_connection() done, defined at /opt/app/main.dist/websockets/protocol.py:1153> result=None>
<Task cancelled coro=<WebSocketCommonProtocol.keepalive_ping() done, defined at /opt/app/main.dist/websockets/protocol.py:1103>>
<Task finished coro=<WebSocketCommonProtocol.transfer_data() done, defined at /opt/app/main.dist/websockets/protocol.py:818> result=None>
```
