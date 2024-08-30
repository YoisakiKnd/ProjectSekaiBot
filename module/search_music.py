import json
import re
from fuzzywuzzy import fuzz

# 加载音乐数据
def load_data(musics_file='musics.json', difficulties_file='musicDifficulties.json'):
    with open(musics_file, encoding="utf-8") as f:
        musics_data = json.load(f)

    with open(difficulties_file, encoding="utf-8") as f:
        difficulties_data = json.load(f)

    return musics_data, difficulties_data

# 创建音乐ID到标题的映射
def create_mappings(musics_data):
    id_to_music = {entry['id']: entry for entry in musics_data}
    return id_to_music

# 创建音乐难度信息映射
def create_difficulty_mapping(difficulties_data):
    music_difficulties_by_id = {}
    for entry in difficulties_data:
        music_id = entry['musicId']
        if music_id not in music_difficulties_by_id:
            music_difficulties_by_id[music_id] = []
        music_difficulties_by_id[music_id].append({
            'id': entry['id'],
            'difficulty': entry['musicDifficulty'],
            'playLevel': entry['playLevel']
        })
    return music_difficulties_by_id

# 查找最佳匹配标题
def find_best_match(title_query, titles):
    best_match = None
    highest_score = 0
    for title in titles:
        score = fuzz.partial_ratio(title_query, title)
        if score > highest_score:
            highest_score = score
            best_match = title
    return best_match, highest_score

# 查找音乐信息
def find_music_info(title_query, musics_file='musics.json', difficulties_file='musicDifficulties.json'):
    # 加载数据
    musics_data, difficulties_data = load_data(musics_file, difficulties_file)
    
    # 创建映射
    id_to_music = create_mappings(musics_data)
    music_difficulties_by_id = create_difficulty_mapping(difficulties_data)
    
    # 获取所有标题
    titles = [entry['title'] for entry in musics_data]
    
    # 获取最佳匹配的标题
    best_match_title, score = find_best_match(title_query, titles)
    
    results = []
    
    if best_match_title:
        # 找到与最佳匹配标题相关的 musicId
        music_id = None
        for entry in musics_data:
            if entry['title'] == best_match_title:
                music_id = entry['id']
                break

        if music_id is not None:
            # 查找与 musicId 相关的所有难度信息
            difficulties = music_difficulties_by_id.get(music_id, [])
            
            if difficulties:
                result = f"\n乐曲：{best_match_title}"
                for entry in difficulties:
                    result += f"\n难度 ：{entry['difficulty']}, 等级: {entry['playLevel']}"
                results.append(result)
            else:
                results.append(f"没有找到 musicId 为 {music_id} 的难度信息。")
    else:
        results.append(f"没有找到匹配标题包含 '{title_query}' 的歌曲。")
    
    return results

# 如果需要运行测试，可以在此调用
if __name__ == "__main__":
    title_query = input("请输入要查找的标题（模糊匹配）:")
    results = find_music_info(title_query)
    for result in results:
        print(result)
