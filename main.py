from module.search_music import find_music_info

title_query = input("请输入乐曲名:")
results = find_music_info(title_query)
for result in results:
    print(result)
