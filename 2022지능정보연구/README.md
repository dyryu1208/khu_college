## 2022지능정보연구
본 리포지토리는 한국지능정보시스템학회 주관 2022년 추계학술대회 참가 및 2023년 3월 지능정보연구지에 게재 예정된 연구와 관련된 자료를 포함.

<br/>
<br/>

## 참고자료 
 
* [리뷰 유용성 관련 선행연구](https://www.notion.so/Reference-adf1eb1610b34e34825adcbf387a9670)
* [XAI 관련 선행연구](https://www.notion.so/XAI-Reference-4e81a6549ccd47e9b4ae1aefb5fd25a3)

<br/>
<br/>

## 연구명(영문) : XAI 기법을 이용한 리뷰 유용성 예측 결과 설명에 관한 연구(Explainable Artificial Intelligence Applied in Deep Learning for Review Helpfulness Prediction)

<br/>
본 연구는 비즈니스 리뷰 플랫폼 Yelp.com에서 제공하는 [Yelp Open Dataset](https://www.yelp.com/dataset)을 사용해 리뷰 유용성을 예측하는 동시에 예측에 대한 설명이 가능한 방법론을 제안

<br/>

1. [model_comparison](/2022지능정보연구/model_comparison.ipynb) : 텍스트 데이터에 대한 전처리와 6개의 머신러닝 및 딥러닝 모델의 리뷰 유용성 분류 성능을 비교
   
2. [xai_test](/2022지능정보연구/xai_test.ipynb) : 리뷰 유용성 분류 성능이 가장 우수한 LSTM 모델에 XAI(SHAP/LIME) 기법을 적용해 리뷰 내 어떤 단어가 유용성에 영향을 미쳤는지 확인
   
3. [xai_word_extraction](/2022지능정보연구/xai_word_extraction.ipynb) : 리뷰 유용성에 영향을 미친 단어와 그 중요도를 추출해서 csv파일로 만드는 코드
