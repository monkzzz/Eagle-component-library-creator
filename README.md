# Eagle component library creator

## Description
Autodesk Eagle stores it's component library details in a lbr file, which is usually created by the library creation option in the software.

The library creation option is not difficult to use, however for simple designs or someone new to the software it can lead to simple mistakes or taking too long for it to be created.

The ideia behind this program is to be a simpler Autodesk Eagle component library creator, using only some command line inputs which then creates the lbr file to be imported by the Autodesk Eagle software.

For now it only creates a library for a single component in a small list of IC packages , but the objective is to diversify to have more package types.

## Features
- Supports Single Package SMT components ( SIL )

- Supports Small Outline Package components ( DFN, DIL, SOIC, SOJ, SON, PSON, WSON, USON, SOP, CSOP, DSOP, HSOP, SSOP, TSOP, HTSOP, VSOP, TVSOP, MSOP, PSOP, QSOP, SSOP, HSSOP,  TSSOP, VSSOP, HTSSOP, TSOP)

- Supports Quad Flat Package components ( DFN, QFN, PQFN, UQFN, VQFN, HVQFN, WQFN, CFP, QFP,  BQFP, CQFP, LQFP, MQFP, PQFP, TQFP, ETQFP, VQFP)

- Creates the component library.

- Creates the component symbol.

- Creates the component footprint.

## Usage
The program asks for information to create the library, some is required other is opcional.
All the measurements inserted must be in milimeters.

Most are pretty self-explanatory but some may can be confusing, especially the measurements.

### Example
We will use the common 555 timer ic in a SOIC package as an example:
(Datasheet in example folder).

```

Question 1:
- What is the name of the library? (required)
timer_555

Question 2:
- What is the name of the component? (required)
LM555CM

Question 3:
- What is the value of the component? (optional)

Question 4:
- What is the description? (optional)
IC OSC SINGLE TIMER 8-SOP

Question 5:
- What is the link to the datasheet? (optional)
https://www.onsemi.com/pub/Collateral/LM555-D.pdf

Question 6:
- What is the package? (required)
SOIC

Question 7:
- How many pins does it have? (required)
8

Question 8:
- Does it have a Bottom/Center/Thermal pad? (required)
n

Question 9:
- What is the lenght(L)? (mm) (required)
4.90

Question 10:
- What is the width(W)? (mm) (required)
3.90

Question 11:
- How much is the spacing(S) between pins? (mm) (required)
1.27

Question 12:
- How much is the length of the pad? (mm) (required)
1.75

Question 13:
- How much is the width of the pad? (mm) (required)
0.65

Question 14:
- How much is the distance(P) between the Left and Righ pads center? (mm) (required)
5.60

Question 15:
- What is the Orientation symbol? (required)
0

Question 16:
- What is the name of pin1 ? (required)
GND

Question 17:
- What is the direction of pin1 ? (required)
8

Question 18:
- What is the name of pin2 ? (required)
TRIG

Question 19:
- What is the direction of pin2 ? (required)
2

Question 20:
- What is the name of pin3 ? (required)
OUT

Question 21:
- What is the direction of pin3 ? (required)
3

Question 22:
- What is the name of pin4 ? (required)
RESET

Question 23:
- What is the direction of pin4 ? (required)
2

Question 24:
- What is the name of pin5 ? (required)
CONT

Question 25:
- What is the direction of pin5 ? (required)
4

Question 26:
- What is the name of pin6 ? (required)
THRES

Question 27:
- What is the direction of pin6 ? (required)
2

Question 28:
- What is the name of pin7 ? (required)
DISCH

Question 29:
- What is the direction of pin7 ? (required)
out

Question 30:
- What is the name of pin8 ? (required)
VCC

Question 31:
- What is the direction of pin8 ? (required)
8

```


After the timer_555.lbr is created, move it to the folder libraries in Eagle folder.

The libray will be imported automatically next time you open the software.

## Future Improvements
- Split part of the required text in a template txt file

- Allow the creation of libraries based on more types of package, by using specific fuctions in package creation

- Allow to store multiple packages of a component in a single library file
