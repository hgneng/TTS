from tokenizers import ByteLevelBPETokenizer

# 初始化tokenizer
tokenizer = ByteLevelBPETokenizer()

# 从语料库训练
tokenizer.train(files=["jyutpings.txt"], vocab_size=5000)

# 保存vocab.json和merges.txt
tokenizer.save_model("tokenizer")
