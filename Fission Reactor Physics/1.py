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
list.clear() 

#tuple, techniccally different from lists
#a tuple is not changable
tuples = ("Hi", 3)



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

