"""문제 20. Bin 판정과 요약 (난이도 상)

## 핵심

**플랜(스펙)과 측정값을 짝지어 PASS/FAIL/ERROR 를 판정하는 것**입니다.
ini 파일(테스트 플랜)을 읽는 방법도 이 문제에서 다룹니다.

## 풀이 순서 (⏱ 40분)

1. ini 파일 읽기 — 10분
2. 측정값 비교 (경계 포함) — 10분
3. INVALID > FAIL > PASS 판정 + Bin 매핑 — 10분
4. 출력 3개 파일 — 10분

> 1·3번만 해도 판정 로직은 나옵니다.

## 상황

ATE는 유닛마다 모든 항목을 검사하고, 하나라도 스펙을 벗어나면 불량입니다.
그 결과를 Bin 번호로 묶어서 공정 쪽에 보고합니다. 이게 ATE 테스트 프로그램의 중심 작업입니다.

입력은 `input20_plan.ini`(플랜)와 `input20_measurements.csv`(측정) 두 파일이다.
측정 CSV의 컬럼 이름이 플랜의 `[TEST <id>]` id 와 같아야 한다.

```csv
Serial,Site,T1,T2,T3
U001,1,5.0,0.005,1.20
```

규칙은 다음과 같다.

1. 유닛 판정은 **INVALID > FAIL > PASS** 순서로 먼저 걸리는 게 이긴다.
   - INVALID 인 테스트가 하나라도 있으면 → `ErrorBin`
   - 그렇지 않고 FAIL 인 테스트가 하나라도 있으면 → `FailBin`
   - 전부 PASS 면 → `PassBin`
2. 값이 비었거나 숫자가 아니면 그 테스트만 INVALID 이다.
   Site가 1~8 밖이거나 Serial이 비면 그 유닛의 **모든 테스트가** INVALID 이다.
3. 경계값은 포함(`Low <= value <= High`)이고, 숫자는 소수 넷째 자리까지 **사사오입**한다.
4. 측정 CSV에 플랜의 test id 컬럼이 하나라도 없으면 플랜 구조 오류라 종료 코드 1이다.
5. 출력은 아래 세 파일이다.
   - `output20_datalog.csv` — 헤더 `Serial,Site,Test,Name,Value,Low,High,Unit,Result`.
     **모든 유닛 × 모든 테스트** 조합을 순서대로 쓴다. INVALID 테스트도 `Result=INVALID` 으로 쓴다.
   - `output20_summary.csv` — 헤더 `Serial,Site,Bin,FailTests,InvalidTests`.
   - `output20_report.txt` — 아래 형태다.

```text
Plan=PMIC_FT
Units=2
Pass=1
Fail=1
Error=0
Yield=50.00%
```

6. `Units` 는 측정 CSV에 등장한 유닛 수(중복 Serial 1개로 센다)이고,
   `Yield` 는 `Pass 유닛 수 / Units × 100` 을 소수 둘째 자리까지 사사오입한 값이다.
7. 파일을 열 수 없으면 종료 코드 1이다.

## 예시

입력 (`input20_measurements.csv`):

```text
Serial,Site,T1,T2
U001,1,5.0,0.005
U002,1,5.6,0.004
```

출력 (`output20_datalog.csv`):

```text
Serial,Site,Test,Name,Value,Low,High,Unit,Result
U001,1,T1,Vin,5.0000,4.5000,5.5000,V,PASS
U001,1,T2,Iq,0.0050,0.0000,0.0100,A,PASS
U002,1,T1,Vin,5.6000,4.5000,5.5000,V,FAIL
U002,1,T2,Iq,0.0040,0.0000,0.0100,A,PASS
```

출력 (`output20_summary.csv`):

```text
Serial,Site,Bin,FailTests,InvalidTests
U001,1,1,0,0
U002,1,2,1,0
```

출력 (`output20_report.txt`):

```text
Plan=PMIC_FT
Units=2
Pass=1
Fail=1
Error=0
Yield=50.00%
```

> `U002` 는 T1 이 스펙(4.5~5.5) 밖이라 FAIL, T2 는 PASS 인데
> **유닛 전체 판정은 FAIL** 이다. 한 개라도 FAIL 이면 그 유닛은 FAILBin 다.

## 실행

    python3 problem20.py

입력: input20_plan.ini
입력: input20_measurements.csv
출력: output20_datalog.csv
출력: output20_summary.csv
출력: output20_report.txt
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

PLAN_PATH = HERE / "input20_plan.ini"
MEASUREMENTS_PATH = HERE / "input20_measurements.csv"
DATALOG_PATH = HERE / "output20_datalog.csv"
SUMMARY_PATH = HERE / "output20_summary.csv"
REPORT_PATH = HERE / "output20_report.txt"


def solve() -> int:
    """문제 20. Bin 판정과 요약 (난이도 상)"""
    return 0


if __name__ == "__main__":
    raise SystemExit(solve())
