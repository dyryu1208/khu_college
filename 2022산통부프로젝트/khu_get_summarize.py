from datetime import datetime
from optparse import Values
from re import I
from typing import Union
from math import isnan
import pandas as pd
import numpy as np
import time

# 
# 1. 기업 개요 요약문 출력
#    - 모든 컬럼 값이 다 있다고 가정하는 경우와 없는 경우에 대한 요약문
#    - 현재는 print()로 문장을 출력함. 필요에 따라서 return 방식을 수정할 수 있음.

#   1) 모든 컬럼값이 있는 경우 --> 이상적인 Rule-based 문장 출력

#   2) 없는 경우 : 어떤 값이 꼭 기업 개요에 들어가야 하는가? --> 기업명, 기업규모, 대표자명
#      - 위 세가지 값이 있는 경우 : 문장을 3개로 분류 후 2안 문장 출력 
#                             (기업명/기업규모/대표자명).  (시작연도/영업연도).  (종업원수)
#
#      - 위 세가지 값 중 하나라도 없는 경우 : 다른 사업자 번호 입력하게 유도  

def company_intro(company_number, df: pd.DataFrame):

    temp = df[df['사업자번호']==company_number]
    
    company_name = temp['기업명'].tolist()[0]
    industry = temp['산업명'].tolist()[0]
    company_size = temp['기업규모'].tolist()[0]
    start_year = temp['설립연도'].tolist()[0]
    business_year = datetime.today().year - start_year
    ceo = temp['대표자명'].tolist()[0]
    standard_time = datetime.today().strftime('%Y.%m')
    employee_num = temp['직원수'].tolist()[0]

    # 모든 요소가 다 있는 경우
    if (str(company_name) != 'nan') & (str(industry) != 'nan') & (str(company_size) != 'nan') & (str(start_year) != 'nan') & (str(ceo) != 'nan') & (str(employee_num) != 'nan') : 
        print(f'{company_name} 은(는) {industry}분야의 {company_size}으로, {start_year}년 부터 {business_year}년간 사업을 영위하고 있다. 대표자는 {ceo}이며, {standard_time} 기준 종업원은 {employee_num}명이다.')    
    
    # 시작연도/영업연도만 없는 경우
    elif (str(start_year) == 'nan') & (str(employee_num) != 'nan'):
        print(f'{company_name} 은(는) {company_size}이며, 대표자는 {ceo}이다. {standard_time} 기준 종업원은 {employee_num}명이다.')
        
    # 종업원수만 없는 경우
    elif (str(employee_num) == 'nan') & (str(start_year) != 'nan'):
        print(f'{company_name} 은(는) {company_size}이며, 대표자는 {ceo}이다. {start_year}년 부터 {business_year}년간 사업을 영위하고 있다.')
        
    # 시작연도/영업연도 & 종업원수 모두 없는 경우 + 기업명/기업규모/대표자명은 존재
    elif (str(employee_num) == 'nan') & (str(start_year) == 'nan') & (str(ceo) != 'nan'):
        print(f'{company_name} 은(는) {company_size}이며, 대표자는 {ceo}이다.')
    
    # 기업명/기업규모/대표자명 중 하나라도 없는 경우
    else:
        print('다른 사업자 번호를 입력하세요.')


# 2. 동종업계와 비교시 기업의 강점&약점 요약문 출력

# 1) 각 컬럼을 Key:Value로 가지는 딕셔너리 만들기
#    딕셔너리는 Key를 6대지수로, Value를 지수별 세부역량지수로 가짐
#    --> 해당 변수명 : detail_dict

# detail_dict : 각 컬럼을 6대지수:세부역량지수 로 갖는 dict()
detail_dict = {
                "R&D역량지수": ['기술인력비중평가점수', '전년대비R&D투자증액수준평가점수',
                                '국가R&D실적평가점수', '4차산업혁명대응수준평가점수'],

                "인적자원지수" : ['경영지원/전략기획인력수준평가점수', '종사자1인당매출액수준평가점수',
                                    '기업종사자비율증가수준평가점수'],

                "BM지수" : ['고용전망평가점수','체감경기전망평가점수',
                                '매출액증가추이평가점수', '사업화기반구축수준평가점수'],

                "마케팅역량지수" : ['고객응대서비스고도화수준평가점수','마케팅네트워크보유역량평가점수',
                                    '영업·마케팅인력비중평가점수','선도기업대비마케팅비용비중평가점수'],

                "미래성장지수" : ['매출액증가율', '순이익증가율', '신용점수', 'R&D점수',
                                    'BM점수', 'BM2기술성점수', 'BM2사업성점수'],

                "평판정보지수" : ['긍정백분율', '중립백분율', '부정백분율']

                }

# 2) 특정 지수의 차이를 계산하는 함수
# 차이 = 지수 - 동종업계에 속한 모든 기업들의 지수 평균값
def get_diff(company_number: Union[int, float], detail_dict: dict, df: pd.DataFrame) -> dict:
  result_dict = dict()
  temp = df[df['사업자번호']==company_number]
  
  for factor in detail_dict.keys():
    com_factor = float(temp[factor])
    avg_factor = float(temp[factor+'평균'])
    
    # 특정 지수를 구성하는 세부요인 중 어느 하나라도 결측값인 경우, 해당 지수에 대한 차이값을 nan으로 정의
    if pd.isna(com_factor) == False and pd.isna(avg_factor) == False:
      factor_diff = com_factor - avg_factor
      result_dict[factor] = factor_diff
    else:
      result_dict[factor] = np.nan

  return result_dict
  

# 3) 각 지수의 세부역량차이를 계산하는 함수
def get_detail_diff(company_number: Union[int, float], detail_dict: dict, factor : str, df: pd.DataFrame) -> dict:
  result_dict = dict()
  temp = df[df['사업자번호'] == company_number]
  for detail_factor in detail_dict[factor]:
    com_factor = float(temp[detail_factor])
    avg_factor = float(temp[detail_factor+'평균'])
    
    if pd.isna(com_factor) == False and pd.isna(avg_factor) == False:
      factor_diff = com_factor - avg_factor
      result_dict[detail_factor] = factor_diff
    else:
      result_dict[detail_factor] = np.nan  
    result_dict2 = {k: result_dict[k] for k in result_dict if not isnan(result_dict[k])}
  return result_dict2  


# 2-1. 강점만 있는 시나리오
def only_strong(company_number, main_factor_2 :dict, df: pd.DataFrame) -> list:
    """
    강점만 있는 경우에 대하여, 요약문을 출력하는 함수 -> 요약문 출력 형식은 필요에 따라 변경 가능
    input
        1) company_number: 사업자 번호
        2) main_factor_2: 지수 별 차이값을 저장한 dict -> ex) {'R&D역량지수': 50, '미래성장지수': 10}
        3) df: raw dataframe(기업 정보 데이터프레임)
    output
        1) diff_list: 지수명(리스트 형식) -> 추후, 해당 기업에 대한 보완 가이드라인 생성에 사용
    """
    temp = df[df['사업자번호']==company_number]
    company_name = temp['기업명'].tolist()[0]
    
    
    # 외부 main_factor_2에서 가져온 지수가 몇 개인지에 따른 출력문 생성
    # diff_list : main_factor_2에서 가져온 지수가 몇 개인지 확인하기 위한 리스트(동종업계 평균값과 차이가 큰 지수부터 나열됨)
    # diff_list는 추후 only_strong 함수의 반환값
    diff_list = sorted(main_factor_2, key=main_factor_2.get, reverse=True)

    # diff_list에 포함된 지수가 1개인 경우(=strong_1만 있고 weak_1은 없는 경우) -> strong_1에 대해서만 요약문 출력
    if len(diff_list) == 1:  
        strong_1 = diff_list[0]
        strong_detail = get_detail_diff(company_number, detail_dict, strong_1, df)
        if len(strong_detail) != 0:
            strong_factor = max(strong_detail, key=strong_detail.get)
            
            # 평판정보지수 키워드가 NULL인 경우에 대한 조건문 생성
            if strong_1 == '평판정보지수':
                
                # 평판정보지수 키워드가 NULL이 아닌 경우
                # 키워드를 포함하는 요약문 출력
                if pd.isna(temp["상위5개의긍정키워드"].values) == False:
                    print(f'{company_name}은(는) 동종업계 평균 대비 6대지수가 모두 우수한 역량을 보이고 있다. '+
                        f'특히, {strong_1}가 {temp[strong_1].values[0]}점으로 동종업계 평균인 {np.round(temp[strong_1+"평균"].values[0], 2)}점 대비 가장 우수하며, 상위 5개의 긍정적 키워드는 {list(temp["상위5개의긍정키워드"])}이다.')
                
                # 평판정보지수 키워드가 NULL인 경우
                # 키워드를 포함하지 않는 요약문 출력
                else:
                    print(f'{company_name}은(는) 동종업계 평균 대비 6대지수가 모두 우수한 역량을 보이고 있다. '+
                        f'특히, {strong_1}가 {temp[strong_1].values[0]}점으로 동종업계 평균인 {np.round(temp[strong_1+"평균"].values[0], 2)}점 대비 가장 우수하다.')
        else:
            print(f'{company_name}은(는) 동종업계 평균 대비 6대지수가 모두 우수한 역량을 보이고 있다.')
            pass
        
    # diff_list에 포함된 지수가 2개 이상인 경우 -> diff_list에서 최대값 지수 1개, 최소값 지수 1개씩 가져와 요약문을 출력
    else:
        strong_1 = diff_list[0]
        weak_1 = diff_list[-1]
        
        # 가장 차이가 큰 지수, 차이가 적은 지수의 세부역량점수차이 딕셔너리를 가져옴
        strong_detail = get_detail_diff(company_number, detail_dict, strong_1, df)
        weak_detail = get_detail_diff(company_number, detail_dict, weak_1, df)
         
        # 가장 차이가 큰 지수 및 가장 차이가 적은 지수의 세부 요인이 모두 존재하는 경우
        if len(strong_detail) != 0 and len(weak_detail) != 0:  
    
            strong_factor = max(strong_detail, key=strong_detail.get)
            weak_factor = min(weak_detail, key=weak_detail.get)
            
            # 평판정보지수가 강점인 경우 상위 5개의 긍정키워드 출력
            if strong_1 == '평판정보지수':
                
                # 평판정보지수 키워드가 NULL이 아닌 경우
                if pd.isna(temp["상위5개의긍정키워드"].values) == False: 
                    
                    # weak_1 내 세부역량지수 차이가 제일 작은 값의 차이가 0보다 큰 경우
                    # 출력문 마지막 부분을 "크게 차이가 나지 않는 모습을 보이고 있다." 로 설정
                    if (temp[weak_factor].values[0] - temp[weak_factor+"평균"].values[0]) > 0 :
                        print(f'{company_name}은(는) 동종업계 평균 대비 6대지수가 모두 우수한 역량을 보이고 있다. '+
                            f'특히, {strong_1}가 {temp[strong_1].values[0]}점으로 동종업계 평균인 {np.round(temp[strong_1+"평균"].values[0], 2)}점 대비 가장 우수하며, 상위 5개의 긍정적 키워드는 {list(temp["상위5개의긍정키워드"])}이다. '+
                            f'단, {weak_1}에서는 {weak_factor}가(이) {temp[weak_factor].values[0]}점으로 동종업계 평균인 {np.round(temp[weak_factor+"평균"].values[0], 2)}점과 크게 차이가 나지 않는 모습을 보여주고 있다.')
                    
                    # weak_1 내 세부역량지수 차이가 제일 작은 값의 차이가 0보다 작은 경우
                    # ~점에 비해 오히려 부족한 모습을 보이고 있다.
                    else:
                        print(f'{company_name}은(는) 동종업계 평균 대비 6대지수가 모두 우수한 역량을 보이고 있다. '+
                            f'특히, {strong_1}가 {temp[strong_1].values[0]}점으로 동종업계 평균인 {np.round(temp[strong_1+"평균"].values[0], 2)}점 대비 가장 우수하며, 상위 5개의 긍정적 키워드는 {list(temp["상위5개의긍정키워드"])}이다. '+
                            f'단, {weak_1}에서는 {weak_factor}가(이) {temp[weak_factor].values[0]} 점으로 동종업계 평균인 {np.round(temp[weak_factor+"평균"].values[0], 2)}점에 비해 오히려 부족한 모습을 보이고 있다.')
                        
                
                # 평판정보지수 키워드가 NULL인 경우
                # 키워드를 포함하지 않는 요약문 출력
                else:
                    # weak_1 내 세부역량지수 차가 제일 작은 값의 차이가 0보다 큰 경우
                    if (temp[weak_factor].values[0] - temp[weak_factor+"평균"].values[0]) > 0 :
                        print(f'{company_name}은(는) 동종업계 평균 대비 6대지수가 모두 우수한 역량을 보이고 있다. '+
                            f'특히, {strong_1}가 {temp[strong_1].values[0]}점으로 동종업계 평균인 {np.round(temp[strong_1+"평균"].values[0], 2)}점 대비 매우 우수한 역량을 보여주고 있다. '+
                            f'단, {weak_1}에서는 {weak_factor}가(이) {temp[weak_factor].values[0]}점으로 동종업계 평균인 {np.round(temp[weak_factor+"평균"].values[0], 2)}점 대비 크게 차이가 나지 않는 모습을 보여주고 있다.')
                    
                    # weak_1 내 세부역량지수 차가 제일 작은 값의 차이가 0보다 작은 경우
                    else:
                        print(f'{company_name}은(는) 동종업계 평균 대비 6대지수가 모두 우수한 역량을 보이고 있다. '+
                            f'특히, {strong_1}가 {temp[strong_1].values[0]}점으로 동종업계 평균인 {np.round(temp[strong_1+"평균"].values[0], 2)}점 대비 매우 우수한 역량을 보여주고 있다. '+
                            f'단, {weak_1}에서는 {weak_factor}가(이) {temp[weak_factor].values[0]}점으로 동종업계 평균인 {np.round(temp[weak_factor+"평균"].values[0], 2)}점에 비해 오히려 부족한 모습을 보이고 있다.')
                    
            # 평판정보지수가 약점인 경우 상위 5개의 부정키워드 출력
            elif weak_1 == '평판정보지수':  
                # 평판정보지수 키워드가 NULL이 아닌 경우
                if pd.isna(temp["상위5개의부정키워드"].values) == False:
                    print(f'{company_name}은(는) 동종업계 평균 대비 6대지수가 모두 우수한 역량을 보이고 있다. '+
                        f'특히, {strong_1}에서는 {strong_factor}가(이) {temp[strong_factor].values[0]}점으로 동종업계 평균인 {np.round(temp[strong_factor+"평균"].values[0], 2)}점 대비 매우 우수한 역량을 보여주고 있다. '+
                        f'단, {weak_1}는 {temp[weak_1].values[0]}점으로 동종업계 평균인 {np.round(temp[weak_1+"평균"].values[0], 2)}점 대비 크게 차이가 나지 않으며, 상위 5개의 부정적 키워드는 {list(temp["상위5개의부정키워드"])}이다.')
                    
                    
                # 평판정보지수 키워드가 NULL인 경우
                # 키워드를 포함하지 않는 요약문 출력
                else:
                    print(f'{company_name}은(는) 동종업계 평균 대비 6대지수가 모두 우수한 역량을 보여주고 있다. '+
                        f'특히, {strong_1}에서는 {strong_factor}가(이) {temp[strong_factor].values[0]}점으로 동종업계 평균인 {np.round(temp[strong_factor+"평균"].values[0], 2)}점 대비 매우 우수한 역량을 보여주고 있다. '+
                        f'단, {weak_1}는 {temp[weak_1].values[0]}점으로 동종업계 평균인 {np.round(temp[weak_1+"평균"].values[0], 2)}점 대비 크게 차이가 나지 않는 모습을 보여주고 있다.')
                    
                
            # 평판정보지수가 강점 또는 약점이 아닌 경우    
            # 각 세부역량점수 딕셔너리에서 차이가 가장 큰 값과 작은값 출력
            else : 
                # weak_1 내 세부역량지수 차가 제일 작은 값의 차이가 0보다 큰 경우 
                if (temp[weak_factor].values[0] - np.round(temp[weak_factor+"평균"].values[0], 2)) > 0:
                    print(f'{company_name}은(는) 동종업계 평균 대비 6대지수가 모두 우수한 역량을 보이고 있다. '+
                        f'특히, {strong_1}에서는 {strong_factor}가(이) {temp[strong_factor].values[0]}점으로 동종업계 평균인 {np.round(temp[strong_factor+"평균"].values[0], 2)}점 대비 매우 우수한 역량을 보여주고 있다. '+
                        f'단, {weak_1}에서는 {weak_factor}가(이) {temp[weak_factor].values[0]}점으로 동종업계 평균인 {np.round(temp[weak_factor+"평균"].values[0], 2)}점 대비 크게 차이가 나지 않는 모습을 보여주고 있다.')
                
                else:
                    print(f'{company_name}은(는) 동종업계 평균 대비 6대지수가 모두 우수한 역량을 보이고 있다. '+
                        f'특히, {strong_1}에서는 {strong_factor}가(이) {temp[strong_factor].values[0]}점으로 동종업계 평균인 {np.round(temp[strong_factor+"평균"].values[0], 2)}점 대비 매우 우수한 역량을 보여주고 있다. '+
                        f'단, {weak_1}에서는 {weak_factor}가(이) {temp[weak_factor].values[0]}점으로 동종업계 평균인 {np.round(temp[weak_factor+"평균"].values[0], 2)}점에 비해 오히려 부족한 모습을 보여주고 있다.')          
            
        # 가장 차이가 큰 지수의 세부 요인만 존재하는 경우
        elif len(strong_detail) != 0 and len(weak_detail) == 0:
            strong_factor = max(strong_detail, key=strong_detail.get)

            # 평판정보지수가 강점인 경우 상위 5개의 긍정키워드 출력
            if strong_1 == '평판정보지수':
                
                # 평판정보지수 키워드가 NULL이 아닌 경우
                if pd.isna(temp["상위5개의긍정키워드"].values) == False: 
                    
                    # weak_1 내 세부역량지수 차이가 제일 작은 값의 차이가 0보다 큰 경우
                    # 출력문 마지막 부분을 "크게 차이가 나지 않는 모습을 보이고 있다." 로 설정
                    print(f'{company_name}은(는) 동종업계 평균 대비 6대지수가 모두 우수한 역량을 보이고 있다. '+
                        f'특히, {strong_1}가 {temp[strong_1].values[0]}점으로 동종업계 평균인 {np.round(temp[strong_1+"평균"].values[0], 2)}점 대비 가장 우수하며, 상위 5개의 긍정적 키워드는 {list(temp["상위5개의긍정키워드"])}이다.')
                            
                
                # 평판정보지수 키워드가 NULL인 경우
                # 키워드를 포함하지 않는 요약문 출력
                else:
                    print(f'{company_name}은(는) 동종업계 평균 대비 6대지수가 모두 우수한 역량을 보이고 있다. '+
                        f'특히, {strong_1}가 {temp[strong_1].values[0]}점으로 동종업계 평균인 {np.round(temp[strong_1+"평균"].values[0], 2)}점 대비 매우 우수한 역량을 보여주고 있다.')
                
            # 평판정보지수가 약점인 경우 상위 5개의 부정키워드 출력
            elif weak_1 == '평판정보지수':
                
                # 평판정보지수 키워드가 NULL이 아닌 경우
                if pd.isna(temp["상위5개의부정키워드"].values) == False:
                    print(f'{company_name}은(는) 동종업계 평균 대비 6대지수가 모두 우수한 역량을 보이고 있다. '+
                        f'특히, {strong_1}에서는 {strong_factor}가(이) {temp[strong_factor].values[0]}점으로 동종업계 평균인 {np.round(temp[strong_factor+"평균"].values[0], 2)}점 대비 매우 우수한 역량을 보여주고 있다. '+
                        f'단, {weak_1}는 {temp[weak_1].values[0]}점으로 동종업계 평균인 {np.round(temp[weak_1+"평균"].values[0], 2)}점 대비 크게 차이가 나지 않으며, 상위 5개의 부정적 키워드는 {list(temp["상위5개의부정키워드"])}이다.')
                    
                    
                # 평판정보지수 키워드가 NULL인 경우
                # 키워드를 포함하지 않는 요약문 출력
                else:
                    print(f'{company_name}은(는) 동종업계 평균 대비 6대지수가 모두 우수한 역량을 보여주고 있다. '+
                        f'특히, {strong_1}에서는 {strong_factor}가(이) {temp[strong_factor].values[0]}점으로 동종업계 평균인 {np.round(temp[strong_factor+"평균"].values[0], 2)}점 대비 매우 우수한 역량을 보여주고 있다. '+
                        f'단, {weak_1}는 {temp[weak_1].values[0]}점으로 동종업계 평균인 {np.round(temp[weak_1+"평균"].values[0], 2)}점 대비 크게 차이가 나지 않는 모습을 보여주고 있다.')
                    
                
            # 평판정보지수가 강점 또는 약점이 아닌 경우    
            # 각 세부역량점수 딕셔너리에서 차이가 가장 큰 값과 작은값 출력
            else : 
                print(f'{company_name}은(는) 동종업계 평균 대비 6대지수가 모두 우수한 역량을 보이고 있다. '+
                    f'특히, {strong_1}에서는 {strong_factor}가(이) {temp[strong_factor].values[0]}점으로 동종업계 평균인 {np.round(temp[strong_factor+"평균"].values[0], 2)}점 대비 매우 우수한 역량을 보여주고 있다.')
                        
        # 가장 차이가 작은 지수의 세부지수만 존재하는 경우
        elif len(strong_detail) == 0 and len(weak_detail) != 0:
            
            weak_factor = min(weak_detail, key=weak_detail.get)

            # 평판정보지수가 강점인 경우 상위 5개의 긍정키워드 출력
            if strong_1 == '평판정보지수':
                
                # 평판정보지수 키워드가 NULL이 아닌 경우
                if pd.isna(temp["상위5개의긍정키워드"].values) == False: 
                    
                    # weak_1 내 세부역량지수 차이가 제일 작은 값의 차이가 0보다 큰 경우
                    # 출력문 마지막 부분을 "크게 차이가 나지 않는 모습을 보이고 있다." 로 설정
                    if (temp[weak_factor].values[0] - temp[weak_factor+"평균"].values[0]) > 0 :
                        print(f'{company_name}은(는) 동종업계 평균 대비 6대지수가 모두 우수한 역량을 보이고 있다. '+
                            f'특히, {strong_1}가 {temp[strong_1].values[0]}점으로 동종업계 평균인 {np.round(temp[strong_1+"평균"].values[0], 2)}점 대비 가장 우수하며, 상위 5개의 긍정적 키워드는 {list(temp["상위5개의긍정키워드"])}이다. '+
                            f'단, {weak_1}에서는 {weak_factor}가(이) {temp[weak_factor].values[0]}점으로 동종업계 평균인 {np.round(temp[weak_factor+"평균"].values[0], 2)}점과 크게 차이가 나지 않는 모습을 보여주고 있다.')
                    
                    # weak_1 내 세부역량지수 차이가 제일 작은 값의 차이가 0보다 작은 경우
                    # ~점에 비해 오히려 부족한 모습을 보이고 있다.
                    else:
                        print(f'{company_name}은(는) 동종업계 평균 대비 6대지수가 모두 우수한 역량을 보이고 있다. '+
                            f'특히, {strong_1}가 {temp[strong_1].values[0]}점으로 동종업계 평균인 {np.round(temp[strong_1+"평균"].values[0], 2)}점 대비 가장 우수하며, 상위 5개의 긍정적 키워드는 {list(temp["상위5개의긍정키워드"])}이다. '+
                            f'단, {weak_1}에서는 {weak_factor}가(이) {temp[weak_factor].values[0]} 점으로 동종업계 평균인 {np.round(temp[weak_factor+"평균"].values[0], 2)}점에 비해 오히려 부족한 모습을 보이고 있다.')
                        
                
                # 평판정보지수 키워드가 NULL인 경우
                # 키워드를 포함하지 않는 요약문 출력
                else:
                    # weak_1 내 세부역량지수 차가 제일 작은 값의 차이가 0보다 큰 경우
                    if (temp[weak_factor].values[0] - temp[weak_factor+"평균"].values[0]) > 0 :
                        print(f'{company_name}은(는) 동종업계 평균 대비 6대지수가 모두 우수한 역량을 보이고 있다. '+
                            f'특히, {strong_1}가 {temp[strong_1].values[0]}점으로 동종업계 평균인 {np.round(temp[strong_1+"평균"].values[0], 2)}점 대비 매우 우수한 역량을 보여주고 있다. '+
                            f'단, {weak_1}에서는 {weak_factor}가(이) {temp[weak_factor].values[0]}점으로 동종업계 평균인 {np.round(temp[weak_factor+"평균"].values[0], 2)}점 대비 크게 차이가 나지 않는 모습을 보여주고 있다.')
                    
                    # weak_1 내 세부역량지수 차가 제일 작은 값의 차이가 0보다 작은 경우
                    else:
                        print(f'{company_name}은(는) 동종업계 평균 대비 6대지수가 모두 우수한 역량을 보이고 있다. '+
                            f'특히, {strong_1}가 {temp[strong_1].values[0]}점으로 동종업계 평균인 {np.round(temp[strong_1+"평균"].values[0], 2)}점 대비 매우 우수한 역량을 보여주고 있다. '+
                            f'단, {weak_1}에서는 {weak_factor}가(이) {temp[weak_factor].values[0]}점으로 동종업계 평균인 {np.round(temp[weak_factor+"평균"].values[0], 2)}점에 비해 오히려 부족한 모습을 보이고 있다.')
                    
            # 평판정보지수가 약점인 경우 상위 5개의 부정키워드 출력
            elif weak_1 == '평판정보지수':
                
                # 평판정보지수 키워드가 NULL이 아닌 경우
                if pd.isna(temp["상위5개의부정키워드"].values) == False:
                    print(f'{company_name}은(는) 동종업계 평균 대비 6대지수가 모두 우수한 역량을 보이고 있다. '+
                        f'단, {weak_1}는 {temp[weak_1].values[0]}점으로 동종업계 평균인 {np.round(temp[weak_1+"평균"].values[0], 2)}점 대비 크게 차이가 나지 않으며, 상위 5개의 부정적 키워드는 {list(temp["상위5개의부정키워드"])}이다.')
                    
                    
                # 평판정보지수 키워드가 NULL인 경우
                # 키워드를 포함하지 않는 요약문 출력
                else:
                    print(f'{company_name}은(는) 동종업계 평균 대비 6대지수가 모두 우수한 역량을 보여주고 있다. '+
                        f'단, {weak_1}는 {temp[weak_1].values[0]}점으로 동종업계 평균인 {np.round(temp[weak_1+"평균"].values[0], 2)}점 대비 크게 차이가 나지 않는 모습을 보여주고 있다.')
                    
                
            # 평판정보지수가 강점 또는 약점이 아닌 경우    
            # 각 세부역량점수 딕셔너리에서 차이가 가장 큰 값과 작은값 출력
            else : 
                
                # weak_1 내 세부역량지수 차가 제일 작은 값의 차이가 0보다 큰 경우 
                if (temp[weak_factor].values[0] - np.round(temp[weak_factor+"평균"].values[0], 2)) > 0:
                    print(f'{company_name}은(는) 동종업계 평균 대비 6대지수가 모두 우수한 역량을 보이고 있다. '+
                        f'단, {weak_1}에서는 {weak_factor}가(이) {temp[weak_factor].values[0]}점으로 동종업계 평균인 {np.round(temp[weak_factor+"평균"].values[0], 2)}점 대비 크게 차이가 나지 않는 모습을 보여주고 있다.')
                
                else:
                    print(f'{company_name}은(는) 동종업계 평균 대비 6대지수가 모두 우수한 역량을 보이고 있다. '+
                        f'단, {weak_1}에서는 {weak_factor}가(이) {temp[weak_factor].values[0]}점으로 동종업계 평균인 {np.round(temp[weak_factor+"평균"].values[0], 2)}점에 비해 오히려 부족한 모습을 보여주고 있다.')
    
        else:
            print(f'{company_name}은(는) 동종업계 평균 대비 6대지수가 모두 우수한 역량을 보이고 있다.')
            pass
           
    return diff_list  # 6대지수를 포함하는 list 반환 

# 2-2. 약점만 있는 시나리오

def only_weak(company_number, main_factor_2 :dict, df) -> str:
    """
    약점만 있는 경우에 대하여, 요약문을 출력하는 함수 -> 요약문 출력 형식은 필요에 따라 변경 가능
    input
        1) company_number: 사업자 번호
        2) main_factor_2: 지수 별 차이값을 저장한 dict -> ex) {'R&D역량지수': 50, '미래성장지수': 10}
        3) df: raw dataframe(기업 정보 데이터프레임)
    output
        1) diff_list: 지수명(리스트 형식) -> 추후, 해당 기업에 대한 보완 가이드라인 생성에 사용
    """
    # 외부의 main_factor_2에서 가져온 약점들 중 제일 약한 지수 3개 추출
    temp = df[df['사업자번호']==company_number]
    company_name = temp['기업명'].tolist()[0]
    
    print(f'{company_name}은(는) 동종업계 평균 대비 6대지수가 모두 부진한 역량을 보이고 있다. ')
    
    # 외부 main_factor_2에서 가져온 지수가 몇 개인지에 따른 출력문 생성
    # diff_list : main_factor_2에서 가져온 지수가 몇 개인지 확인하기 위한 리스트(동종업계 평균값과 차이가 음(-)의 방향으로 큰 지수부터 나열됨)
    # diff_list는 추후 only_weak 함수의 반환값    
    diff_list = sorted(main_factor_2, key=main_factor_2.get)

    
    # diff_list 내 6대 지수가 1개만 들어있는 경우 -> 해당 지수에 대해서만 요약문 출력
    if len(diff_list) == 1:
        
        weak_detail = get_detail_diff(company_number, detail_dict, diff_list[0], df)
        
        # 세부요인의 차이값이 하나라도 존재하는 경우
        if len(weak_detail) != 0:  
            weak_factor = min(weak_detail, key=weak_detail.get)  # 세부요인 검색
            
            if diff_list[0] == '평판정보지수':
                if pd.isna(temp["상위5개의부정키워드"].values) == False:
                    print(f'특히, 평판정보지수는 {temp["평판정보지수"].values[0]}점으로 동종업계 평균인 {np.round(temp["평판정보지수평균"].values[0], 2)}점 대비 매우 부진하며, 상위 5개의 부정적 키워드는 {list(temp["상위5개의부정키워드"])}이다. ')   
                else:
                    print(f'특히, 평판정보지수는 {temp["평판정보지수"].values[0]}점으로 동종업계 평균인 {np.round(temp["평판정보지수평균"].values[0], 2)}점 대비 매우 부진하다. ')        
            else:
                print(f'특히, {diff_list[0]}는 {weak_factor}가(이) {temp[weak_factor].values[0]}점으로 동종업계 평균인 {np.round(temp[weak_factor+"평균"].values[0], 2)}점 대비 매우 부진한 역량을 보인다. ')
        
        else:
            pass    
        
    # diff_list 내 6대지수가 2개 들어있는 경우 -> 해당 지수들에 대해서만 요약문 출력
    elif len(diff_list) == 2:   
        count = 0  # 문장 갯수를 카운팅하는 변수
        for idx in range(2):
            weak_detail = get_detail_diff(company_number, detail_dict, diff_list[idx], df)
            
            if len(weak_detail) != 0:  # 세부요인의 차이값이 하나라도 존재하는 경우
                if idx == 0:
                    weak_factor = min(weak_detail,key=weak_detail.get) # - 방향으로 가장 차이값이 큰 세부요인 검색

                    if diff_list[idx] == '평판정보지수':
                        if pd.isna(temp["상위5개의부정키워드"].values) == False:
                            print(f'특히, 평판정보지수는 {temp["평판정보지수"].values[0]}점으로 동종업계 평균인 {np.round(temp["평판정보지수평균"].values[0], 2)}점 대비 매우 부진하며, 상위 5개의 부정적 키워드는 {list(temp["상위5개의부정키워드"])}이다. ')

                        else:
                            print(f'특히, 평판정보지수는 {temp["평판정보지수"].values[0]}점으로 동종업계 평균인 {np.round(temp["평판정보지수평균"].values[0], 2)}점 대비 매우 부진하다. ')
                    
                    else:
                        print(f'특히, {diff_list[idx]}는 {weak_factor}가(이) {temp[weak_factor].values[0]}점으로 동종업계 평균인 {np.round(temp[weak_factor+"평균"].values[0], 2)}점 대비 매우 부진한 역량을 보인다. ')
                    count += 1
                    
                else:
                    weak_factor = min(weak_detail,key=weak_detail.get) # 세부요인 검색

                    if diff_list[idx] == '평판정보지수':  # 평판정보지수인 경우
                        if pd.isna(temp["상위5개의부정키워드"].values) == False:  # 키워드가 존재하는 경우
                            sentence = f'평판정보지수는 {temp["평판정보지수"].values[0]}점으로 동종업계 평균인 {np.round(temp["평판정보지수평균"].values[0], 2)}점 대비 매우 부진하며, 상위 5개의 부정적 키워드는 {list(temp["상위5개의부정키워드"])}이다. '
                            if count == 0: # 첫 번째 출력 문장인 경우
                                print("특히, " + sentence)
                            elif count == 1:
                                print("또한, " + sentence)
                        else:  # 키워드가 존재하지 않는 경우
                            sentence = f'평판정보지수는 {temp["평판정보지수"].values[0]}점으로 동종업계 평균인 {np.round(temp["평판정보지수평균"].values[0], 2)}점 대비 매우 부진하다. '
                            if count == 0: # 첫 번째 출력 문장인 경우
                                print("특히, " + sentence)
                            elif count == 1:
                                print("또한, " + sentence)
                    
                    else:  # 평판정보지수가 아닌 경우
                        sentence = f'{diff_list[idx]}는 {weak_factor}가(이) {temp[weak_factor].values[0]}점으로 동종업계 평균인 {np.round(temp[weak_factor+"평균"].values[0], 2)}점 대비 매우 부진한 역량을 보인다. '
                        if count == 0: # 첫 번째 출력 문장인 경우
                            print("특히, " + sentence)
                        elif count == 1:
                            print("또한, " + sentence)
                        
            else:
                pass
        
    # diff_list 내 6대지수가 3개 이상 들어가는 경우 -> 해당 지수들에 대한 요약문 출력       
    else:           
        count = 0  # 문장 갯수를 카운팅하는 변수
        for idx in range(3):
            weak_detail = get_detail_diff(company_number, detail_dict, diff_list[idx], df)
                                
            if len(weak_detail) != 0: # 세부요인의 차이값이 하나라도 존재하는 경우
            # if all(np.isnan(x) for x in weak_detail.values()) != True:  # 세부요인의 차이값이 하나라도 존재하는 경우
                if idx == 0:
                    weak_factor = min(weak_detail,key=weak_detail.get)
                    # print(f'weak_factor: {weak_factor}')

                    if diff_list[idx] == '평판정보지수':
                        if pd.isna(temp["상위5개의부정키워드"].values) == False:
                            print(f'특히, 평판정보지수는 {temp["평판정보지수"].values[0]}점으로 동종업계 평균인 {np.round(temp["평판정보지수평균"].values[0], 2)}점 대비 매우 부진하며, 상위 5개의 부정적 키워드는 {list(temp["상위5개의부정키워드"])}이다. ')

                        else:
                            print(f'특히, 평판정보지수는 {temp["평판정보지수"].values[0]}점으로 동종업계 평균인 {np.round(temp["평판정보지수평균"].values[0], 2)}점 대비 매우 부진하다. ')
                    
                    else:
                        print(f'특히, {diff_list[idx]}는 {weak_factor}가(이) {temp[weak_factor].values[0]}점으로 동종업계 평균인 {np.round(temp[weak_factor+"평균"].values[0], 2)}점 대비 매우 부진한 역량을 보인다. ')
                    count += 1
                    
                elif idx == 1:
                    weak_factor = min(weak_detail,key=weak_detail.get)
                    # print(f'weak_factor: {weak_factor}')

                    if diff_list[idx] == '평판정보지수':
                        if pd.isna(temp["상위5개의부정키워드"].values) == False:
                            sentence = f'평판정보지수는 {temp["평판정보지수"].values[0]}점으로 동종업계 평균인 {np.round(temp["평판정보지수평균"].values[0], 2)}점 대비 매우 부진하며, 상위 5개의 부정적 키워드는 {list(temp["상위5개의부정키워드"])}이다. '
                            if count == 0:
                                print("특히, " + sentence)
                            elif count == 1:
                                print("또한, " + sentence)

                        else:
                            sentence = f'평판정보지수는 {temp["평판정보지수"].values[0]}점으로 동종업계 평균인 {np.round(temp["평판정보지수평균"].values[0], 2)}점 대비 매우 부진하다. '
                            if count == 0:
                                print("특히, " + sentence)
                            elif count == 1:
                                print("또한, " + sentence)
                    
                    else:
                        sentence = f'{diff_list[idx]}는 {weak_factor}가(이) {temp[weak_factor].values[0]}점으로 동종업계 평균인 {np.round(temp[weak_factor+"평균"].values[0], 2)}점 대비 매우 부진한 역량을 보인다. '
                        if count == 0:
                            print("특히, " + sentence)
                        elif count == 1:
                            print("또한, " + sentence)
                    count += 1

                else:
                    # factor 구하기
                    weak_factor = min(weak_detail,key=weak_detail.get)
                    # print(f'weak_factor: {weak_factor}')

                    if diff_list[idx] == '평판정보지수':
                        if pd.isna(temp["상위5개의부정키워드"].values) == False:
                            sentence = f'평판정보지수는 {temp["평판정보지수"].values[0]}점으로 동종업계 평균인 {np.round(temp["평판정보지수평균"].values[0], 2)}점 대비 매우 부진하며, 상위 5개의 부정적 키워드는 {list(temp["상위5개의부정키워드"])}이다. '
                            if count == 0:
                                print("특히, " + sentence)
                            elif count == 1:
                                print("또한, " + sentence)
                            elif count == 2:
                                print("마지막으로, " + sentence)

                        else:
                            sentence = f'평판정보지수는 {temp["평판정보지수"].values[0]}점으로 동종업계 평균인 {np.round(temp["평판정보지수평균"].values[0], 2)}점 대비 매우 부진하다. '
                            if count == 0:
                                print("특히, " + sentence)
                            elif count == 1:
                                print("또한, " + sentence)
                            elif count == 2:
                                print("마지막으로, " + sentence)
                    
                    else:
                        sentence = f'{diff_list[idx]}는 {weak_factor}가(이) {temp[weak_factor].values[0]}점으로 동종업계 평균인 {np.round(temp[weak_factor+"평균"].values[0], 2)}점 대비 매우 부진한 역량을 보인다. '
                        if count == 0:
                            print("특히, " + sentence)
                        elif count == 1:
                            print("또한, " + sentence)
                        elif count == 2:
                            print("마지막으로, " + sentence)

            else:
                pass
        
    return diff_list
            


# 2-3. 강점과 약점이 전부 있는 시나리오
# 6대지수별로 (지수-동종업계 평균값)이 양(+)의 값인 경우 강점으로,
# 음(-)의 값인 경우 약점으로 분류

def strong_and_weak(company_number, main_factor_2 :dict, df :pd.DataFrame):
    temp = df[df['사업자번호']==company_number]
    company_name = temp['기업명'].tolist()[0]
    
    plus_factor = list()
    minus_factor = list()

    for key,value in main_factor_2.items():
        if value > 0:
            plus_factor.append(key)
        else:
            minus_factor.append(key)

    
    print(f'{company_name}은(는) 동종업계 기업들의 평균 대비 {plus_factor}가 우수한 역량을 보이고 있다. '+
          f'반면, {minus_factor}의 경우 동종업계 기업들의 평균 대비 부족한 역량을 보이고 있다.')
    
    # 약점지수와 약점지수별 제일 취약한 세부역량 1개를 골라 표현
    # 약점 개수가 1~5이므로 경우의 수를 전부 고려
    # 또한, 평판정보지수를 포함하는 경우에 대해서도 고려
    # --> minus_factor에 평판정보지수가 있으면 우선적으로 평판정보지수 관련 요약문을 출력하고,
    #     minus_factor에서 평판정보지수가 제거된 new_minus_factor 생성
    
    if len(minus_factor) == 1:
        weak_detail = get_detail_diff(company_number, detail_dict, minus_factor[0], df)
        
        if len(weak_detail) != 0:
            weak_factor = min(weak_detail, key=weak_detail.get)
                        
            if minus_factor[0] == '평판정보지수':
                if pd.isna(temp["상위5개의부정키워드"].values) == False:
                    print(f'특히, 평판정보지수는 {temp["평판정보지수"].values[0]}점으로 동종업계 평균인 {np.round(temp["평판정보지수평균"].values[0], 2)}점 대비 매우 부진하며, 상위 5개의 부정적 키워드는 {list(temp["상위5개의부정키워드"])}이다. ')

                else:
                    print(f'특히, 평판정보지수는 {temp["평판정보지수"].values[0]}점으로 동종업계 평균인 {np.round(temp["평판정보지수평균"].values[0], 2)}점 대비 매우 부진하다. ')
            
            else:
                print(f'특히, {minus_factor[0]}는 {weak_factor}가(이) {temp[weak_factor].values[0]}점으로 동종업계 평균인 {np.round(temp[weak_factor+"평균"].values[0], 2)}점 대비 매우 부진한 역량을 보인다. ')
        
        else:
            pass
    
    elif len(minus_factor) == 2:
        count = 0
        for idx in range(2):
            weak_detail = get_detail_diff(company_number, detail_dict, minus_factor[idx], df)
            if len(weak_detail) != 0:
                if idx == 0:
                    weak_factor = min(weak_detail,key=weak_detail.get)

                    if minus_factor[idx] == '평판정보지수':
                        if pd.isna(temp["상위5개의부정키워드"].values) == False:
                            print(f'특히, 평판정보지수는 {temp["평판정보지수"].values[0]}점으로 동종업계 평균인 {np.round(temp["평판정보지수평균"].values[0], 2)}점 대비 매우 부진하며, 상위 5개의 부정적 키워드는 {list(temp["상위5개의부정키워드"])}이다. ')

                        else:
                            print(f'특히, 평판정보지수는 {temp["평판정보지수"].values[0]}점으로 동종업계 평균인 {np.round(temp["평판정보지수평균"].values[0], 2)}점 대비 매우 부진하다. ')     
                    else:
                        print(f'특히, {minus_factor[idx]}는 {weak_factor}가(이) {temp[weak_factor].values[0]}점으로 동종업계 평균인 {np.round(temp[weak_factor+"평균"].values[0], 2)}점 대비 매우 부진한 역량을 보인다. ')
                    count += 1
                    
                else:
                    # factor 구하기
                    weak_factor = min(weak_detail,key=weak_detail.get)

                    if minus_factor[idx] == '평판정보지수':
                        if pd.isna(temp["상위5개의부정키워드"].values) == False:
                            sentence = f'평판정보지수는 {temp["평판정보지수"].values[0]}점으로 동종업계 평균인 {np.round(temp["평판정보지수평균"].values[0], 2)}점 대비 매우 부진하며, 상위 5개의 부정적 키워드는 {list(temp["상위5개의부정키워드"])}이다. '
                            if count == 0:
                                print("특히, " + sentence)
                            elif count == 1:
                                print("또한, " + sentence)
                        
                        else:
                            sentence = f'평판정보지수는 {temp["평판정보지수"].values[0]}점으로 동종업계 평균인 {np.round(temp["평판정보지수평균"].values[0], 2)}점 대비 매우 부진하다. '
                            if count == 0:
                                print("특히, " + sentence)
                            elif count == 1:
                                print("또한, " + sentence)
                    
                    else:
                        sentence = f'{minus_factor[idx]}는 {weak_factor}가(이) {temp[weak_factor].values[0]}점으로 동종업계 평균인 {np.round(temp[weak_factor+"평균"].values[0], 2)}점 대비 매우 부진한 역량을 보인다. '
                        if count == 0:
                            print("특히, " + sentence)
                        elif count == 1:
                            print("또한, " + sentence)
            else:
                pass
        
    elif len(minus_factor) == 3:
        count = 0
        for idx in range(3):
            weak_detail = get_detail_diff(company_number, detail_dict, minus_factor[idx], df)
            
            if len(weak_detail) != 0: 
                if idx == 0:
                    weak_factor = min(weak_detail,key=weak_detail.get)

                    if minus_factor[idx] == '평판정보지수':
                        if pd.isna(temp["상위5개의부정키워드"].values) == False:
                            print(f'특히, 평판정보지수는 {temp["평판정보지수"].values[0]}점으로 동종업계 평균인 {np.round(temp["평판정보지수평균"].values[0], 2)}점 대비 매우 부진하며, 상위 5개의 부정적 키워드는 {list(temp["상위5개의부정키워드"])}이다. ')

                        else:
                            print(f'특히, 평판정보지수는 {temp["평판정보지수"].values[0]}점으로 동종업계 평균인 {np.round(temp["평판정보지수평균"].values[0], 2)}점 대비 매우 부진하다. ')
                    
                    else:
                        print(f'특히, {minus_factor[idx]}는 {weak_factor}가(이) {temp[weak_factor].values[0]}점으로 동종업계 평균인 {np.round(temp[weak_factor+"평균"].values[0], 2)}점 대비 매우 부진한 역량을 보인다. ')
                    count += 1
                    
                elif idx == 1:
                    weak_factor = min(weak_detail,key=weak_detail.get)

                    if minus_factor[idx] == '평판정보지수':
                        if pd.isna(temp["상위5개의부정키워드"].values) == False:
                            sentence = f'평판정보지수는 {temp["평판정보지수"].values[0]}점으로 동종업계 평균인 {np.round(temp["평판정보지수평균"].values[0], 2)}점 대비 매우 부진하며, 상위 5개의 부정적 키워드는 {list(temp["상위5개의부정키워드"])}이다. '
                            if count == 0:
                                print("특히, " + sentence)
                            elif count == 1:
                                print("또한, " + sentence)

                        else:
                            sentence = f'평판정보지수는 {temp["평판정보지수"].values[0]}점으로 동종업계 평균인 {np.round(temp["평판정보지수평균"].values[0], 2)}점 대비 매우 부진하다. '
                            if count == 0:
                                print("특히, " + sentence)
                            elif count == 1:
                                print("또한, " + sentence)
                    
                    else:
                        sentence = f'{minus_factor[idx]}는 {weak_factor}가(이) {temp[weak_factor].values[0]}점으로 동종업계 평균인 {np.round(temp[weak_factor+"평균"].values[0], 2)}점 대비 매우 부진한 역량을 보인다. '
                        if count == 0:
                            print("특히, " + sentence)
                        elif count == 1:
                            print("또한, " + sentence)
                    count += 1

                else:
                    # factor 구하기
                    weak_factor = min(weak_detail,key=weak_detail.get)

                    if minus_factor[idx] == '평판정보지수':
                        if pd.isna(temp["상위5개의부정키워드"].values) == False:
                            sentence = f'평판정보지수는 {temp["평판정보지수"].values[0]}점으로 동종업계 평균인 {np.round(temp["평판정보지수평균"].values[0], 2)}점 대비 매우 부진하며, 상위 5개의 부정적 키워드는 {list(temp["상위5개의부정키워드"])}이다. '
                            if count == 0:
                                print("특히, " + sentence)
                            elif count == 1:
                                print("또한, " + sentence)
                            elif count == 2:
                                print("마지막으로, " + sentence)

                        else:
                            sentence = f'평판정보지수는 {temp["평판정보지수"].values[0]}점으로 동종업계 평균인 {np.round(temp["평판정보지수평균"].values[0], 2)}점 대비 매우 부진하다. '
                            if count == 0:
                                print("특히, " + sentence)
                            elif count == 1:
                                print("또한, " + sentence)
                            elif count == 2:
                                print("마지막으로, " + sentence)
                    
                    else:
                        sentence = f'{minus_factor[idx]}는 {weak_factor}가(이) {temp[weak_factor].values[0]}점으로 동종업계 평균인 {np.round(temp[weak_factor+"평균"].values[0], 2)}점 대비 매우 부진한 역량을 보인다. '
                        if count == 0:
                            print("특히, " + sentence)
                        elif count == 1:
                            print("또한, " + sentence)
                        elif count == 2:
                            print("마지막으로, " + sentence)
            else:
                pass       
        
    elif len(minus_factor) == 4:
        count = 0
        for idx in range(4):
            weak_detail = get_detail_diff(company_number, detail_dict, minus_factor[idx], df)
            
            if len(weak_detail) != 0:
                if idx == 0:
                    # factor 구하기
                    weak_factor = min(weak_detail,key=weak_detail.get)

                    if minus_factor[idx] == '평판정보지수':
                        if pd.isna(temp["상위5개의부정키워드"].values) == False:
                            sentence = f'평판정보지수는 {temp["평판정보지수"].values[0]}점으로 동종업계 평균인 {np.round(temp["평판정보지수평균"].values[0], 2)}점 대비 매우 부진하며, 상위 5개의 부정적 키워드는 {list(temp["상위5개의부정키워드"])}이다. '
                            print("특히, " + sentence)
                                
                        else:
                            sentence = f'평판정보지수는 {temp["평판정보지수"].values[0]}점으로 동종업계 평균인 {np.round(temp["평판정보지수평균"].values[0], 2)}점 대비 매우 부진하다. '
                            print("특히, " + sentence)
                               
                    else:
                        print(f'특히, {minus_factor[idx]}는 {weak_factor}가(이) {temp[weak_factor].values[0]}점으로 동종업계 평균인 {np.round(temp[weak_factor+"평균"].values[0], 2)}점 대비 매우 부진한 역량을 보인다. ')
                    count += 1

                elif idx == 1:
                    # factor 구하기
                    weak_factor = min(weak_detail,key=weak_detail.get)

                    if minus_factor[idx] == '평판정보지수':
                        if pd.isna(temp["상위5개의부정키워드"].values) == False:
                            sentence = f'평판정보지수는 {temp["평판정보지수"].values[0]}점으로 동종업계 평균인 {np.round(temp["평판정보지수평균"].values[0], 2)}점 대비 매우 부진하며, 상위 5개의 부정적 키워드는 {list(temp["상위5개의부정키워드"])}이다. '
                            if count == 0:
                                print("특히, " + sentence)
                            elif count == 1:
                                print("그리고, " + sentence)

                        else:
                            sentence = f'평판정보지수는 {temp["평판정보지수"].values[0]}점으로 동종업계 평균인 {np.round(temp["평판정보지수평균"].values[0], 2)}점 대비 매우 부진하다. '
                            if count == 0:
                                print("특히, " + sentence)
                            elif count == 1:
                                print("그리고, " + sentence)
                    
                    else:
                        sentence = f'{minus_factor[idx]}는 {weak_factor}가(이) {temp[weak_factor].values[0]}점으로 동종업계 평균인 {np.round(temp[weak_factor+"평균"].values[0], 2)}점 대비 매우 부진한 역량을 보인다. '
                        if count == 0:
                            print("특히, " + sentence)
                        elif count == 1:
                            print("그리고, " + sentence)
                    count += 1
                
                elif idx == 2:
                    # factor 구하기
                    weak_factor = min(weak_detail,key=weak_detail.get)

                    if minus_factor[idx] == '평판정보지수':
                        if pd.isna(temp["상위5개의부정키워드"].values) == False:
                            sentence = f'평판정보지수는 {temp["평판정보지수"].values[0]}점으로 동종업계 평균인 {np.round(temp["평판정보지수평균"].values[0], 2)}점 대비 매우 부진하며, 상위 5개의 부정적 키워드는 {list(temp["상위5개의부정키워드"])}이다. '
                            if count == 0:
                                print("특히, " + sentence)
                            elif count == 1:
                                print("그리고, " + sentence)
                            elif count == 2:
                                print("또한, " + sentence)

                        else:
                            sentence = f'평판정보지수는 {temp["평판정보지수"].values[0]}점으로 동종업계 평균인 {np.round(temp["평판정보지수평균"].values[0], 2)}점 대비 매우 부진하다. '
                            if count == 0:
                                print("특히, " + sentence)
                            elif count == 1:
                                print("그리고, " + sentence)
                            elif count == 2:
                                print("또한, " + sentence)
                    
                    else:
                        sentence = f'{minus_factor[idx]}는 {weak_factor}가(이) {temp[weak_factor].values[0]}점으로 동종업계 평균인 {np.round(temp[weak_factor+"평균"].values[0], 2)}점 대비 매우 부진한 역량을 보인다. '
                        if count == 0:
                            print("특히, " + sentence)
                        elif count == 1:
                            print("그리고, " + sentence)
                        elif count == 2:
                            print("또한, " + sentence)
                    count += 1
                
                else:
                    weak_factor = min(weak_detail,key=weak_detail.get)

                    if minus_factor[idx] == '평판정보지수':
                        if pd.isna(temp["상위5개의부정키워드"].values) == False:
                            sentence = f'평판정보지수는 {temp["평판정보지수"].values[0]}점으로 동종업계 평균인 {np.round(temp["평판정보지수평균"].values[0], 2)}점 대비 매우 부진하며, 상위 5개의 부정적 키워드는 {list(temp["상위5개의부정키워드"])}이다. '
                            if count == 0:
                                print("특히, " + sentence)
                            elif count == 1:
                                print("그리고, " + sentence)
                            elif count == 2:
                                print("또한, " + sentence)
                            elif count == 3:
                                print("마지막으로, " + sentence)

                        else:
                            sentence = f'평판정보지수는 {temp["평판정보지수"].values[0]}점으로 동종업계 평균인 {np.round(temp["평판정보지수평균"].values[0], 2)}점 대비 매우 부진하다. '
                            if count == 0:
                                print("특히, " + sentence)
                            elif count == 1:
                                print("그리고, " + sentence)
                            elif count == 2:
                                print("또한, " + sentence)
                            elif count == 3:
                                print("마지막으로, " + sentence)
                    
                    else:
                        sentence = f'{minus_factor[idx]}는 {weak_factor}가(이) {temp[weak_factor].values[0]}점으로 동종업계 평균인 {np.round(temp[weak_factor+"평균"].values[0], 2)}점 대비 매우 부진한 역량을 보인다. '
                        if count == 0:
                            print("특히, " + sentence)
                        elif count == 1:
                            print("그리고, " + sentence)
                        elif count == 2:
                            print("또한, " + sentence)
                        elif count == 3:
                            print("마지막으로, " + sentence)
            else:
                pass 
        
    else:
        count = 0
        for idx in range(5):
            weak_detail = get_detail_diff(company_number, detail_dict, minus_factor[idx], df)
            
            if len(weak_detail) != 0:
                if idx == 0:
                    weak_factor = min(weak_detail,key=weak_detail.get)

                    if minus_factor[idx] == '평판정보지수':
                        if pd.isna(temp["상위5개의부정키워드"].values) == False:
                            print(f'특히, 평판정보지수는 {temp["평판정보지수"].values[0]}점으로 동종업계 평균인 {np.round(temp["평판정보지수평균"].values[0], 2)}점 대비 매우 부진하며, 상위 5개의 부정적 키워드는 {list(temp["상위5개의부정키워드"])}이다. ')
                        else:
                            print(f'특히, 평판정보지수는 {temp["평판정보지수"].values[0]}점으로 동종업계 평균인 {np.round(temp["평판정보지수평균"].values[0], 2)}점 대비 매우 부진하다. ')
                    
                    else:
                        print(f'특히, {minus_factor[idx]}는 {weak_factor}가(이) {temp[weak_factor].values[0]}점으로 동종업계 평균인 {np.round(temp[weak_factor+"평균"].values[0], 2)}점 대비 매우 부진한 역량을 보인다. ')
                    count += 1
                    
                elif idx == 1:
                    # factor 구하기
                    weak_factor = min(weak_detail,key=weak_detail.get)

                    if minus_factor[idx] == '평판정보지수':
                        if pd.isna(temp["상위5개의부정키워드"].values) == False:
                            sentence = f'평판정보지수는 {temp["평판정보지수"].values[0]}점으로 동종업계 평균인 {np.round(temp["평판정보지수평균"].values[0], 2)}점 대비 매우 부진하며, 상위 5개의 부정적 키워드는 {list(temp["상위5개의부정키워드"])}이다. '
                            if count == 0:
                                print("특히, " + sentence)
                            elif count == 1:
                                print("또한, " + sentence)

                        else:
                            sentence = f'평판정보지수는 {temp["평판정보지수"].values[0]}점으로 동종업계 평균인 {np.round(temp["평판정보지수평균"].values[0], 2)}점 대비 매우 부진하다. '
                            if count == 0:
                                print("특히, " + sentence)
                            elif count == 1:
                                print("또한, " + sentence)
                    
                    else:
                        sentence = f'{minus_factor[idx]}는 {weak_factor}가(이) {temp[weak_factor].values[0]}점으로 동종업계 평균인 {np.round(temp[weak_factor+"평균"].values[0], 2)}점 대비 매우 부진한 역량을 보인다. '
                        if count == 0:
                            print("특히, " + sentence)
                        elif count == 1:
                            print("또한, " + sentence)
                    count += 1

                elif idx == 2:
                    # factor 구하기
                    weak_factor = min(weak_detail,key=weak_detail.get)

                    if minus_factor[idx] == '평판정보지수':
                        if pd.isna(temp["상위5개의부정키워드"].values) == False:
                            sentence = f'평판정보지수는 {temp["평판정보지수"].values[0]}점으로 동종업계 평균인 {np.round(temp["평판정보지수평균"].values[0], 2)}점 대비 매우 부진하며, 상위 5개의 부정적 키워드는 {list(temp["상위5개의부정키워드"])}이다. '
                            if count == 0:
                                print("특히, " + sentence)
                            elif count == 1:
                                print("그리고, " + sentence)
                            elif count == 2:
                                print("또한, " + sentence)

                        else:
                            sentence = f'평판정보지수는 {temp["평판정보지수"].values[0]}점으로 동종업계 평균인 {np.round(temp["평판정보지수평균"].values[0], 2)}점 대비 매우 부진하다. '
                            if count == 0:
                                print("특히, " + sentence)
                            elif count == 1:
                                print("그리고, " + sentence)
                            elif count == 2:
                                print("또한, " + sentence)
                    
                    else:
                        sentence = f'{minus_factor[idx]}는 {weak_factor}가(이) {temp[weak_factor].values[0]}점으로 동종업계 평균인 {np.round(temp[weak_factor+"평균"].values[0], 2)}점 대비 매우 부진한 역량을 보인다. '
                        if count == 0:
                                print("특히, " + sentence)
                        elif count == 1:
                            print("그리고, " + sentence)
                        elif count == 2:
                            print("또한, " + sentence)
                    count += 1
                
                elif idx == 3:
                    # factor 구하기
                    weak_factor = min(weak_detail,key=weak_detail.get)

                    if minus_factor[idx] == '평판정보지수':
                        if pd.isna(temp["상위5개의부정키워드"].values) == False:
                            sentence = f'평판정보지수는 {temp["평판정보지수"].values[0]}점으로 동종업계 평균인 {np.round(temp["평판정보지수평균"].values[0], 2)}점 대비 매우 부진하며, 상위 5개의 부정적 키워드는 {list(temp["상위5개의부정키워드"])}이다. '
                            if count == 0:
                                print("특히, " + sentence)
                            elif count == 1:
                                print("그리고, " + sentence)
                            elif count == 2:
                                print("또한, " + sentence)
                            elif count == 3:
                                replaced_sentence = sentence.replace("이다.", "이며,")
                                print("한편, " + replaced_sentence)

                        else:
                            sentence = f'평판정보지수는 {temp["평판정보지수"].values[0]}점으로 동종업계 평균인 {np.round(temp["평판정보지수평균"].values[0], 2)}점 대비 매우 부진하다. '
                            if count == 0:
                                print("특히, " + sentence)
                            elif count == 1:
                                print("그리고, " + sentence)
                            elif count == 2:
                                print("또한, " + sentence)
                            elif count == 3:
                                replaced_sentence = sentence.replace("이다.", "이며,")
                                print("한편, " + replaced_sentence)
                    
                    else:
                        sentence = f'{minus_factor[idx]}는 {weak_factor}가(이) {temp[weak_factor].values[0]}점으로 동종업계 평균인 {np.round(temp[weak_factor+"평균"].values[0], 2)}점 대비 매우 부진한 역량을 보인다. '
                        if count == 0:
                            print("특히, " + sentence)
                        elif count == 1:
                            print("그리고, " + sentence)
                        elif count == 2:
                            print("또한, " + sentence)
                        elif count == 3:
                            replaced_sentence = sentence.replace("이다.", "이며,")
                            print("한편, " + replaced_sentence)
                    count += 1
                
                else:
                    # factor 구하기
                    weak_factor = min(weak_detail,key=weak_detail.get)

                    if minus_factor[idx] == '평판정보지수':
                        if pd.isna(temp["상위5개의부정키워드"].values) == False:
                            sentence = f'평판정보지수는 {temp["평판정보지수"].values[0]}점으로 동종업계 평균인 {np.round(temp["평판정보지수평균"].values[0], 2)}점 대비 매우 부진하며, 상위 5개의 부정적 키워드는 {list(temp["상위5개의부정키워드"])}이다. '
                            if count == 0:
                                print("특히, " + sentence)
                            elif count == 1:
                                print("그리고, " + sentence)
                            elif count == 2:
                                print("또한, " + sentence)
                            elif count == 3:
                                replaced_sentence = sentence.replace("이다.", "이며,")
                                print("한편, " + replaced_sentence)
                            elif count == 4:
                                print("마지막으로, " + sentence)

                        else:
                            sentence = f'평판정보지수는 {temp["평판정보지수"].values[0]}점으로 동종업계 평균인 {np.round(temp["평판정보지수평균"].values[0], 2)}점 대비 매우 부진하다. '
                            if count == 0:
                                print("특히, " + sentence)
                            elif count == 1:
                                print("그리고, " + sentence)
                            elif count == 2:
                                print("또한, " + sentence)
                            elif count == 3:
                                replaced_sentence = sentence.replace("이다.", "이며,")
                                print("한편, " + replaced_sentence)
                            elif count == 4:
                                print("마지막으로, " + sentence)
                    
                    else:
                        sentence = f'{minus_factor[idx]}는 {weak_factor}가(이) {temp[weak_factor].values[0]}점으로 동종업계 평균인 {np.round(temp[weak_factor+"평균"].values[0], 2)}점 대비 매우 부진한 역량을 보인다. '
                        if count == 0:
                            print("특히, " + sentence)
                        elif count == 1:
                            print("그리고, " + sentence)
                        elif count == 2:
                            print("또한, " + sentence)
                        elif count == 3:
                            replaced_sentence = sentence.replace("이다.", "이며,")
                            print("한편, " + replaced_sentence)
                        elif count == 4:
                            print("마지막으로, " + sentence)
            else:
                pass  
                  
    return minus_factor


# 3. 보완 가이드라인 출력
# 지수별로 가이드라인 문장은 고정되어 있음 --> guide_dict 참고
# 단, 시나리오별로 다른 요약문을 출력하게 함


# guide_dict :  각 지수별로 가이드라인을 담은 dict()
guide_dict = {'R&D역량지수' : '연구소 인력, 연구개발비 대비 실적, 그리고 최근 5개년 이내 국가 R&D 실적 등을 확인하고, 부족한 요소에 대한 보완 계획을 수립할 필요가 있다.',
            '미래성장지수' : '매출액 및 순이익에 악영향을 끼치는 요소를 확인하고 이에 대한 대책을 세우며, 기술성 및 사업성을 향상시키기 위한 비즈니스 모델을 구축할 필요가 있다.',
            '인적자원지수' : '경영지원 또는 전략기획 등의 인력 수준, 직원의 자기 개발 지원 정도, 종사자 1인당 매출액 수준 등의 세부요소를 고려하여 인적자원 역량 전문화를 추진할 필요가 있다.',
            'BM지수' : '해당 분야에 대한 시장 경쟁력, 규모, 제품 생명 주기 등을 고려하여 사업화 역량을 고도화시켜하며, 이에 따른 비즈니스 모델을 수립할 필요가 있다.',
            '마케팅역량지수' : '고객응대 서비스, 인력 및 네트워크 보유 측면에서 마케팅 비용 투자를 진행할 필요가 있다.',
            '평판정보지수' : '기업 내부 평판으로서 복지, 급여 및 자기 개발 지원 등의 요소를, 기업 외부 평판으로서 고객 서비스 및 대응 방식에 대한 만족도 등의 요소를 고려하여, 미비한 요소를 보완하기 위한 계획을 수립할 필요가 있다.'
            }   

def guideline(company_number, guide_dict, main_factor_2:dict, df:pd.DataFrame):
    temp = df[df['사업자번호']==company_number]
    company_name = temp['기업명'].tolist()[0]

    # 강점만 있는 경우
    # 강점 중 제일 취약한 지수 1개에 대해서만 가이드라인 문장 출력
    # strong_1만 출력되는 경우에 대한 if코드 작성
    if all(x > 0 for x in main_factor_2.values()):
        diff_list = only_strong(company_number, main_factor_2, df)
        
        # strong_1만 존재하는 경우(=weak_1이 존재하지 않는 경우)
        if len(diff_list) == 1:
            print(f'따라서, {company_name}은(는) 각 6대지수에 대한 강점을 유지할 수 있도록 지속적인 관심과 노력이 필요하다.')
        
        # strong_1과 weak_1이 모두 존재하는 경우
        # weak_1에 대한 가이드라인 문장 출력
        else:
            weak_1 = diff_list[-1]
            weak_1_sentence = guide_dict[weak_1]
            print(f'따라서, {company_name}은(는) {weak_1_sentence}')
    
    # 약점만 있는 경우
    # 약점 3개 전부에 대해 가이드라인 문장 출력
    # weak_1만 있는 경우, weak_1 / weak_2만 있는 경우에 대한 if 코드 작성
    elif all(x < 0 for x in main_factor_2.values()):
        diff_list = only_weak(company_number, main_factor_2, df)
        
        # weak_1만 있는 경우(=약점이 1개만 나오는 경우)
        if len(diff_list) == 1:
            weak_1 = diff_list[0]
            weak_1_sentence = guide_dict[weak_1]
            print(f'따라서, {company_name}은(는) {weak_1_sentence}')
        
        elif len(diff_list) == 2:
            weak_1 = diff_list[0]
            weak_2 = diff_list[1]
            weak_1_sentence = guide_dict[weak_1]
            weak_2_sentence = guide_dict[weak_2]
            print(f'따라서 {company_name}은(는) {weak_1_sentence}'+
                  f'또한, {weak_2_sentence}')
        
        else:
            weak_1 = diff_list[0]
            weak_2 = diff_list[1]
            weak_3 = diff_list[2]      
            weak_1_sentence = guide_dict[weak_1]
            weak_2_sentence = guide_dict[weak_2]
            weak_3_sentence = guide_dict[weak_3]
            
            print(f'따라서 {company_name}은(는) {weak_1_sentence}'+
                f'또한, {weak_2_sentence}'+
                f'마지막으로, {weak_3_sentence}'
                )
    
    # 강점, 약점 둘 다 있는 경우
    # minus_factor(약점지수만 모아놓은 리스트)의 개수에 따라 다른 가이드라인 문장 출력
    else:
        minus_factor = strong_and_weak(company_number, main_factor_2, df)
        
        if len(minus_factor) == 1:
            weak_1_sentence = guide_dict[minus_factor[0]]
            
            print(f'따라서 {company_name}은(는) {weak_1_sentence}')
        
        elif len(minus_factor) == 2:
            weak_1_sentence = guide_dict[minus_factor[0]]
            weak_2_sentence = guide_dict[minus_factor[1]]
            
            print(f'따라서 {company_name}은(는) {weak_1_sentence}'+
                  f' 또한, {weak_2_sentence}')

        elif len(minus_factor) == 3:
            weak_1_sentence = guide_dict[minus_factor[0]]
            weak_2_sentence = guide_dict[minus_factor[1]]            
            weak_3_sentence = guide_dict[minus_factor[2]]
            
            print(f'따라서, {company_name}은(는) {weak_1_sentence}'+
                  f' 또한, {weak_2_sentence}'+
                  f' 마지막으로, {weak_3_sentence}')     
        
        elif len(minus_factor) == 4:
            weak_1_sentence = guide_dict[minus_factor[0]]
            weak_2_sentence = guide_dict[minus_factor[1]]            
            weak_3_sentence = guide_dict[minus_factor[2]]            
            weak_4_sentence = guide_dict[minus_factor[3]]
            
            print(f'따라서, {company_name}은(는) {weak_1_sentence}'+
                  f' 또한, {weak_2_sentence}'+
                  f' 또, {weak_3_sentence}' +
                  f' 마지막으로, {weak_4_sentence}')     

            
        else:
            weak_1_sentence = guide_dict[minus_factor[0]]
            weak_2_sentence = guide_dict[minus_factor[1]]            
            weak_3_sentence = guide_dict[minus_factor[2]]            
            weak_4_sentence = guide_dict[minus_factor[3]]
            weak_5_sentence = guide_dict[minus_factor[4]]

            print(f'따라서, {company_name}은(는) {weak_1_sentence}'+
                  f' 또한, {weak_2_sentence}'+
                  f' 또, {weak_3_sentence}'+
                  f' 그리고, {weak_4_sentence}'
                  f' 마지막으로, {weak_5_sentence}') 
            
# 4. 위 요약문 함수들을 한번에 출력하는 함수

def print_summarize_sentence(company_number, df):
    
    # 기업 개요 요약문 출력
    company_intro(company_number, df)
    
    # 입력된 기업의 6대지수별 차이를 담은 dict() 생성
    # 예시 :
    # {'R&D역량지수' : 1.56487, '인적자원지수' : -3.2156788, 'BM지수' : np.nan, 
    # '미래성장지수' : -8.444874216, '마케팅역량지수' : np.nan, '평판정보지수' : np.nan}
    main_factor = get_diff(company_number, detail_dict, df)
    
    # main_factor에 대해서 nan값을 가진 것들은 전부 배제한 main_factor_2 생성
    # 예시 : 
    # {'R&D역량지수' : 1.56487, '인적자원지수' : -3.2156788, '미래성장지수' : -8.444874216}    
    main_factor_2 = {k: main_factor[k] for k in main_factor if not isnan(main_factor[k])}
    
    # main_factor_2의 값이 모두 nan값을 가진 경우(=딕셔너리 안에 6대지수 중 어느 하나라도 값이 없는 경우)
    if main_factor_2:
        # 동종업계 비교시 기업의 강점 & 약점 출력하는
        # 시나리오별 요약문 출력 + 보완 가이드라인 출력
        guideline(company_number, guide_dict, main_factor_2, df)
    else:  # {}
        print("해당 기업에 대한 지수 정보가 존재하지 않습니다. 요약문 생성을 중단합니다.")

    

if __name__ == '__main__':
    
    # 실행시간 측정
    start = time.time()
    
    # 실행에 사용한 데이터프레임
    # 이전 khu_make_test_file.py 파일에서 만든 임의의 값이 들어간 데이터프레임

    df = pd.read_csv('KHU_기업요약_요청데이터_20221215.csv')
    
    # 사업자 번호 입력 후 코드 시작
    company_number = input('사업자 번호를 입력하세요 : ')
    
    print('-'*20, '기업 요약문 출력', '-'*20)

    print_summarize_sentence(int(company_number), df)
    print('\n')
    print("* 작업 소요시간 :", time.time() - start)