import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import GPT2LMHeadModel, AutoModel

import time
import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate a text"
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

    model_path = args.model_name_or_path
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(model_path)
    text = args.prompt_text
    input_ids = tokenizer.encode(text)
    # Check generation time
    start = time.time() 
    gen_ids = model.generate(torch.tensor([input_ids]),
                            max_length=1024,
                            repetition_penalty=2.0,
                            pad_token_id=tokenizer.pad_token_id,
                            eos_token_id=tokenizer.eos_token_id,
                            bos_token_id=tokenizer.bos_token_id,
                            # num_beams=5,
                            do_sample=True,
                            top_k=30, 
                            top_p=0.95,
                            use_cache=True)
    generated_text = tokenizer.decode(gen_ids[0,:].tolist())
    end = time.time()
    
    print(generated_text)
    print(f"{end - start:.5f} sec")


if __name__ == '__main__':
    main()