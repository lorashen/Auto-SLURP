# Auto-SLURP: A Benchmark Dataset for Evaluating Multi-Agent Frameworks in Smart Personal Assistant

Official repository for the paper [Auto-SLURP: A Benchmark Dataset for Evaluating Multi-Agent Frameworks in Smart Personal Assistant](https://arxiv.org/abs/2504.18373)

## 1. start simulated servers
```
cd server
sh run.sh
```
## 2. run the test
Some external servers require API keys. Therefore, to test and send requests to these servers, please make sure to provide the necessary API keys first.

The LLM used in the example code also requires configuration. Please make sure to specify the model name and provide the corresponding API key.

Please also remember to put the data files into ~/data. Or you can modify the data path in test.py.
```
cd examples/autogen
sh run.sh
```
## 3. run evaluation
We are using gpt-4 for evaluating. Please set apikey properly. For e.g., export OPENAI_API_KEY="***".

If you want to use other models, please modify eval.py.
```
sh eval.sh
```

## Citing

If you found the data or code useful, free to cite:
```bibtex
@misc{shen2025autoslurpbenchmarkdatasetevaluating,
      title={Auto-SLURP: A Benchmark Dataset for Evaluating Multi-Agent Frameworks in Smart Personal Assistant}, 
      author={Lei Shen and Xiaoyu Shen},
      year={2025},
      eprint={2504.18373},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2504.18373}, 
}
```
