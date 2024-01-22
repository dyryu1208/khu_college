## 2023CDRS
본 리포지토리는 대한산업공학회/한국경영과학회 공동주관 2023년 춘계학술대회 참가 및 Electronic Commerce Research 심사 중(Status - Under Review)인 연구와 관련된 자료를 포함.

<br/>
<br/>

## 참고자료 
 
* [CDRS 관련 선행연구](https://www.notion.so/Cross-Domain-Recommendation-Ref-b0b19566c9194314a8bca813d0c2aad6)

<br/>

## 연구명(국문) : A Doc2Vec-based cross-domain recommendation for alleviating data sparsity problems(데이터 희소성 문제 해결을 위한 Doc2Vec 기반의 교차 도메인 추천시스템 모형 개발 및 평가)

<br/>

### 요약 : 사용자의 정보가 희소한 도메인의 추천 성능을 향상시키기 위해 해당 사용자가 남긴 다양한 도메인 내 풍부한 정보를 결합하는 연구

<br/>

### 데이터 : [Yelp Open Dataset](https://www.yelp.com/dataset) 사용

<br/>

### 실험 코드 

1. [Dataset Making](/2023CDRS/codes/yelp_make_dset.ipynb) : 교차 도메인 추천시스템을 위한 실험 데이터를 생성하는 코드
   

2. [Data Preprocessing](/2023CDRS/codes/yelp_preprocessing.ipynb) : 실험에 투입 전 데이터를 최종 전처리하는 코드

3. [Doc2Vec Embeddings](/2023CDRS/codes/Doc2Vec_embeddings.ipynb) : 사용자와 제품별 고정된 크기의 Doc2Vec 문서 임베딩을 생성하는 코드

4. [Cross-Domain Model](/2023CDRS/codes/Cross_Domain_Model.ipynb) : 사용자 및 제품별 임베딩을 입력받아 사용자의 제품에 대한 평점을 예측하는 코드

5. [Baselines](/2023CDRS/codes/Baselines.ipynb) : 제안된 모델과 추천 성능을 비교하는 모델 코드

6. [Ablation_1](/2023CDRS/codes/Ablation_1.ipynb) : Doc2Vec 임베딩 벡터 크기를 다르게 적용하여 최적 임베딩 크기를 탐색하는 추가실험 코드

7. [Ablation_2](/2023CDRS/codes/Ablation_2.ipynb) : 소스 도메인과 타겟 도메인의 임베딩 결합방식을 변경하는 추가실험 코드

8. [Ablation_3](/2023CDRS/codes/Ablation_3.ipynb) : 두 도메인 간 중복 사용자 비율을 조절하는 추가실험 코드

9. [Ablation_4](/2023CDRS/codes/Ablation_4.ipynb) : 최적의 하이퍼 파라미터를 탐색하는 추가실험 코드
