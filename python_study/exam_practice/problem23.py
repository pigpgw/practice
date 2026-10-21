"""문제 23. 디버깅: 시간 구간 계산 오류 (난이도 상)


## 핵심

**자정을 넘는 시간 구간을 계산하는 것**입니다. 분 단위 변환과 24×60 보정.

새로 짜는 문제가 아니라 **고치는 문제**다. 장비 로그에서 "이 시간대에 뭐가 있었나"를
찾는 도구를 만들었는데, 자정을 넘는 시간대와 분 단위 시각에서 결과가 이상하다.

확인할 것.

1. `22:30 → 01:15` 같은 구간의 길이가 음수가 되지 않는가?
2. 끝 시각이 시작 시각보다 빠른 구간은 하루를 넘어간 건데, 지금 코드는 그걸 어떻게
   계산하는가?

지금 이 코드를 그대로 돌리면 자정을 넘는 두 구간이 음수가 된다.

```text
NIGHT 22:30-01:15 -1275
MIDNIGHT 23:50-00:10 -1420
```

요구 사항은 아래와 같다.

1. `input23.txt`의 `RANGE <시작> <끝> <이름>` 줄을 읽는다. `#` 주석과 빈 줄은 무시한다.
2. 시각은 `HH:MM` 형식이고, **끝 시각이 시작 시각보다 빠르면 자정을 지난 것으로
   처리한다.** (예: `22:30 → 01:15` 는 170 분)
3. 구간 길이는 분 단위다.
4. 출력은 아래 형식으로 쓴다.

   ```text
   R1 09:00-12:00 180
   ```

5. 시각 형식이 틀리면 그 줄은 오류로 세고 건너뛴다.
   오류는 stderr에 `ERROR line N: 이유` 형식으로 출력하고, 마지막 줄에 `ERRORS=n`을
   **출력 파일에** 쓴다.

## 풀이 순서 (⏱ 15분)

1. 음수 길이 나오는 것 확인 — 3분
2. 시각을 분 단위로 변환 — 4분
3. 자정 넘김 보정 — 5분
4. diff — 3분

> 버그 2개만 찾으면 끝입니다.

## 예시

입력 (`input23.txt`):

```text
# 장비 로그 시간대 조회
RANGE 09:00 12:00 MORNING
RANGE 13:30 14:15 SHORT
RANGE 22:30 01:15 NIGHT
RANGE 10:05 10:45 TIGHT
RANGE 23:50 00:10 MIDNIGHT
RANGE 08:00 09:30 OPENING
RANGE 15:00 16:45 CLOSING
RANGE 21:15 21:45 NIGHTTIGHT
```

출력 (`output23.txt`):

```text
MORNING 09:00-12:00 180
SHORT 13:30-14:15 45
NIGHT 22:30-01:15 165
TIGHT 10:05-10:45 40
MIDNIGHT 23:50-00:10 20
OPENING 08:00-09:30 90
CLOSING 15:00-16:45 105
NIGHTTIGHT 21:15-21:45 30
ERRORS=0
```

> `NIGHT` 는 자정을 넘어서 22:30(1350분) → 01:15(75분) 이므로 24×60 - 1350 + 75 = 165 분이다.
> `MIDNIGHT` 는 23:50(1430분) → 00:10(10분) 이므로 1440 - 1430 + 10 = 20 분이다.

## 실행

    python3 problem23.py

입력: input23.txt
출력: output23.txt
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

INPUT_PATH = HERE / "input23.txt"
OUTPUT_PATH = HERE / "output23.txt"


def to_minutes(text: str) -> int:
    """HH:MM 을 분 단위 정수로 바꾼다."""
    hour, minute = text.split(":")
    return int(hour) * 60 + int(minute)


def solve() -> int:
    """문제 23. 디버깅: 시간 구간 계산 오류 (난이도 상)"""
    try:
        lines = []
        errors = 0

        with open(INPUT_PATH, "r", encoding="utf-8") as in_file:
            for lineno, raw in enumerate(in_file, start=1):
                text = raw.strip()
                if not text or text.startswith("#"):
                    continue
                parts = text.split()
                if parts[0].upper() != "RANGE" or len(parts) != 4:
                    errors += 1
                    print(f"ERROR line {lineno}: 형식이 잘못됐습니다: {text}", file=sys.stderr)
                    continue
                start, end, name = parts[1], parts[2], parts[3]

                try:
                    start_minutes = to_minutes(start)
                    end_minutes = to_minutes(end)
                except ValueError:
                    errors += 1
                    print(f"ERROR line {lineno}: 시각 형식이 잘못됐습니다: {text}", file=sys.stderr)
                    continue

                length = end_minutes - start_minutes

                lines.append(f"{name} {start}-{end} {length}")

        lines.append(f"ERRORS={errors}")
        OUTPUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    except (OSError, ValueError) as error:
        print(f"파일 처리 오류: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(solve())
