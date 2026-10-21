"""문제 18. 명령/응답 로그 상관과 타임아웃 (난이도 상)


## 핵심

**Transaction 으로 명령과 응답을 짝짓는 것**입니다. 지연 계산과 500ms 경계.

장비에 명령을 보내면 응답이 나중에 돌아온다. 명령과 응답이 따로따로 로그에 남기 때문에
둘을 Transaction ID로 맞춰 봐야 "늦게 온 응답", "아무도 안 기다린 응답"을 찾을 수 있다.
실전 6번 유형과 가장 가깝다.

입력은 `input18_commands.csv`(`Timestamp,Transaction,Command`)와
`input18_responses.csv`(`Timestamp,Transaction,Response`) 두 파일이다.
Timestamp는 정수 밀리초다.

같은 Transaction ID를 가진 명령과 응답을 1:1로 연결한다.

| 상황 | Status |
|---|---|
| 정상, 지연 <= 500 ms | `OK` |
| 지연 > 500 ms 또는 응답 없음 | `TIMEOUT` |
| 응답이 명령보다 빠름 | `OUT_OF_ORDER` |
| 명령보다 많은 응답 | `DUPLICATE` |
| 명령이 없는 응답 | `ORPHAN` |

매칭 규칙은 아래와 같다.

1. 명령은 Timestamp 오름차순으로 처리한다. 정렬 기준은 **숫자로 변환한 뒤**이고,
   같은 Timestamp인 명령은 파일에 나온 순서를 유지한다.
2. 명령 하나를 처리할 때, 같은 Transaction 의 **아직 쓰지 않은 응답** 중에서
   **명령 시각 이후에 나온 응답**을 찾는다.
   - 있으면 그중 **가장 이른 것**을 이 명령의 응답으로 쓰고, 그 응답은 다시 쓰지 않는다.
   - 지연이 500 ms 이하면 `OK`, 500 ms 를 넘으면 `TIMEOUT` 이다.
3. 명령 시각 이후에 응답이 하나도 없는데, 같은 Transaction 의 **이전 응답**이 남아 있으면
   그 응답을 소비하고 `OUT_OF_ORDER` 로 판정한다.
   (명령보다 먼저 온 응답을 뒤늦게 연결한 경우다)
4. 연결할 응답이 아예 없으면 `TIMEOUT` 이다.
5. 500 ms 는 `OK`, 500 ms 를 **초과**하면 `TIMEOUT` 이다.
6. 같은 Transaction 에 명령이 2개 이상 있으면 첫 번째 명령만 처리하고 나머지는 Invalid다.
7. 같은 Transaction 에 응답이 2개 이상 있으면 매칭 규칙대로 하나씩 소비한다.
   명령을 다 처리하고도 남은 응답은 `DUPLICATE` 다.
8. 명령이 하나도 없는 응답은 `ORPHAN` 이다.
9. Timestamp가 숫자가 아니거나, `Transaction`이 비었거나, `Command`/`Response`가 비면
   그 행은 Invalid다. (빈 응답을 "응답 없음"으로 취급하지 않는다.)
10. Invalid는 stderr에 `ERROR line N: 이유` 형식으로 출력하고, summary의 `Invalid=n`에 집계한다.
11. 파일을 열 수 없으면 종료 코드 1이다.

## 풀이 순서 (⏱ 40분)

1. 명령 정렬 — 8분
2. Transaction별 응답 매칭 — 14분
3. Status 판정 (500ms 경계) — 10분
4. 집계·출력 — 8분

> 2번(매칭)이 핵심입니다. 시간이 부족하면 1·3번만.

## 출력

- `output18_report.csv` — 헤더는 `Timestamp,Transaction,Command,Response,LatencyMs,Status`다.
- `output18_summary.txt` — 아래 형태다.

```text
Commands=2
Responses=2
OK=1
TIMEOUT=1
OUT_OF_ORDER=0
DUPLICATE=0
ORPHAN=0
Invalid=0
```

## 예시

> 이 예시는 앞부분만 옮긴 것이다. `input18_commands.csv` 파일이 더 길어서 출력도 그만큼 더 나온다.

입력 (`input18_commands.csv`):

```text
Timestamp,Transaction,Command
100,T12,MEAS:VOLT?
200,T13,MEAS:CURR?
```

입력 (`input18_responses.csv`):

```text
Timestamp,Transaction,Response
700,T12,5.00
700,T13,0.10
```

출력 (`output18_report.csv`):

```text
Timestamp,Transaction,Command,Response,LatencyMs,Status
100,T12,MEAS:VOLT?,5.00,600,TIMEOUT
200,T13,MEAS:CURR?,0.10,500,OK
```

출력 (`output18_summary.txt`):

```text
Commands=2
Responses=2
OK=1
TIMEOUT=1
OUT_OF_ORDER=0
DUPLICATE=0
ORPHAN=0
Invalid=0
```

## 실행

    python3 problem18.py

입력: input18_commands.csv
입력: input18_responses.csv
출력: output18_report.csv
출력: output18_summary.txt
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

COMMANDS_PATH = HERE / "input18_commands.csv"
RESPONSES_PATH = HERE / "input18_responses.csv"
REPORT_PATH = HERE / "output18_report.csv"
SUMMARY_PATH = HERE / "output18_summary.txt"


def solve() -> int:
    """문제 18. 명령/응답 로그 상관과 타임아웃 (난이도 상)"""
    return 0


if __name__ == "__main__":
    raise SystemExit(solve())
