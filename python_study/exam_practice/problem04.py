"""문제 4. 디버깅: CSV 파싱과 반올림 오류 (난이도 중상)


## 핵심

**CSV 따옴표와 공백을 처리하는 것**입니다. `csv` 모듈, `strip()`, 그리고 사사오입.

이 문제는 새로 짜는 게 아니라 **고치는 문제**다. 장비 측정 결과를 CSV로 읽어 한 줄 요약으로 바꾸는
프로그램을 만들었는데, 돌려 보면 결과가 나오지 않는다.

장비마다 CSV를 만드는 방식이 달라서 쉼표가 들어간 항목명이 있고, 사람이 편집한 파일이라
쉼표 뒤에 공백이 남는 경우도 있다. 게다가 값은 소수 둘째 자리까지 **사사오입**해야 하는데
그 부분도 틀렸다.

확인할 것.

1. 프로그램이 아예 죽나? 죽는다면 어느 줄에서, 왜?
2. 첫 번째 줄의 출력이 원본과 다르게 나오지 않나?
3. `1.005`는 `1.01`이 나와야 하는데 `1.00`이 나오지 않나?

지금 이 코드를 그대로 돌리면 두 번째 줄에서 죽는다.

```text
파일 처리 오류: too many values to unpack (expected 5)
```

첫 번째 줄의 출력도 공백이 그대로 남아 있다.

```text
[EQ01]  Voltage=24.57  V ( PASS)
```

요구 사항은 아래와 같다.

1. `input04.csv`의 첫 줄은 헤더고, 그다음 각 행에서 장비, 항목, 측정값, 단위, 결과를 읽는다.
2. 쉼표가 들어간 값(따옴표로 묶인 필드)도 제대로 읽어야 한다.
3. 값 앞뒤의 공백은 제거해야 한다.
4. 측정값은 소수 둘째 자리까지 **사사오입**한다.
   (사사오입은 0.5일 때 무조건 올리는 쪽이다. `round()`는 사사오입이 아니다.)
5. 출력은 아래 형식으로 쓴다.

   ```text
   [EQ01] Voltage=24.57 V (PASS)
   ```

6. 값을 숫자로 변환할 수 없으면 stderr에 `파일 처리 오류: ...` 형식으로 남기고
   종료 코드 1을 반환한다.

## 풀이 순서 (⏱ 15분 ★실전5번)

1. `too many values to unpack` 확인 — 2분
2. `split(",")` → `csv` 모듈 — 5분
3. 앞뒤 공백 제거 — 3분
4. `round()` → 사사오입 — 5분

> 버그 2개만 찾으면 실전 5번 유형이 됩니다.

## 예시

입력 (`input04.csv`):

```text
Equipment,Item,Value,Unit,Result
EQ01, Voltage,24.567, V, PASS
EQ01,"Vol,DC",1.005,A,PASS
EQ02,Current,0.876,A,FAIL
EQ02, Resistance,2.675,kOhm, PASS
EQ03,Voltage,24.999,V,PASS
EQ03,Current,0.005,A,FAIL
EQ04,Temperature,45.5,C,PASS
EQ05,Voltage,1.005,V,PASS
```

출력 (`output04.txt`):

```text
[EQ01] Voltage=24.57 V (PASS)
[EQ01] Vol,DC=1.01 A (PASS)
[EQ02] Current=0.88 A (FAIL)
[EQ02] Resistance=2.68 kOhm (PASS)
[EQ03] Voltage=25.00 V (PASS)
[EQ03] Current=0.01 A (FAIL)
[EQ04] Temperature=45.50 C (PASS)
[EQ05] Voltage=1.01 V (PASS)
```

> `Vol,DC` 는 쉼표가 들어간 필드라 `split(",")`로는 여섯 조각으로 깨진다.
> ` Voltage` 처럼 앞뒤에 공백이 있는 필드는 공백까지 출력에 남는다.
> `1.005` 와 `2.675` 와 `0.005` 는 사사오입이면 `1.01`, `2.68`, `0.01` 이 된다.

## 실행

    python3 problem04.py

입력: input04.csv
출력: output04.txt
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

INPUT_PATH = HERE / "input04.csv"
OUTPUT_PATH = HERE / "output04.txt"


def solve() -> int:
    """문제 4. 디버깅: CSV 파싱과 반올림 오류 (난이도 중상)"""
    try:
        with (
            open(INPUT_PATH, "r", encoding="utf-8") as in_file,
            open(OUTPUT_PATH, "w", encoding="utf-8") as out_file,
        ):
            in_file.readline()

            for line in in_file:
                if not line.strip():
                    continue
                equipment_id, item, value, unit, result = line.rstrip("\n").split(",")
                out_file.write(
                    f"[{equipment_id}] {item}={round(float(value), 2):.2f} {unit} ({result})\n"
                )
    except (OSError, ValueError) as error:
        print(f"파일 처리 오류: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(solve())
