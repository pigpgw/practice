"""문제 11. SCPI 스타일 명령 처리기 (난이도 중상)


## 핵심

**명령마다 상태를 두고 오류를 큐에 쌓는 것**입니다. 큐는 FIFO, `SYST:ERR?` 로 oldest를 꺼냅니다.

계측 장비는 보통 `*IDN?`, `MEAS:VOLT?` 같은 명령을 주고받는다. 명령마다 장비 상태가 바뀌고,
틀린 명령은 오류 큐에 쌓였다가 `SYST:ERR?`로 하나씩 꺼내 조회한다.
실제 장비 제어와 가장 가까운 문제다.

`input11.txt`의 명령을 순서대로 처리하며 전압·전류·출력·오류 큐 상태를 유지한다.
명령은 대소문자를 구분하지 않고, 각 줄을 `명령 => 응답` 형식으로 `output11.txt`에 쓴다.
`#`으로 시작하는 줄과 빈 줄은 무시한다. 출력의 `명령` 부분은 **입력받은 원문 그대로** 쓴다.

| 명령 | 동작 |
|---|---|
| `*RST` | 전압/전류 0, 출력 OFF |
| `*IDN?` | `TERADYNE,SCPI-SIM,1.0` |
| `CONF:VOLT <v>` | 0~50 V 설정 |
| `CONF:CURR <a>` | 0~5 A 설정 |
| `OUTP ON\|OFF` | 출력 상태 |
| `MEAS:VOLT?` | 출력 ON이면 `VOLT=5.000 V`, 아니면 `ERROR: OUTPUT_OFF` |
| `MEAS:CURR?` | 출력 ON이면 `CURR=0.100 A`, 아니면 `ERROR: OUTPUT_OFF` |
| `STAT?` | `VOLT=...,CURR=...,OUTP=ON/OFF` |
| `SYST:ERR?` | 오류 큐에서 가장 오래된 오류를 꺼내 출력 |

오류 큐는 아래와 같다.

| 상황 | 코드 | 메시지 | 응답 |
|---|---|---|---|
| 알 수 없는 명령 | -113 | Undefined header | `ERROR: UNDEFINED_HEADER` |
| 인자 누락 | -109 | Missing argument | `ERROR: MISSING_ARGUMENT` |
| 숫자 변환 실패 | -104 | Data type error | `ERROR: DATA_TYPE_ERROR` |
| 범위/열거값 오류 | -222 | Data out of range | `ERROR: DATA_OUT_OF_RANGE` |

1. 큐가 비어 있으면 `0,"No error"`를 출력한다.
2. `MEAS`와 `STAT`에 찍는 전압·전류는 **소수 셋째 자리**까지 출력한다.
   (`CONF:VOLT 5.0` 을 줬으면 `VOLT=5.000 V` — 두 자리나 한 자리로 찍으면 안 된다)
3. `MEAS`의 `OUTPUT_OFF`는 정상 명령이지만 측정을 거부한 거라 `ERRORS`에 세지 않는다.
4. `COMMANDS`는 주석을 제외하고 처리한 명령 줄 수다. 오류 응답을 만든 명령도 포함한다.
5. `ERRORS`는 오류 큐에 들어간 오류 수다. `SYST:ERR?`로 큐에서 꺼낸 오류는 다시 더하지 않는다.
6. 마지막에 `COMMANDS=n ERRORS=n`을 출력한다.

## 풀이 순서 (⏱ 35분)

1. 명령 파싱 + 대소문자 무시 — 8분
2. 전압/전류/출력 상태 관리 — 8분
3. 오류 큐(FIFO) — list + `pop(0)` — 8분
4. `SYST:ERR?` 처리 + `COMMANDS/ERRORS` 집계 — 8분
5. 출력 형식 — 3분

> 1~3번만 해도 명령 해석 + 상태 관리는 나옵니다.

## 출력

`output11.txt`에 쓴다.

## 예시

> 이 예시는 앞부분만 옮긴 것이다. `input11.txt` 파일이 더 길어서 출력도 그만큼 더 나온다.

입력 (`input11.txt`):

```text
*RST
CONF:VOLT 5.0
OUTP ON
MEAS:VOLT?
BAD:CMD
SYST:ERR?
```

출력 (`output11.txt`):

```text
*RST => OK
CONF:VOLT 5.0 => OK
OUTP ON => OK
MEAS:VOLT? => VOLT=5.000 V
BAD:CMD => ERROR: UNDEFINED_HEADER
SYST:ERR? => -113,"Undefined header"
COMMANDS=6 ERRORS=1
```

## 실행

    python3 problem11.py

입력: input11.txt
출력: output11.txt
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

INPUT_PATH = HERE / "input11.txt"
OUTPUT_PATH = HERE / "output11.txt"


def solve() -> int:
    """문제 11. SCPI 스타일 명령 처리기 (난이도 중상)"""
    return 0


if __name__ == "__main__":
    raise SystemExit(solve())
