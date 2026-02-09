# 01_Slicing.md

## 1. 序列切片 (Slicing)
**标准格式：** `sequence[start:stop:step]`
**核心逻辑：** 左闭右开 `[start, stop)`

| 语法 | 说明 | 示例 (`a = [0, 1, 2, 3, 4]`) | 结果 |
| :--- | :--- | :--- | :--- |
| `a[1:3]` | 基础范围 | `a[1:3]` | `[1, 2]` |
| `a[:2]` | 从头开始 | `a[:2]` | `[0, 1]` |
| `a[2:]` | 取到末尾 | `a[2:]` | `[2, 3, 4]` |
| `a[-1]` | 末尾索引 | `a[-1]` | `4` |
| `a[-3:]` | 最后三个 | `a[-3:]` | `[2, 3, 4]` |
| `a[::-1]` | **序列反转** | `a[::-1]` | `[4, 3, 2, 1, 0]` |
| `a[::2]` | 步长取值 | `a[::2]` | `[0, 2, 4]` |
| `a[:]` | 浅拷贝 | `b = a[:]` | 创建新列表对象 |
# 02_Functional_Programming.md

## 2. 函数式编程与算法语法

### 2.1 列表推导式 (List Comprehension)
```python
# [expression for item in iterable if condition]
nums = [1, 2, 3, 4, 5, 6]

# 基础过滤与转换
evens_squared = [x**2 for x in nums if x % 2 == 0] # [4, 16, 36]

# 嵌套循环 (等同于双重 for 嵌套)
pairs = [(i, j) for i in range(2) for j in range(2)]
# [(0, 0), (0, 1), (1, 0), (1, 1)]
```
### 2.2Lamba表达式
```python
# lambda 参数: 表达式 (隐式返回)
f = lambda x, y: x + y
res = (lambda x: x * x)(5) # 25
```

### 2.3 高阶函数映射

| 函数 | 说明 | 示例 |
| :--- | :--- | :--- |
| `map(f, it)` | 应用 f 到每个元素 | `list(map(abs, [-1, 2]))` -> `[1, 2]` |
| `filter(f, it)` | 保留 f 为 True 的元素 | `list(filter(lambda x: x>0, [-1, 1]))` -> `[1]` |
| `zip(it1, it2)` | 并行迭代打包 | `list(zip('AB', [1, 2]))` -> `[('A',1), ('B',2)]` |
| `reduce(f, it)` | 归约计算 | `reduce(lambda x,y: x+y, [1,2,3])` -> `6` |

# 03_File_Handling.md

## 3. 文件操作 (File I/O)

### 3.1 模式对照表
| 模式 | 描述 | 注意事项 |
| :--- | :--- | :--- |
| `'r'` | 读取 (Read) | 默认模式，文件不存在报错 |
| `'w'` | 写入 (Write) | 文件存在则清空，不存在则创建 |
| `'a'` | 追加 (Append) | 在文件末尾写入 |
| `'r+'` | 读写 | 不会清空文件，可同时进行读写 |

### 3.2 核心代码模板
```python
# 推荐写法：使用 with 自动关闭文件
with open('data.txt', 'r', encoding='utf-8') as f:
    # 方式A: 一次性读取全文
    content = f.read()
    
    # 方式B: 逐行读取到列表
    lines = f.readlines()
    
    # 方式C: 迭代器读取 (处理超大文件最优)
    for line in f:
        process(line.strip()) # strip() 去除换行符

# 写入
with open('out.txt', 'w') as f:
    f.write("Text\n")
    f.writelines(["Line1\n", "Line2\n"])
```

# 04_Data_Structures.md

## 4. 高效数据结构 (Dict & Set)

### 4.1 字典 (Dictionary) - $O(1)$ 复杂度
| 方法 | 说明 |
| :--- | :--- |
| `d.get(k, default)` | 安全取值，key 不存在时不报错而是返回默认值 |
| `d.items()` | 遍历键值对 `for k, v in d.items():` |
| `d.keys() / d.values()` | 获取所有键 / 获取所有值 |
| `d.pop(k)` | 删除键 k 并返回对应的值 |
| `d.setdefault(k, v)` | key 不存在则设置默认值 v |

### 4.2 集合 (Set) - 去重与运算
* **定义**：`s = {1, 2, 3}` 或 `set(iterable)`
* **运算**：
    * 交集：`s1 & s2`
    * 并集：`s1 | s2`
    * 差集：`s1 - s2`
    * 对称差：`s1 ^ s2`


# 05_Scope_And_State.md

## 5. 作用域与状态管理 (CS61A 重点)

### 5.1 nonlocal 关键字
用于在闭包（嵌套函数）中修改外部非全局变量。
```python
def make_counter():
    count = 0
    def counter():
        nonlocal count  # 必须声明，否则 count += 1 会报 UnboundLocalError
        count += 1
        return count
    return counter
```
### 5.2关键字
在函数内部修改局部变量
```python
x = 10
def modify():
    global x
    x = 20
```
### 递归限制
Python 默认递归深度约为 1000 层。
```python
import sys
sys.setrecursionlimit(2000) # 手动提升递归深度限制
```

# 06_Builtin_Algorithms.md

## 6. 算法必备内置函数

| 函数 | 说明 | 示例 |
| :--- | :--- | :--- |
| `enumerate(it)` | 返回 `(index, value)` | `for i, v in enumerate(['a', 'b']):` |
| `sorted(it, key=f)` | 返回排序后的新列表 | `sorted(d, key=lambda x: d[x])` |
| `reversed(it)` | 返回反向迭代器 | `for x in reversed([1, 2, 3]):` |
| `all(it)` | 逻辑“与”：全部为 True 才返回 True | `all([True, True, False])` -> `False` |
| `any(it)` | 逻辑“或”：任一为 True 则返回 True | `any([0, 0, 1])` -> `True` |
| `min/max(it, key=f)` | 根据规则取最值 | `max(['a', 'abc'], key=len)` -> `'abc'` |
| `sum(it, start=0)` | 序列求和 | `sum([1, 2, 3])` -> `6` |