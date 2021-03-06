# RGBants
這是一款簡易地模擬三種螞蟻生命的程式，一共分為紅、藍、綠三種顏色的螞蟻，依照各自不同的行為準則，讓使用者觀察其生存機率。
本作品的特色除了各自不同的行為準則，更加入了以螞蟻顏色代表其壽命、螞蟻走過的地方會留下只有同族才能進入的費洛蒙路線等創意，這些因素，皆會影響螞蟻生存的結果。

### 規則：食物會固定時間隨機出現於視窗座標位置，螞蟻離開蟻巢後壽命內必須吃掉食物，否則會死亡，若吃掉食物則必須在壽命時間內會返回巢穴，返回成功後巢穴會再多生一隻螞蟻。
以下為簡單的三種螞蟻行為準則：
紅：每隻螞蟻會找尋離自己最近的食物，也就是同族間也會相互競爭。
藍：每隻螞蟻會找尋最近的食物，但若是該食物已經被壽命較短的老螞蟻鎖定，則自動尋找次近目標食物。
綠：比較紅、藍螞蟻吃掉的食物數量，自動依照吃掉食物較多的那一方為行為準則。

### 觀察結果：
紅、藍螞蟻的生存機率，據多次觀察下來，藍螞蟻的生存率較高，但三種螞蟻生存機率最為低下的為綠螞蟻，這並非主要是受到行為準則影響，而是巢穴位置的影響，而造成這種影響的主要是因為費洛蒙非同族不得進的這項設定。綠螞蟻的巢穴位置在左上，勢必會受到紅螞蟻跟藍螞蟻的夾攻。而紅螞蟻跟藍螞蟻皆有右下方為可拓展的鄰方，因此受巢穴位置影響較不多，所以紅藍螞蟻之間唯一可以比較的就是會不會同族競爭的差異了。
