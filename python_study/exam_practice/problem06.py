"""문제 6. 디버깅: 인덱스 범위 오류와 결과 누적 누수 (난이도 중상)


## 핵심

**리스트 인덱스 범위와 용량 제한**입니다. `range()` 한 칸 초과, CAP 미적용 두 가지.

이 문제도 **고치는 문제**다. 테스트 결과를 일정 개수까지만 모아 두는 누적기를 만들었는데,
돌려 보면 두 가지가 이상하다.

1. `SUMMARY` 명령이 실행될 때 `IndexError`로 프로그램이 죽는다.
2. 범위 오류를 고쳤더니, `CAP 3`으로 준데도 `SUMMARY`의 `count`가 4로 나온다.
   오래된 결과가 사라지지 않아 계속 쌓인다.

버그가 두 개 있다. 둘 다 고쳐야 한다.

지금 이 코드를 그대로 돌리면 `SUMMARY` 에서 죽는다.

```text
Traceback (most recent call last):
  File "problem06.py", line 148, in <module>
    raise SystemExit(solve())
                     ^^^^^^^
  ...
IndexError: list index out of range
```

(줄 번호는 코드를 고칠 때마다 달라진다. 핵심은 마지막 `IndexError` 다.)

요구 사항은 아래와 같다.

1. `CAP <n>` — 결과를 최대 n개까지만 보관한다. 이미 모아 둔 결과도 n개를 넘으면
   **가장 오래된 것부터** 버린다.
2. `PUSH <unit> <PASS|FAIL> <value>` — 결과를 하나 추가한다.
   `value`는 소수 둘째 자리까지 사사오입해서 평균을 낸다.
3. `SUMMARY` — 지금 모아 둔 결과로 아래 한 줄을 출력한다.
   `count`는 보관 중인 개수, `pass`/`fail`은 각각의 개수, `avg`는 값의 평균이다.

   ```text
   SUMMARY count=3 pass=2 fail=1 avg=8.10
   ```

4. `CAP` 없이 `PUSH`가 나오면 오류다. `PUSH`의 인자가 3개가 아니거나
   상태가 PASS/FAIL이 아니면 오류다.
   오류는 stderr에 `ERROR line N: 이유` 형식으로 출력하고, 마지막 줄에 `ERRORS=n`을
   **출력 파일에** 쓴다.
5. 오류가 나도 프로그램은 계속 돌아가야 한다.

## 풀이 순서 (⏱ 15분)

1. 돌려서 IndexError 확인 — 2분
2. `range(len(x) + 1)` → `range(len(x))` — 5분
3. 용량 초과 안 되게 오래된 것 제거 — 5분
4. diff — 3분

> 버그 2개만 찾으면 끝입니다.

## 입력

`input06.txt`에 명령이 한 줄씩 들어 있다. `#` 주석과 빈 줄은 무시한다.

```text
CAP 3
PUSH U001 PASS 12.5
PUSH U002 FAIL 0.0
PUSH U003 PASS 13.1
PUSH U004 PASS 11.2
PUSH U005 MAYBE 5.0
PUSH U006 PASS
SUMMARY
```

## 출력

`output06.txt`에 쓴다.

## 예시

입력 (`input06.txt`):

```text
# 테스트 결과 누적기
CAP 3
PUSH U001 PASS 12.5
PUSH U002 FAIL 0.0
PUSH U003 PASS 13.1
PUSH U004 PASS 11.2
PUSH U005 MAYBE 5.0
PUSH U006 PASS
SUMMARY
```

출력 (`output06.txt`):

```text
SUMMARY count=3 pass=2 fail=1 avg=8.10
ERRORS=2
```

`CAP 3`이라 oldest인 `U001 12.5`가 빠진다. 남은 값은 `0.0`, `13.1`, `11.2`고
평균은 `24.3 / 3 = 8.1`이다.
`PUSH U005`는 상태가 `MAYBE`라서, `PUSH U006`은 인자가 2개라서 오류다.

## 실행

    python3 problem06.py

입력: input06.txt
출력: output06.txt
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

INPUT_PATH = HERE / "input06.txt"
OUTPUT_PATH = HERE / "output06.txt"


def solve() -> int:
    """문제 6. 디버깅: 인덱스 범위 오류와 결과 누적 누수 (난이도 중상)"""
    capacity = None
    results = []

    lines = []
    errors = 0

    for lineno, raw in enumerate(INPUT_PATH.read_text(encoding="utf-8").splitlines(), 1):
        text = raw.strip()
        if not text or text.startswith("#"):
            continue
        parts = text.split()
        command = parts[0].upper()

        if command == "CAP":
            capacity = int(parts[1])

        elif command == "PUSH":
            if capacity is None:
                errors += 1
                print(f"ERROR line {lineno}: CAP 이 없어 먼저 선언해야 합니다", file=sys.stderr)
                continue
            unit, status, value = parts[1], parts[2].upper(), parts[3]
            results.append((unit, status, float(value)))

        elif command == "SUMMARY":
            count = 0
            passed = 0
            failed = 0
            total = 0.0
            for index in range(len(results) + 1):
                unit, status, value = results[index]
                count += 1
                total += value
                if status == "PASS":
                    passed += 1
                else:
                    failed += 1
            average = total / count if count else 0.0
            lines.append(f"SUMMARY count={count} pass={passed} fail={failed} avg={average:.2f}")

        else:
            errors += 1
            print(f"ERROR line {lineno}: 알 수 없는 명령 {command}", file=sys.stderr)

    lines.append(f"ERRORS={errors}")
    OUTPUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(solve())
