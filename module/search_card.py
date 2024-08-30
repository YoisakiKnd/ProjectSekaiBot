from PIL import Image, ImageDraw, ImageFont
import json
import re
import fuzzywuzzy


# 加载卡片数据
def load_card_data(file_path='cards.json'):
    with open(file_path, encoding="utf-8") as f:
        card_data = json.load(f)
    return card_data

# 根据 characterId 查找所有相关的 assetbundleName
def find_assetbundle_names(character_id, file_path='cards.json'):
    card_data = load_card_data(file_path)
    assetbundle_names = []
    
    # 遍历每个条目，查找匹配的 characterId
    for entry in card_data:
        if entry.get('characterId') == character_id:
            assetbundle_name = entry.get('assetbundleName')
            if assetbundle_name:
                assetbundle_names.append(assetbundle_name)
    
    if assetbundle_names:
        return assetbundle_names
    else:
        return ['没有找到匹配的 characterId']

# 主函数
def main():
    try:
        character_id = int(input("请输入 characterId: "))
        assetbundle_names = find_assetbundle_names(character_id)
        if assetbundle_names:
            print(f"assetbundleNames: {', '.join(assetbundle_names)}")
        else:
            print("没有找到匹配的 assetbundleName")
    except ValueError:
        print("请输入有效的数字 characterId")

# 运行主函数
if __name__ == "__main__":
    main()