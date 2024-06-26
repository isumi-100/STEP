まず、best-fit を実装した。
授業スライドにある best-fit の説明と、すでに実装されている first-fit のコードを元に作成した。

実装したアルゴリズムを下記に説明する。
まず、すべてのフリースロット`metadata`において、そのサイズが今欲しいサイズ以上かつ、今見つかっている`best`なサイズよりも小さい(またはまだ見つかっていない)場合は`best`であるフリースロットを今見ているフリースロット`metadata`に更新する。
上記を while 文で実装することですべてのフリースロットについて調べるが、各ループの最後に prev, metadata の更新を行うことで次のフリースロットを見れるようにしている、

while 文を抜けた後に、今回選ぶスロット`metadata`を`best`にし、prev の更新を行い空き領域から削除できるようにしている。

`metadata`がない場合の処理は first-fit から変更していない。