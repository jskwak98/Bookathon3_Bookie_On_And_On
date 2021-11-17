import pandas as pd
from tqdm import tqdm, trange
from elasticsearch import Elasticsearch, helpers
import argparse
import time

INDEX_NAME = "bookathon_index"

INDEX_SETTINGS = {
    "settings": {
        "index": {
            "analysis": {
                "analyzer": {
                    "korean": {
                        "type": "custom",
                        "tokenizer": "nori_tokenizer",
                        "filter": ["shingle"],

                    }
                }
            }
        }
    },
    "mappings": {

        "properties": {
            "content": {
                "type": "text",
                "analyzer": "korean",
                "search_analyzer": "korean"
            },
            "title": {
                "type": "text",
                "analyzer": "korean",
                "search_analyzer": "korean"
            }
        }

    }
}


def init_corpus(corpus):
    docs = [
        {
            '_index': INDEX_NAME,
            '_id': i,
            # 'title' : corpus.iloc[i]['title'],
            'content': corpus.iloc[i]['context']
        }
        for i in range(corpus.shape[0]) if i not in [1474]
    ]
    return docs


def init_elastic_search_engine(docs):
    try:
        es.transport.close()
    except:
        pass

    es = Elasticsearch()
    print(es.info())

    if es.indices.exists(INDEX_NAME):
        es.indices.delete(index=INDEX_NAME)
    es.indices.create(index=INDEX_NAME, body=INDEX_SETTINGS)

    start_time = time.time()
    try:
        response = helpers.bulk(es, docs)
        print("\nRESPONSE:", response)
    except Exception as e:
        print("\nERROR:", e)
        pass

    end_time = time.time()

    print(end_time - start_time)


def search_query(questions, size):
    global es

    error_queries = []
    results = []
    for question in questions:
        try:
            res = es.search(index=INDEX_NAME, q=question, size=size)
            results.append(res)
        except:
            error_queries.append(question)
    return results, error_queries


def make_retrieval_datasets(elastic_search_results, query):
    datas = []
    for i in range(len(elastic_search_results[0]['hits']['hits'])):
        text = elastic_search_results[0]['hits']['hits'][i]['_source']['content']
        datas.append({
            'id': i,
            'text': text,
        })

    df = pd.DataFrame(datas)
    with open(f"train_{query}.txt", 'w') as f:
        f.write('\n'.join([row[1]['text'] for row in df.iterrows()]))
    with open(f"valid_{query}.txt", 'w') as f:
        f.write('\n'.join([row[1]['text'] for row in df[:100].iterrows()]))


def main(args):
    query = args.query
    corpus_dir = args.corpus_dir
    if corpus_dir == '':
        assert "CORPUS DIR IS EMPTY STRING"
    num_samples_for_retrieval = args.num_samples

    docs = init_corpus(corpus_dir)
    init_elastic_search_engine(docs)

    res, err = search_query([query], num_samples_for_retrieval)
    make_retrieval_datasets(res, query)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--query', type=str, default='함께')
    parser.add_argument('--corpus_dir', type=str,
                        default='')
    parser.add_argument('--num_samples', type=int, default=500)

    args = parser.parse_args()

    main(args)
