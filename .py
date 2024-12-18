import os
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt

# 指定 wav 文件名
filename = "MusiqueBruit.wav"

# 当前目录路径
directory = os.getcwd()

# 拼接完整路径
file_path = os.path.join(directory, filename)

# 初始化变量
audio_signal = None
Fs = None

# 检查文件是否存在并读取数据
if os.path.isfile(file_path):
    Fs, data = wavfile.read(file_path)
    
    # 只有在直接运行 A-E.py 文件时才会打印信息
    if __name__ == "__main__":
        print("Frequence d’échantillonnage: {} Hz".format(Fs))
        print("Nombre d’échantillons: {}".format(data.shape[0]))
        print("Codage des amplitudes en: {}".format(data.dtype))
    
    # 推断幅值范围
    dtype_info = {
        'int16': (-2**15, 2**15 - 1),
        'int32': (-2**31, 2**31 - 1),
        'uint8': (0, 2**8 - 1)
    }
    
    if data.dtype.name in dtype_info:
        theoretical_min, theoretical_max = dtype_info[data.dtype.name]
        if __name__ == "__main__":
            print("Théorique amplitude range: [{} à {}]".format(theoretical_min, theoretical_max))
    else:
        if __name__ == "__main__":
            print("Type de codage inconnu. Impossible de déduire la plage théorique des amplitudes.")
    
    # 实际计算最小值和最大值
    actual_min = data.min()
    actual_max = data.max()
    if __name__ == "__main__":
        print("Amplitude réelle: min = {}, max = {}".format(actual_min, actual_max))
    
    # 归一化处理
    data = data.astype(np.float32)  # 转换为浮点数进行归一化
    audio_signal = (data - actual_min) / (actual_max - actual_min) * 2 - 1  # 归一化到 [-1, 1]
    
    # 如果数据是多通道（例如立体声），选择一个通道进行绘制
    if len(audio_signal.shape) > 1:
        audio_signal = audio_signal[:, 0]  # 选择左通道或第一个通道

# 只有在直接运行 A-E.py 文件时才会绘制图像
if __name__ == "__main__":
    # 创建时间轴
    time = np.linspace(0, len(audio_signal) / Fs, num=len(audio_signal))
    
    # 绘制信号波形
    plt.figure(figsize=(10, 6))
    plt.plot(time, audio_signal, label="Audio Signal")
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.title("Waveform of the Audio Signal")
    plt.legend()
    plt.show()
