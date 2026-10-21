"""문제 9. 디버깅: 예외를 삼키는 처리 (난이도 중상)


## 핵심

**예외를 삼키지 않는 것**입니다. `except: pass` 를 쓰면 오류가 조용히 사라집니다.

새로 짜는 문제가 아니라 **고치는 문제**다. 로그 파싱 프로그램이 어떤 입력에서는
조용히 결과가 적게 나오고, 뭐가 틀렸는지 stderr에도 아무것도 안 찍힌다.

확인할 것.

1. 잘못된 줄이 있어도 프로그램이 멈추지 않는 대신, **그 줄이 그냥 사라진다.**
2. 오류 개수가 출력에 안 나온다.
3. 잘못된 줄이 있어도 **종료 코드가 0**이다.

지금 이 코드를 그대로 돌리면 이렇게 나온다. 잘못된 줄은 그냥 사라진다.

```text
U001 PASS 1.20
U002 FAIL 0.98
U004 PASS 2.10
U006 PASS 1.05
...
```

요구 사항은 아래와 같다.

1. `input09.txt`의 `<유닛> <PASS|FAIL> <값>` 줄을 읽는다. `#` 주석과 빈 줄은 무시한다.
2. 값이 숫자가 아니면 그 줄은 오류로 세고 건너뛴다. 나머지 줄은 계속 처리한다.
3. 오류는 stderr에 `ERROR line N: 이유` 형식으로 출력한다.
4. 마지막 줄에 `ERRORS=n`을 **출력 파일에** 쓴다.
5. 오류가 하나라도 있으면 **종료 코드 1**을 반환한다.

## 풀이 순서 (⏱ 15분)

1. stderr 에 아무것도 안 찍히는 것 확인 — 2분
2. `except: pass` → 구체적 예외 + 메시지 — 5분
3. 오류 개수 집계 + 종료 코드 — 5분
4. diff — 3분

> 버그 2개만 찾으면 끝입니다.

## 예시

입력 (`input09.txt`):

```text
# 유닛별 측정 결과
U001 PASS 1.20
U002 FAIL 0.98
U003 PASS abc
U004 PASS 2.10
U005 FAIL
U006 PASS 1.05
U007 PASS 0.44
U008 FAIL 2.90
U009 PASS xyz
U010 PASS 3.15
U011 FAIL 1.07
U012 PASS 0.62
```

출력 (`output09.txt`):

```text
U001 PASS 1.20
U002 FAIL 0.98
U004 PASS 2.10
U006 PASS 1.05
U007 PASS 0.44
U008 FAIL 2.90
U010 PASS 3.15
U011 FAIL 1.07
U012 PASS 0.62
ERRORS=3
```

> `U003`은 값이 숫자가 아니고, `U005`는 필드가 2개라서, `U009`은 값이 숫자가 아니어서
> 오류다. 세 줄은 출력에 없고 `ERRORS=3` 으로만 집계된다.

## 실행

    python3 problem09.py

입력: input09.txt
출력: output09.txt
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

INPUT_PATH = HERE / "input09.txt"
OUTPUT_PATH = HERE / "output09.txt"


def solve() -> int:
    """문제 9. 디버깅: 예외를 삼키는 처리 (난이도 중상)"""
    lines = []

    try:
        with open(INPUT_PATH, "r", encoding="utf-8") as in_file:
            for raw in in_file:
                text = raw.strip()
                if not text or text.startswith("#"):
                    continue
                try:
                    parts = text.split()
                    unit, status, value = parts[0], parts[1].upper(), parts[2]
                    float(value)
                    lines.append(f"{unit} {status} {value}")
                except Exception:
                    pass

        OUTPUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    except (OSError, ValueError) as error:
        print(f"파일 처리 오류: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(solve())
