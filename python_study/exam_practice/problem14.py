"""문제 14. 리페어(RA) 전후 수율 비교 (난이도 중상)


## 핵심

**리페어 전후 수율을 비교하는 것**입니다. 회수(Recovered) 수와 개선도(pp) 계산.

웨이퍼 테스트에서 불량이 난 다이는 리던던시 회로(RA)로 우회해서 한 번 더 돌려보는
리페어를 하곤 한다. 리페어로 몇 개를 살려냈는지, 최종 수율이 얼마나 올랐는지를
정확히 말할 수 있어야 FAE로서 일할 수 있다. 실제 웨이퍼 테스트에서 매일 하는 계산이다.

`input14.csv`의 각 행은 다이 하나의 1차 테스트 결과와, 그 다이를 리페어한 뒤 재시험한
결과다.

```text
Wafer,Die,First,Retest
W01,D01,FAIL,PASS
W01,D03,PASS,
```

- `First` — 1차 테스트 결과(PASS/FAIL)
- `Retest` — 리페어 후 재시험 결과. 1차가 PASS면 비어 있고, 1차가 FAIL면 보통 채워진다.

1. 1차가 PASS면 그 다이는 처음부터 최종 PASS다. `Retest`는 무시한다.
2. 1차가 FAIL이고 `Retest`가 PASS면 **회수(Recovered)**된 다이다. 최종 PASS다.
3. 1차가 FAIL이고 `Retest`가 FAIL이거나 비어 있으면 최종 FAIL이다.
   (리페어 실패, 혹은 재시험을 못 한 경우)
4. 수율은 `PASS 수 / 전체 다이 수 × 100`이고 소수 둘째 자리까지 **사사오입**한다.
   `First` 수율과 최종(Final) 수율을 따로 계산한다.
5. `Improved`는 최종 수율 - 1차 수율이고 단위는 퍼센트포인트(pp)다.
   소수 둘째 자리까지 사사오입한다.
6. `Wafer`, `Die`가 비었거나 `First`가 PASS/FAIL이 아니면 오류로 세고 제외한다.
   `Retest`가 비어 있으면 3번 규칙으로 처리한다(오류 아님).
   `Retest`에 PASS/FAIL 외의 값이 있으면 오류다.
7. 웨이퍼 출력 순서는 첫 등장 순서를 유지한다.
8. 오류는 stderr에 `ERROR line N: 이유` 형식으로 출력하고, 마지막 줄에 `ERRORS=n`을
   **리포트 파일에** 쓴다.

## 풀이 순서 (⏱ 30분)

1. 1차/재시험 결과 읽기 — 7분
2. 회수(Recovered) 판정 — 8분
3. 1차 수율 / 최종 수율 / 개선도(pp) — 10분
4. 출력 — 5분

> 1~2번만 해도 재검 개념은 나옵니다.

## 출력

- `output14_summary.csv` — 웨이퍼별 집계. 헤더는
  `Wafer,Dies,FirstPass,FirstFail,Recovered,FinalPass,FinalFail,FirstYield,FinalYield,DeltaPp`다.
- `output14_report.txt` — 전체 요약이다.

```text
Wafers=2
Dies=7
FirstPass=2
Recovered=3
FinalPass=5
FinalYield=71.43%
FirstYield=28.57%
Improved=42.86pp
ERRORS=2
```

## 예시

입력 (`input14.csv`):

```text
Wafer,Die,First,Retest
W01,D01,FAIL,PASS
W01,D02,FAIL,FAIL
W01,D03,PASS,
W01,D04,FAIL,
W02,D01,FAIL,PASS
W02,D02,FAIL,PASS
W02,D03,PASS,
W02,D04,FAIL,UNKNOWN
W02,D05,,PASS
```

출력 (`output14_summary.csv`):

```text
Wafer,Dies,FirstPass,FirstFail,Recovered,FinalPass,FinalFail,FirstYield,FinalYield,DeltaPp
W01,4,1,3,1,2,2,25.00,50.00,25.00
W02,3,1,2,2,3,0,33.33,100.00,66.67
```

출력 (`output14_report.txt`):

```text
Wafers=2
Dies=7
FirstPass=2
Recovered=3
FinalPass=5
FinalYield=71.43%
FirstYield=28.57%
Improved=42.86pp
ERRORS=2
```

`W01,D01`은 1차 FAIL이고 재시험 PASS라 회수된 다이다.
`W01,D04`는 재시험을 못 한 경우라 최종 FAIL이다.
`W02,D04`(Retest 값이 이상), `W02,D05`(First가 빈 칸)는 오류라 제외된다.

## 실행

    python3 problem14.py

입력: input14.csv
출력: output14_summary.csv
출력: output14_report.txt
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

INPUT_PATH = HERE / "input14.csv"
SUMMARY_PATH = HERE / "output14_summary.csv"
REPORT_PATH = HERE / "output14_report.txt"


def solve() -> int:
    """문제 14. 리페어(RA) 전후 수율 비교 (난이도 중상)"""
    return 0


if __name__ == "__main__":
    raise SystemExit(solve())
