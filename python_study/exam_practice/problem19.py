"""문제 19. Site/Test별 통계와 Cpk (난이도 상)


## 핵심

**표본 표준편차와 Cpk**입니다. 분모 `n-1`, NA 조건, 1.33 미만만 카운트.

수율만으로는 공정 상태를 알 수 없다. 측정한 값의 분포(평균, 표준편차)를 보고
스펙(하한·상한) 대비 값이 얼마나 정상적인지 Cpk로 판단한다. 테스트 엔지니어라면
반드시 들어본 지표다.

입력은 `input19_limits.csv`(`Test,Low,High,Unit`)와
`input19_measurements.csv`(`Site,Test,Value`) 두 파일이다.

```text
Cpk = min(High - mean, mean - Low) / (3 * sample_stdev)
sample_stdev = sqrt(sum((x-mean)^2) / (n-1))
```

1. `Site, Test` 조합별로 묶는다. (같은 Site 라도 Test 가 다르면 별도 그룹이다)
2. Cpk를 **계산할 수 없는 경우**는 아래 세 가지이고, 이때는 `NA` 를 쓴다.
   - `Low` 나 `High` 중 하나라도 비어 있는 경우
   - 측정값이 2개 미만(`n < 2`)인 경우
   - 표준편차가 0인 경우 (모든 측정값이 같을 때)
3. `Low`/`High`가 있는데 `Low > High`이면 그 Test는 Limit 오류라 종료 코드 1이다.
5. Site가 1~8 밖이거나, Value가 숫자가 아니거나, Limit에 없는 Test는 InvalidRows로 세고
   제외한다. InvalidRows는 stderr에 `ERROR line N: 이유` 형식으로 출력한 뒤,
   report에 개수만 쓴다.
6. 측정값이 한 개도 없는 Test는 그룹으로 만들지 않는다.
7. Mean/Stdev/Min/Max는 소수 넷째 자리까지 **사사오입**해서 출력한다.
   `Stdev`는 **표본 표준편차**(분모 `n-1`)다.
8. 출력 순서는 Test 오름차순, Site 오름차순이다.
9. `CpkBelow1.33`은 계산된 Cpk가 1.33 **미만**인 그룹 수다. 1.33은 포함하지 않는다.
10. 파일을 열 수 없으면 종료 코드 1이다.

## 풀이 순서 (⏱ 35분)

1. 그룹별 집계 — 8분
2. 평균 / 표본 표준편차(분모 n-1) — 10분
3. Cpk 계산 + NA 조건 — 10분
4. 출력 — 7분

> 2번만 풀어도 통계의 절반은 나옵니다.

## 출력

- `output19_cpk.csv` — 헤더는 `Test,Site,N,Mean,Stdev,Min,Max,Cpk,Unit`다.
- `output19_report.txt` — 아래 형태다.

```text
Groups=1
InvalidRows=0
CpkBelow1.33=0
```

## 예시

> 이 예시는 앞부분만 옮긴 것이다. `input19_limits.csv` 파일이 더 길어서 출력도 그만큼 더 나온다.

입력 (`input19_limits.csv`):

```text
Test,Low,High,Unit
VDD,1.10,1.30,V
```

입력 (`input19_measurements.csv`):

```text
Site,Test,Value
1,VDD,1.20
1,VDD,1.21
1,VDD,1.19
```

출력 (`output19_cpk.csv`):

```text
Test,Site,N,Mean,Stdev,Min,Max,Cpk,Unit
VDD,1,3,1.2000,0.0100,1.1900,1.2100,3.33,V
```

출력 (`output19_report.txt`):

```text
Groups=1
InvalidRows=0
CpkBelow1.33=0
```

## 실행

    python3 problem19.py

입력: input19_limits.csv
입력: input19_measurements.csv
출력: output19_cpk.csv
출력: output19_report.txt
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

LIMITS_PATH = HERE / "input19_limits.csv"
MEASUREMENTS_PATH = HERE / "input19_measurements.csv"
CPK_PATH = HERE / "output19_cpk.csv"
REPORT_PATH = HERE / "output19_report.txt"


def solve() -> int:
    """문제 19. Site/Test별 통계와 Cpk (난이도 상)"""
    return 0


if __name__ == "__main__":
    raise SystemExit(solve())
