import numpy as np, scipy, pylab
import cv2, copy, math


class calcEnergy4(object):
	def __init__(self, img, imgWidth, imgHeight, edgeBasedMeasure, rminN, rmaxN):
		
		
		imgEnergyTitle = 'Energy4.jpg'
		
		retE = edgeBasedMeasure
		
		
		updateFirstRow = False
		updateLastRow = False
		
		if rminN == -1:
			rminN = 0
			updateLastRow = True
		
		if rmaxN == imgHeight:
			rmaxN = imgHeight-1
			updateFirstRow = True

		
		maxbest = 0
		
		
		for c in range(1,imgWidth-1):
				for r in range(1, imgHeight-1):
					if rminN <= r and r <= rmaxN:

						Rx = img[r][c+1][2] - img[r][c-1][2]
						Gx = img[r][c+1][1] - img[r][c-1][1]
						Bx = img[r][c+1][0] - img[r][c-1][0]
		
						Dxsq = math.sqrt(Rx**2 + Gx**2 + Bx**2)
						Ry = img[r+1][c][2] - img[r-1][c][2]
						Gy = img[r+1][c][1] - img[r-1][c][1]
						By = img[r+1][c][0] - img[r-1][c][0]

						Dysq = math.sqrt(Ry**2 + Gy**2 + By**2)
				
						# pixel in the corner
						retE[r][c] = Dxsq + Dysq 
						if Dxsq + Dysq > maxbest:
							maxbest = Dxsq + Dysq
		

		if rminN == 0 or updateFirstRow:
		# Topmost row, r = 0
			for c in range(1,imgWidth-1):
			#if cminN <= c and c <= cmaxN:
				Rx = img[0][c+1][2] - img[0][c-1][2]
				Gx = img[0][c+1][1] - img[0][c-1][1]
				Bx = img[0][c+1][0] - img[0][c-1][0]

				Dxsq = math.sqrt(Rx**2 + Gx**2 + Bx**2)
				Ry = img[1][c][2] - img[imgHeight-1][c][2]
				Gy = img[1][c][1] - img[imgHeight-1][c][1]
				By = img[1][c][0] - img[imgHeight-1][c][0]
				Dysq = math.sqrt(Ry**2 + Gy**2 + By**2)
		
				# pixel in the corner
				retE[0][c] = Dxsq + Dysq 
				if Dxsq + Dysq > maxbest:
					maxbest = Dxsq + Dysq
		
		

		# Bottom most row
		if rmaxN == imgHeight-1 or updateLastRow: 
			for c in range(1, imgWidth-1):
			#if cminN <= c and c <= cmaxN:
				Rx = img[imgHeight-1][c+1][2] - img[imgHeight-1][c-1][2]
				Gx = img[imgHeight-1][c+1][1] - img[imgHeight-1][c-1][1]
				Bx = img[imgHeight-1][c+1][0] - img[imgHeight-1][c-1][0]

				Dxsq = math.sqrt(Rx**2 + Gx**2 + Bx**2)
				Ry = img[0][c][2] - img[imgHeight-2][c][2]
				Gy = img[0][c][1] - img[imgHeight-2][c][1]
				By = img[0][c][0] - img[imgHeight-2][c][0]
				Dysq = math.sqrt(Ry**2 + Gy**2 + By**2)
		

				# pixel in the corner
				retE[imgHeight-1][c] = Dxsq + Dysq 
				if Dxsq + Dysq > maxbest:
					maxbest = Dxsq + Dysq
		
		
		

		# Left most column
		#if cminN == 0 or updateFirstCol:
		for r in range(1, imgHeight-1):
			if rminN <= r and r <= rmaxN:
				Rx = img[r][1][2] - img[r][imgWidth-1][2]
				Gx = img[r][1][1] - img[r][imgWidth-1][1]
				Bx = img[r][1][0] - img[r][imgWidth-1][0]

				Dxsq = math.sqrt(Rx**2 + Gx**2 + Bx**2)
				Ry = img[r+1][0][2] - img[r-1][0][2]
				Gy = img[r+1][0][1] - img[r-1][0][1]
				By = img[r+1][0][0] - img[r-1][0][0]
				Dysq = math.sqrt(Ry**2 + Gy**2 + By**2)
		
		
				# pixel in the corner
				retE[r][0] = Dxsq + Dysq 
				if Dxsq + Dysq > maxbest:
					maxbest = Dxsq + Dysq
		
		
		
		
		# Right most column
		#if cmaxN == imgWidth-1 or updateLastCol:
		for r in range(1, imgHeight-1):
			if rminN <= r and r <= rmaxN:
				Rx = img[r][0][2] - img[r][imgWidth-2][2]
				Gx = img[r][0][1] - img[r][imgWidth-2][1]
				Bx = img[r][0][0] - img[r][imgWidth-2][0]

				Dxsq = math.sqrt(Rx**2 + Gx**2 + Bx**2)
				Ry = img[r+1][imgWidth-1][2] - img[r-1][imgWidth-1][2]
				Gy = img[r+1][imgWidth-1][1] - img[r-1][imgWidth-1][1]
				By = img[r+1][imgWidth-1][0] - img[r-1][imgWidth-1][0]
				Dysq = math.sqrt(Ry**2 + Gy**2 + By**2)
		
		
				# pixel in the corner 
				retE[r][imgWidth-1] = Dxsq + Dysq 
				if Dxsq + Dysq > maxbest:
					maxbest = Dxsq + Dysq
			
		
		
		# Top left corner
		if rminN == 0 or updateFirstRow:
			Rx = img[0][1][2] - img[0][imgWidth-1][2]
			Gx = img[0][1][1] - img[0][imgWidth-1][1]
			Bx = img[0][1][0] - img[0][imgWidth-1][0]

			Dxsq = math.sqrt(Rx**2 + Gx**2 + Bx**2)
			Ry = img[1][0][2] - img[imgHeight-1][0][2]
			Gy = img[1][0][1] - img[imgHeight-1][0][1]
			By = img[1][0][0] - img[imgHeight-1][0][0]
			Dysq = math.sqrt(Ry**2 + Gy**2 + By**2)
		
			# pixel in the corner
			retE[0][0] = Dxsq + Dysq 
			if Dxsq + Dysq > maxbest:
				maxbest = Dxsq + Dysq

		
		
		
		# Top right corner
		if rminN == 0 or updateFirstRow:
			Rx = img[0][0][2] - img[0][imgWidth-2][2]
			Gx = img[0][0][1] - img[0][imgWidth-2][1]
			Bx = img[0][0][0] - img[0][imgWidth-2][0]
	
			Dxsq = math.sqrt(Rx**2 + Gx**2 + Bx**2)
			Ry = img[1][imgWidth-1][2] - img[imgHeight-1][imgWidth-1][2]
			Gy = img[1][imgWidth-1][1] - img[imgHeight-1][imgWidth-1][1]
			By = img[1][imgWidth-1][0] - img[imgHeight-1][imgWidth-1][0]
			Dysq = math.sqrt(Ry**2 + Gy**2 + By**2)
		
		
			# pixel in the corner
			retE[0][imgWidth-1] = Dxsq + Dysq 
			if Dxsq + Dysq > maxbest:
				maxbest = Dxsq + Dysq
			
		
		
		
		
		# Bottom left corner
		if rmaxN == imgHeight-1 or updateLastRow:
			Rx = img[imgHeight-1][1][2] - img[imgHeight-1][imgWidth-1][2]
			Gx = img[imgHeight-1][1][1] - img[imgHeight-1][imgWidth-1][1]
			Bx = img[imgHeight-1][1][0] - img[imgHeight-1][imgWidth-1][0]

			Dxsq = math.sqrt(Rx**2 + Gx**2 + Bx**2)
			Ry = img[0][0][2] - img[imgHeight-2][0][2]
			Gy = img[0][0][1] - img[imgHeight-2][0][1]
			By = img[0][0][0] - img[imgHeight-2][0][0]
			Dysq = math.sqrt(Ry**2 + Gy**2 + By**2)
		
		
			# pixel in the corner
			retE[imgHeight-1][0] = Dxsq + Dysq 
			if Dxsq + Dysq > maxbest:
				maxbest = Dxsq + Dysq
		
		
		
		
		
		if rmaxN == imgHeight-1 or updateLastRow:
			# Bottom right corner
			Rx = img[imgHeight-1][0][2] - img[imgHeight-1][imgWidth-2][2]
			Gx = img[imgHeight-1][0][1] - img[imgHeight-1][imgWidth-2][1]
			Bx = img[imgHeight-1][0][0] - img[imgHeight-1][imgWidth-2][0]
	
			Dxsq = math.sqrt(Rx**2 + Gx**2 + Bx**2)
			Ry = img[0][imgWidth-1][2] - img[imgHeight-2][imgWidth-1][2]
			Gy = img[0][imgWidth-1][1] - img[imgHeight-2][imgWidth-1][1]
			By = img[0][imgWidth-1][0] - img[imgHeight-2][imgWidth-1][0]
			Dysq = math.sqrt(Ry**2 + Gy**2 + By**2)
		
			# pixel in the corner
			retE[imgHeight-1][imgWidth-1] = Dxsq + Dysq 
			if Dxsq + Dysq > maxbest:
				maxbest = Dxsq + Dysq
		
				
		# Fill up for the corners
		retE = np.array(retE)
		cv2.imwrite(imgEnergyTitle, retE)
		self.retE = retE

