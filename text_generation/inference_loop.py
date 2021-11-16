import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import GPT2LMHeadModel, AutoModel

import time
from time import sleep
from kss import split_sentences

from tqdm import tqdm
import os

import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate a short text"
    )
    parser.add_argument(
        "--model_name_or_path",
        type=str,
        default=None,
        help="Path to pretrained model or model identifier from huggingface.co/models.",
    )
    parser.add_argument(
        "--prompt_text",
        type=str,
        default="함께",
        help="Prompting text",
    )

    # Sanity checks
    if args.model_name_or_path is None:
        raise ValueError("Need model name or path.")

    return args


def main():
    args = parse_args()

    model_path = agrs.model_name_or_path
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(model_path)

    # text = "삶과 죽음이 공존하는 위험성에 항상 노출되어 있다는 것은"
    text = args.prompt_text

    input_ids = tokenizer.encode(text)
    start = time.time()

    gen_txt = ""

    total = list(range(3000))
    with tqdm(total=len(total)) as pbar:

        while len(gen_txt) < 3000:

            if "\n" in text:
                text = text[: text.index("\n")]

            input_ids = tokenizer.encode(text)
            gen_ids = model.generate(
                torch.tensor([input_ids]),
                max_length=128,
                repetition_penalty=2.0,
                pad_token_id=tokenizer.pad_token_id,
                eos_token_id=tokenizer.eos_token_id,
                bos_token_id=tokenizer.bos_token_id,
                # num_beams=5,
                do_sample=True,
                top_k=30,
                top_p=0.95,
                use_cache=True,
            )

            generated = tokenizer.decode(gen_ids[0, :].tolist())

            if "\n" in generated:
                gen_txt += generated[: generated.index("\n")]

                if len(gen_txt) > 1000:
                    break
            elif len(gen_txt) < 128:
                gen_txt += generated
            else:
                gen_txt += generated[len(text) :]

            pbar.update(len(generated))

            splited_sentences = split_sentences(generated)
            # text = splited_sentences[-1]
            if len(splited_sentences) < 2:
                text = splited_sentences[-1]
            else:
                text = splited_sentences[-2] + " " + splited_sentences[-1]

            sleep(0.1)

    end = time.time()
    print(gen_txt)
    print(f"{end - start:.5f} sec")


if __name__ == "__main__":
    os.environ["TOKENIZERS_PARALLELISM"] = "true"
    main()
