_sound_library = {}
 
 
# 播放音效(与背景音乐可同时播放，但默认只支持wav格式)
def play_sound(path):
    global _sound_library
    sound = _sound_library.get(path)
    if sound is None:
        temp = path.replace('/', os.sep).replace('\\', os.sep)
        sound = pygame.mixer.Sound(temp)
        sound.set_volume(0.1)
        _sound_library[path] = sound
    sound.play()