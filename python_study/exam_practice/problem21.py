"""문제 21. 디버깅: 설정 파일 섹션 파싱 오류 (난이도 상)


## 핵심

**설정 파일의 섹션 경계를 처리하는 것**입니다. 이전 섹션 저장, 키 누락 검사.

새로 짜는 문제가 아니라 **고치는 문제**다. 테스트 항목 정의 파일(.ini)을 읽어서
항목별 스펙을 모으는 코드를 짰는데, 항목이 하나밖에 안 잡힌다.

확인할 것.

1. 항목이 몇 개 잡혔나? 정의 파일에는 몇 개가 있는가?
2. 각 항목의 `Low`/`High`/`Unit`이 자기 항목 값인가, 다른 항목 값인가?

지금 이 코드를 그대로 돌리면 항목이 하나만 나온다.

```text
T6 Clock 0.00 0.00 MHz
ERRORS=0
```

요구 사항은 아래와 같다.

1. `input21.ini`를 읽는다. `[TEST <id>]` 로 시작하는 줄이 새 항목의 시작이고,
   그다음 `Name=`/`Low=`/`High=`/`Unit=` 줄이 그 항목의 값이다.
2. 항목마다 `id`, `Name`, `Low`, `High`, `Unit` 을 모은다.
   `Name`, `Low`, `High`, `Unit` 이 하나라도 없으면 그 항목은 오류다.
3. 출력은 아래 형식으로 쓴다. `Low`·`High` 는 소수 둘째 자리까지 **사사오입**한다.

   ```text
   T1 Vin 4.50 5.50 V
   ```

4. 오류는 stderr에 `ERROR line N: 이유` 형식으로 출력하고, 마지막 줄에 `ERRORS=n`을
   **출력 파일에** 쓴다.
5. `#` 주석과 빈 줄은 무시한다.

## 풀이 순서 (⏱ 15분)

1. 항목이 하나만 잡히는 것 확인 — 3분
2. 섹션이 끝날 때 저장 — 5분
3. 키 누락 검사 — 4분
4. diff — 3분

> 버그 2개만 찾으면 끝입니다.

## 예시

입력 (`input21.ini`):

```text
# 테스트 항목 정의
[TEST T1]
Name=Vin
Low=4.5
High=5.5
Unit=V

[TEST T2]
Name=Iq
Low=0.0
High=0.010
Unit=A

[TEST T3]
Name=Vout
Low=1.15
High=1.25
Unit=V

[TEST T4]
Name=Temp
Low=0.0
High=85.0
Unit=C

[TEST T5]
Name=Res
Low=1.0
High=10.0
Unit=kOhm

[TEST T6]
Name=Clock
Low=0.0
Unit=MHz
```

출력 (`output21.txt`):

```text
T1 Vin 4.50 5.50 V
T2 Iq 0.00 0.01 A
T3 Vout 1.15 1.25 V
T4 Temp 0.00 85.00 C
T5 Res 1.00 10.00 kOhm
ERRORS=1
```

> `T6`은 `High` 가 없어서 오류다. 나머지 다섯 항목은 다 출력된다.

## 실행

    python3 problem21.py

입력: input21.ini
출력: output21.txt
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

INPUT_PATH = HERE / "input21.ini"
OUTPUT_PATH = HERE / "output21.txt"


def solve() -> int:
    """문제 21. 디버깅: 설정 파일 섹션 파싱 오류 (난이도 상)"""
    try:
        lines = []
        errors = 0
        current = None
        tests = []

        with open(INPUT_PATH, "r", encoding="utf-8") as in_file:
            for lineno, raw in enumerate(in_file, start=1):
                text = raw.strip()
                if not text or text.startswith("#"):
                    continue

                if text.startswith("[TEST"):
                    current = {
                        "id": text[6:-1].strip(),
                        "Name": "",
                        "Low": "",
                        "High": "",
                        "Unit": "",
                    }
                elif "=" in text:
                    key, value = text.split("=", 1)
                    if current is not None:
                        current[key.strip()] = value.strip()

        if current is not None:
            tests.append(current)

        for test in tests:
            low = float(test["Low"] or 0)
            high = float(test["High"] or 0)
            lines.append(f"{test['id']} {test['Name']} {low:.2f} {high:.2f} {test['Unit']}")

        lines.append(f"ERRORS={errors}")
        OUTPUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    except (OSError, ValueError) as error:
        print(f"파일 처리 오류: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(solve())
