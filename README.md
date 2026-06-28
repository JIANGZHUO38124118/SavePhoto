# README

## 1. ソースコードの構成（フォルダ構成）

```text
PhotoCommunity
│
├── boundary/           # GUI画面（PyQt5）
│   ├── FirstForm.py
│   ├── RegisterForm.py
│   ├── LoginForm.py
│   ├── MainForm.py
│   ├── PersonalForm.py
│   ├── CommunityForm.py
│   ├── UploadForm.py
│   ├── ShowForm.py
│   └── ImagePreviewDialog.py
│
├── control/            # ビジネスロジック
│   ├── RegisterService.py
│   ├── LoginService.py
│   ├── UploadService.py
│   ├── ShowService.py
│   └── DeleteService.py
│
├── dao/                # データベースアクセス
│   ├── UserDAO.py
│   ├── PhotoDAO.py
│   └── ParameterDAO.py
│
├── entity/             # エンティティ
│   ├── User.py
│   ├── Photo.py
│   ├── Parameter.py
│   ├── Personal.py
│   ├── Community.py
│   └── PhotoVisibility.py
│
├── database/
│   ├── photo.db
│   └── init_db.py
│
├── main.py             # プログラム起動
│
└── README.md
```

本システムは **Boundary - Control - DAO - Entity** の4層構造で設計されている。

- **Boundary**：画面表示・ユーザ操作
- **Control**：業務処理
- **DAO**：SQLiteデータベースとのアクセス
- **Entity**：データモデル

---

# 2. プログラムの起動・コンパイル方法

## 動作環境

- Python 3.13.3
- SQLite3
- PyQt5

## 必要パッケージ

本プログラムは Python 仮想環境（venv）の利用を推奨する。

### ① 仮想環境の作成

```bash
python -m venv venv
```

### ② 仮想環境の有効化

**Windows（PowerShell）**

```powershell
.\venv\Scripts\Activate.ps1
```

**Windows（Command Prompt）**

```cmd
venv\Scripts\activate.bat
```

### ③ 必要パッケージのインストール

```bash
pip install PyQt5
```

または `requirements.txt` を使用する場合：

```bash
pip install -r requirements.txt
```

SQLite は Python 標準ライブラリを使用しているため、追加インストールは不要である。

---

## データベース作成

初回のみ以下を実行する。

```bash
python database/init_db.py
```

または

```bash
python main.py
```

を実行すると、必要なテーブルが自動生成される。

---

## プログラム起動

プロジェクトのルートディレクトリで以下を実行する。

```bash
python main.py
```

起動すると **First Page** が表示される。

---

## 注意事項

- 本プロジェクトには仮想環境（venv）は含まれていない。
- プログラムを実行する前に、各自の環境で仮想環境を作成し、必要パッケージをインストールすること。
- PyQt5 の実行環境によっては、プロジェクトを日本語などのマルチバイト文字を含むフォルダに配置すると、Qt プラグインの読み込みエラーが発生する場合がある。その場合は、英数字のみのフォルダ（例：`C:\Projects\PhotoCommunity`）へ移動して実行することを推奨する。

---

# 3. プログラムの操作方法（アプリの使用方法）

## ① アカウント登録

1. First Pageで **Register** をクリック
2. 以下を入力する
   - Account
   - Password
   - User Name
3. **Register** ボタンを押す

登録成功後、First Page画面へ戻る。

---

## ② ログイン

1. **Login** をクリック
2. AccountとPasswordを入力
3. **Login** を押す

認証成功後、Main Menu画面が表示される。

---

## ③ Main Menu

Main Menuでは以下の機能を利用できる。

- Personal Space
- Community
- Logout

---

## ④ Personal Space

Personal Spaceでは以下の操作が可能である。

- Upload Photo
- My Photos
- Back

---

## ⑤ 写真アップロード

「Upload Photo」をクリックする。

入力内容は以下の通り。

- 写真ファイルの選択
- Photo Name（必須）
- Upload Date（必須）
- Custom Parameters（任意）

Parameterには例えば以下のような情報を追加できる。

| Key | Value |
|------|-------|
| ISO | 400 |
| Camera | Canon EOS |
| Location | Nagasaki |
| Aperture | F2.8 |

アップロード後、写真は **Private** として保存される。

---

## ⑥ My Photos

自分がアップロードした写真を一覧表示する。

一覧画面では

- サムネイル表示
- ファイル名
- Public / Private状態

を確認できる。

写真をダブルクリックすると詳細画面が表示される。

---

## ⑦ 写真詳細画面

写真詳細画面では以下の機能を利用できる。

- 写真の拡大表示
- ファイル名表示
- パラメータ表示
- Public / Private切替
- パラメータ編集

また、

- ←キー：前の写真
- →キー：次の写真
- ESCキー：画面を閉じる

に対応している。

---

## ⑧ Community

Main Menuから **Community** を選択すると、

公開（Public）に設定された写真のみ表示される。

表示内容

- サムネイル
- 投稿者(Account)
- Like数

写真をダブルクリックすると詳細画面が表示される。

---

## ⑨ Like機能

Community画面では

- Like
- Like解除

を切り替えることができる。

Like数は自動更新される。

---

## ⑩ 写真削除

My Photosで写真を選択し、

**Delete Selected Photo**

を押す。

確認ダイアログで **Yes** を選択すると削除される。

---

## ⑪ ログアウト

Main Menuの **Logout** を押す。

確認後、First Pageへ戻る。

---

# 実装機能一覧(ユースケース対応)

## 1. アカウント作成する

- アカウント・パスワード・ユーザー名を入力して登録できる。
- 同一アカウントの重複登録を防止する。

---

## 2. ログインする

- アカウントとパスワードによる認証を行う。
- ログイン成功後、Main Menu画面へ遷移する。
- ログアウト機能を実装している。

---

## 3. 写真と情報アップロードする

- 写真ファイルをアップロードできる。
- 写真名を設定できる。
- アップロード日を登録できる。
- 任意の撮影パラメータ（ISO、Camera、Locationなど）を追加できる。
- 写真のサムネイルをプレビュー表示する。
- 登録済み写真の情報・パラメータを編集できる。
- 写真を Public / Private に切り替えられる。

---

## 4. 写真を閲覧する

- 自分がアップロードした写真を一覧表示する。
- 写真をダブルクリックすると詳細画面を表示する。
- Community画面では公開写真のみ表示する。
- 写真の拡大表示
- ← → キーによる前後写真の切り替え
- 投稿者名・Like数の表示
- Like機能

---

## 5. 写真とその情報を削除する

- 写真および関連する情報（パラメータ）を削除できる。
- 削除前に確認ダイアログを表示する。