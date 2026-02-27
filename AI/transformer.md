# 1.NLP和LLM

NLP(**natural language processing**)是一个专注于理解与人类语言相关的一切的语言学和机器学习领域。NLP任务的目标不仅是理解单个单词，更在于能够理解这些单词的语境。

例如：
1.整句分类：获取评论的情感，判断邮件是否为垃圾邮件，判断句子语法正确，或两句是否逻辑相关
2.对句子中的每个词进行分类：识别句子的语法成分（名词、动词、形容词），或命名的实体（人称、地点、组织）
3.生成文本内容：用自动生成文本完成提示，用遮罩词填补文本中的空白
4.从文本中提取答案：给定一个问题和上下文，基于上下文中提供的信息提取问题的答案
5.从输入文本生成新句子：将文本翻译成另一种语言，摘要文本

但是，随着LLM **(large language model)**的崛起，NLP领域被彻底改变了

这些模型包括GPT（生成预训练变换器）和Llama等架构，彻底改变了语言处理的可能性。

大型语言模型（LLM）是一种基于大量文本数据训练的人工智能模型，能够理解并生成类人类文本，识别语言模式，并执行多种语言任务，无需特定任务训练。它们代表了自然语言处理（NLP）领域的重大进展。

LLM的特点包括：

规模：它们包含数百万、数十亿甚至数千亿个参数
一般能力：他们可以在没有特定任务培训的情况下完成多项任务
情境学习：他们可以从提示中提供的例子中学习
涌现能力：随着这些模型规模的扩大，它们展示了一些未被明确编程或预料到的能力
LLM的出现使得模式从为特定NLP任务构建专门模型，转变为使用一个大型的单一模型，可以被提示或微调以应对广泛的语言任务。这使得复杂的语言处理变得更加可及，同时也带来了效率、伦理和部署等新挑战。

然而，LLMs也存在重要局限性：

幻觉(**hallucinations**)：它们可以自信地产生错误信息
缺乏真正理解：他们缺乏对世界的真正理解，完全依赖统计模式
偏见：它们可能重现训练数据或输入中的偏见。
上下文窗口：它们的上下文窗口有限（虽然正在改善）
计算资源：它们需要大量计算资源
**所以，解决上面这一些问题，成了人工智能研究的重要课题**

为什么语言处理具有挑战性？
计算机处理信息的方式与人类不同。例如，当我们读到句子“我饿了”时，很容易理解它的含义。同样，给定两句话如“我饿了”和“我很难过”，我们可以轻松判断它们有多相似。对于机器学习（ML）模型，这类任务更为困难。文本需要以一种能够让模型学习的方式处理。而且因为语言很复杂，我们需要认真思考如何进行这种处理。关于如何表示文本已经有大量研究，我们将在下一章中介绍一些方法。

即使LLM技术取得了进步，许多根本性的挑战依然存在。这些包括理解歧义、文化背景、讽刺和幽默。LLM通过对多样化数据集的大规模训练来应对这些挑战，但在许多复杂场景下仍常常无法达到人类层面的理解水平。

# 2.introduce to transformer

## 1.pipeline
transformer library中🤗最基本的对象是函数。它将模型与必要的预处理(pre-processing)和后处理步骤连接起来，使我们能够直接输入任何文本并获得可理解的答案：pipeline()

```python
from transformers import pipeline

classifier = pipeline("sentiment-analysis")
classifier("I've been waiting for a HuggingFace course my whole life.")
```
```python
[{'label': 'POSITIVE', 'score': 0.9598047137260437}]
我们甚至可以传几句话！
```
```python
classifier(
    ["I've been waiting for a HuggingFace course my whole life.", "I hate this so much!"]
)
[{'label': 'POSITIVE', 'score': 0.9598047137260437},
 {'label': 'NEGATIVE', 'score': 0.9994558095932007}]
```
默认情况下，该流水线会选择一个经过英语情感分析微调的预训练模型。模型在创建对象时会被下载并缓存。如果你重新运行该命令，缓存中的模型会被使用，无需重新下载模型。classifier

当你将文本传递到管道时，主要涉及三个步骤：

1.文本经过预处理，成为模型能理解的格式。
2.预处理的输入会传递给模型。
3.模型的预测是后期处理的，所以你可以理解它们。

## 2.不同模态的pipeline

该函数支持多种模态，允许你处理文本、图像、音频，甚至多模态任务。本课程将重点介绍文本任务，但理解变换器架构的潜力也很有帮助，因此以下是pipeline的简要介绍。
### 文本管道
- text-generation：从提示词生成文本
- text-classification：将文本分类到预定义的类别
- summarization：在保留关键信息的前提下创建简短文本
- translation：将文本从一种语言翻译到另一种
- zero-shot-classification：未经特定标签培训即可对文本进行分类
- feature-extraction： 提取文本的向量表示
### 图像管道
- image-to-text生成图像的文本描述
- image-classification：识别图像中的物体
- object-detection：在图像中定位并识别物体
### 音频流水线
- automatic-speech-recognition：将语音转换为文本
- audio-classification：将音频分类
- text-to-speech：将文本转换为语音
### 多模态管道
- image-text-to-text：根据文本提示回复图片

## 3.零发分级(zero-shot-classification)
我们将从一个更具挑战性的任务开始，需要对尚未标注的文本进行分类。这在现实项目中很常见，因为注释文本通常耗时且需要领域专业知识。在这个用例中，流水线非常强大：它允许你指定分类时使用哪些标签，这样你就不必依赖预训练模型的标签。你已经看到模型如何用这两个标签将句子分类为正面或否定——但它也可以用你喜欢的其他一组标签来分类文本。

```python
from transformers import pipeline

classifier = pipeline("zero-shot-classification")
classifier(
    "This is a course about the Transformers library",
    candidate_labels=["education", "politics", "business"],
)

{'sequence': 'This is a course about the Transformers library',
 'labels': ['education', 'business', 'politics'],
 'scores': [0.8445963859558105, 0.111976258456707, 0.043427448719739914]}
 ```
这种流程被称为零样本，因为你不需要微调数据模型来使用它。它可以直接返回你想要的任何标签列表的概率分数！

    下面记录和GPT的mindstorm：
    1.零样本存在精度低的问题，因为他不经过训练直接适应新环境
    2.零样本这种强适应性的特点也成为了它的优点
    3.零样本需要底层模型有强大的逻辑能力和推理能力，这对模型的训练提出了新的要求
    4.如何无中生有的得出标记？基于我们已经提供的语料库，采用训练过的大模型进行相似度分析

## 4.NER 命名实体识别(Named entity recognition)

```python
from transformers import pipeline

ner = pipeline("ner", grouped_entities=True)
ner("My name is Sylvain and I work at Hugging Face in Brooklyn.")
[{'entity_group': 'PER', 'score': 0.99816, 'word': 'Sylvain', 'start': 11, 'end': 18}, 
 {'entity_group': 'ORG', 'score': 0.97960, 'word': 'Hugging Face', 'start': 33, 'end': 45}, 
 {'entity_group': 'LOC', 'score': 0.99321, 'word': 'Brooklyn', 'start': 49, 'end': 57}
]
```
和GPT的mindstorm:
    命名实体识别（NER，Named Entity Recognition） 是自然语言处理（NLP）中的一种关键任务，旨在识别文本中具有特定意义的实体，如人名、地点、组织机构、时间、日期等。NER 是信息抽取（Information Extraction）的一部分，广泛应用于搜索引擎、机器翻译、问答系统、自动摘要等领域。
    1. NER的目标
    NER 的目标是将输入文本中所有的“命名实体”标记出来，并进行分类（如人名、地点名、组织名等）
    2. NER 的常见实现方法
    NER 的实现方法经历了几个阶段，传统方法通常依赖于规则或统计模型，而现代方法多采用基于深度学习的神经网络模型，特别是 基于 Transformer 的预训练模型。下面介绍常见的实现方法：
    2.3 基于深度学习的NER方法
    随着深度学习的兴起，基于神经网络的 NER 方法逐渐成为主流，尤其是基于 循环神经网络（RNN） 和 卷积神经网络（CNN） 的方法。常见的深度学习方法有：
    LSTM-CRF（长短时记忆-条件随机场）：结合 LSTM 和 CRF 的优势，LSTM 用于处理序列数据的上下文信息，CRF 用于建模标签之间的依赖关系，从而提高 NER 的准确性。
    BiLSTM-CRF：在 LSTM 的基础上引入双向（BiLSTM）网络，同时考虑文本中的前后信息，进一步提高了模型的表达能力。
    2.4 基于Transformer的NER方法（目前主流）
    当前，基于 Transformer 架构的模型在 NER 中表现出色，特别是 BERT（Bidirectional Encoder Representations from Transformers） 和其变种（如 RoBERTa、DistilBERT 等）被广泛应用于 NER 任务。
    Transformer 模型的优势在于：
    它能够同时捕捉文本中上下文的依赖关系，特别是 BERT 是双向的，能同时关注一个词的前后上下文。
    通过大规模预训练，在多种NLP任务上进行迁移学习，模型能够学习到丰富的语义信息。