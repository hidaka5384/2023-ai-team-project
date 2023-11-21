import glob
import os

# 変換したいID
CHANGE_ID = "1"
TRAIN_DATA_PATH = (
    "/Users/ritsushi/Desktop/Python/2022-AI-TeamProject/test/train/*.jpg"
)
VAL_DATA_PATH = (
    "/Users/ritsushi/Desktop/Python/2022-AI-TeamProject/test/val/*.jpg"
)
WRITE_TRAIN_TXT_PATH = "./train.txt"
WRITE_VAL_TXT_PATH = "./val.txt"
# .txtファイルがあるパス
TXT_PATH = (
    "/Users/ritsushi/Desktop/Python/2022-AI-TeamProject/test/train/*.txt"
)


class YoloUtils:
    def __init__(
        self,
        label_id: str,
        train_data_path: str,
        val_data_path: str,
        write_train_txt_path: str,
        write_val_txt_path: str,
        txt_path: str,
    ) -> None:
        self._id = label_id
        self._train_data_path = train_data_path
        self._val_data_path = val_data_path
        self._write_train_txt_path = write_train_txt_path
        self._write_val_txt_path = write_val_txt_path
        self._txt_path = txt_path

    # NOTE: idが2桁以上だと上手く動作しない
    def change_id(self) -> None:
        """
        idを任意の数字に変える
        """

        for file_name in glob.glob(self._txt_path):
            print(f"ファイル名: {file_name}")
            with open(file_name) as f:
                id_list = []
                for line in f:
                    # split_list = line.split()
                    # nwe_list = ['1' if i == "0" else i for i in split_list]
                    # new_word = " ".join(nwe_list)
                    # list.append(f'{new_word}\n')

                    str_id = f"{self._id}{line[1:]}"
                    id_list.append(str_id)

                # 上書き保存
                # with open(file_name, mode="w", encoding="cp932") as f:
                with open(file_name, mode="w") as f:
                    id_list.append("\n")
                    f.writelines(id_list)

        print(f"ラベルIDを{self._id}に変換しました。")

    def remove_space(self) -> None:
        """
        ファイル名の空白を削除
        """

        for file_name in glob.glob(self._txt_path):
            new_file_name = file_name.replace(" ", "")
            os.rename(file_name, new_file_name)
            print(f"ファイル名を{file_name} -> {new_file_name}に変換しました。")

        print("ファイル名の変換処理が終わりました。")

    def add_blank(self) -> None:
        """
        ファイルの最後に空白を追加
        """
        for file_name in glob.glob(self._txt_path):
            with open(file_name, mode="a") as f:
                f.write("\n")

    def make_path_list(self) -> None:
        """
        学習データのパスが格納されたtrain.txtと検証データのパスが格納されたval.txtを作成する関数
        """
        write_txt_path_list = [
            self._write_train_txt_path,
            self._write_val_txt_path,
        ]
        data_path_list = [self._train_data_path, self._val_data_path]

        for txt_path, data_path in zip(write_txt_path_list, data_path_list):
            data_paths = glob.glob(data_path)
            txt_file = open(txt_path, "w")
            for data_path in data_paths:
                txt_file.write("." + data_path + "\n")

            txt_file.close()


if __name__ == "__main__":
    yolo_utils = YoloUtils(
        CHANGE_ID,
        TRAIN_DATA_PATH,
        VAL_DATA_PATH,
        WRITE_TRAIN_TXT_PATH,
        WRITE_VAL_TXT_PATH,
        TXT_PATH,
    )
    yolo_utils.change_id()
    yolo_utils.remove_space()
    yolo_utils.add_blank()
    yolo_utils.make_path_list()
