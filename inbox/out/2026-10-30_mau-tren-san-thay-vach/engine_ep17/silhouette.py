"""Rough polygon -> object silhouette (GrabCut) -> loose hand-drawn style contour."""
import cv2
import numpy as np


def silhouette(img_rgb, poly, margin=36, iters=6):
    """poly: rough outline in image px. Returns a 0/255 mask hugging the object."""
    h, w = img_rgb.shape[:2]
    bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
    poly = np.array(poly, np.int32)
    rough = np.zeros((h, w), np.uint8)
    cv2.fillPoly(rough, [poly], 255)
    near = cv2.dilate(rough, np.ones((margin * 2 + 1, margin * 2 + 1), np.uint8))
    core = cv2.erode(rough, np.ones((15, 15), np.uint8))
    gc = np.full((h, w), cv2.GC_BGD, np.uint8)
    gc[near > 0] = cv2.GC_PR_BGD
    gc[rough > 0] = cv2.GC_PR_FGD
    gc[core > 0] = cv2.GC_FGD
    bgd = np.zeros((1, 65), np.float64)
    fgd = np.zeros((1, 65), np.float64)
    cv2.grabCut(bgr, gc, None, bgd, fgd, iters, cv2.GC_INIT_WITH_MASK)
    m = np.where((gc == cv2.GC_FGD) | (gc == cv2.GC_PR_FGD), 255, 0).astype(np.uint8)
    # keep biggest component, close holes, smooth
    n, lab, stats, _ = cv2.connectedComponentsWithStats(m)
    if n > 1:
        k = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
        m = np.where(lab == k, 255, 0).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((25, 25), np.uint8))
    m = cv2.GaussianBlur(m, (0, 0), 7)
    return np.where(m > 127, 255, 0).astype(np.uint8)


def loose_contour(mask, offset=14, eps=5.0):
    """Outward-offset, slightly angular outline (list of (x, y)), like a quick pen sketch."""
    k = 2 * offset + 1
    big = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k)))
    big = cv2.GaussianBlur(big, (0, 0), 3.5)
    big = np.where(big > 127, 255, 0).astype(np.uint8)
    cs, _ = cv2.findContours(big, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    c = max(cs, key=cv2.contourArea)
    ap = cv2.approxPolyDP(c, eps, True)
    return [tuple(p[0]) for p in ap]
