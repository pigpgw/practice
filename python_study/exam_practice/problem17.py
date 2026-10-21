"""문제 17. 테스트 실행 상태 머신과 재검 (난이도 상)


## 핵심

**상태 전이표를 그대로 구현하는 것**입니다. IDLE/RUNNING/PASS/FAIL/ABORTED.

테스트 프로그램은 유닛을 잡고 단계를 진행하다가 PASS/FAIL/ABORT로 결과를 낸다.
이 과정을 상태 머신으로 표현하면 어떤 이벤트가 언제 잘못됐는지 정확히 알 수 있다.
실전 6번 유형의 "상태 관리" 버전이다.

`input17_events.txt`의 이벤트를 순서대로 처리한다.
`MAX_RETRY`는 첫 부분의 `# MAX_RETRY=n` 주석에서 읽고, 없으면 2다.

상태: `IDLE -> RUNNING -> PASS / FAIL / ABORTED`

| 이벤트 | 규칙 |
|---|---|
| `SERIAL <id>` | 새 유닛 시작. 이전 유닛이 RUNNING이면 ABORTED(NEW_SERIAL), IDLE이면 ABORTED(NO_START) |
| `START` | IDLE에서만 RUNNING |
| `STEP <name>` | RUNNING에서만 step 수 증가 |
| `FAIL <test>` | RUNNING에서만 FAIL, failures 증가 |
| `RETRY` | FAIL에서만, retries < MAX_RETRY일 때 RUNNING |
| `PASS` | RUNNING에서만 PASS |
| `ABORT <reason>` | RUNNING/FAIL에서 ABORTED, reason 저장. 유닛 확정은 END |
| `END` | PASS/FAIL/ABORTED 확정. RUNNING이면 ABORTED(END_WHILE_RUNNING) |

1. 잘못된 전이는 `InvalidEvents`로 세고 상태를 바꾸지 않는다.
   stderr에 `ERROR line N: 이유` 형식으로 출력한다.
2. `ABORT`는 상태만 ABORTED로 바꾸고, 유닛 확정은 뒤의 `END`에서 한다.
3. EOF에서 RUNNING/FAIL이면 ABORTED(EOF), IDLE이면 ABORTED(NO_START).
4. 유닛 상태가 `IDLE` 이라는 건 "`SERIAL` 로 유닛은 열렸는데 `START` 는 아직 안 왔음" 이라는 뜻이다.
   유닛이 열릴 때마다 상태를 이렇게 정한다.
   - 이전 유닛이 `RUNNING` 이었다면 → `ABORTED(NEW_SERIAL)`
   - 이전 유닛이 `IDLE` 이었다면 → `ABORTED(NO_START)`
   - 이전 유닛이 이미 `PASS`/`FAIL` 로 확정됐었다면 → 그대로 두고 새 유닛 시작
5. `ABORT <reason>`의 reason은 공백을 포함한 나머지 전체 문자열이다.
6. `MAX_RETRY`가 0이면 `RETRY`는 언제나 잘못된 전이다.
7. `STEP`의 name은 출력에 쓰지 않는다. 개수만 센다.
8. 출력 순서는 유닛이 처음 등장한 순서다.
9. `Steps`는 RUNNING일 때 처리한 STEP 수, `Failures`는 FAIL 이벤트 수,
   `Retries`는 성공한 RETRY 수다.
10. 오류가 나도 계속 진행한다. 마지막에 `InvalidEvents=n`으로 집계한다.

## 풀이 순서 (⏱ 40분)

1. 상태 변수 두기 (IDLE/RUNNING/PASS/FAIL/ABORTED) — 10분
2. 이벤트별 전이 구현 — 12분
3. EOF 마무리 처리 — 8분
4. 출력 — 10분

> 상태 전이표만 보고 구현하면 됩니다. 시간이 부족하면 미루세요.

## 출력

- `output17_units.csv` — 헤더는 `Serial,FinalState,Steps,Retries,Failures,AbortReason`다.
- `output17_report.txt` — 아래 형태다.

```text
Units=1
PASS=1
FAIL=0
ABORTED=0
InvalidEvents=0
```

## 예시

> 이 예시는 앞부분만 옮긴 것이다. `input17_events.txt` 파일이 더 길어서 출력도 그만큼 더 나온다.

입력 (`input17_events.txt`):

```text
# MAX_RETRY=2
SERIAL U001
START
STEP contact
PASS
END
```

출력 (`output17_units.csv`):

```text
Serial,FinalState,Steps,Retries,Failures,AbortReason
U001,PASS,1,0,0,
```

출력 (`output17_report.txt`):

```text
Units=1
PASS=1
FAIL=0
ABORTED=0
InvalidEvents=0
```

## 실행

    python3 problem17.py

입력: input17_events.txt
출력: output17_units.csv
출력: output17_report.txt
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

INPUT_PATH = HERE / "input17_events.txt"
UNITS_PATH = HERE / "output17_units.csv"
REPORT_PATH = HERE / "output17_report.txt"


def solve() -> int:
    """문제 17. 테스트 실행 상태 머신과 재검 (난이도 상)"""
    return 0


if __name__ == "__main__":
    raise SystemExit(solve())
