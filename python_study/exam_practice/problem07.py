"""문제 7. 디버깅: 스펙 판정과 중앙값 계산 오류 (난이도 중상)


## 핵심

**스펙 경계 판정과 중앙값 계산**입니다. 경계 포함 여부와 괄호 하나.

새로 짜는 문제가 아니라 **고치는 문제**다. 측정값을 스펙과 비교해서 PASS/FAIL을 내는
프로그램을 만들었는데, 스펙 경계에 딱 걸린 케이스가 자꾸 반대로 나온다.

확인할 것.

1. 스펙과 정확히 같은 값(하한, 상한)이 PASS로 나오나?
2. 스펙 중앙값에서 얼마나 벗어났는지가 맞아? `Low`가 크고 `High`가 작게 들어간
   스펙도 있다.

지금 이 코드를 그대로 돌리면 이렇게 나온다.

```text
U001 VDD PASS delta=0.55
U002 VDD FAIL delta=0.45
U003 VDD FAIL delta=0.65
U004 VDD PASS delta=0.50
U005 IDD PASS delta=0.01
U006 IDD FAIL delta=0.01
```

요구 사항은 아래와 같다.

1. `input07.csv`의 첫 줄은 헤더이고, 그다음 각 행에서 유닛, 항목, 측정값, 하한, 상한을
   읽는다. (`Unit`은 유닛 이름, `Test`는 항목 이름)
2. `Low <= Measured <= High` 면 PASS, 아니면 FAIL이다. **경계값을 포함한다.**
3. `Delta` 는 스펙 중앙값과 측정값의 차이이고, 중앙값은 `(Low + High) / 2` 다.
   `Delta = abs(Measured - 중앙값)`
4. 출력은 아래 형식으로 쓴다. 소수는 둘째 자리까지 **사사오입**한다.

   ```text
   U001 VDD PASS delta=0.05
   ```

## 풀이 순서 (⏱ 15분)

1. 스펙 경계값(=Low, =High) 케이스 찾기 — 3분
2. `>` `<` → `>=` `<=` 로 수정 — 5분
3. 중앙값 계산 괄호 — 5분
4. diff — 2분

> 버그 2개만 찾으면 끝입니다.

## 예시

입력 (`input07.csv`):

```text
Unit,Test,Measured,Low,High
U001,VDD,1.20,1.10,1.30
U002,VDD,1.30,1.10,1.30
U003,VDD,1.10,1.10,1.30
U004,VDD,1.25,1.10,1.30
U005,IDD,0.017,0.0,0.020
U006,IDD,0.020,0.0,0.020
U007,IDD,0.000,0.0,0.020
U008,IDD,0.025,0.0,0.020
U009,TEMP,25,20,30
U010,TEMP,30,20,30
U011,TEMP,35,20,30
```

출력 (`output07.txt`):

```text
U001 VDD PASS delta=0.00
U002 VDD PASS delta=0.10
U003 VDD PASS delta=0.10
U004 VDD PASS delta=0.05
U005 IDD PASS delta=0.01
U006 IDD PASS delta=0.01
U007 IDD PASS delta=0.01
U008 IDD FAIL delta=0.02
U009 TEMP PASS delta=0.00
U010 TEMP PASS delta=5.00
U011 TEMP FAIL delta=10.00
```

> VDD 중앙값은 1.20, IDD 중앙값은 0.010, TEMP 중앙값은 25 다.
> `U002`·`U003`은 스펙 경계값이라 PASS 여야 하고, `U006`·`U007`·`U010`도 마찬가지다.
> `U008`·`U011`은 스펙 밖이라 FAIL 이다.

## 실행

    python3 problem07.py

입력: input07.csv
출력: output07.txt
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

INPUT_PATH = HERE / "input07.csv"
OUTPUT_PATH = HERE / "output07.txt"


def solve() -> int:
    """문제 7. 디버깅: 스펙 판정과 중앙값 계산 오류 (난이도 중상)"""
    try:
        lines = []

        with open(INPUT_PATH, "r", encoding="utf-8") as in_file:
            in_file.readline()

            for raw in in_file:
                text = raw.strip()
                if not text or text.startswith("#"):
                    continue
                fields = text.split(",")
                if len(fields) != 5:
                    raise ValueError(f"필드 수가 {len(fields)}개입니다 (5개 필요): {text}")
                unit, item, measured, low, high = fields
                measured_value = float(measured)
                low_value = float(low)
                high_value = float(high)

                center = low_value + high_value / 2
                delta = abs(measured_value - center)

                if measured_value > low_value and measured_value < high_value:
                    status = "PASS"
                else:
                    status = "FAIL"

                lines.append(f"{unit} {item} {status} delta={delta:.2f}")

        OUTPUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    except (OSError, ValueError) as error:
        print(f"파일 처리 오류: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(solve())
