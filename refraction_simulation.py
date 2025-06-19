import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from math import sin, asin, radians, degrees, tan, cos

# 設置自訂字型以支援中文
font_path = "font.otf"  # 字型檔案位於根目錄
custom_font = FontProperties(fname=font_path)

# 設置 Streamlit 頁面
st.title("光線折射模擬")
st.write("調整入射角和介質折射率，觀察光線路徑變化")

# 側邊欄輸入（改為中文）
st.sidebar.header("參數設置")
incident_angle = st.sidebar.slider("入射角 (度)", 0, 90, 45)
n1 = st.sidebar.slider("介質1折射率 (n1)", 1.0, 3.0, 1.0, step=0.1)
n2 = st.sidebar.slider("介質2折射率 (n2)", 1.0, 3.0, 1.5, step=0.1)

# 計算折射角 (斯涅爾定律: n1 * sin(θ1) = n2 * sin(θ2))
theta1 = radians(incident_angle)
sin_theta2 = n1 * sin(theta1) / n2

# 檢查是否發生全反射
if sin_theta2 > 1:
    st.warning("發生全反射！折射角不存在。")
    theta2 = None
else:
    theta2 = asin(sin_theta2)
    st.write(f"折射角: {degrees(theta2):.2f} 度")

# 繪製光線路徑
fig, ax = plt.subplots(figsize=(8, 6))

# 設置坐標軸，確保原點 (0, 0) 在圖表中心
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_aspect('equal')
ax.grid(True)

# 繪製介質分界面 (y=0)
ax.axhline(0, color='black', linestyle='--')

# 入射光線：從左上方 (x<0, y>0) 射向原點 (0, 0)
x_start = -1.0
y_start = tan(radians(90 - incident_angle)) * abs(x_start)
x_incident = np.array([x_start, 0.0])
y_incident = np.array([y_start, 0.0])
ax.plot(x_incident, y_incident, 'b-', label='入射光線')

# 繪製法線（在原點，沿 y 軸）
ax.plot([0, 0], [-1.5, 1.5], 'k:', label='法線')

# 折射光線：從原點 (0, 0) 射向右下方 (x>0, y<0)
if theta2 is not None:
    x_end = 1.0
    y_end = -tan(radians(90 - degrees(theta2))) * x_end
    x_refracted = np.array([0.0, x_end])
    y_refracted = np.array([0.0, y_end])
    ax.plot(x_refracted, y_refracted, 'r-', label='折射光線')
else:
    x_end = -1.0
    y_end = tan(radians(90 - incident_angle)) * abs(x_end)
    x_reflected = np.array([0.0, x_end])
    y_reflected = np.array([0.0, y_end])
    ax.plot(x_reflected, y_reflected, 'g-', label='反射光線')

# 添加標籤和圖例，使用自訂字型顯示中文
ax.text(-1.4, 1, f'介質1 (n1 = {n1})', fontsize=12, fontproperties=custom_font)
ax.text(-1.4, -1, f'介質2 (n2 = {n2})', fontsize=12, fontproperties=custom_font)
ax.legend(prop=custom_font)
ax.set_xlabel('X 軸', fontproperties=custom_font)
ax.set_ylabel('Y 軸', fontproperties=custom_font)
ax.set_title('光線折射模擬', fontproperties=custom_font)

# 顯示圖表
st.pyplot(fig)

# 說明（改為中文）
st.write("""
### 模擬說明
- **入射角**：光線從介質1（左上，x<0, y>0）射向原點 (0, 0) 的角度，範圍0°到90°，相對於法線（Y 軸）。
- **折射率**：介質1 (n1) 和介質2 (n2) 的折射率，範圍1.0到3.0。
- **斯涅爾定律**：n1 * sin(θ1) = n2 * sin(θ2)。
- 光線從左上射向原點，折射後從右下 (x>0, y<0) 射出。若發生全反射，光線回到介質1 (y>0)。
""")