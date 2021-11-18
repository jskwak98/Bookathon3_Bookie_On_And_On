# 2021 SKKU AI x Bookathon 3th

## 1. Introduction
성균관대학교에서 주최하는 AI x Bookathon 대회로 인공지능 모델을 사용하여 주제가 '함께'인 수필을 작성하는 것이 목적입니다. 

### 🥇 1st of 15 teams

저희는 `내가 나와 함께 살아가는 법` 을 글의 컨셉으로 하여 수필을 생성하였고, 최종적으로 1위를 하며 대상을 받을 수 있었습니다.

[>> 발표자료 보러가기](./북이온앤온_발표자료.pdf)

[>> 최종작품 보러가기](./내가%20나와%20함께%20살아가는%20법%20(I%20%2B%20I%20%3D%20We).md)

## 2. Data Preprocessing Strategy
크롤링한 데이터를 [KLUE: Korean Language Understanding Evaluation](https://arxiv.org/pdf/2105.09680.pdf) 논문에서 사용한 전처리 기법들을 사용하여 정제하였습니다. 

## 3. Model Training Strategy
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

### Retrieval for Elastic Search
수집한 전체 데이터셋의 크기가 굉장히 크고, 소주제별 Professional Writer Model 을 각각 만들기 위하여 전체데이터셋에서 주제에 맞는 Keyword 를 Query 로 하여 유사도 높은 문장만을 선별해 fine-tuning 하였습니다.

`elastic_search.py` 를 실행하면 train/valid 두 가지의 txt 파일이 생성됩니다.

## 4. Model Inference Strategy
Beam Search를 사용하는 경우 repetition problem이 발생할 확률이 높기 때문에 top-k sampling, top-p sampling 방법을 이용하여 텍스트 생성을 진행하였습니다. 

또한, 긴 문장을 생성하기 위해 max_length를 적게 설정하는 대신, 짧은 문장을 연달아서 여러 번 생성하는 방법을 사용하였습니다. 



# Structure
```
text_generation/train.py: 모델 학습 코드
text_generation/inference.py: 텍스트 생성 (추론)코드
text_generation/inference_loop.py: 짧은 텍스트를 연달아 생성하는 (추론)코드
```

# Usage
## 1. Installation
```
$ pip install -r requirements.txt
```

## 2. Retrieval
```
$ python elastic_search.py --query '함께' --corpus_dir 'YOUR_CORPUS_PATH' --num_samples 500
```
## 3. Training
```
$ sh text_generation/train.sh
```

## 4. Inference
```
$ sh text_generation/inference.sh
```

