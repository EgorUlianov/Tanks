всякие звуки танка нам оно не надо
sndShot = pygame.mixer.Sound('sounds/shot.wav')
sndDestroy = pygame.mixer.Sound('sounds/destroy.wav')
sndDead = pygame.mixer.Sound('sounds/dead.wav')
sndLive = pygame.mixer.Sound('sounds/live.wav')
sndStar = pygame.mixer.Sound('sounds/star.wav')
sndEngine = pygame.mixer.Sound('sounds/engine.wav')
sndEngine.set_volume(0.5)
sndMove = pygame.mixer.Sound('sounds/move.wav')
sndMove.set_volume(0.5)
начало уровня
pygame.mixer.music.load('sounds/level_start.mp3')
pygame.mixer.music.play()

конец уровня
pygame.mixer.music.load('sounds/level_finish.mp3')
        pygame.mixer.music.play()
