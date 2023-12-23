### StockFlow

- `StockDatabase`, `Django`, `PostgreSQL` 를 활용한 **주식 섹터에 대한 거래대금 기반 주식 정보 제공**을 위한 `RESTful API` 서버 프로젝트입니다.

- `RESTful API` 명세서는 다음 링크에 있습니다. → [Notion Link](https://righteous-cuticle-5ba.notion.site/StockFlow-API-f905aa86afe541019af46298457e4c9a?pvs=4)

- `StockFlow` 개발 요구사항에 대한 이슈는 다음 링크에 있습니다. → [StockFlow Main Issue](https://github.com/DevTae/StockFlow/issues/4)

<br/>

- 프로젝트 구조
  - [`StockTools`](https://github.com/DevTae/StockToolsPreview)
    - `StockTools` 프로젝트 내에 있는 `StockDatabase` 프로젝트를 바탕으로 주가 데이터 수집
    - 테마 및 업종 정보 수집

  - [`StockTools`](https://github.com/DevTae/StockToolsPreview) → `StockFlow`
    - 주가 데이터 + 가격 예측 결과 + 테마 및 업종 정보 전송
    - `rabbitMQ` 를 바탕으로 `Redis Cache Server` 에 이벤트 전송
      - 수치가 변경된 정보들에 대한 Reloading 작업 진행

  - `StockFlow` → User
    - 수집된 데이터들을 바탕으로 한 `업종 및 테마 별 누적 거래대금 및 순위` 기능 제공
    - `Redis Cache Server` 활용
      - 계산 중 반복적으로 발생하는 `Database I/O` 를 줄이고자 적용

<!--
  - [`StockTools`](https://github.com/DevTae/StockToolsPreview) ↔ [`StockPricePrediction`](https://github.com/DevTae/StockPricePredictionPreview)
    - 수집한 주가 데이터를 바탕으로 가격 예측 결과 수집
    - 추후 개발 예정
-->