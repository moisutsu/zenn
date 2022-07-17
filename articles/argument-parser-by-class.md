---
title: "【Python】クラスで定義するコマンドラインパーサー"
emoji: "🐍"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: ["Python", "argparse"]
published: true
---

# はじめに

本記事では、筆者が作成した『クラスでコマンドラインパーサーを定義できるライブラリ[classopt](https://github.com/moisutsu/classopt) 』を紹介します。

https://github.com/moisutsu/classopt

このライブラリはRustの[StructOpt](https://github.com/TeXitoi/structopt)を参考に作成した、コマンドライン引数を解析するためのライブラリであり、Pythonの標準ライブラリである[argparse](https://docs.python.org/ja/3/library/argparse.html)の**変数の型が推定できない**という問題を解決しています。
変数の型を推定できるようにすることで、VSCodeなどのエディタでコーディングする際に、引数に対する補完(インテリセンス)を効かせることができます。

**argparseを使った際のコーディング**
![argparse_demo](/images/argument-parser-by-class/argparse_demo.png)

**classoptを使った際のコーディング**

![classopt_demo](/images/argument-parser-by-class/classopt_demo.png)

argparseを使った場合、解析するコマンドライン引数は動的に定義されるため、静的解析で引数名と型が解析できておらず、インテリセンスが効いていません。
一方で、classoptを使った場合、解析するコマンドライン引数はクラスで定義されており、静的解析で引数名と型がわかるため、インテリセンスを効かせることができます。

型が解析可能であるため、例えば`str`型のコマンドライン引数の場合だと、`str`のメソッドである`split`など、それぞれの型で定義されたメソッドも補完で出すことが可能です。

このように補完が効く部分を増やすことで、長い変数名を簡単に入力できるだけでなく、タイポなどのミスも減らすことができ、快適なコーディングを行なうことができるようになります。


# Install & Usage

### Install

[PyPI](https://pypi.org/)で公開しており、pipでインストールすることができます。

```bash
pip install classopt
```

### Usage

classoptでは、デコレータを活用してコマンドラインパーサーの定義を行います。

まずはシンプルな例を用いて説明を行います。
```python:demo.py
from classopt import classopt

@classopt
class Args:
    count: int
    text: str

args: Args = Args.from_args()

print(args.count)
print(args.text)
```

実行例

```bash
$ python demo.py 10 hello
10
hello
```

コマンドラインパーサーを作成するために、デコレータ`classopt`でデコレートしたクラスを定義します。
そして、このクラス内で`<引数名>: <型>`の形で解析するコマンドライン引数を定義します。
これは内部で用いている[dataclasses.dataclass](https://docs.python.org/ja/3/library/dataclasses.html)と同じ定義方法です。

また、classoptは内部で[argparse](https://docs.python.org/ja/3/library/argparse.html)を用いており、`config`関数を用いることで、[ArgumentParser.add_argument](https://docs.python.org/ja/3/library/argparse.html#argparse.ArgumentParser.add_argument)で指定することができる全てのオプションを指定することができます(オプション引数と位置引数の指定以外)。

オプション引数と位置引数の指定は、`ArgumentParser.add_argument`では、以下のように引数名の指定と同時に行います。
```python:argparse
# 位置引数
parser.add_argument("foo")

# オプション引数
parser.add_argument("-b", "--bar")
```

一方、classoptの場合は引数名はクラス定義時に指定しているので、`config`関数でオプション引数か位置引数かを指定します。
具体的には、`config`関数に`short=True`を渡すとショートオプション、`long=True`を渡すとロングオプションを引数名から自動で定義し、どちらも渡さなければ位置引数となります。
```python:classopt
@classopt
class Args:
    # 位置引数
    foo: str

    # オプション引数
    bar: str = config(long=True, short=True)
    # bar: str = config(long="--foo", short="-f") のように別名のオプション引数も指定可能
```

他にも便利な機能として、`@classopt(default_long=True, default_short=True)`のようにデコレータに`default_long=True`や`default_short=True`を渡すことで、全てのコマンドライン引数をオプション引数化することができます。

また、型として`list[型]`を与えると`nargs="*"`を自動で定義し、`bool`を与えると`action="store_true"`を自動で定義してくれます。

まとめると、classoptは以下のように使うことができます。

```python:demo.py
from classopt import classopt, config

@classopt(default_long=True, default_short=True)
class Args:
    paths: list[str] = config(help="Input paths")
    flag: bool = config(help="Input flag")

args: Args = Args.from_args()

print(args.paths)
print(args.flag)
```

実行例

```bash
$ python demo.py --paths sample/path1 sample/path2 -f
['sample/path1', 'sample/path2']
True

$ python demo.py --help
usage: demo.py [-h] [--paths [PATHS ...]] [--flag]

optional arguments:
  -h, --help            show this help message and exit
  --paths [PATHS ...], -p [PATHS ...]
                        Input paths
  --flag, -f            Input flag
```

# おわりに

本記事では、クラスで定義するコマンドラインパーサーclassoptを紹介しました。
Pythonでのコーディングを快適にできる便利なライブラリなので、是非使ってみてください。
