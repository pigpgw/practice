"""문제 22. 디버깅: 그룹 집계와 출력 순서 오류 (난이도 상)


## 핵심

**그룹을 누적해서 집계하는 것**입니다. 덮어쓰기 버그와 정렬로 순서가 바뀌는 버그.

이 문제는 새로 짜는 게 아니라 **고치는 문제**다. Lot별 테스트 결과를 묶어서 개수와 수율을 내는
프로그램을 만들었는데, 두 가지가 이상하다.

1. 같은 Lot이 여러 번 나왔는데도 개수가 1로만 잡힌다.
2. 결과가 나열되는 순서가 파일에 있던 순서와 다르다.

수율 보고서를 장비에 바로 쓰기 때문에 순서까지 틀리면 곤란하다.

확인할 것.

1. 같은 Lot이 두 번 나온 줄이 있는데도 `total`이 1인지 확인해 보라.
2. 파일의 첫 등장 순서가 `L01 → L10 → L02`인데, 출력은 어떤 순서인지 확인해 보라.
3. 수율(%)이 맞는지 계산해 보라.

지금 이 코드를 그대로 돌리면 이렇게 나온다.

```text
L01 total=1 pass=1 fail=0 yield=100.00
L02 total=1 pass=1 fail=0 yield=100.00
L03 total=1 pass=0 fail=1 yield=0.00
L10 total=1 pass=1 fail=0 yield=100.00
```

> 개수가 누적되지 않고, 순서도 첫 등장 순서가 아니다.

요구 사항은 아래와 같다.

1. `input22.txt`의 `<Lot> <PASS|FAIL> <초>` 줄을 읽는다. `#` 주석과 빈 줄은 무시한다.
2. Lot별로 총 개수, PASS 개수, FAIL 개수를 **누적**한다.
3. 출력 순서는 **Lot이 처음 등장한 순서**다. 알파벳순으로 정렬하지 않는다.
4. 수율은 `PASS / total × 100`이고 소수 둘째 자리까지 **사사오입**한다.
5. 출력은 아래 형식으로 쓴다.

   ```text
   L01 total=2 pass=1 fail=1 yield=50.00
   ```

6. Lot이나 상태가 올바르지 않으면 stderr에 `파일 처리 오류: ...` 형식으로 남기고
   종료 코드 1을 반환한다.

## 풀이 순서 (⏱ 15분)

1. `total` 이 1 인 것 확인 — 3분
2. 덮어쓰기 → 누적으로 — 5분
3. 정렬 → 첫 등장 순서로 — 4분
4. diff — 3분

> 버그 2개만 찾으면 끝입니다.

## 예시

입력 (`input22.txt`):

```text
# Lot별 테스트 결과
L01 PASS 2.4
L10 FAIL 3.1
L02 PASS 2.8
L01 FAIL 1.9
L10 PASS 3.3
L02 PASS 2.1
L03 FAIL 4.0
L01 PASS 2.6
```

출력 (`output22.txt`):

```text
L01 total=3 pass=2 fail=1 yield=66.67
L10 total=2 pass=1 fail=1 yield=50.00
L02 total=2 pass=2 fail=0 yield=100.00
L03 total=1 pass=0 fail=1 yield=0.00
```

> 첫 등장 순서는 `L01 → L10 → L02 → L03` 이다. 알파벳순으로 정렬하면 `L02` 가 두 번째로
> 올라와서 순서가 틀어진다. `L01` 은 세 번 나왔으니 total 은 3 이고 pass 는 2 다.

## 실행

    python3 problem22.py

입력: input22.txt
출력: output22.txt
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

INPUT_PATH = HERE / "input22.txt"
OUTPUT_PATH = HERE / "output22.txt"


def solve() -> int:
    """문제 22. 디버깅: 그룹 집계와 출력 순서 오류 (난이도 상)"""
    try:
        groups = {}
        with open(INPUT_PATH, "r", encoding="utf-8") as in_file:
            for line in in_file:
                text = line.strip()
                if not text or text.startswith("#"):
                    continue
                parts = text.split()
                if len(parts) != 3:
                    raise ValueError(f"필드 수가 {len(parts)}개입니다 (3개 필요): {text}")
                lot, status = parts[0], parts[1].upper()
                if status not in ("PASS", "FAIL"):
                    raise ValueError(f"알 수 없는 상태입니다: {parts[1]}")

                groups[lot] = [
                    1 if status == "PASS" else 0,
                    0 if status == "PASS" else 1,
                ]

        lines = []
        for lot in sorted(groups):
            passed, failed = groups[lot]
            total = passed + failed
            yield_percent = passed / total * 100
            lines.append(
                f"{lot} total={total} pass={passed} fail={failed} " f"yield={yield_percent:.2f}"
            )

        OUTPUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    except (OSError, ValueError) as error:
        print(f"파일 처리 오류: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(solve())
