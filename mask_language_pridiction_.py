# -*- coding: utf-8 -*-
"""Mask language pridiction....ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1oQ7JltnPHp2HACB2XFkeuJc4HR5G7F7Y
"""

!pip install torch
!pip install tokenizers
!pip install transformers

vocab_length = 30522

import tokenizers
# 
roman_BWPT = tokenizers.BertWordPieceTokenizer(
#     # add_special_tokens=True, # This argument doesn't work in the latest version of BertWordPieceTokenizer
     unk_token='[UNK]',
     sep_token='[SEP]',
     cls_token='[CLS]',
     clean_text=True,
     handle_chinese_chars=True,
     strip_accents=True,
     lowercase=True,
     wordpieces_prefix='##'
 )
 
roman_BWPT.train(
     files=["roman.txt"],
     vocab_size=vocab_length,
     min_frequency=3,
     limit_alphabet=1000,
     show_progress=True,
     special_tokens=['[PAD]', '[UNK]', '[CLS]', '[MASK]', '[SEP]']
 )
 
roman_BWPT.save_model(".", "roman-urdu"+str(vocab_length))

# Load the tokenizer
from transformers import BertTokenizer, LineByLineTextDataset

vocab_file_dir = 'vocab.txt' 

tokenizer = BertTokenizer.from_pretrained(vocab_file_dir)

sentence = 'ppp chill pmln lorey lag gayi har tarah'

encoded_input = tokenizer.tokenize(sentence)
print(encoded_input)
# print(encoded_input['input_ids'])

dataset= LineByLineTextDataset(
    tokenizer = tokenizer,
    file_path = '/content/roman.txt',
    block_size = 128  # maximum sequence length
)

print('No. of lines: ', len(dataset)) # No of lines in your datset

from transformers import BertConfig, BertForMaskedLM, DataCollatorForLanguageModeling

config = BertConfig(
    vocab_size=50000,
    hidden_size=768, 
    num_hidden_layers=6, 
    num_attention_heads=12,
    max_position_embeddings=512
)
 
model = BertForMaskedLM(config)
print('No of parameters: ', model.num_parameters())


data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer, mlm=True, mlm_probability=0.15
)

from transformers import Trainer, TrainingArguments

training_args = TrainingArguments(
    output_dir='model_dir',
    overwrite_output_dir=True,
    num_train_epochs=1,
    per_device_train_batch_size=32,
    save_steps=10_000,
    save_total_limit=2,
)

trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=dataset,
    #prediction_loss_only=False,
)

# Commented out IPython magic to ensure Python compatibility.
# %%time
# trainer.train()
# trainer.save_model('model_dir')

from transformers import pipeline

model = BertForMaskedLM.from_pretrained('model_dir')

fill_mask = pipeline(
    "fill-mask",
    model=model,
    tokenizer=tokenizer
)

fill_mask(' [MASK] ka shukar pti won')

#

#