"""문제 8. 디버깅: 리스트를 순회하면서 수정 (난이도 중상)


## 핵심

**순회 중에 리스트를 건드리지 않는 것**입니다. 중복 제거, 첫 결과/마지막 결과 구분.

새로 짜는 문제가 아니라 **고치는 문제**다. 같은 유닛이 여러 번 테스트된 로그에서
유닛별 마지막 결과만 남기려고 했는데, 중복이 다 안 빠진다. 남아버린 유닛의 마지막
결과도 값이 옛날 것이고.

확인할 것.

1. 중복 유닛이 남는 개수가 입력 줄 수와 맞아? 남는 유닛이 몇 개인지 세어 봐라.
2. 남은 유닛의 결과는 **마지막** 테스트 결과인가, 첫 번째인가?

지금 이 코드를 그대로 돌리면 이렇게 나온다.

```text
U001 PASS 1.20
U002 PASS 0.98
U003 FAIL 2.10
U006 PASS 1.01
U004 PASS 0.55
U005 FAIL 3.02
```

> 중복 유닛이 그대로 남아 있고, 나열 순서도 섞여 있고, 값도 첫 번째 값이다.

요구 사항은 아래와 같다.

1. `input08.txt`의 `UNIT <유닛> <PASS|FAIL> <값>` 줄을 읽는다.
   `#` 주석과 빈 줄은 무시한다.
2. **유닛별 마지막 결과만** 남긴다.
3. 남기는 순서는 **유닛이 처음 등장한 순서**다. (알파벳순으로 정렬하지 않는다)
4. 출력은 아래 형식으로 쓴다. 값은 소수 둘째 자리까지 **사사오입**한다.

   ```text
   U001 PASS 1.22
   ```

5. 값이 숫자가 아니면 그 줄은 오류로 세고 건너뛴다.
   오류는 stderr에 `ERROR line N: 이유` 형식으로 출력하고, 마지막 줄에 `ERRORS=n`을
   **출력 파일에** 쓴다.

## 풀이 순서 (⏱ 15분)

1. 중복 유닛이 남는 것 확인 — 3분
2. 순회 중 리스트 수정 → 복사본 순회 — 5분
3. 첫 결과 → 마지막 결과 — 5분
4. diff — 2분

> 버그 2개만 찾으면 끝입니다.

## 예시

입력 (`input08.txt`):

```text
# 유닛별 테스트 결과 (같은 유닛이 여러 번 나올 수 있음)
UNIT U001 PASS 1.20
UNIT U001 FAIL 1.35
UNIT U002 PASS 0.98
UNIT U003 FAIL 2.10
UNIT U001 PASS 1.22
UNIT U002 PASS 0.99
UNIT U003 FAIL 2.14
UNIT U004 PASS 0.55
UNIT U005 FAIL 3.02
UNIT U006 PASS 1.01
UNIT U004 PASS 0.57
UNIT U005 FAIL 3.04
UNIT U007 PASS 2.50
```

출력 (`output08.txt`):

```text
U001 PASS 1.22
U002 PASS 0.99
U003 FAIL 2.14
U004 PASS 0.57
U005 FAIL 3.04
U006 PASS 1.01
U007 PASS 2.50
ERRORS=0
```

> `U001`은 세 번 나왔는데 마지막이 `PASS 1.22` 다. `U002`는 마지막이 `PASS 0.99`,
> `U003`는 마지막이 `FAIL 2.14` 다. `U007`은 한 번만 나왔다.

## 실행

    python3 problem08.py

입력: input08.txt
출력: output08.txt
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

INPUT_PATH = HERE / "input08.txt"
OUTPUT_PATH = HERE / "output08.txt"


def solve() -> int:
    """문제 8. 디버깅: 리스트를 순회하면서 수정 (난이도 중상)"""
    try:
        units = []
        results = []
        errors = 0

        with open(INPUT_PATH, "r", encoding="utf-8") as in_file:
            for lineno, raw in enumerate(in_file, start=1):
                text = raw.strip()
                if not text or text.startswith("#"):
                    continue
                parts = text.split()
                if parts[0].upper() != "UNIT" or len(parts) != 4:
                    errors += 1
                    print(f"ERROR line {lineno}: 형식이 잘못됐습니다: {text}", file=sys.stderr)
                    continue
                unit, status, value = parts[1], parts[2].upper(), parts[3]
                try:
                    float(value)
                except ValueError:
                    errors += 1
                    print(f"ERROR line {lineno}: 값이 숫자가 아닙니다: {value}", file=sys.stderr)
                    continue

                units.append(unit)
                results.append((unit, status, value))

        for unit in units:
            if units.count(unit) > 1:
                units.remove(unit)

        lines = []
        for unit in units:
            for name, status, value in results:
                if name == unit:
                    lines.append(f"{unit} {status} {value}")
                    break

        lines.append(f"ERRORS={errors}")
        OUTPUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    except (OSError, ValueError) as error:
        print(f"파일 처리 오류: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(solve())
