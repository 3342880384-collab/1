"""四季数据可视化模板（雷达图）

使用方式：
1) 把 spring_data / summer_data / autumn_data / winter_data 替换为你的真实数据字典。
2) 运行：python seasonal_visualization.py
3) 输出：seasonal_radar.png

要求：四个字典的 key（指标名）需要一致，value 为数值。
说明：允许四个字典的 key 顺序不同，程序会按春季字典的顺序统一绘图。
"""

import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List, Sequence


# =========================
# 1) 在这里填写你的数据
# =========================
# 示例格式（请替换）：
# 每个字典的 key 必须一致，例如：温度、湿度、风速、降水量...
spring_data = {
    "指标A": 72,
    "指标B": 64,
    "指标C": 80,
    "指标D": 58,
    "指标E": 75,
    "指标F": 69,
}

summer_data = {
    "指标A": 88,
    "指标B": 72,
    "指标C": 77,
    "指标D": 66,
    "指标E": 83,
    "指标F": 74,
}

autumn_data = {
    "指标A": 76,
    "指标B": 68,
    "指标C": 85,
    "指标D": 62,
    "指标E": 79,
    "指标F": 71,
}

winter_data = {
    "指标A": 61,
    "指标B": 57,
    "指标C": 70,
    "指标D": 53,
    "指标E": 65,
    "指标F": 60,
}


# =========================
# 2) 可视化参数（可按需微调）
# =========================
SEASON_STYLE = {
    "春": {"color": "#66C2A5"},
    "夏": {"color": "#FC8D62"},
    "秋": {"color": "#8DA0CB"},
    "冬": {"color": "#A6D854"},
}


def _validate_and_get_labels(*dicts: Dict[str, float]) -> List[str]:
    """确保四个字典指标内容一致（允许 key 顺序不同）。"""
    labels = list(dicts[0].keys())
    base_keys = set(labels)

    for idx, current in enumerate(dicts[1:], start=2):
        current_keys = set(current.keys())
        if current_keys != base_keys:
            missing = sorted(base_keys - current_keys)
            extra = sorted(current_keys - base_keys)
            raise ValueError(
                f"第 {idx} 个季节字典的指标与春季不一致。"
                f" 缺少: {missing if missing else '无'};"
                f" 多出: {extra if extra else '无'}。"
            )

    return labels


def _close(values: Sequence[float]) -> List[float]:
    """雷达图闭环。"""
    values_list = list(values)
    return values_list + [values_list[0]]


def _values_in_label_order(data: Dict[str, float], labels: Sequence[str]) -> List[float]:
    """按指定标签顺序取值，确保各季节数据一一对应。"""
    return [float(data[label]) for label in labels]


def plot_seasonal_radar(
    spring: Dict[str, float],
    summer: Dict[str, float],
    autumn: Dict[str, float],
    winter: Dict[str, float],
    save_path: str = "seasonal_radar.png",
) -> None:
    labels = _validate_and_get_labels(spring, summer, autumn, winter)
    n = len(labels)

    angles = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
    angles = _close(angles)

    series = {
        "春": _close(_values_in_label_order(spring, labels)),
        "夏": _close(_values_in_label_order(summer, labels)),
        "秋": _close(_values_in_label_order(autumn, labels)),
        "冬": _close(_values_in_label_order(winter, labels)),
    }

    plt.figure(figsize=(9, 9), dpi=160)
    ax = plt.subplot(111, polar=True)
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    # 坐标标签
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=11)

    # 背景网格
    ax.grid(alpha=0.25)
    ax.spines["polar"].set_alpha(0.2)

    # 动态设置纵轴范围
    all_values = [v for values in series.values() for v in values[:-1]]
    min_v, max_v = min(all_values), max(all_values)
    margin = max(1, (max_v - min_v) * 0.15)
    ax.set_ylim(max(0, min_v - margin), max_v + margin)

    for season, values in series.items():
        color = SEASON_STYLE[season]["color"]
        ax.plot(angles, values, color=color, linewidth=2.2, label=season)
        ax.fill(angles, values, color=color, alpha=0.20)

    plt.title("四季指标对比雷达图", fontsize=15, pad=24)
    plt.legend(loc="upper right", bbox_to_anchor=(1.2, 1.12), frameon=False)
    plt.tight_layout()
    plt.savefig(save_path, bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    plot_seasonal_radar(
        spring=spring_data,
        summer=summer_data,
        autumn=autumn_data,
        winter=winter_data,
        save_path="seasonal_radar.png",
    )
