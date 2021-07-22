---
title: "GPUベースのターミナルKittyをmacOS用に使いやすく設定する"
emoji: "😺"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: ["kitty", "terminal", "macOS"]
published: true
---

# はじめに

[kitty](https://github.com/kovidgoyal/kitty)は高速に動き、機能が豊富で、クロスプラットフォームに対応しているGPUベースのターミナルエミュレーターです。
非常に動作が軽く、Zoomなどの重いアプリが起動していてiTerm2ではもっさりする場合でもKittyなら軽快に動作します。
また同じGPUベースのターミナルエミュレーターとして[Alacritty](https://github.com/alacritty/alacritty)がありますが、日本語IME関連のバグ(もうすぐ解消されそうな気配がありますが)があったり、ターミナルレベルの画面分割やタブに対応していないなどの問題点があり、Kittyはこれらの点を解決しています。
本記事では、このKittyをmacOSで使いやすく設定する方法を紹介します。

この記事を読むと以下の設定を行うことができます。
- iTerm2のようにホットキー(ショートカット)で全画面ターミナルを表示/非表示
- ターミナルを透過
- `cmd+d`で画面分割、`cmd+t`で新規タブ、`cmd+w`でWindowを閉じる
- Icebergインスパイアの美しいカラーテーマ

![kitty-with-hotkey](https://storage.googleapis.com/zenn-user-upload/dee7c7116a16d5e2582188bb.gif)

# クイックスタート

とりあえず設定したいという方は、以下で設定することができます。

kittyをインストール
```bash
brew install --cask kitty
```

ホットキーでターミナルを表示/非表示するために利用する、Hammerspoonをインストール
```bash
brew install --cask hammerspoon
```

Kittyの設定ファイル`~/.config/kitty/kitty.conf`と`~/.config/kitty/macos-launch-services-cmdline`を作成

``` python:kitty.conf
font_size 13.5

cursor #c7c7c7
cursor_text_color #FEFFFF

foreground #D1D2D3
background #16171E

#: black
color0 #000000
color8 #676767

#: red
color1 #E68E8E
color9 #FF6D67

#: green
color2  #83AC8E
color10 #5FF967

#: yellow
color3  #F5B78A
color11 #FEFB67

#: blue
color4  #9BB8DC
color12 #6871FF

#: magenta
color5  #BAACE2
color13 #FF76FF

#: cyan
color6  #00C5C7
color14 #5FFDFF

#: white
color7  #C7C7C7
color15 #FEFFFF

background_opacity 0.8

scrollback_lines 10000

enabled_layouts Grid

tab_bar_edge top
tab_bar_style powerline
tab_powerline_style angled
tab_title_template " {index}: {'{: <501}'.format(title)}"

kitty_mod cmd
map kitty_mod+d new_window_with_cwd
map kitty_mod+t new_tab_with_cwd
map kitty_mod+w close_window

macos_option_as_alt yes
macos_quit_when_last_window_closed yes
macos_traditional_fullscreen yes
```


```bash:macos-launch-services-cmdline
--start-as=fullscreen
```


もしくは、[kitty.conf](https://github.com/moisutsu/dotfiles/blob/main/kitty/kitty.conf)と[macos-launch-services-cmdline](https://github.com/moisutsu/dotfiles/blob/main/kitty/macos-launch-services-cmdline)

Hammerspoonの設定ファイル`~/.hammerspoon/init.lua`を作成
```lua:init.lua
hs.hotkey.bind({"ctrl"}, "t", function()
    local kitty = hs.application.get("kitty")
    if kitty == nil then
        hs.application.launchOrFocus("/Applications/kitty.app")
    elseif kitty:isFrontmost() then
        kitty:hide()
    else
        hs.application.launchOrFocus("/Applications/kitty.app")
    end
end)
```

もしくは、[init.lua](https://github.com/moisutsu/dotfiles/blob/main/.hammerspoon/init.lua)

この後、Hammerspoonの設定を再読み込みする必要があるかもしれません。(GUIのアプリから行うことができます)

以上で設定は終了で、`ctrl+t`でターミナルの表示/非表示、`cmd+d`で画面分割、`cmd+t`で新規タブ作成、`cmd+w`でWindowの終了を行うことができます。

# Kittyの設定

ここではKittyの設定について詳しく見ていきます。

## インストール

KittyはHomebrewのcaskでインストールすることができます。

```bash
brew install --cask kitty
```

## 設定ファイル

基本的に設定ファイルについてはすべて[こちら](https://sw.kovidgoyal.net/kitty/conf/)に記載されています。

まず`~/.config/kitty/kitty.conf`を作成します。既にデフォルトで生成された設定ファイルがあるかもしれません。

次に設定する項目について一つずつ見ていきます。

### フォントサイズ

フォントサイズを設定します。

```
font_size 13.5
```

### カラーテーマ
Icebergインスパイアのカラーテーマを設定します。

```
cursor #c7c7c7
cursor_text_color #FEFFFF

foreground #D1D2D3
background #16171E

#: black
color0 #000000
color8 #676767

#: red
color1 #E68E8E
color9 #FF6D67

#: green
color2  #83AC8E
color10 #5FF967

#: yellow
color3  #F5B78A
color11 #FEFB67

#: blue
color4  #9BB8DC
color12 #6871FF

#: magenta
color5  #BAACE2
color13 #FF76FF

#: cyan
color6  #00C5C7
color14 #5FFDFF

#: white
color7  #C7C7C7
color15 #FEFFFF
```

### 画面の透過
画面の透過率を設定します。
```
background_opacity 0.8
```

### スクロールバックサイズ
スクロールバックサイズを設定します。
```
scrollback_lines 10000
```

### 画面分割
画面分割方法を設定します。
Kittyは画面分割方法が特殊で、ユーザーが縦分割や横分割を指定するのではなく、ユーザーが画面分割をするたびに、アプリ側が設定に沿って縦分割か横分割かを自動で判断します。
本記事では、筆者が最も直感的にだった分割方法を採用していますが、もし使いづらい場合は[こちら](https://sw.kovidgoyal.net/kitty/overview/#layouts)に全ての分割方法が記載されています。
```
enabled_layouts Grid
```

### タブ
タブの見た目を設定します。
```
tab_bar_edge top
tab_bar_style powerline
tab_powerline_style angled
tab_title_template " {index}: {'{: <501}'.format(title)}"
```
Kittyではタブの横幅が、タブの内容によってインタラクティブに変化します。
つまり、コマンドを実行したりディレクトリを移動するたびに、タブの横幅が変化してしまうということであり、これがかなり気になってしまいました。
これを解決するため、タブの内容のテンプレートを設定する`tab_title_template`で右に空白を表示することで、常にタブの横幅が最大になるように設定しました。
もしタブの横幅の変化が気にならないなら、`tab_title_template " {index}: {title}"`と設定することで、より表示をシンプルにすることができます。

### ショートカット
ショートカットを設定します。
```
kitty_mod cmd
map kitty_mod+d new_window_with_cwd
map kitty_mod+t new_tab_with_cwd
map kitty_mod+w close_window
```
上記の設定では、新しいWindow(分割)やタブを生成するときに、元のディレクトリを引き継ぐようになっています。
もしこの設定が不要ならば`new_window_with_cwd`、`new_tab_with_cwd`の代わりに`new_window`、`new_tab`を使うことができます。

### macOS固有の設定
macOS向けの設定を行います。
```
macos_option_as_alt yes
macos_quit_when_last_window_closed yes
macos_traditional_fullscreen yes
```
`macos_traditional_fullscreen`は必須ですが、`macos_option_as_alt`(optionをaltとして扱う)と`macos_quit_when_last_window_closed`(最後のシェルが終了したときにKittyも終了する)は任意です。

最後に以下の内容の設定ファイル`~/.config/kitty/macos-launch-services-cmdline`を作成します。
```bash:macos-launch-services-cmdline
--start-as=fullscreen
```

# Hammerspoonの設定

[Hammerspoon](https://github.com/Hammerspoon/hammerspoon)はmacOSで自動化を行うためのツールであり、本記事ではKittyをホットキーで表示/非表示するために利用します。

## インストール

HammerspoonはHomebrewのcaskでインストールすることができます。

```bash
brew install --cask hammerspoon
```

## 設定ファイル

Hammerspoonの設定ファイル`~/.hammerspoon/init.lua`を作成します。
`ctrl+t`でKittyを表示/非表示します。

```lua: init.lua
hs.hotkey.bind({"ctrl"}, "t", function()
    local kitty = hs.application.get("kitty")
    if kitty == nil then
        hs.application.launchOrFocus("/Applications/kitty.app")
    elseif kitty:isFrontmost() then
        kitty:hide()
    else
        hs.application.launchOrFocus("/Applications/kitty.app")
    end
end)
```
この関数ではKittyのプロセスを取得し、最前面にあるなら非表示にし、それ以外なら最前面に表示します。
また、`hs.hotkey.bind`の第1引数、第2引数を変更することでホットキーを変更することができます。

設定ファイルを作成した後に、設定を再読み込みする必要がある可能性があります。
これはHammerspoonのアプリアイコンをクリックすることで起動できるHammerspoon Consoleの右上の`Reload config`から行うことができます。


# おわりに

本記事では、GPUベースのターミナルKittyをmacOS用に使いやすく設定する方法を紹介しました。
Kittyは画像を表示することができるなど、他にも様々な機能があるので是非[ホームページ](https://sw.kovidgoyal.net/kitty/)で確認してみてください。
