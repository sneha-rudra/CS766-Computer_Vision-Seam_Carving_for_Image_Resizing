#Seam Carving

#Importing libraries
import numpy as np, scipy, pylab
import cv2, copy, math
import calcEnergy3, calcEnergy4 


class seamCarving(object):
	def __init__(self, imgTitle):
		
		self.imgTitle = imgTitle
		img = cv2.imread(imgTitle, -1)
		self.img = img
		self.orgImg = img
		self.imgWidth = len(self.img[0]) 
		self.imgHeight = len(self.img)
		

		
		self.edgeBasedMeasure = None
		self.wRed = False
		self.wExp = False
		self.hRed = False
		self.hExp = False
		
		msg1 = '\n' + 'The width of the image is ' + str(self.imgWidth) + '. Enter the number of vertical seams to remove:  '			
		numVertSeams = raw_input(msg1)
		
		msg2 = '\n' + 'The height of the image is ' + str(self.imgHeight) + '. Enter the number of horizontal seams to remove:  '	
		numHoriSeams = raw_input(msg2)
		
		
		self.numVertSeams = int(numVertSeams)   
		self.numHoriSeams = int(numHoriSeams)  
		
		self.wPrime = self.imgWidth - self.numVertSeams
		self.hPrime = self.imgHeight - self.numHoriSeams 
		
		
		if self.wPrime > self.imgWidth:
			self.wExp = True
			self.numVertSeams = self.wPrime - self.imgWidth  
			
		elif self.wPrime < self.imgWidth:
			self.wRed = True
			self.numVertSeams = self.imgWidth - self.wPrime 
			
			
			
		if self.hPrime > self.imgHeight:
			self.hExp = True
			self.numHoriSeams = self.hPrime - self.imgHeight #0
			
		elif self.hPrime < self.imgHeight:
			self.hRed = True
			self.numHoriSeams = self.imgHeight - self.hPrime #0
	
	
 
		self.optimalSeamsOrdering()	
		msg = '\n' + 'Final retargeted result has been saved as \'final.jpg\' in the same folder as this python script' + '\n'
		print(msg)
	


	
		
	# Energy of pixel at column x and row y	
	def calcEnergyOrg(self):
		imgEnergyTitle = self.imgTitle[0:-4] + 'Energy.jpg'
		
		self.edgeBasedMeasure = []

		for r in range(0, self.imgHeight):
			self.edgeBasedMeasure.append([])
			for c in range(0,self.imgWidth):
				self.edgeBasedMeasure[r].append(0)
				
		maxbest = 0
		
		for c in range(1,self.imgWidth-1):
			for r in range(1, self.imgHeight-1):

					Rx = self.img[r][c+1][2] - self.img[r][c-1][2]
					Gx = self.img[r][c+1][1] - self.img[r][c-1][1]
					Bx = self.img[r][c+1][0] - self.img[r][c-1][0]

					Dxsq = math.sqrt(Rx**2 + Gx**2 + Bx**2)
					Ry = self.img[r+1][c][2] - self.img[r-1][c][2]
					Gy = self.img[r+1][c][1] - self.img[r-1][c][1]
					By = self.img[r+1][c][0] - self.img[r-1][c][0]

					Dysq = math.sqrt(Ry**2 + Gy**2 + By**2)
		
		
		# pixel in the corner
					self.edgeBasedMeasure[r][c] = Dxsq + Dysq 
					if Dxsq + Dysq > maxbest:
						maxbest = Dxsq + Dysq
		
		
		# Topmost row, r = 0
		for c in range(1,self.imgWidth-1):
			Rx = self.img[0][c+1][2] - self.img[0][c-1][2]
			Gx = self.img[0][c+1][1] - self.img[0][c-1][1]
			Bx = self.img[0][c+1][0] - self.img[0][c-1][0]

			Dxsq = math.sqrt(Rx**2 + Gx**2 + Bx**2)
			Ry = self.img[1][c][2] - self.img[self.imgHeight-1][c][2]
			Gy = self.img[1][c][1] - self.img[self.imgHeight-1][c][1]
			By = self.img[1][c][0] - self.img[self.imgHeight-1][c][0]
			Dysq = math.sqrt(Ry**2 + Gy**2 + By**2)
		
		
			# pixel in the corner
			self.edgeBasedMeasure[0][c] = Dxsq + Dysq 
			if Dxsq + Dysq > maxbest:
				maxbest = Dxsq + Dysq
		
		
		
		# Bottom most row
		for c in range(1,self.imgWidth-1):
			Rx = self.img[self.imgHeight-1][c+1][2] - self.img[self.imgHeight-1][c-1][2]
			Gx = self.img[self.imgHeight-1][c+1][1] - self.img[self.imgHeight-1][c-1][1]
			Bx = self.img[self.imgHeight-1][c+1][0] - self.img[self.imgHeight-1][c-1][0]

			Dxsq = math.sqrt(Rx**2 + Gx**2 + Bx**2)
			Ry = self.img[0][c][2] - self.img[self.imgHeight-2][c][2]
			Gy = self.img[0][c][1] - self.img[self.imgHeight-2][c][1]
			By = self.img[0][c][0] - self.img[self.imgHeight-2][c][0]
			Dysq = math.sqrt(Ry**2 + Gy**2 + By**2)
		
		
			# pixel in the corner
			self.edgeBasedMeasure[self.imgHeight-1][c] = Dxsq + Dysq 
			if Dxsq + Dysq > maxbest:
				maxbest = Dxsq + Dysq
		
		
		
		
		# Left most column
		for r in range(1, self.imgHeight-1):
			Rx = self.img[r][1][2] - self.img[r][self.imgWidth-1][2]
			Gx = self.img[r][1][1] - self.img[r][self.imgWidth-1][1]
			Bx = self.img[r][1][0] - self.img[r][self.imgWidth-1][0]

			Dxsq = math.sqrt(Rx**2 + Gx**2 + Bx**2)
			Ry = self.img[r+1][0][2] - self.img[r-1][0][2]
			Gy = self.img[r+1][0][1] - self.img[r-1][0][1]
			By = self.img[r+1][0][0] - self.img[r-1][0][0]
			Dysq = math.sqrt(Ry**2 + Gy**2 + By**2)
		
		
			# pixel in the corner
			self.edgeBasedMeasure[r][0] = Dxsq + Dysq 
			if Dxsq + Dysq > maxbest:
				maxbest = Dxsq + Dysq
		
		
		
		
		
		# Right most column
		for r in range(1, self.imgHeight-1):
			Rx = self.img[r][0][2] - self.img[r][self.imgWidth-2][2]
			Gx = self.img[r][0][1] - self.img[r][self.imgWidth-2][1]
			Bx = self.img[r][0][0] - self.img[r][self.imgWidth-2][0]

			Dxsq = math.sqrt(Rx**2 + Gx**2 + Bx**2)
			Ry = self.img[r+1][self.imgWidth-1][2] - self.img[r-1][self.imgWidth-1][2]
			Gy = self.img[r+1][self.imgWidth-1][1] - self.img[r-1][self.imgWidth-1][1]
			By = self.img[r+1][self.imgWidth-1][0] - self.img[r-1][self.imgWidth-1][0]
			Dysq = math.sqrt(Ry**2 + Gy**2 + By**2)
		
		
			# pixel in the corner
			self.edgeBasedMeasure[r][self.imgWidth-1] = Dxsq + Dysq 
			if Dxsq + Dysq > maxbest:
				maxbest = Dxsq + Dysq

			
		
		
		# Top left corner
		Rx = self.img[0][1][2] - self.img[0][self.imgWidth-1][2]
		Gx = self.img[0][1][1] - self.img[0][self.imgWidth-1][1]
		Bx = self.img[0][1][0] - self.img[0][self.imgWidth-1][0]

		Dxsq = math.sqrt(Rx**2 + Gx**2 + Bx**2)
		Ry = self.img[1][0][2] - self.img[self.imgHeight-1][0][2]
		Gy = self.img[1][0][1] - self.img[self.imgHeight-1][0][1]
		By = self.img[1][0][0] - self.img[self.imgHeight-1][0][0]
		Dysq = math.sqrt(Ry**2 + Gy**2 + By**2)
		
		
		# pixel in the corner
		self.edgeBasedMeasure[0][0] = Dxsq + Dysq 
		if Dxsq + Dysq > maxbest:
			maxbest = Dxsq + Dysq

		
		
		
		# Top right corner
		Rx = self.img[0][0][2] - self.img[0][self.imgWidth-2][2]
		Gx = self.img[0][0][1] - self.img[0][self.imgWidth-2][1]
		Bx = self.img[0][0][0] - self.img[0][self.imgWidth-2][0]

		Dxsq = math.sqrt(Rx**2 + Gx**2 + Bx**2)
		Ry = self.img[1][self.imgWidth-1][2] - self.img[self.imgHeight-1][self.imgWidth-1][2]
		Gy = self.img[1][self.imgWidth-1][1] - self.img[self.imgHeight-1][self.imgWidth-1][1]
		By = self.img[1][self.imgWidth-1][0] - self.img[self.imgHeight-1][self.imgWidth-1][0]
		Dysq = math.sqrt(Ry**2 + Gy**2 + By**2)
		
		
		# pixel in the corner
		self.edgeBasedMeasure[0][self.imgWidth-1] = Dxsq + Dysq 
		if Dxsq + Dysq > maxbest:
			maxbest = Dxsq + Dysq

			
		
		
		
		
		# Bottom left corner
		Rx = self.img[self.imgHeight-1][1][2] - self.img[self.imgHeight-1][self.imgWidth-1][2]
		Gx = self.img[self.imgHeight-1][1][1] - self.img[self.imgHeight-1][self.imgWidth-1][1]
		Bx = self.img[self.imgHeight-1][1][0] - self.img[self.imgHeight-1][self.imgWidth-1][0]

		Dxsq = math.sqrt(Rx**2 + Gx**2 + Bx**2)
		Ry = self.img[0][0][2] - self.img[self.imgHeight-2][0][2]
		Gy = self.img[0][0][1] - self.img[self.imgHeight-2][0][1]
		By = self.img[0][0][0] - self.img[self.imgHeight-2][0][0]
		Dysq = math.sqrt(Ry**2 + Gy**2 + By**2)
		
		
		# pixel in the corner
		self.edgeBasedMeasure[self.imgHeight-1][0] = Dxsq + Dysq 
		if Dxsq + Dysq > maxbest:
			maxbest = Dxsq + Dysq
		
		
		
		
		
		
		# Bottom right corner
		Rx = self.img[self.imgHeight-1][0][2] - self.img[self.imgHeight-1][self.imgWidth-2][2]
		Gx = self.img[self.imgHeight-1][0][1] - self.img[self.imgHeight-1][self.imgWidth-2][1]
		Bx = self.img[self.imgHeight-1][0][0] - self.img[self.imgHeight-1][self.imgWidth-2][0]

		Dxsq = math.sqrt(Rx**2 + Gx**2 + Bx**2)
		Ry = self.img[0][self.imgWidth-1][2] - self.img[self.imgHeight-2][self.imgWidth-1][2]
		Gy = self.img[0][self.imgWidth-1][1] - self.img[self.imgHeight-2][self.imgWidth-1][1]
		By = self.img[0][self.imgWidth-1][0] - self.img[self.imgHeight-2][self.imgWidth-1][0]
		Dysq = math.sqrt(Ry**2 + Gy**2 + By**2)
		
		
		# pixel in the corner 
		self.edgeBasedMeasure[self.imgHeight-1][self.imgWidth-1] = Dxsq + Dysq 
		if Dxsq + Dysq > maxbest:
			maxbest = Dxsq + Dysq
		
		
		
						
		# Fill up for the corners
		self.edgeBasedMeasure = np.array(self.edgeBasedMeasure)
		cv2.imwrite(imgEnergyTitle, self.edgeBasedMeasure)
		




	
	# Energy of pixel at column x and row y	
	def calcEnergy2(self, img, imgWidth, imgHeight):
		imgEnergyTitle = 'Energy2.jpg'
		
				
		edgeBasedMeasure = []

		for r in range(0, imgHeight):
			edgeBasedMeasure.append([])
			for c in range(0,imgWidth):
				edgeBasedMeasure[r].append(0)
				
		maxbest = 0
		

		for c in range(1,imgWidth-1):
			for r in range(1, imgHeight-1):

						Rx = img[r][c+1][2] - img[r][c-1][2]
						Gx = img[r][c+1][1] - img[r][c-1][1]
						Bx = img[r][c+1][0] - img[r][c-1][0]

						Dxsq = math.sqrt(Rx**2 + Gx**2 + Bx**2)
						Ry = img[r+1][c][2] - img[r-1][c][2]
						Gy = img[r+1][c][1] - img[r-1][c][1]
						By = img[r+1][c][0] - img[r-1][c][0]

						Dysq = math.sqrt(Ry**2 + Gy**2 + By**2)
				
						# pixel in the corner
						edgeBasedMeasure[r][c] = Dxsq + Dysq 
						if Dxsq + Dysq > maxbest:
							maxbest = Dxsq + Dysq
		

		# Topmost row, r = 0
		for c in range(1,imgWidth-1):
				Rx = img[0][c+1][2] - img[0][c-1][2]
				Gx = img[0][c+1][1] - img[0][c-1][1]
				Bx = img[0][c+1][0] - img[0][c-1][0]

				Dxsq = math.sqrt(Rx**2 + Gx**2 + Bx**2)
				Ry = img[1][c][2] - img[imgHeight-1][c][2]
				Gy = img[1][c][1] - img[imgHeight-1][c][1]
				By = img[1][c][0] - img[imgHeight-1][c][0]
				Dysq = math.sqrt(Ry**2 + Gy**2 + By**2)
		
				# pixel in the corner
				edgeBasedMeasure[0][c] = Dxsq + Dysq 
				if Dxsq + Dysq > maxbest:
					maxbest = Dxsq + Dysq
		
		

		# Bottom most row
		for c in range(1, imgWidth-1):
				Rx = img[imgHeight-1][c+1][2] - img[imgHeight-1][c-1][2]
				Gx = img[imgHeight-1][c+1][1] - img[imgHeight-1][c-1][1]
				Bx = img[imgHeight-1][c+1][0] - img[imgHeight-1][c-1][0]

				Dxsq = math.sqrt(Rx**2 + Gx**2 + Bx**2)
				Ry = img[0][c][2] - img[imgHeight-2][c][2]
				Gy = img[0][c][1] - img[imgHeight-2][c][1]
				By = img[0][c][0] - img[imgHeight-2][c][0]
				Dysq = math.sqrt(Ry**2 + Gy**2 + By**2)
		
		
				# pixel in the corner 
				edgeBasedMeasure[imgHeight-1][c] = Dxsq + Dysq 
				if Dxsq + Dysq > maxbest:
					maxbest = Dxsq + Dysq
		
		

		# Left most column
		for r in range(1, imgHeight-1):
				Rx = img[r][1][2] - img[r][imgWidth-1][2]
				Gx = img[r][1][1] - img[r][imgWidth-1][1]
				Bx = img[r][1][0] - img[r][imgWidth-1][0]

				Dxsq = math.sqrt(Rx**2 + Gx**2 + Bx**2)
				Ry = img[r+1][0][2] - img[r-1][0][2]
				Gy = img[r+1][0][1] - img[r-1][0][1]
				By = img[r+1][0][0] - img[r-1][0][0]
				Dysq = math.sqrt(Ry**2 + Gy**2 + By**2)
		
		
				# pixel in the corner
				edgeBasedMeasure[r][0] = Dxsq + Dysq 
				if Dxsq + Dysq > maxbest:
					maxbest = Dxsq + Dysq
		
		
		

		# Right most column
		for r in range(1, imgHeight-1):
				Rx = img[r][0][2] - img[r][imgWidth-2][2]
				Gx = img[r][0][1] - img[r][imgWidth-2][1]
				Bx = img[r][0][0] - img[r][imgWidth-2][0]

				Dxsq = math.sqrt(Rx**2 + Gx**2 + Bx**2)
				Ry = img[r+1][imgWidth-1][2] - img[r-1][imgWidth-1][2]
				Gy = img[r+1][imgWidth-1][1] - img[r-1][imgWidth-1][1]
				By = img[r+1][imgWidth-1][0] - img[r-1][imgWidth-1][0]
				Dysq = math.sqrt(Ry**2 + Gy**2 + By**2)
		
		
				# pixel in the corner
				edgeBasedMeasure[r][imgWidth-1] = Dxsq + Dysq 
				if Dxsq + Dysq > maxbest:
					maxbest = Dxsq + Dysq

			
		
		
		# Top left corner
		Rx = img[0][1][2] - img[0][imgWidth-1][2]
		Gx = img[0][1][1] - img[0][imgWidth-1][1]
		Bx = img[0][1][0] - img[0][imgWidth-1][0]

		Dxsq = math.sqrt(Rx**2 + Gx**2 + Bx**2)
		Ry = img[1][0][2] - img[imgHeight-1][0][2]
		Gy = img[1][0][1] - img[imgHeight-1][0][1]
		By = img[1][0][0] - img[imgHeight-1][0][0]
		Dysq = math.sqrt(Ry**2 + Gy**2 + By**2)
		
		
		# pixel in the corner
		edgeBasedMeasure[0][0] = Dxsq + Dysq 
		if Dxsq + Dysq > maxbest:
			maxbest = Dxsq + Dysq

		
		
		
		# Top right corner
		Rx = img[0][0][2] - img[0][imgWidth-2][2]
		Gx = img[0][0][1] - img[0][imgWidth-2][1]
		Bx = img[0][0][0] - img[0][imgWidth-2][0]

		Dxsq = math.sqrt(Rx**2 + Gx**2 + Bx**2)
		Ry = img[1][imgWidth-1][2] - img[imgHeight-1][imgWidth-1][2]
		Gy = img[1][imgWidth-1][1] - img[imgHeight-1][imgWidth-1][1]
		By = img[1][imgWidth-1][0] - img[imgHeight-1][imgWidth-1][0]
		Dysq = math.sqrt(Ry**2 + Gy**2 + By**2)
		
		
		# pixel in the corner 
		edgeBasedMeasure[0][imgWidth-1] = Dxsq + Dysq 
		if Dxsq + Dysq > maxbest:
			maxbest = Dxsq + Dysq

			
		
		
		
		
		# Bottom left corner
		Rx = img[imgHeight-1][1][2] - img[imgHeight-1][imgWidth-1][2]
		Gx = img[imgHeight-1][1][1] - img[imgHeight-1][imgWidth-1][1]
		Bx = img[imgHeight-1][1][0] - img[imgHeight-1][imgWidth-1][0]

		Dxsq = math.sqrt(Rx**2 + Gx**2 + Bx**2)
		Ry = img[0][0][2] - img[imgHeight-2][0][2]
		Gy = img[0][0][1] - img[imgHeight-2][0][1]
		By = img[0][0][0] - img[imgHeight-2][0][0]
		Dysq = math.sqrt(Ry**2 + Gy**2 + By**2)
		
		
		# pixel in the corner 
		edgeBasedMeasure[imgHeight-1][0] = Dxsq + Dysq 
		if Dxsq + Dysq > maxbest:
			maxbest = Dxsq + Dysq
		
		
		
		
		
		
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
		edgeBasedMeasure[imgHeight-1][imgWidth-1] = Dxsq + Dysq 
		if Dxsq + Dysq > maxbest:
			maxbest = Dxsq + Dysq
		
		
		
					
		# Fill something for the corners
		edgeBasedMeasure = np.array(edgeBasedMeasure)
		cv2.imwrite(imgEnergyTitle, edgeBasedMeasure)
		return edgeBasedMeasure
		
	
		
	def identifyHoriSeamOrg(self):
		# Initialize an M of the size of the image
		self.horiMinMat = copy.deepcopy(self.edgeBasedMeasure)
		self.horiMinInd = copy.deepcopy(self.edgeBasedMeasure)
		
		
		# For the topmost row, let the min energy be e(i,j) and store corresponding column number
		# already true
		for i in range(0,self.imgHeight):
			self.horiMinInd[i][0] = i 
		
		
		# For subsequent rows, check if an index exists, find min + eij and store column number of min
		for c in range(1, self.imgWidth):
			for  r in range(0, self.imgHeight):
		
				if r >=1 and r <= self.imgHeight-2:
					
					Vals = [self.horiMinMat[r-1][c-1], self.horiMinMat[r][c-1], self.horiMinMat[r+1][c-1]] 
					minVal = min(Vals)
					minInd = Vals.index(minVal) + r-1
					self.horiMinMat[r][c] = self.horiMinMat[r][c] + minVal
					self.horiMinInd[r][c] = minInd
					
				elif r == 0:
					Vals = [self.horiMinMat[r][c-1], self.horiMinMat[r+1][c-1]] 
					minVal = min(Vals)
					minInd = Vals.index(minVal) + r
					self.horiMinMat[r][c] = self.horiMinMat[r][c] + minVal
					self.horiMinInd[r][c] = minInd
					
				elif r == self.imgHeight-1:
					Vals = [self.horiMinMat[r-1][c-1], self.horiMinMat[r][c-1]] 
					minVal = min(Vals)
					minInd = Vals.index(minVal) + r-1
					self.horiMinMat[r][c] = self.horiMinMat[r][c] + minVal
					self.horiMinInd[r][c] = minInd
		
		

		# Ultimately look for the smallest val on the last row and backtrack
		backTrackArrHori = self.backTrackHori()			
		self.printHoriSeam(backTrackArrHori)
		self.backTrackArrHori = backTrackArrHori
		

		



		
	def identifyHoriSeam2(self, edgeBasedMeasure, img, imgWidth, imgHeight):
		# Initialize an M of the size of the image
		horiMinMat = copy.deepcopy(edgeBasedMeasure)
		horiMinInd = copy.deepcopy(edgeBasedMeasure)
		
		

		for i in range(0, imgHeight):
			horiMinInd[i][0] = i 
		
		
		# For subsequent rows, check if an index exists, find min + eij and store column number of min
		for c in range(1, imgWidth):
			for  r in range(0, imgHeight):
		
				if r >=1 and r <= imgHeight-2:
					
					Vals = [horiMinMat[r-1][c-1], horiMinMat[r][c-1], horiMinMat[r+1][c-1]] 
					minVal = min(Vals)
					minInd = Vals.index(minVal) + r-1
					horiMinMat[r][c] = horiMinMat[r][c] + minVal
					horiMinInd[r][c] = minInd
					
				elif r == 0:
					Vals = [horiMinMat[r][c-1], horiMinMat[r+1][c-1]] 
					minVal = min(Vals)
					minInd = Vals.index(minVal) + r
					horiMinMat[r][c] = horiMinMat[r][c] + minVal
					horiMinInd[r][c] = minInd
					
				elif r == imgHeight-1:
					Vals = [horiMinMat[r-1][c-1], horiMinMat[r][c-1]] 
					minVal = min(Vals)
					minInd = Vals.index(minVal) + r-1
					horiMinMat[r][c] = horiMinMat[r][c] + minVal
					horiMinInd[r][c] = minInd
		
		

		# Ultimately look for the smallest val on the last row and backtrack

		backTrackArrHori = self.backTrackHori2(imgWidth, imgHeight, horiMinMat, horiMinInd)			
		self.printHoriSeam2(backTrackArrHori[0], img, imgWidth)

		
		del horiMinMat
		del horiMinInd
		return backTrackArrHori
		

		

		
		
	def removeHoriSeamOrg(self):	
		removed = copy.deepcopy(self.img)

		removedT = removed.transpose(1,0,2)

		
		removedT = removedT.tolist()
		for r in range(0, self.imgWidth):
			
			c = int(self.backTrackArrHori[r])
			del removedT[r][c]

			
		removedT = np.array(removedT)
		removed = removedT.transpose(1,0,2)

		self.imgHeight = self.imgHeight - 1
		self.img = removed

		
		

	def removeHoriSeam2(self, img, imgWidth, imgHeight, backTrackArrHori):	
		removed = img

		removedT = removed.transpose(1,0,2)

		
		removedT = removedT.tolist()
		for r in range(0, imgWidth):
			
			c = int(backTrackArrHori[0][r])
			del removedT[r][c]
			
		removedT = np.array(removedT)
		removed = removedT.transpose(1,0,2)

		imgHeight = imgHeight - 1
		img = removed
		return [img, imgWidth, imgHeight]
		

	def printHoriSeam(self,backTrackArr):	
		self.horiSeam = copy.deepcopy(self.img)
		for c in range(0, self.imgWidth):
				self.horiSeam[int(backTrackArr[c])][c][1] = 0
				self.horiSeam[int(backTrackArr[c])][c][0] = 0				
		cv2.imwrite('horiSeam.jpg', self.horiSeam)		
				


	def printHoriSeam2(self,backTrackArr, img, imgWidth):	
		horiSeam = img
		for c in range(0, imgWidth):
				horiSeam[int(backTrackArr[c])][c][1] = 0
				horiSeam[int(backTrackArr[c])][c][0] = 0				
		cv2.imwrite('horiSeam.jpg', horiSeam)		
				
				
				
				
	def backTrackHori(self):
		backTrackArrHori = [i for i in range(0, self.imgWidth)]
		Vals = [self.horiMinMat[i][-1] for i in range(0, self.imgHeight)]
		minVal = min(Vals)
		minInd = Vals.index(minVal)
		
		backTrackArrHori[-1] = minInd
		cIn = self.imgWidth-1
		
		while cIn > 0:
			rIn = self.horiMinInd[minInd][cIn]
			cIn = cIn -1
			backTrackArrHori[cIn] = rIn

			minInd = rIn
		
		return backTrackArrHori			

	

	
	
	
	def backTrackHori2(self, imgWidth, imgHeight, horiMinMat, horiMinInd):
		backTrackArrHori = [i for i in range(0, imgWidth)]
		Vals = [horiMinMat[i][-1] for i in range(0, imgHeight)]
		minVal = min(Vals)
		HseamE = minVal
		minInd = Vals.index(minVal)
		
		backTrackArrHori[-1] = minInd
		cIn = imgWidth-1
		
		while cIn > 0:
			rIn = horiMinInd[minInd][cIn]
			cIn = cIn -1
			backTrackArrHori[cIn] = rIn

			minInd = rIn

		
		return [backTrackArrHori, HseamE]			


		
		
	def identifyVerticalSeamOrg(self):
		# Initialize an M of the size of the image
		self.vertMinMat = copy.deepcopy(self.edgeBasedMeasure)
		self.vertMinInd = copy.deepcopy(self.edgeBasedMeasure)
		
		
		# For the topmost row, let the min energy be e(i,j) and store corresponding column number
		# already true
		self.vertMinInd[0] = [i for i in range(0,self.imgWidth)]
		
		# For subsequent rows, check if an index exists, find min + eij and store column number of min
		for  r in range(1, self.imgHeight):
			for c in range(0, self.imgWidth):
				if c >=1 and c <= self.imgWidth-2:
					
					Vals = [self.vertMinMat[r-1][c-1], self.vertMinMat[r-1][c], self.vertMinMat[r-1][c+1]] 
					minVal = min(Vals)
					minInd = Vals.index(minVal) + c-1
					self.vertMinMat[r][c] = self.vertMinMat[r][c] + minVal
					self.vertMinInd[r][c] = minInd
					
				elif c == 0:
					Vals = [self.vertMinMat[r-1][c], self.vertMinMat[r-1][c+1]] 
					minVal = min(Vals)
					minInd = Vals.index(minVal) + c
					self.vertMinMat[r][c] = self.vertMinMat[r][c] + minVal
					self.vertMinInd[r][c] = minInd
					
				elif c == self.imgWidth-1:
					Vals = [self.vertMinMat[r-1][c-1], self.vertMinMat[r-1][c]] 
					minVal = min(Vals)
					minInd = Vals.index(minVal) + c-1
					self.vertMinMat[r][c] = self.vertMinMat[r][c] + minVal
					self.vertMinInd[r][c] = minInd
		
	

		backTrackArr = self.backTrack()		

		self.printVertSeam(backTrackArr)
		self.backTrackArr = backTrackArr
		


	def identifyVerticalSeam2(self, edgeBasedMeasure, img, imgWidth, imgHeight):
		# Initialize an M of the size of the image
		vertMinMat = copy.deepcopy(edgeBasedMeasure)
		vertMinInd = copy.deepcopy(edgeBasedMeasure)
		
		
		# For the topmost row, let the min energy be e(i,j) and store corresponding column number
		# already true
		vertMinInd[0] = [i for i in range(0, imgWidth)]
		
		# For subsequent rows, check if an index exists, find min + eij and store column number of min
		for  r in range(1, imgHeight):
			for c in range(0, imgWidth):
				if c >=1 and c <= imgWidth-2:
					
					Vals = [vertMinMat[r-1][c-1], vertMinMat[r-1][c], vertMinMat[r-1][c+1]] 
					minVal = min(Vals)
					minInd = Vals.index(minVal) + c-1
					vertMinMat[r][c] = vertMinMat[r][c] + minVal
					vertMinInd[r][c] = minInd
					
				elif c == 0:
					Vals = [vertMinMat[r-1][c], vertMinMat[r-1][c+1]] 
					minVal = min(Vals)
					minInd = Vals.index(minVal) + c
					vertMinMat[r][c] = vertMinMat[r][c] + minVal
					vertMinInd[r][c] = minInd
					
				elif c == imgWidth-1:
					Vals = [vertMinMat[r-1][c-1], vertMinMat[r-1][c]] 
					minVal = min(Vals)
					minInd = Vals.index(minVal) + c-1
					vertMinMat[r][c] = vertMinMat[r][c] + minVal
					vertMinInd[r][c] = minInd
		
		

		backTrackArr = self.backTrack2(imgHeight, imgWidth, vertMinMat, vertMinInd)			
		self.printVertSeam2(backTrackArr, img, imgHeight)

		del vertMinMat
		del vertMinInd
		return backTrackArr 

		
	def printVertSeam2(self,backTrackArr, img, imgHeight):	
		vertSeam = img
		for r in range(0, imgHeight):
				vertSeam[r][int(backTrackArr[0][r])][1] = 0
				vertSeam[r][int(backTrackArr[0][r])][0] = 0				
		cv2.imwrite('vertSeam.jpg', vertSeam)		
				




		
	def printVertSeam(self,backTrackArr):	
		self.vertSeam = copy.deepcopy(self.img)

		for r in range(0, self.imgHeight):
			self.vertSeam[r][int(backTrackArr[r])][1] = 0
			self.vertSeam[r][int(backTrackArr[r])][0] = 0								
		cv2.imwrite('vertSeam.jpg', self.vertSeam)		
				
	

	def removeVerticalSeamOrg(self):
		removed = copy.deepcopy(self.img)
		removed = removed.tolist()
		for r in range(0, self.imgHeight):

				del removed[r][int(self.backTrackArr[r])]

		removed = np.array(removed)

		self.imgWidth = self.imgWidth - 1
		self.img = removed
	
	
	


	def removeVerticalSeam2(self, img, imgWidth ,imgHeight, backTrackArr):
		removed = img
		removed = removed.tolist()
		for r in range(0, imgHeight):

				del removed[r][int(backTrackArr[0][r])]

		removed = np.array(removed)
		cv2.imwrite('removed.jpg', removed)	
		imgWidth = imgWidth - 1
		img = removed
		return [img, imgWidth, imgHeight]
		
	
	
	def printImg2(self, img):
		cv2.imwrite('final.jpg', img)
	
	
	def printImg(self):
		cv2.imwrite('final.jpg', self.img)

		
	def backTrack(self):
		backTrackArr = [i for i in range(0, self.imgHeight)]
		Vals = [self.vertMinMat[-1][i] for i in range(0, self.imgWidth)]
		minVal = min(Vals)
		minInd = Vals.index(minVal)
		
		backTrackArr[-1] = minInd
		rIn = self.imgHeight-1
		
		while rIn > 0:
			cIn = self.vertMinInd[rIn][minInd]
			rIn = rIn -1
			backTrackArr[rIn] = cIn
			minInd = cIn
		
		return backTrackArr
		
		
		
	
	def backTrack2(self, imgHeight, imgWidth, vertMinMat, vertMinInd):
		backTrackArr = [i for i in range(0, imgHeight)]
		Vals = [vertMinMat[-1][i] for i in range(0, imgWidth)]
		minVal = min(Vals)
		seamE = minVal
		minInd = Vals.index(minVal)
		
		backTrackArr[-1] = minInd
		rIn = imgHeight-1
		
		while rIn > 0:
			cIn = vertMinInd[rIn][minInd]
			rIn = rIn -1
			backTrackArr[rIn] = cIn

			minInd = cIn
		
		return [backTrackArr, minVal]
		
		
	def optimalSeamsOrdering(self):
		# compute the optimal order through the transport map T
		# call funstion for that here
		
		self.computeTransportMap()
		
		self.printImg2(self.TransportImgs[self.numHoriSeams][self.numVertSeams])
		
		
		
		
		
		
	def retargetImage(self):
		# if no retargeting return
		if self.numHoriSeams == 0  and self.numVertSeams == 0:
			return	
			
		# identify whether to compress or expand in a given dim or none
		self.retargetBackTrack = []
		
		# set up for loop for number of seams
		for p in range(0, self.numHoriSeams + self.numVertSeams):
			self.retargetBackTrack.append(None)
			

		r = self.numHoriSeams-1
		c = self.numVertSeams-1
		for k in range(self.numHoriSeams + self.numVertSeams-1, -1, -1):
			vals = self.TransportMap[r][c][0:2]
			minInd = vals.index(self.TransportMap[r][c][2])
			pass
			
			
			
			
	def computeTransportMap(self):
		self.TransportMap = []
		self.TransportImgs = []
		self.EnergyMatrix = []
		
		for r in range(0,self.numHoriSeams+1):
			row = []
			for c in range(0,self.numVertSeams+1):
				row.append([0,0,0])
			self.TransportMap.append(row)
				
				
		for r in range(0,self.numHoriSeams+1):
			row = []
			for c in range(0,self.numVertSeams+1):
				row.append(None)
			self.TransportImgs.append(row)
			
		for r in range(0,self.numHoriSeams+1):
			row = []
			for c in range(0,self.numVertSeams+1):
				row.append(None)
			self.EnergyMatrix.append(row)	
		
		
		msg = '\n' + 'Details printed below simply correspond to progress in Transport Map calculation.'+ '\n' 
		print(msg)
		self.FillUpTEnergies(self.orgImg, self.imgWidth, self.imgHeight, 0, 0)		


		

	def updateEBMafterVSR(self, img, imgWidth, imgHeight, edgeBasedMeasure, cmin, cmax):
		
			cminN = cmin-1
			cmaxN = cmax

			edgeBasedMeasure = edgeBasedMeasure.tolist()

			for r in range(0, imgHeight):
				del edgeBasedMeasure[r][cmin]
			
			newE = calcEnergy3.calcEnergy3(img, imgWidth, imgHeight, edgeBasedMeasure, cminN, cmaxN)
			retE= newE.retE
			return retE
			
			
			
	def updateEBMafterHSR(self, img, imgWidth, imgHeight, edgeBasedMeasure, rmin, rmax):
		
			rminN = rmin-1
			rmaxN = rmax

			edgeBasedMeasureT = edgeBasedMeasure.transpose(1,0)
			edgeBasedMeasureT = edgeBasedMeasureT.tolist()

			for r in range(0, imgWidth):

				del edgeBasedMeasureT[r][rmin]
			
			edgeBasedMeasureT = np.array(edgeBasedMeasureT)
			edgeBasedMeasure = edgeBasedMeasureT.transpose(1,0)
			edgeBasedMeasure = edgeBasedMeasure.tolist()
			
			newE = calcEnergy4.calcEnergy4(img, imgWidth, imgHeight, edgeBasedMeasure, rminN, rmaxN)
			retE= newE.retE
			return retE
		
		


	def FillUpTEnergies(self, img, imgWidth, imgHeight, r, c):

		# Fill up first row first

		self.TransportImgs[0][0] = img
			
		for c in range(0, self.numVertSeams):
			# compute vertical energy map on this img
			print c
			if (self.EnergyMatrix[0][c] == None):		
				edgeBasedMeasure = self.calcEnergy2(img, imgWidth, imgHeight)
				self.EnergyMatrix[0][c] = edgeBasedMeasure
			else:
				edgeBasedMeasure = self.EnergyMatrix[0][c]
				

			# find best vertical seam and its energy
			backTrackArr = self.identifyVerticalSeam2(edgeBasedMeasure, img,imgWidth, imgHeight)
			# fill this energy into the element on the right

			self.TransportMap[0][c+1][0] = self.TransportMap[0][c][2] + backTrackArr[1]
			self.TransportMap[0][c+1][2] = self.TransportMap[0][c][2] + backTrackArr[1]
			# remove this vertical seam to get a new img
			retVal = self.removeVerticalSeam2(img, imgWidth, imgHeight, backTrackArr)

				
			self.TransportImgs[0][c+1] = retVal[0]

			img = retVal[0]
			imgWidth = retVal[1]
			imgHeight = retVal[2]
			cmin = int(min(backTrackArr[0]))
			cmax =  int(max(backTrackArr[0]))

			retE = self.updateEBMafterVSR(img, imgWidth, imgHeight, edgeBasedMeasure, cmin, cmax)
			self.EnergyMatrix[0][c+1] = retE

			
		img = self.TransportImgs[0][0]
		imgWidth = len(self.TransportImgs[0][0][0])
		imgHeight = len(self.TransportImgs[0][0]) 
		# Fill up first column next	
		for r in range(0, self.numHoriSeams):
			# compute horizontal energy map

			print r

			if (self.EnergyMatrix[r][0] == None):		
				edgeBasedMeasure = self.calcEnergy2(img, imgWidth, imgHeight)
				self.EnergyMatrix[r][0] = edgeBasedMeasure
			else:
				edgeBasedMeasure = self.EnergyMatrix[r][0]
			# find best horizontal seam and its energy
			backTrackArrHori = self.identifyHoriSeam2(edgeBasedMeasure, img, imgWidth, imgHeight)
			# fill this energy into the element on the bottom
			self.TransportMap[r+1][0][1] = self.TransportMap[r][0][2] + backTrackArrHori[1]
			self.TransportMap[r+1][0][2] = self.TransportMap[r][0][2] + backTrackArrHori[1]
			# remove this horizontal seam to get a new img
			retVal = self.removeHoriSeam2(img, imgWidth, imgHeight, backTrackArrHori)

			self.TransportImgs[r+1][0] = retVal[0]
			img = retVal[0]
			imgWidth = retVal[1]
			imgHeight = retVal[2]
			rmin = int(min(backTrackArrHori[0]))
			rmax =  int(max(backTrackArrHori[0]))

			retE = self.updateEBMafterHSR(img, imgWidth, imgHeight, edgeBasedMeasure, rmin, rmax)
			self.EnergyMatrix[r+1][0] = retE
			
			
			
		# Start from second row, second column and fill up row wise
		for r in range(1, self.numHoriSeams+1):
			for c in range(1, self.numVertSeams+1):
				print r, c
				
				img = self.TransportImgs[r-1][c] # remove a horizontal seam
				imgWidth = len(img[0])
				imgHeight = len(img) 
				# compute horizontal energy map
				if (self.EnergyMatrix[r-1][c] == None):
					edgeBasedMeasure = self.calcEnergy2(img, imgWidth, imgHeight)
					self.EnergyMatrix[r-1][c] = edgeBasedMeasure
				else:
					edgeBasedMeasure = self.EnergyMatrix[r-1][c]
				# find best horizontal seam and its energy
				backTrackArrHori = self.identifyHoriSeam2(edgeBasedMeasure, img, imgWidth, imgHeight)
				# fill this energy into the element on the bottom
				self.TransportMap[r][c][1] =  self.TransportMap[r-1][c][2] + backTrackArrHori[1]
				# remove this horizontal seam to get a new img
				retValH = self.removeHoriSeam2(img, imgWidth, imgHeight, backTrackArrHori)


				img = retValH[0]
				imgWidth = retValH[1]
				imgHeight = retValH[2]
				rmin = int(min(backTrackArrHori[0]))
				rmax =  int(max(backTrackArrHori[0]))
				retE = self.updateEBMafterHSR(img, imgWidth, imgHeight, edgeBasedMeasure, rmin, rmax)
				energyMatrixAfterHSR = retE
				
				img = self.TransportImgs[r][c-1] # remove a vert seam
				imgWidth = len(img[0])
				imgHeight = len(img)
				# compute vertical energy map on this img
				if (self.EnergyMatrix[r][c-1] == None):
					edgeBasedMeasure = self.calcEnergy2(img, imgWidth, imgHeight)
					self.EnergyMatrix[r][c-1] = edgeBasedMeasure
				else:
					edgeBasedMeasure = self.EnergyMatrix[r][c-1]
				# find best vertical seam and its energy
				backTrackArr = self.identifyVerticalSeam2(edgeBasedMeasure, img,imgWidth, imgHeight)
				# fill this energy into the element on the right
				self.TransportMap[r][c][0] = self.TransportMap[r][c-1][2] + backTrackArr[1]
				# remove this vertical seam to get a new img
				retValV = self.removeVerticalSeam2(img, imgWidth, imgHeight, backTrackArr)


				img = retValV[0]
				imgWidth = retValV[1]
				imgHeight = retValV[2]
				cmin = int(min(backTrackArr[0]))
				cmax =  int(max(backTrackArr[0]))

				retE = self.updateEBMafterVSR(img, imgWidth, imgHeight, edgeBasedMeasure, cmin, cmax)
				energyMatrixAfterVSR = retE
				
				# fill up the minimum
				vals = [self.TransportMap[r][c][0], self.TransportMap[r][c][1]]
				minVal = min(vals)
				minInd = vals.index(minVal)
				self.TransportMap[r][c][2] = minVal
				# fill the right img
				if minInd == 0:
					self.TransportImgs[r][c] = retValV[0]
					self.EnergyMatrix[r][c] = energyMatrixAfterVSR
					
				
				elif minInd == 1:
					self.TransportImgs[r][c] = retValH[0]
					self.EnergyMatrix[r][c] = energyMatrixAfterHSR


			
		
msg = '\n' + 'Enter the name of the image file to retarget. (eg format: butterfly.jpg)'+ '\n' +'Please make sure the image is in the same folder as this python script: '			
imgFileName = raw_input(msg)	
seamCarving(imgFileName)






