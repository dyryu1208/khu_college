## 2023BHelP-CoRT
본 리포지토리는 Applied Intelligence에 심사 중(Status - Under Review)인 연구와 관련된 자료를 포함.

<br/>
<br/>

## 참고자료 
 
* [BERT Model Link_1](https://tfhub.dev/tensorflow/base_bert/bert_en_uncased_L-12_H-768_A-12/1)
* [BERT Model Link_2](https://huggingface.co/transformers/v3.0.2/model_doc/bert.html)

<br/>

## 연구명 : A BERT-based Review Helpfulness Prediction Model Utilizing Consistency of Ratings and Texts 

<br/>

### 요약 : ML모델(SVM, RandomForest)과 DL모델(Dual-CNN, Bi-LSTM, Bi-GRU, BERT), 그리고 제안모델 BHelp-CoRT의 리뷰 유용성 예측 성능을 비교하여 평점 및 리뷰의 일관성이 성능 향상에 미치는 영향 탐색

<br/>

### 데이터 : E-Commerce 플랫폼 [Amazon](https://cseweb.ucsd.edu/~jmcauley/datasets.html#amazon_reviews)의 Toys and Games, CDs and Vinyls 의 데이터셋을 사용

<br/>

### 실험 코드

1. [ML_eda](/2023BHelp-CoRT/codes/ML_eda.ipynb) : 
   머신러닝 모델 투입용 데이터 전처리 과정

2. [ML_comparison](/2023BHelp-CoRT/codes/ML_comparison.ipynb) : 전처리된 머신러닝용 데이터셋을 ML모델에 투입하여 성능 확인

3. [DL_comparison](/2023BHelp-CoRT/codes/DL_comparison.ipynb) : 실험 데이터셋에 대한 딥러닝용 전처리 및 DL모델에 투입하여 성능 확인

4. [BHelp-CoRT](/2023BHelp-CoRT/codes/BHelp-CoRT.ipynb) : 제안 모델의 성능 확인, 제안 모델은 리뷰를 BERT로 학습한 다음 리뷰와 평점 정보에 Attention, Multiple 등 추가 커스텀 Layer 학습을 통해 리뷰 유용성을 예측

5. [BHelp-CoRT_SMALL](/2023BHelp-CoRT/codes/BHelp-CoRT_SMALL.ipynb) : 제안 모델의 BERT를 경량화된 버전으로 학습한 다음 성능 확인