---
title: "Rustで宣言マクロを用いてキーワード引数を実現する (Builderパターン)"
emoji: "🦀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: ["Rust"]
published: true
---

# 本記事の目標

本記事では、Builderパターンで設計された構造体のインスタンス化に、`method_chain.rs`のようなメソッドチェーンではなく、`keyword_argument.rs`のようなキーワード引数を用いる方法を説明します。

```rust:method_chain.rs
let query: ArxivQuery = ArxivQueryBuilder::new()
    .search_query("cat:cs.CL")
    .max_results(5)
    .sort_by("submittedDate")
    .build();
```

↓

```rust:keyword_argument.rs
let query: ArxivQuery = query!(
    search_query = "cat:cs.CL",
    max_results = 5,
    sort_by = "submittedDate",
);
```

# はじめに

Rustでは構造体の設計に、Builderパターン([参考](https://doc.rust-lang.org/1.0.0/style/ownership/builders.html))がよく使われます。
基本的には、Builderパターンでのインスタンス化にはメソッドチェーンが使われますが、宣言マクロを使うことで、関数にキーワード引数を渡すように構造体をインスタンス化することができます。

キーワード引数によるインスタンス化のメリットとしては、最後に`build()`メソッドを追加で呼ぶ必要がなく、コードをシンプルに書ける点が挙げられます。
また、この方法を応用することで、Rustではサポートされていない関数へのキーワード引数の受け渡しと同等の機能を、宣言マクロで実現できるかもしれません。

今回は、自作の[arXiv API](https://arxiv.org/help/api/)のラッパーライブラリを用いて説明します。
https://github.com/moisutsu/arxiv-rs

なお、基本的な宣言マクロの文法については説明しません。


# 宣言マクロによるキーワード引数の実現

arXiv APIで使うクエリを表す構造体`ArxivQuery`のビルダー`ArxivQueryBuilder`を例に説明します。

メソッドチェーンによるインスタンス化は以下のようになります。

```rust:method_chain.rs
let query: ArxivQuery = ArxivQueryBuilder::new()
    .search_query("cat:cs.CL")
    .max_results(5)
    .sort_by("submittedDate")
    .build();
```

宣言マクロでのキーワード引数を実現する際にも、内部では`ArxivQueryBuilder`を用います。

具体的な宣言マクロの定義は以下のようになります。

```rust:macro.rs
macro_rules! query {
    ( $($i:ident = $e:expr),* ) => {
        {
            let temp_query = $crate::ArxivQueryBuilder::new();
            $(
                $crate::query!(@inner, $i, $e, temp_query);
            )*
            temp_query.build()
        }
    };

    (@inner, search_query, $e:expr, $temp_query:ident) => {
        let $temp_query = $temp_query.search_query($e);
    };

    (@inner, max_results, $e:expr, $temp_query:ident) => {
        let $temp_query = $temp_query.max_results($e);
    };

    (@inner, sort_by, $e:expr, $temp_query:ident) => {
        let $temp_query = $temp_query.sort_by($e);
    };
}
```

### コードの解説

以下のパターンマッチが、メインの部分となっています。
処理の流れとしては、最初に`ArxivQueryBuilder`のインスタンスを生成します。
次に`$crate::query!(@inner, ...)`を繰り返し呼ぶことで、各キーワード引数をフィールドにセットします。
そして、最後に`build()`を呼び出して`ArxivQuery`のインスタンスを生成します。

```rust
( $($i:ident = $e:expr),* ) => {
    {
        let temp_query = $crate::ArxivQueryBuilder::new();
        $(
            $crate::query!(@inner, $i, $e, temp_query);
        )*
        temp_query.build()
    }
};
```

このメインの部分では、`$i`がフィールド名、`$e`が値にマッチして、各キーワード引数をフィールドにセットするために`$crate::query!(@inner, $i, $e, temp_query)`に渡されます。
これは以下のパターンマッチに対応しており、例えば`$i`が`search_query`の場合は一番上のパターンにマッチし、`let temp_query = temp_query.search_query($e)`に変換されます。


```rust
(@inner, search_query, $e:expr, $temp_query:ident) => {
    let $temp_query = $temp_query.search_query($e);
};

(@inner, max_results, $e:expr, $temp_query:ident) => {
    let $temp_query = $temp_query.max_results($e);
};

(@inner, sort_by, $e:expr, $temp_query:ident) => {
    let $temp_query = $temp_query.sort_by($e);
};
```

つまり、このマクロは以下のように展開されるイメージです。

```rust
let query: ArxivQuery = query!(
    search_query = "cat:cs.CL",
    max_results = 5,
    sort_by = "submittedDate",
);
```
↓

```rust
let query: ArxivQuery = {
    let temp_query = ArxivQueryBuilder::new();
    let temp_query = temp_query.search_query("cat:cs.CL");
    let temp_query = temp_query.max_results(5);
    let temp_query = temp_query.sort_by("submittedDate");
    temp_query.build()
}
```

最初に空のインスタンス`temp_query`を生成し、シャドーイングを行いながらフィールドに値をセットしていき、最後にビルドしています。

# おわりに

本記事では、Rustでキーワード引数を実現する方法の1つを紹介しました。
実用性を目指したというよりは、もしRustでキーワード引数を実現するならどうするかというので考えた方法ですが、誰かの参考になれば幸いです。
