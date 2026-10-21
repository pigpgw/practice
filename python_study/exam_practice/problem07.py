"""문제 7. 웨이퍼 테스트 결과 집계와 수율 (난이도 중상)


## 핵심

**웨이퍼별로 묶어서 수율과 Bin 분포를 내는 것**입니다. 첫 등장 순서 유지, INVALID 처리.

웨이퍼 테스트를 하고 나면 "이 웨이퍼 수율이 얼마냐", "어느 Bin에서 많이 떨어졌냐"를
보면서 공정 상태를 본다. FAE의 기본 업무라 수학이라기보다 집계에 가깝다.
Bin이라는 개념(합격/불량 분류 번호)을 실제로 다뤄보는 문제다.

`input07.csv`의 각 행은 다이(die) 하나의 테스트 결과다.

```text
Wafer,Lot,Die,Status,Bin
```

1. `Wafer`별로 묶어 집계한다. 웨이퍼 출력 순서는 **첫 등장 순서**를 유지한다.
2. 한 웨이퍼 안에서 개수를 이렇게 센다.
   - `Dies` — 그 웨이퍼의 전체 다이 수
   - `Pass` — `Status` 가 PASS 인 다이 수
   - `Fail` — `Status` 가 FAIL 인 다이 수
   - `Status` 가 PASS/FAIL 이 외의 값(INVALID)인 다이는 **`Dies` 에만** 들어가고,
     `Pass` 나 `Fail` 어느 쪽에도 세지 않는다.
3. 수율 `YieldPercent` 는 `Pass / Dies × 100` 이고 소수 둘째 자리까지 **사사오입**한다.
   INVALID 다이가 `Dies` 에 들어가므로 **수율 분모에도 들어간다.**
4. Bin 분포는 **Bin 번호 오름차순**으로 센다. Bin 번호는 정수다.
   INVALID 다이도 자기 Bin 번호로 집계된다.
5. `Wafer`, `Lot`, `Die` 가 비었거나 `Bin` 이 정수가 아니면 오류로 세고 제외한다.
   `Status` 가 비어 있으면 오류고, PASS/FAIL 외의 값이면 2번 규칙으로 처리한다.
6. 오류는 stderr에 `ERROR line N: 이유` 형식으로 출력하고, 마지막 줄에 `ERRORS=n`을
   **리포트 파일에** 쓴다.

## 풀이 순서 (⏱ 35분)

1. Wafer별 그룹핑 — 8분
2. Total/Pass/Fail 집계 — 8분
3. 수율 계산 (사사오입) — 7분
4. Bin 분포 — 7분
5. 출력 3개 파일 — 5분

> 1~3번만 해도 실전 5번(CSV 집계) 유형이 됩니다.

## 출력

- `output07.csv` — 웨이퍼별 집계. 헤더는
  `Wafer,Lot,Dies,Pass,Fail,YieldPercent`다.
- `output07_bins.txt` — Bin 분포. 헤더는 `Bin,Count`다.
- `output07_report.txt` — 아래 형태다.

```text
Wafers=3
Lots=2
Dies=12
Pass=6
Fail=5
Yield=50.00%
ERRORS=2
```

## 예시

입력 (`input07.csv`):

```text
Wafer,Lot,Die,Status,Bin
W01,L24A,D01,PASS,1
W01,L24A,D02,FAIL,5
W01,L24A,D03,FAIL,5
W01,L24A,D04,PASS,1
W01,L24A,D05,PASS,1
W02,L24A,D01,PASS,1
W02,L24A,D02,FAIL,9
W02,L24A,D03,FAIL,9
W03,L25B,D01,PASS,1
W03,L25B,D02,PASS,3
W03,L25B,D03,FAIL,5
W03,L25B,D04,INVALID,7
W03,L25B,D05,,1
W03,L25B,D06,PASS,abc
```

출력 (`output07.csv`):

```text
Wafer,Lot,Dies,Pass,Fail,YieldPercent
W01,L24A,5,3,2,60.00
W02,L24A,3,1,2,33.33
W03,L25B,4,2,1,50.00
```

출력 (`output07_bins.txt`):

```text
Bin,Count
1,5
3,1
5,3
7,1
9,2
```

출력 (`output07_report.txt`):

```text
Wafers=3
Lots=2
Dies=12
Pass=6
Fail=5
Yield=50.00%
ERRORS=2
```

`D04`는 Status가 INVALID라 전체 수에는 들어가지만 PASS/FAIL 분자에는 안 들어가서,
`W03`은 Dies가 4인데 Pass는 2, Fail은 1이다.
`D05`(Die 빈 칸), `D06`(Bin이 숫자 아님)은 오류라 통째로 제외된다.

## 실행

    python3 problem07.py

입력: input07.csv
출력: output07.csv
출력: output07_bins.txt
출력: output07_report.txt
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

INPUT_PATH = HERE / "input07.csv"
SUMMARY_PATH = HERE / "output07.csv"
BINS_PATH = HERE / "output07_bins.txt"
REPORT_PATH = HERE / "output07_report.txt"


def solve() -> int:
    """문제 7. 웨이퍼 테스트 결과 집계와 수율 (난이도 중상)"""
    return 0


if __name__ == "__main__":
    raise SystemExit(solve())
