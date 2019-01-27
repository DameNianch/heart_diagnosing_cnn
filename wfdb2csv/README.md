wfdb2csv
====

Overview
ECGデータをcsvに変換することができます。
データの一定時間分割も可能です。

## Description
- DL_checker.sh: データのディレクトリダウンロードが成功しているのか簡易的な確認をすることができます。
- head_collect.sh: ヘッダーデータ（病名、性別、年齢等）をcsvに変換します。
- kuhaku_del.sh: データにスペースを消します。（クリーニング）
- wfdb2csv.sh: wfdb形式のデータをcsv形式に変換します。
- splitter.go: csv形式のデータを特定の時間窓として取り出し、スライドによるaugmentをして分割をします。
- data_maker.sh: splitter.goに従いデータをスプリットし、病名毎にワンホットベクトルを割当てます。

## Demo

## VS. 

## Requirement

## Usage

## Install

## Contribution

## Licence

## Author

##すごいひとたち紹介
https://www.ahajournals.org/doi/full/10.1161/01.cir.101.23.e215
