"""
This Python code is based on Java code by Lee Jacobson found in an article
entitled "Applying a genetic algorithm to the travelling salesman problem"
that can be found at: http://goo.gl/cJEY1
"""

import math
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

#Se crea un objeto tipo ciudad con los parametros "x" e "y" de sus coordenadas. Si uno es nulo, se genera valores aleatorios
class City:
   def __init__(self, x=None, y=None):
      self.x = None
      self.y = None
      if x is not None:
         self.x = x
      else:
         self.x = int(random.random() * 200)
      if y is not None:
         self.y = y
      else:
         self.y = int(random.random() * 200)
   
   def getX(self):
      return self.x
   
   def getY(self):
      return self.y
   
   def distanceTo(self, city):
      xDistance = abs(self.getX() - city.getX())
      yDistance = abs(self.getY() - city.getY())
      distance = math.sqrt( (xDistance*xDistance) + (yDistance*yDistance) )
      return distance
   
   def __repr__(self):
      return str(self.getX()) + ", " + str(self.getY())


class TourManager:
   destinationCities = []
   
   def addCity(self, city):
      self.destinationCities.append(city)
   
   def getCity(self, index):
      return self.destinationCities[index]
   
   def numberOfCities(self):
      return len(self.destinationCities)


class Tour:
   def __init__(self, tourmanager, tour=None):
      self.tourmanager = tourmanager
      self.tour = []
      self.fitness = 0.0
      self.distance = 0
      if tour is not None:
         self.tour = tour
      else:
         for i in range(0, self.tourmanager.numberOfCities()):
            self.tour.append(None)
   
   def __len__(self):
      return len(self.tour)
   
   def __getitem__(self, index):
      return self.tour[index]
   
   def __setitem__(self, key, value):
      self.tour[key] = value
   
   def __repr__(self):
      geneString = "|"
      for i in range(0, self.tourSize()):
         geneString += str(self.getCity(i)) + "|"
      return geneString
   
   def generateIndividual(self):
      for cityIndex in range(0, self.tourmanager.numberOfCities()):
         self.setCity(cityIndex, self.tourmanager.getCity(cityIndex))
      #Cambia las posiciones al azar del array
      random.shuffle(self.tour)
   
   def getCity(self, tourPosition):
      return self.tour[tourPosition]
   
   def setCity(self, tourPosition, city):
      self.tour[tourPosition] = city
      self.fitness = 0.0
      self.distance = 0
   
   def getFitness(self):
      if self.fitness == 0:
         self.fitness = 1/float(self.getDistance())
      return self.fitness
   
   def getDistance(self):
      if self.distance == 0:
         tourDistance = 0
         for cityIndex in range(0, self.tourSize()):
            fromCity = self.getCity(cityIndex)
            destinationCity = None
            if cityIndex+1 < self.tourSize():
               destinationCity = self.getCity(cityIndex+1)
            else:
               destinationCity = self.getCity(0)
            tourDistance += fromCity.distanceTo(destinationCity)
         self.distance = tourDistance
      return self.distance
   
   def tourSize(self):
      return len(self.tour)
   
   def containsCity(self, city):
      return city in self.tour


class Population:
   def __init__(self, tourmanager, populationSize, initialise):
      self.tours = []
      for i in range(0, populationSize):
         self.tours.append(None)
      
      if initialise:
         for i in range(0, populationSize):
            # se crea un objeto tour de nombre newtour y se crea un array tour del tamanio del numero de ciudades
            newTour = Tour(tourmanager)
            newTour.generateIndividual()
            self.saveTour(i, newTour)
      
   def __setitem__(self, key, value):
      self.tours[key] = value
   
   def __getitem__(self, index):
      return self.tours[index]
   
   def saveTour(self, index, tour):
      self.tours[index] = tour
   
   def getTour(self, index):
      return self.tours[index]
   
   def getFittest(self):
      fittest = self.tours[0]
      for i in range(0, self.populationSize()):
         # Si es mas optimo, se cambia de tour
         if fittest.getFitness() <= self.getTour(i).getFitness():
            fittest = self.getTour(i)
      return fittest
   
   def populationSize(self):
      return len(self.tours)


class GA:
  def __init__(self, tourmanager):
      self.tourmanager = tourmanager
      self.mutationRate = 0.02
      self.tournamentSize = 5
      self.elitism = True
      self.valor=0
   
  def evolvePopulation(self, pop):
      newPopulation = Population(self.tourmanager, pop.populationSize(), False)
      elitismOffset = 0
      if self.elitism:
         newPopulation.saveTour(0, pop.getFittest())
         elitismOffset = 1
      
      for i in range(elitismOffset, newPopulation.populationSize()):
         parent1 = self.tournamentSelection(pop)
         parent2 = self.tournamentSelection(pop)
         child = self.crossover(parent1, parent2)
         newPopulation.saveTour(i, child)
      
      for i in range(elitismOffset, newPopulation.populationSize()):
         self.mutate(newPopulation.getTour(i),pop)
      
      return newPopulation
   
  def crossover(self, parent1, parent2):
      child = Tour(self.tourmanager)
      
      startPos = int(random.random() * parent1.tourSize())
      endPos = int(random.random() * parent1.tourSize())
      
      for i in range(0, child.tourSize()):
         if startPos < endPos and i > startPos and i < endPos:
            child.setCity(i, parent1.getCity(i))
         elif startPos > endPos:
            if not (i < startPos and i > endPos):
               child.setCity(i, parent1.getCity(i))
      for i in range(0, parent2.tourSize()):
         if not child.containsCity(parent2.getCity(i)):
            for ii in range(0, child.tourSize()):
               if child.getCity(ii) == None:
                  child.setCity(ii, parent2.getCity(i))
                  break
      
      return child
   
  def mutate(self, tour, pop):
    for tourPos1 in range(0, tour.tourSize()):
      if random.random() < self.mutationRate:
        condi=False
        asd=False
        while condi==False:
          cont=0
          tourPos2 = int(tour.tourSize() * random.random())
          city1 = tour.getCity(tourPos1)
          city2 = tour.getCity(tourPos2)
          tour.setCity(tourPos2, city1)
          tour.setCity(tourPos1, city2)
          # Validando si existe la misma ruta
          for i in range(0,pop.populationSize()):
            if pop.getTour(i)==tour:
              cont+=1
              break
          # Validando que no existan rutas iguales desde inicios diferentes
          repetido=False
          if cont==0:
            for ii in range(0,pop.populationSize()):
              for iii in range(0,pop.getTour(ii).tourSize()):
                for j in range(0,tour.tourSize()):
                  tour1=[]
                  tour2=[]
                  if pop.getTour(ii).getCity(iii)==tour.getCity(j):
                    for a in range(j,tour.tourSize()):
                      tour1.append(tour.getCity(a))
                    for c in range(0,j-1):
                      tour1.append(tour.getCity(c))
                    for b in range(iii,pop.getTour(iii).tourSize()):
                      tour2.append(pop.getTour(iii).getCity(b))
                    for d in range(0,iii-1):
                      tour2.append(pop.getTour(iii).getCity(d))
                    if tour1==tour2:
                      repetido=True
                      break
          # Validando que no haya cruces de rutas
          cruce=False
          cont_cruce=0
          if cont==0 and repetido==False:
            for i in range(0,tour.tourSize()):
              #if i<tour.tourSize()-1:
                if tourPos1+2<tour.tourSize():
                  if i<tourPos1 or tourPos1+2<i :
                    cruce=self.interseccion(
                      tour.getCity(tourPos1).getX(), tour.getCity(tourPos1).getY(), 
                      tour.getCity(tourPos1+1).getX(), tour.getCity(tourPos1+1).getY(), 
                      tour.getCity(tourPos1+2).getX(), tour.getCity(tourPos1+2).getY(), 
                      tour.getCity(i).getX(), tour.getCity(i).getY())
                if cruce==True:
                    ciudad1=tour.getCity(tourPos1+1)
                    cuidad2=tour.getCity(i)
                    tour.setCity(i, ciudad1)
                    tour.setCity(tourPos1+1, cuidad2)
                    cont_cruce+=1
                if cont_cruce>0:
                    break        
          # solo si no hay ningun repetido, se sale del bucle y pasa a la siguiente evolucion  
          if cont==0 and repetido==False and cont_cruce==0:
            condi=True

  def interseccion(self,x1,y1,x2,y2,xa1,ya2,xb1,yb2):
    if x2-x1>0:
      m=(y2-y1)/(x2-x1)
      b=y2-m*x2
      ycxa1=m*xa1+b
      ycxb1=m*xb1+b
      if (ycxa1<ya2 and ycxb1>yb2) or (ycxa1>ya2 and ycxb1<yb2):
          return True
      else:
          return False
    else:
      return False

  def tournamentSelection(self, pop):
      tournament = Population(self.tourmanager, self.tournamentSize, False)
      numram=0
      while (numram>0 and numram<pop.populationSize()-self.tourmanager):
        numram=int(random.random()*pop.populationSize())
      for i in range(0, self.tournamentSize):
         tournament.saveTour(i, pop.getTour(numram))
         numram+=1
      fittest = tournament.getFittest()
      return fittest

def main():
  # Se crea el contenedor de las rutas posibles
  tourmanager = TourManager()
  # Creamos las ciudades
  city = City(60, 200)
  tourmanager.addCity(city)
  city2 = City(180, 200)
  tourmanager.addCity(city2)
  city3 = City(80, 180)
  tourmanager.addCity(city3)
  city4 = City(140, 180)
  tourmanager.addCity(city4)
  city5 = City(20, 160)
  tourmanager.addCity(city5)
  city6 = City(100, 160)
  tourmanager.addCity(city6)
  city7 = City(200, 160)
  tourmanager.addCity(city7)
  city8 = City(140, 140)
  tourmanager.addCity(city8)
  city9 = City(40, 120)
  tourmanager.addCity(city9)
  city10 = City(100, 120)
  tourmanager.addCity(city10)
  city11 = City(180, 100)
  tourmanager.addCity(city11)
  city12 = City(60, 80)
  tourmanager.addCity(city12)
  city13 = City(120, 80)
  tourmanager.addCity(city13)
  city14 = City(180, 60)
  tourmanager.addCity(city14)
  city15 = City(20, 40)
  tourmanager.addCity(city15)
  city16 = City(100, 40)
  tourmanager.addCity(city16)
  city17 = City(200, 40)
  tourmanager.addCity(city17)
  city18 = City(20, 20)
  tourmanager.addCity(city18)
  city19 = City(60, 20)
  tourmanager.addCity(city19)
  city20 = City(160, 20)
  tourmanager.addCity(city20)
      
  # Creamos la poblacion inicial
  pop = Population(tourmanager, 50, True);
  # Se calcula la ruta optima antes de las mutaciones
  print "Initial distance: " + str(pop.getFittest().getDistance())
  print pop.getFittest()
  print " "
  varX=[]
  varY=[]
  for i in range(0,pop.getFittest().tourSize()):
    varX.append(pop.getFittest().getCity(i).getX())
    varY.append(pop.getFittest().getCity(i).getY())
  varX.append(pop.getFittest().getCity(0).getX())
  varY.append(pop.getFittest().getCity(0).getY())
  plt.plot(varX,varY)
  plt.show()

  # Evolucionar la poblacion para 100 generaciones
  ga = GA(tourmanager)
  for i in range(0, 100):
    pop = ga.evolvePopulation(pop)
    print i

  # Resultados finales
  print "Finished"
  print "Final distance: " + str(pop.getFittest().getDistance())
  print "Solution:"
  print pop.getFittest()
  varX=[]
  varY=[]
  for i in range(0,pop.getFittest().tourSize()):
    varX.append(pop.getFittest().getCity(i).getX())
    varY.append(pop.getFittest().getCity(i).getY())
  varX.append(pop.getFittest().getCity(0).getX())
  varY.append(pop.getFittest().getCity(0).getY())
  plt.plot(varX,varY)
  plt.show()

if __name__ == '__main__':
   main()