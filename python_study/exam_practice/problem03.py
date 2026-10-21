"""문제 3. 디버깅: 숫자 정렬과 평균 계산 오류 (난이도 중상)


## 핵심

**문자열로 숫자를 다뤄서 생기는 오류**입니다. 정렬 순서와 `//` 나눗셈 두 가지.

이 문제는 새로 짜는 문제가 아니라 **고치는 문제**다. 실제 시험에서 나온 적 있는 유형이라서,
버그 있는 코드를 읽고 원인을 찾아 고치는 연습을 한다.

측정값 목록을 받아 개수·최솟값·최댓값·평균·정렬 결과를 내보내는 프로그램을 만들었는데,
값이 이상하게 나온다. `12.5`와 `9.75`를 나란히 놓고 보면 `9.75`가 더 작은 값이라는 걸
누가 알 텐데, 결과는 `12.5`가 앞에 나온다. 평균도 이상하다.

1. 정렬된 순서가 숫자 크기 순서가 맞나?
2. 최솟값과 최댓값이 실제 최솟값·최댓값인가?
3. 평균이 정확한가?

지금 이 코드를 그대로 돌리면 이렇게 나온다.

```text
COUNT=10
MIN=10.25
MAX=9.75
AVG=17.00
SORTED=10.25,10.25,10.25,100.75,12.5,2.0,3.5,7.25,8.0,9.75
```

요구 사항은 아래와 같다.

1. `input03.txt`의 `VALUE <숫자>` 줄을 모두 읽는다. `#` 주석과 빈 줄은 무시한다.
2. 값은 **숫자로** 다뤄야 한다. 문자열로 비교하면 `9.75`와 `12.5`의 순서가 뒤집힌다.
3. 출력은 아래 순서로 쓴다. 소수는 둘째 자리까지 **사사오입**한다.

   ```text
   COUNT=4
   MIN=8.00
   MAX=12.50
   AVG=10.13
   SORTED=8.00,9.75,10.25,12.50
   ```

4. `SORTED`는 오름차순으로 정렬한 값을 쉼표로 이어서 쓴다.
5. 값이 한 개도 없으면 `COUNT=0`만 출력한다.
6. 숫자로 변환할 수 없으면 stderr에 `파일 처리 오류: ...` 형식으로 남기고 종료 코드 1을 반환한다.

## 풀이 순서 (⏱ 15분)

1. 돌려서 이상한 출력 확인 — 2분
2. 문자열로 정렬되는 부분 찾고 숫자로 변환 — 5분
3. `//` 나눗셈 찾고 소수점 계산으로 교체 — 5분
4. 예시와 diff — 3분

> 버그 2개만 찾으면 끝입니다.

## 예시

입력 (`input03.txt`):

```text
# 측정값 목록
VALUE 12.5
VALUE 9.75
VALUE 10.25
VALUE 8.0
VALUE 10.25
VALUE 3.5
VALUE 100.75
VALUE 2.0
VALUE 7.25
VALUE 10.25
```

출력 (`output03.txt`):

```text
COUNT=10
MIN=2.00
MAX=100.75
AVG=17.45
SORTED=2.00,3.50,7.25,8.00,9.75,10.25,10.25,10.25,12.50,100.75
```

> 문자열로 정렬하면 `100.75` 이 `12.5` 보다 앞에 온다. 그리고 `9.75` 와 `12.5` 의 순서도
> 뒤집힌다. 평균은 `174.5 / 10 = 17.45` 이다.

## 실행

    python3 problem03.py

입력: input03.txt
출력: output03.txt
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

INPUT_PATH = HERE / "input03.txt"
OUTPUT_PATH = HERE / "output03.txt"


def solve() -> int:
    """문제 3. 디버깅: 숫자 정렬과 평균 계산 오류 (난이도 중상)"""
    try:
        values = []
        with open(INPUT_PATH, "r", encoding="utf-8") as in_file:
            for line in in_file:
                text = line.strip()
                if not text or text.startswith("#"):
                    continue
                parts = text.split()
                if parts[0].upper() != "VALUE" or len(parts) != 2:
                    raise ValueError(f"알 수 없는 줄입니다: {text}")
                values.append(parts[1])

        values.sort()

        count = len(values)
        lines = [f"COUNT={count}"]
        if count:
            lowest = values[0]
            highest = values[-1]
            average = sum(float(v) for v in values) // count
            lines.append(f"MIN={lowest}")
            lines.append(f"MAX={highest}")
            lines.append(f"AVG={average:.2f}")
            lines.append("SORTED=" + ",".join(values))
        else:
            lines.append("MIN=")
            lines.append("MAX=")
            lines.append("AVG=")
            lines.append("SORTED=")

        OUTPUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    except (OSError, ValueError) as error:
        print(f"파일 처리 오류: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(solve())
