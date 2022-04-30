# Specifikation

## Inledning
Jag kommer programmera en scen där ett klot belyses av ljus och skuggar en yta. Ljuset är idealiserat: vågorna antas vara parallella. Programmet kommer ha en fil som innehåller alla matematiska funktioner som behövs. Utöver detta kommer det finnas två olika delprogram som använder dessa funktioner för att illustrera klotet på var sitt sätt. 
Det ena programmet kommer skapa en bild i kommandoterminalen med hjälp av olika ASCII-symboler. Den andra kommer skapa en bild i ett grafikfönster. Användaren kommer kunna ändra riktning på ljuset.

En av de största utmaningarna med uppgiften är att rita skuggan av klotet på det bakomliggande planet på ett någorlunda effektivt sätt. Detta kommer bli svårt eftersom varje punkt på sfären kan skugga en, flera eller inga punkter på planet, beroende på hur ljuset faller in mot punkten. Alltså måste man utgå från punkterna på planet som skuggas undersöka skuggan hos varje punkt som uppfyller något randvilkor (exempelvis att ligga inom koordinatsystemet).

# Användarscenarier

Kalle undersöker projektioner, i synnerhet skuggan av tredimensionella objekt på plan. Kalle kör programmet som ritar klotet i ett grafikfönster. Han klickar en gång på den högra delen av klotet och ljuset ändrar riktning så att belysningen blir som störst där han just klickat. Skuggan hamnar samtidigt på motsatt sida av klotet.
Av misstag råkar Kalle klicka på bilden utanför klotet. Som tur var reagerar programmet endast på korrekta klickningar.

# Kodskelett
## Klasser
```
class Sphere:
    """Defines a sphere with center at origin and arbitrary radius."""
    def __init__(self, radius):

    def on_sphere(self, xy_tuple):
        """"If possible, returns z so that (x,y,z) is on the surface of the sphere. Else, returns False."""
        
        
    def within_sphere(self, coords):
        """Returns true if coords are within the sphere. Else, returns False."""
        
        
class LightVector:
    """Defines a vector from origin to the surface of a sphere. Also contains a corresponding direction-vector of length unity."""
    def __init__(self, sphere, xy_tuple):
    
    def change_coords(self, xy_tuple):
        """Redefines the vector according to new coordinates"""
    
class Matrix:
    """Defines a matrix centered around the origin."""
    def __init__(self, width, height):
    
class Gui:
    """Creates a Gui that can display images and bind callbacks to functions."""
    def __init__(self, width, height):
        
        
    def new_image(self, width, height):
        """Deletes existing picture and creates a new blank one."""
```    
## Matematiska funktioner
```
def dot_product(vector_1, vector_2):
    """Defines the dot-product of two threedimensional vectors."""


def vector_addition(vector_1, vector_2):
    """Defines addition of two threedimensional vectors."""
    

def scalar_multiplication(scalar, vector_1):
    """Defines multiplication of vector with scalar."""


def coord_illumnation(sphere, light, coords):
    """Determines the illumination value between 0 and 1 of a coordinate on the surface of the sphere."""
 
```
## Grafikfönster
```

def is_shadowed(sphere, light, coords):
    """Determines if the coordinate is shadowed by the cross section of the sphere orthogonal to lights direction. If shadowed, returns True. Else, False"""
    
Grafikfönster:

def hexcolor(denary):
    """Creates a hexcolor on a greyscale. Returns a string on the format #ABABAB, where AB is a hexnumber."""


def draw_shadow(sphere, light, img):
    """Draws the shadow cast by sphere on the xy-plane. Returns None"""


def draw_sphere(sphere, light, img):
    """Draws the sphere. Every coordinate has a color depending on the level of illumination. Returns None"""

def click(event, sphere, light, gui):
    """Changes light postition and draws new sphere if user has clicked within the sphere. Returns None"""

def main():
  """Creates gui, sphere and light. Draws scene and binds left mousebutton to click(). Returns None, end of program."""
```

## Terminal (ASCII-symboler)
```
def light_symbol(illumination):
    """Returns appropriate symbol for given illumination as a string."""


def draw_shadow(sphere, light, matrix):
    """Draws the shadow cast by the sphere onto the xy-plane. Returns None"""


def draw_sphere(sphere, light, matrix):
    """Draws the illuminated sphere. Returns None"""


def print_matrix(matrix):
    """Prints each row of the matrix to create the a picture. Returns None"""
    
    
def main():
    """Creates a matrix, a sphere and a light vector. Prints a picture of the scene. Returns None, end of program"""
```
# Programflöde och dataflöde

## Grafikfönster
Programmet börjar med att skapa en canvas med given höjd och bredd, ett klot med centrum i origo och given radie, samt en ljusvektor. 
Därefter undersöks alla tänkbara skuggade koordinater; om en koordinat är skuggad färgas den grå (se Skugga). 
Sist undersöks alla punkter där x,y ligger mellan negativ sfärens radie och positiv sfärens radie; om en punkt visar sig ligga på sfärens beräknas dess belysning som ett värde mellan 0 och 1 (se Klot). Varje belyst klot tilldelas en grå nyans baserat på des belysning. 0 ger svar och 1 ger vitt. Koordinaten färgläggs med färgen.

## Terminal
Programmet skapar en ett objekt av type matrix med given bredd och höjd, ett klot med centrum i origo och given radie, samt en ljusvektor. Liksom i Grafikfönster undersöks alla koordinater som kan vara skuggade. Alla platser i den skapade matrisen som korresponderar till en skuggad koordinat tilldelas värdet " ' ". Därefter beräknas belysningen för samtliga punker på sfären. Beroende på belysning tilldelas de olika koorinaterna olika teken. Slutligen printas varje rad a matrisen.

## Skugga
Vektorn från origo till koordinaten projiceras på ljusvektorn. Den nya vektorn subtraheras från koordinaten. Den punkt som återfås ligger garanterat på det plan som är ortogonalt mot ljusvektorn och går igenom origo. 
Programmet undersöker ifall denna punkt ligger inom sfären med hjälp av avståndsformeln. Ifall den gör det är den ursprungliga koordinaten skuggad om färgas grått.

## Klot
För given (x,y) bestäms om möjligt positiva z så att (x,y,z) ligger på sfärens yta. Därefter beräknas skalärprodukten av vektorn som pekar på punkten och ljusvektorn. Värdet blir alltid mellan -1 och 1, men eftersom belysningen inte kan vara negativ sätts alla negativa belysningar till 0.


