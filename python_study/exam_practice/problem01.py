"""문제 1. 장비 로그 시간 정렬 및 필터 (난이도 중상)


## 핵심

**시간 문자열로 정렬하고 시간대로 거르는 것**입니다. `HH:MM:SS` 는 사전순 = 시간순.

이슈가 터지면 그 시간대 장비 로그를 잘라서 봐야 한다. 로그는 장비마다, 테스트 사이트마다
따로 쌓여서 순서가 꼬여 있고, 필요한 시간대만 골라 시간 순서로 맞춰야 한다.
현장 FAE가 제일 자주 하는 작업 중 하나다.

`input01.txt`에는 `RANGE` 명령과 `LOG` 줄이 섞여 있다. `#` 주석과 빈 줄은 무시한다.

```text
RANGE 09:00 12:00
LOG 2026-10-18 10:05:02 SITE=1 TOOL=AOI_01 UNIT=U002 RESULT=FAIL
```

- `RANGE <from> <to>` — `HH:MM` 형식의 시간 범위다. 시작과 끝을 모두 포함한다.
  이 명령이 없으면 전체 시간이 대상이고, 여러 번 나오면 마지막 것으로 덮어쓴다.
- `LOG <날짜> <시각> SITE=<n> TOOL=<이름> UNIT=<id> RESULT=<PASS|FAIL>` — 로그 한 줄이다.

`RANGE 09:00 12:00` 이면 아래처럼 고른다. 시작 분과 끝 분을 모두 포함한다.

```text
08:59:10   <- 버린다
09:00:00   <- 고른다 (시작 분)
12:30:45   <- 버린다
12:00:59   <- 고른다 (끝 분)
```

1. `RANGE`에 준 시각은 같은 날짜 안의 `HH:MM`이며 `09:00` 형식으로만 쓴다.
   `12:00`은 12:00:00을 뜻한다(즉 12:00:00.000 ~ 12:00:59.999).
2. 시간 범위에 들어가는 로그만 남기고 **시각 오름차순으로 정렬**해서 출력한다.
   시각이 같으면 원래 파일에 있던 순서를 유지한다.
3. 범위 밖 로그는 세지 않는다. 버리는 게 아니라 대상이 아니라는 뜻이다.
4. 출력은 로그 원문 한 줄을 그대로 쓴다.
5. `SITE`가 1~8 밖이거나 `RESULT`가 PASS/FAIL이 아니면 그 줄은 오류로 세고 건너뛴다.
   `RANGE`가 먼저 나와야 하고 시각 형식이 틀리면 오류다.
6. 오류는 stderr에 `ERROR line N: 이유` 형식으로 출력하고, 마지막 줄에 `ERRORS=n`을
   **출력 파일에** 쓴다.

## 풀이 순서 (⏱ 40분 ★고배점)

1. `RANGE` 파싱 — 시작/끝 시각을 분 단위로 — 10분
2. `LOG` 줄에서 `SITE=` 등 `키=값` 추출 — 10분
3. 시간 범위로 필터링 — 8분
4. 시각 오름차순 정렬 (같은 시각이면 파일 순서 유지) — 5분
5. 출력 형식 — 5분

> 1~3번만 해도 실전 6번(로그 파싱)의 핵심은 나옵니다.

## 출력

`output01.txt`에 정렬된 로그 줄을 쓰고, 마지막 두 줄에 집계와 오류 수를 쓴다.

```text
Matched=6
Failed=3
ERRORS=2
```

`Matched`는 출력한 로그 줄 수, `Failed`는 그중 `RESULT=FAIL`인 줄 수다.

## 예시

입력 (`input01.txt`):

```text
# 장비 로그 시간 정렬 / 필터
# RANGE 는 관심 시간대입니다. 없으면 전체 시간이 대상입니다.
RANGE 09:00 12:00
LOG 2026-10-18 10:05:02 SITE=1 TOOL=AOI_01 UNIT=U002 RESULT=FAIL
LOG 2026-10-18 09:12:33 SITE=2 TOOL=AOI_01 UNIT=U001 RESULT=PASS
LOG 2026-10-18 08:59:10 SITE=2 TOOL=AOI_01 UNIT=U003 RESULT=FAIL
LOG 2026-10-18 11:41:00 SITE=3 TOOL=AOI_02 UNIT=U004 RESULT=FAIL
LOG 2026-10-18 10:05:02 SITE=4 TOOL=AOI_02 UNIT=U005 RESULT=PASS
LOG 2026-10-18 12:30:45 SITE=1 TOOL=AOI_01 UNIT=U006 RESULT=FAIL
LOG 2026-10-18 09:00:00 SITE=2 TOOL=AOI_02 UNIT=U007 RESULT=FAIL
LOG 2026-10-18 09:59:59 SITE=3 TOOL=AOI_01 UNIT=U008 RESULT=PASS
LOG 2026-10-18 10:20:00 SITE=9 TOOL=AOI_01 UNIT=U009 RESULT=FAIL
LOG 2026-10-18 10:25:00 SITE=1 TOOL=AOI_01 UNIT=U010 RESULT=WARN
```

출력 (`output01.txt`):

```text
2026-10-18 09:00:00 SITE=2 TOOL=AOI_02 UNIT=U007 RESULT=FAIL
2026-10-18 09:12:33 SITE=2 TOOL=AOI_01 UNIT=U001 RESULT=PASS
2026-10-18 09:59:59 SITE=3 TOOL=AOI_01 UNIT=U008 RESULT=PASS
2026-10-18 10:05:02 SITE=1 TOOL=AOI_01 UNIT=U002 RESULT=FAIL
2026-10-18 10:05:02 SITE=4 TOOL=AOI_02 UNIT=U005 RESULT=PASS
2026-10-18 11:41:00 SITE=3 TOOL=AOI_02 UNIT=U004 RESULT=FAIL
Matched=6
Failed=3
ERRORS=2
```

`08:59`이랑 `12:30`은 시간 범위 밖이라 제외된다.
`SITE=9`는 사이트 범위 밖, `RESULT=WARN`는 모르는 결과라 오류다.
`10:05:02`가 두 번 나오면 원래 파일에 있던 순서를 그대로 지킨다.

## 실행

    python3 problem01.py

입력: input01.txt
출력: output01.txt
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

INPUT_PATH = HERE / "input01.txt"
OUTPUT_PATH = HERE / "output01.txt"


def solve() -> int:
    """문제 1. 장비 로그 시간 정렬 및 필터 (난이도 중상)"""
    with open(INPUT_PATH, "r", encoding="utf-8") as in_file:
        lines = in_file.readlines()
        for line in lines:
            line = line.strip()
            if line.startswith("#"):
                continue
    return 0


if __name__ == "__main__":
    raise SystemExit(solve())
