## 2023BERT_TRI
본 리포지토리는 ???게재 미정인 연구와 관련된 자료를 포함.

<br/>
<br/>

## 참고자료 
 
* [BERT Model Link_1](https://tfhub.dev/tensorflow/base_bert/bert_en_uncased_L-12_H-768_A-12/1)
* [BERT Model Link_2](https://huggingface.co/transformers/v3.0.2/model_doc/bert.html)

<br/>

## 연구명(영문) : 미정

<br/>

본 연구는 E-Commerce 플랫폼 [Amazon](https://cseweb.ucsd.edu/~jmcauley/datasets.html#amazon_reviews)의 Toys and Games, CDs and Vinyls 의 데이터셋을 사용하여 ML모델(SVM, RandomForest)과 DL모델(Dual-CNN, Bi-LSTM, Bi-GRU, BERT), 그리고 제안모델 BERT_TRI의 리뷰 유용성 예측 성능을 비교하였음

<br/>

1. [ML_eda](/2023BERT_Helpfulness/codes/ML_eda.ipynb) : 
   머신러닝 모델 투입용 데이터 전처리 과정

2. [ML_comparison](/2023BERT_Helpfulness/codes/ML_comparison.ipynb) : 전처리된 머신러닝용 데이터셋을 ML모델에 투입하여 성능 확인

3. [DL_comparison](/2023BERT_Helpfulness/codes/DL_comparison.ipynb) : 실험 데이터셋에 대한 딥러닝용 전처리 및 DL모델에 투입하여 성능 확인

4. [BERT_TRI](/2023BERT_Helpfulness/codes/BERT_TRI.ipynb) : 제안 모델의 성능 확인, 제안 모델은 리뷰를 BERT로 학습한 다음 리뷰와 평점 정보에 Attention, Multiple 등 추가 Layer 학습을 통해 리뷰 유용성을 예측

5. [BERT_TRI_SMALL](/2023BERT_Helpfulness/codes/BERT_TRI_SMALL.ipynb) : 제안 모델의 BERT를 경량화된 버전으로 학습한 다음 성능 확인