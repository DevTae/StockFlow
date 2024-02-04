### StockFlow

-  `Airflow`, `Django`, [`StockTools`](https://github.com/DevTae/StockToolsPreview), [`StockPricePrediction`](https://github.com/DevTae/StockPricePredictionPreview) 를 활용하여 **주식 섹터 거래대금 분석, 딥러닝 모델 기반 가격예측, 핵심 키워드 분석에 대한 데이터를 ETL 기반으로 가공하여 제공**하는 `Apache Airflow 기반 데이터 파이프라인` 및 `RESTful API 서버` 프로젝트입니다.

- 개발 현황 트래킹
  - `Django RESTful API` 명세서 → [Notion Link](https://righteous-cuticle-5ba.notion.site/StockFlow-API-f905aa86afe541019af46298457e4c9a?pvs=4)
  - `StockFlow` 개발 요구사항에 대한 이슈 → [StockFlow Main Issue](https://github.com/DevTae/StockFlow/issues/4)

<br/>

- 프로젝트 구조
  - `StockFlow` : `Apache Airflow` 를 바탕으로 **데이터 파이프라인** 구축
    - [`StockTools`](https://github.com/DevTae/StockToolsPreview)
      - **회사 내의 데이터베이스 가정** (종가가 확정(*VI 포함*)된 **오후 3시 40분**부터 주식 가격, 업종 및 테마 데이터 스크래핑 작업 시작)
    - `StockFlow` ↔ [`StockTools`](https://github.com/DevTae/StockToolsPreview)
      - `StockTools` 의 스크래핑 작업이 완료된 순간부터 **ASP.net RESTful API 호출을 통한 주가 데이터, 테마 및 업종 정보** 자동 수집
    - `StockFlow` ↔ [`StockPricePrediction`](https://github.com/DevTae/StockPricePredictionPreview)
      - 수집한 주가 데이터를 바탕으로 **딥러닝 모델 기반 가격 예측 결과** 자동 수집
    - `StockFlow` ↔ `StockKeywordAnalysis`
      - 거래대금이 집중되는 종목에 대한 **테마 키워드 분석 결과** 자동 수집

  - `StockFlow` → User
    - 수집된 데이터들을 바탕으로 한 `업종 및 테마 별 누적 거래대금 및 순위`, `다음날 시초가 가격 예측 결과` 및 `핵심 키워드 분석` 기능 제공
    - 레포트 형식으로 개인투자자에게 정보를 제공(*Telegram 및 Slack 이용*)하여 매일매일 시장의 흐름을 파악할 수 있도록 함
    - `Redis Cache Server` 활용 (예정)
      - 계산 중 반복적으로 발생하는 `Database I/O` 를 줄이고자 적용
