# RareHacks

## Getting Started

- **Front-end**

This project is a starting point for a Flutter application.

1. Install [Android Studio](https://developer.android.com/studio) and set it up with [Flutter](https://flutter.dev/docs/get-started/editor). 
2. Git clone this repository
3. Open Android Studio and in the menu "Open an existing Android Studio project" and select the folder of the project.
4. Ready to go!

- **Back-end**

The algorithms of this projects are going to be programmed in Python 3 using the IDE PyCharm.

1. Install [PyCharm](https://www.jetbrains.com/pycharm/download/#section=windows).
2. Create the virtual environment: File->Settings->Project->Project interpreter->Click next to projec interpreter->show all-> + -> "create your environment" -> Ok -> Apply -> Ok


## Errors 

- **ModuleNotFoundError**: File->Settings->Project->Project interpreter-> Interpreter paths -> "Add path with the error" -> Ok -> Apply

- **Can not run Git**: Download git


## Methodology

- Classes structure:
First letter in uppercase. One single word (noun).
```python
class Person:
  """
  Atributes:
    age: [type, description]: int, indicates how old is the person.
    gender: str, (M or F) indicates if its male or famale.
  
  """
  def __init__(self, age, gender):
    self.age = age
    self.gender = gender
 ```
- Functions structure

First letter in uppercase of each word except the first one. First word has to be a verb indication what returns the function.
```python
def getNumberPopulation(place, data): 
  """
  Function that gets the place and all the raw data and returns the population of that place.
  Atributes:
    place: string, indicates the name of the place.
    data: array matrix (mxn), the columns are [sthng, sthng, sthng].
  Returns:
    num_population: float, indicates the number of that population. 
  """
  ```
  - Variables:
  
All the words in lowercase and separate by a lowbar
```python
som_new_variable = sthng
```
