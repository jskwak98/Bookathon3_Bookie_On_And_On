# 2021 SKKU AI x Bookathon 3th
## Introduction
성균관대학교에서 주최하는 AI x Bookathon 대회로, 주제가 '함께'인 수필을 인공지능 모델을 사용하여 쓰는 것이 목적입니다. 

## Model Training Strategy
마인즈랩에서 제공하는 뉴스데이터로 사전학습된 GPT2 모델을 사용하는 대신, 허깅페이스의 skt/ko-gpt-trinity-1.2B-v0.5를 한 번 더 사전학습을 진행한 후 fine-tuning 하는 방법으로 생성 모델을 학습시켰습니다.

NVIDIA T4를 사용하기 때문에 GPU 메모리가 부족하다는 단점이 있었지만 아래와 같은 전략을 통해 해결하였습니다.  
1. batch size를 줄이는 대신 accumulation step 활용
2. half precision 사용
3. 모델의 일부를 Freezing
4. 그 외의 파라미터 조정


GPT2의 경우, 긴 범위의 텍스트를 생성하게 되는 경우 글의 일관성이 부족할 수도 있다는 단점이 있습니다. 따라서 각 문단별로 주제에 맞는 키워드를 정한 후, 각 키워드에 관한 글들을 수집하여 2만자의 글을 생성하도록 하였습니다. 

### Train Datasets
각 학습 단계에서 사용한 데이터셋은 아래와 같습니다. 
```
1. Pretraining: 크롤링한 전체 데이터셋

2. Fine-tuning: Elastic Search를 사용하여 각 키워드에 맞는 데이터셋
```

## Model Inference Strategy
Beam Search를 사용하는 경우 repetition problem이 발생할 확률이 높기 때문에 top-k sampling, top-p sampling 방법을 이용하여 텍스트 생성을 진행하였습니다. 

또한, 긴 문장을 생성하기 위해 max_length를 적게 설정하는 대신, 짧은 문장을 연달아서 여러 번 생성하는 방법을 사용하였습니다. 



# Structure
```
train.py: 모델 학습 코드
inference.py: 텍스트 생성 (추론)코드
```

# Usage
## Installation
```
$ pip install -r requirements.txt
```
## Training
```
$ sh train.sh
```

## Inference
```
$ sh inference.sh
```

