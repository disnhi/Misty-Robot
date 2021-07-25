# Welcome to the Misty-Robot-Skills! <a name="top"></a> 

When running this script on Misty, JSON files with the following format can be used to execute an action script:
 
> { 
> > "**intent**" : "_Enter user intent here_",
> > > **description**": "_Enter description of this action script (optional)_", 
> > > > "**actionList**": [{ "name": "_Enter name action_", "args": ["_Enter all the arguments for this action inside this list_"]}, { "name": "_Enter name action_", "args": ["_Enter all the arguments for this action inside this list_"]}, ...]

> }

Where the series of actions being executed in this script is the value of the _"actionList"_ key in the dictionary/JSON. The value of _"actionList"_ is a list where each action is its own dictionary within that list.

## List of actions that Misty is able to execute: 

`SayText(string userText):`
* **Parameter** - A string of the intended speech
* **Result** - Misty will speak the string from the parameter

`DisplayText(string userText):`
* **Parameter** - A string of the intended display message
* **Output** - Misty will display the message on the screen

`LookInDirection(string direction):`
* **Parameter** - A string of the direction that you'd like Misty to look towards <br /> 
     * _Limited to "upperRight", "lowerRight", "upperLeft", "lowerLeft", "right", "left", "down", "up", and "center"._
* **Result** - Misty will look in the direction that was passed from the parameter

`PointAt(string direction, string arm):`
* **Parameter** - A string of the direction to move the arm/s  and a string for choosing the arm <br/> 
    * _Arm: "left", "right", "both"_ <br /> 
    * _Direction: "straightOut", "upwards", "downwards", "default"_
* **Result** - Misty will move its arm(s) in the intended direction to convey pointing

`Pause(int milliseconds)`
* **Parameter** - An integer amount of milliseconds the user would like Misty to pause
* **Result** - Misty will stop in the exact position it's in for the desired amount of time.

`TiltHead(string direction, string amount):`
* **Parameter** - 
A string of the direction to tilt the head and a string for how large of a tilt to execute <br/> 
    * _Direction: "left", "right"_ <br/>
    * _Amount: "small", "large"_
* **Result** - Misty will tilt its head accordingly depending on the inputted parameter

`SetEyes(string emotion):`
* **Parameter** - A string of what emotion Misty should portray through the eyes <br/>
    * _Emotion: "happy", "confused", "thinking", "scared", "love", "default", "looking"_
* **Result** - Misty will change its eyes on the display according to the inputted emotion

***
_Example of a JSON file for an action script_ <br />  <br />
{"intent" : "missingVanilla2", "description": "Vanilla is missing from a cookie ingredient. Level of Help: 2", "actionList": [{ "name": "LookInDirection", "args": ["center"]}, {"name": "Pause", "args": ["1000"]}, {"name": "TiltHead", "args": ["right","small"]}, {"name": "SayText", "args": ["Keep up the great work!"]}, {"name": "SetEyes", "args": ["default"]}, {"name": "Pause", "args": ["200"]}, {"name": "PointAt", "args": ["default", "both"]}, {"name": "LookInDirection", "args": ["center"]}]}
***

[Top](#top)
          <a name="top"></a> 
