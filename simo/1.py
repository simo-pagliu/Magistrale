#any function needs ()
#strings "" or ''
print("Hi Bitch")

#multiline string by using triple double quotes """ """
print("""ola ehi
another line 
yet another line but it's tabbed""")

#string concatenation
print("first string" + "second string" + "\nthird line, on a new line")

#you can litteraly multiplicate strings...that's cool
print("CIAO \n" * 5)



#input function ALWAYS CONVERTED TO STRING
question = input("Question?\n")

#concatenation with variables ((easy as that since input function saves input as string))
print("you just typed " + question)

#to determine the variable type
var_type = type(question)
print(var_type)

#elevamento a potenza... è un pò particolare :)
print(2**3)

#data convertion
number = input("write a number")
#it's saved as a string
number = 23 + int(number)
number = str(number)
print("it's " + number)

#if statement
# == <= >= < >
number = int(number)
if number == 26:
 print("yep, that's 26")
 exit() #exits the program
elif number < 26: #else if era troppo lungo zio pero
 print("nope, it's not 26")
else:
 print("it's higer then 26")
#IDENTATION IS IMPORTANT THE INDENTATION TEXT IS THE STATEMENT !!!!!

print("test") #this won't show up if its 26

#nested ifs
if number > 26 or number < 26:
 is_odd = number % 2 #SOLITO TEST DEL PARI O DISPARI :)
 if is_odd == 0:
  print("PARI")
 else:
  print("dispari")


#LOGICAL OPERATORS
  #THEY ARE LITTERALY THE THING !!!!!!!!
  #or
  #and
  #not --> if not number == 26

#Lists DIFFERENT TYPES OF VARIABLES
list = ["a", 34, "c", 23.5432]
fourth = list[3] #gli indici sono normali non come zio matlab :(
fourth = list[-1] #you can use negative indexes to easier addres the last items, in this case the last item is @ -1
print(fourth)

#add to a list
#append
#using a method (like function but for objects)
list.append("suca")
list.insert(3, "mmm")
list.extend(["another", "list", 4])
#or list + [the other list]
list.reverse
list.sort #ordina la lista
list.remove("mmm") #you have to specify the actual value to be removed
list.pop(3) #removes things by specifing the index
print(list.index("suca")) #returns the index of a given element
print(list.count("B")) #counts how many given element there are in the list
#list.clear() just removes everything...


print(list)


#tuple, techniccally different from lists
#a tuple is not changable
tuples = ("Hi", 3)

#to time things:)
import timeit
print(timeit.timeit(stmt='["hi", "well", 4]', number=1000000))
print(timeit.timeit(stmt='("hi", "well", 4)', number=1000000))

#TUPLES ARE FASTER (by a lot) then lists beacuse of the way it access memory)7
#usually in a tuple you use different types of variables and use it more like a struct then an array
#some times it's the output of some modules or methods or functions

#hei = 1, --> putting a comma makes it a TUPLE !!!

#NotaBene
list_or_tuple = ("A", 1, "meow")
(lettera, numero, verso) = list_or_tuple
print(lettera)
print(numero)
print(verso)


#Lastly there are SETS
set = {"a", "c", "b"}
print(set)
#you can add or remove elements
#otherwise can't be changed
#the order doesn't matter, it random every time it runs !!!
#NO DUPLICATES ALLOWED
#YOU CAN'T USE INDEXES IN SETS

print(len(set))
print("ciaone" in set) #that's how you look for elements
# every second element [::2]
# from to [0:3]
# from to with a step [1::3]
# backwards [::-1]

#print every element separated
for x in set:
 print(x)

