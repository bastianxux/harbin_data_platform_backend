import numpy as np
from collections import defaultdict
from sklearn.cluster import DBSCAN

KMS_PER_RADIAN = 6371.0088  # 地球平均半径

def dbscan_geo(points, eps_m=200, min_samples=20):
    """
    points: [(lat, lng), ...]  (°)
    eps_m : 聚类半径（米）
    return: [{'id': 0, 'size': 42, 'centroid': [lat, lng]}, ...]
    """
    if not points:
        return []

    coords_rad = np.radians(points)           # DBSCAN(haversine) 需弧度
    eps = eps_m / 1000.0 / KMS_PER_RADIAN     # 米 → 弧度

    labels = DBSCAN(eps=eps, min_samples=min_samples,
                    metric='haversine').fit(coords_rad).labels_

    clusters = defaultdict(list)
    for lbl, (lat, lng) in zip(labels, points):
        if lbl != -1:                         # -1 = 噪声点
            clusters[lbl].append((lat, lng))

    results = []
    for cid, pts in clusters.items():
        arr = np.array(pts)
        centroid = [arr[:, 0].mean(), arr[:, 1].mean()]
        results.append({
            "id": int(cid),
            "size": len(pts),
            "centroid": centroid              # 直接给前端就能画
        })
    return results
