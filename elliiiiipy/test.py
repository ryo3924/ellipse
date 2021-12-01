

import numpy as np
import cv2
import math

#画像読み込み
image=cv2.imread("C:\\Users\\81804\\Pictures\\realsense\\colorssss_Colors.png")

#二値化
grey=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) 
grey_hist=cv2.calcHist([grey],[0],None,[256],[0,256])
eq=cv2.equalizeHist(grey)
blurredA1=cv2.blur(eq,(3,3))

#二値化の閾値(要調整）
(T,thresh)=cv2.threshold(blurredA1,20,255,cv2.THRESH_BINARY)

#白黒反転
thresh = cv2.bitwise_not(thresh)

# 結果画像の黒の部分を灰色にする。
bimg = thresh // 4 + 255 * 3 //4
thresh2 = cv2.bitwise_not(bimg)
cv2.namedWindow('binary window', cv2.WINDOW_KEEPRATIO)
cv2.imshow('binary window', thresh)

resimg = cv2.merge((bimg,bimg,bimg)) 

contours, hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

#楕円検出
if len(contours) != 0:
  for i in range(len(contours)):
    if len(contours[i]) >= 5:
        cv2.drawContours(thresh,contours,-1,(150,150,255),3)
        (cx, cy), (width, height), angle=cv2.fitEllipse(contours[0])

#楕円情報定義
        cxx = int(cx) 
        cyy = int(cy)
        #a = int(ellipse[1][0])
        #b = int(ellipse[1][1])

        h = int(height)
        w = int(width)
        hh = str(height)
        ww = str(width)

        rate_hw = w/h
        rate = str(rate_hw)

        deg = str(angle)
        deggv = int(angle)
        degg = deggv*2*math.pi/360
        degcos = math.cos(degg)
        degsin = math.sin(degg)
        sx_a1 = cxx + h*degsin
        sx_a2 = cxx - h*degsin
        sy_a1 = cyy - h*degcos
        sy_a2 = cyy + h*degcos
        sx_b1 = cxx - w*degcos
        sx_b2 = cxx + w*degcos
        sy_b1 = cyy - w*degsin
        sy_b2 = cyy + w*degsin

        sx_a1 = int(sx_a1)
        sx_a2 = int(sx_a2)
        sy_a1 = int(sy_a1)
        sy_a2 = int(sy_a2)
        sx_b1 = int(sx_b1)
        sx_b2 = int(sx_b2)
        sy_b1 = int(sy_b1)
        sy_b2 = int(sy_b2)

# 楕円描画
        resimg = cv2.ellipse(resimg,((cx, cy), (width, height), angle),(255,0,0),10)
        #cv2.drawMarker(resimg, center, (0,0,255), markerType=cv2.MARKER_CROSS, markerSize=10, thickness=1)

        cv2.line(resimg, (sx_a1, sy_a1),(sx_a2, sy_a2),(0,255,0),10)
        cv2.line(resimg, (sx_b1, sy_b1),(sx_b2, sy_b2),(0,255,0),10)
        
        cv2.putText(resimg, "deg=", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,80,255), 3,cv2.LINE_AA)
        cv2.putText(resimg, "height=", (100, 200), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,80,255), 3,cv2.LINE_AA)
        cv2.putText(resimg, "width=", (100, 300), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,80,255), 3,cv2.LINE_AA)
        cv2.putText(resimg, "rate=", (100, 400), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,80,255), 3,cv2.LINE_AA)

        cv2.putText(resimg, deg, (350, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,80,255), 3,cv2.LINE_AA)
        cv2.putText(resimg, hh, (350, 200), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,80,255), 3,cv2.LINE_AA)
        cv2.putText(resimg, ww, (350, 300), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,80,255), 3,cv2.LINE_AA)
        cv2.putText(resimg, rate, (350, 400), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,80,255), 3,cv2.LINE_AA)
        cv2.putText(resimg, str(cxx), (350, 500), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,80,255), 3,cv2.LINE_AA)
        cv2.putText(resimg, str(cyy), (350, 600), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,80,255), 3,cv2.LINE_AA)
        
    else:
      # optional to "delete" the small contours
      cv2.drawContours(thresh,contours,-1,(0,0,0),-1)


#cv2.imshow("Perfectlyfittedellipses",thresh)

cv2.namedWindow('custom window', cv2.WINDOW_KEEPRATIO)
cv2.imshow('custom window', resimg)
cv2.waitKey(0)
