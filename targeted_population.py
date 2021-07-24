
import random
from samplingrule.samplingrule import dowellsamplingrule
from distribution.distribution import dowelldistribution


def dowelltargetedpopulation():

    #Define the type of data as variable "d"

    #Define the type of data as variable "d"
    database=input()

    #Define number of stages as variable "S"
    stages=number_of_stage_input()

    first_stage()
    stages=stages-1

    #Simulate all the stges
    for i in range(0,stages):
        
        d=a_stage()
        if d==0:
            break
        elif d==1:
           length_selected()
        elif d==2:
            area_selected()
        elif d==3:
            volume_selected()
        elif d==4:
            weight_selected()
        elif d==5:
            time_selected()
            pass
        elif d==6:
            quantity_selected()
        elif d==7:
            lot_seleceted()

        dowellsamplingrule()
        print("Enter distribution type")
        D=int(input())
        dowelldistribution(D)
        """ yet to implement """
        #dowellenventcreation()
        


def lot_selected():
     #dowellsuffle_function()
     
    #define lot size as l
    #l=int(input())
    print("Selecet, 1.Proportion, 2.Random generation.")
    sleceted=int(input())
    
    if selected==1:
        print("What proportion of dataset to be selected as lot?")
        p=int(input())
    else:
        l=random.randint(0,9)
    F=int(input())
    L=int(input())
    
    if L-F != l:
        print("Seelection not matching required lot size")
        return
            		
        

def quantity_selected():
    print("selecet an option")
    print("1. Maximum Piont") 
    print("2. Print Population average")
    
    selected=int(input())
    #define the maximum point as variable "m"
    #Input from frontend programmer or user		
    if selected == 1:
        m=int(input())
    #if population average is selected
    #define population average as a
    elif selected==2:
        A=int(input())

	#define range of selection as variable "r"			
	#Input from frontend programmer or user
    r = int(input())

	#Select the start point of the range "r"			
	#Input from frontend programmer or user	
    start_point= int(input())
	#Select the end point of the range "r"			
	#Input from frontend programmer or user	
    end_point=int(input())	
	#Define number of units to be selected in range "r" as variable "a"("a" number of units to be selected within the range "r")			
	#Input from frontend programmer or user	
    a=int(input())
	#check if "a" is non- negative ,then continue			
	#otherwise prompt " number of units cannot be negative"	
    if a<0:
        print("number of units cannot be negative")
        	
	#Note:"a" should not be more than the total units in selected range			
                    

def weight_selected():
    print("selecet an option")
    print("1. Maximum Piont") 
    print("2. Print Population average")
    
    selected=int(input())
    #define the maximum point as variable "m"
    #Input from frontend programmer or user		
    if selected == 1:
        m=int(input())
    #if population average is selected
    #define population average as a
    elif selected==2:
        A=int(input())

	#define range of selection as variable "r"			
	#Input from frontend programmer or user
    r = int(input())

	#Select the start point of the range "r"			
	#Input from frontend programmer or user	
    start_point= int(input())
	#Select the end point of the range "r"			
	#Input from frontend programmer or user	
    end_point=int(input())	
	#Define number of units to be selected in range "r" as variable "a"("a" number of units to be selected within the range "r")			
	#Input from frontend programmer or user	
    a=int(input())
	#check if "a" is non- negative ,then continue			
	#otherwise prompt " number of units cannot be negative"	
    if a<0:
        print("number of units cannot be negative")
        	
	#Note:"a" should not be more than the total units in selected range			
                    

def volume_selected():
    print("selecet an option")
    print("1. Maximum Piont") 
    print("2. Print Population average")
    
    selected=int(input())
    #define the maximum point as variable "m"
    #Input from frontend programmer or user		
    if selected == 1:
        m=int(input())
    #if population average is selected
    #define population average as a
    elif selected==2:
        A=int(input())

	#define range of selection as variable "r"			
	#Input from frontend programmer or user
    r = int(input())

	#Select the start point of the range "r"			
	#Input from frontend programmer or user	
    start_point= int(input())
	#Select the end point of the range "r"			
	#Input from frontend programmer or user	
    end_point=int(input())	
	#Define number of units to be selected in range "r" as variable "a"("a" number of units to be selected within the range "r")			
	#Input from frontend programmer or user	
    a=int(input())
	#check if "a" is non- negative ,then continue			
	#otherwise prompt " number of units cannot be negative"	
    if a<0:
        print("number of units cannot be negative")
        	
	#Note:"a" should not be more than the total units in selected range			
                    

def area_selected():
    print("selecet an option")
    print("1. Maximum Piont") 
    print("2. Print Population average")
    
    selected=int(input())
    #define the maximum point as variable "m"
    #Input from frontend programmer or user		
    if selected == 1:
        m=int(input())
    #if population average is selected
    #define population average as a
    elif selected==2:
        A=int(input())

	#define range of selection as variable "r"			
	#Input from frontend programmer or user
    r = int(input())

	#Select the start point of the range "r"			
	#Input from frontend programmer or user	
    start_point= int(input())
	#Select the end point of the range "r"			
	#Input from frontend programmer or user	
    end_point=int(input())	
	#Define number of units to be selected in range "r" as variable "a"("a" number of units to be selected within the range "r")			
	#Input from frontend programmer or user	
    a=int(input())
	#check if "a" is non- negative ,then continue			
	#otherwise prompt " number of units cannot be negative"	
    if a<0:
        print("number of units cannot be negative")
        	
	#Note:"a" should not be more than the total units in selected range			
                    


def length_selected():
    print("selecet an option")
    print("1. Maximum Piont") 
    print("2. Print Population average")
    
    selected=int(input())
    #define the maximum point as variable "m"
    #Input from frontend programmer or user		
    if selected == 1:
        m=int(input())
    #if population average is selected
    #define population average as a
    elif selected==2:
        A=int(input())

	#define range of selection as variable "r"			
	#Input from frontend programmer or user
    r = int(input())

	#Select the start point of the range "r"			
	#Input from frontend programmer or user	
    start_point= int(input())
	#Select the end point of the range "r"			
	#Input from frontend programmer or user	
    end_point=int(input())	
	#Define number of units to be selected in range "r" as variable "a"("a" number of units to be selected within the range "r")			
	#Input from frontend programmer or user	
    a=int(input())
	#check if "a" is non- negative ,then continue			
	#otherwise prompt " number of units cannot be negative"	
    if a<0:
        print("number of units cannot be negative")
        	
	#Note:"a" should not be more than the total units in selected range			
              

def first_stage():
					
	#Select "d"					
	#Display a list " length(1),area(2),volume(3),weight(4),time(5),quantity(6),lot(7)"
    print("length(1),area(2),volume(3),weight(4),time(5),quantity(6),lot(7)")
    d=int(input())
    #if time selected at first stage
    if d==5:
        time_selected()
    return
        
        
    
def a_stage(): 
					
	#Select "d"					
	#Display a list " length(1),area(2),volume(3),weight(4),time(5),quantity(6),lot(7)"
    print("length(1),area(2),volume(3),weight(4),time(5),quantity(6),lot(7)")
    d=int(input())
    return d
       

def number_of_stage_input(): 
    print('Enter Number of stages')
    s=int(input())
    return s 


def time_selected():

    print("Enter start Point")
    start_point=input()
    print("Enter end point")
    end_point=input()


dowelltargetedpopulation()
