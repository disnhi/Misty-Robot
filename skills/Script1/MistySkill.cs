using System;
using System.Collections.Generic;
using System.IO;
using System.Text.RegularExpressions;
using System.Threading;
using Windows.Storage;
using Windows.Storage.Streams;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using MistyRobotics.Common;
using MistyRobotics.SDK.Commands;
using MistyRobotics.Common.Data;
using MistyRobotics.SDK.Events;
using MistyRobotics.SDK.Responses;
using MistyRobotics.Common.Types;
using MistyRobotics.SDK;
using MistyRobotics.SDK.Messengers;
using Newtonsoft.Json;


namespace Script1
{
	internal class MistySkill : IMistySkill
	{
		private Random _random = new Random();
		/// <summary>
		/// Make a local variable to hold the misty robot interface, call it whatever you want 
		/// </summary>
		private IRobotMessenger _misty;

		/// <summary>
		/// Skill details for the robot
		/// 
		/// There are other parameters you can set if you want:
		///   Description - a description of your skill
		///   TimeoutInSeconds - timeout of skill in seconds
		///   StartupRules - a list of options to indicate if a skill should start immediately upon startup
		///   BroadcastMode - different modes can be set to share different levels of information from the robot using the 'SkillData' websocket
		///   AllowedCleanupTimeInMs - How long to wait after calling OnCancel before denying messages from the skill and performing final cleanup  
		/// </summary>
		public INativeRobotSkill Skill { get; private set; } = new NativeRobotSkill("Script1", "7d6fe0a1-61b4-4df5-872a-568776310d2f");

		/// <summary>
		///	This method is called by the wrapper to set your robot interface
		///	You need to save this off in the local variable commented on above as you are going use it to call the robot
		/// </summary>
		/// <param name="robotInterface"></param>
		public void LoadRobotConnection(IRobotMessenger robotInterface)
		{
			_misty = robotInterface;
		}


		//This function is from github
		private async Task<int> WriteMe(string userText, string layer, string stringDelimiters = ",!.?", int delayMilliseconds = 500)
		{
			await _misty.SetTextDisplaySettingsAsync
				(
				layer,
				new TextSettings
				{
					Weight = _random.Next(600, 1001),
					Blue = (byte)_random.Next(0, 256),
					Red = (byte)_random.Next(0, 256),
					Green = (byte)_random.Next(0, 256),
					Size = _random.Next(70, 100),
					//VerticalAlignment = ImageVerticalAlignment.Bottom,
					Wrap = true,
					Opacity = 1,
					PlaceOnTop = true,
					Visible = true
				}
				); ;

			string[] stringArray = Regex.Split(userText, $@"(?<=[{stringDelimiters}])");
			foreach (string text in stringArray)
			{
				_misty.DisplayText(text, layer, null);
				if (!_misty.Wait(delayMilliseconds))
				{
					return stringArray.Length;
				}
			}
			return stringArray.Length;

		}

		//Also from github
		private async void DisplayTextLoop()
		{
			while (_misty.Wait(500))
			{
				await WriteMe("Hello everyone, my name is Misty!", "AssetFunLayer1", null);
			}
		}


		public void SayText(string userText)
        {
			_misty.Speak(userText, false, null, null);
        }

		public void DisplayText(string userText)
		{
			_misty.DisplayImage(userText, null, false, null);
			Pause(5);
		}

		public void LookInDirection(string direction)
        {
			//break into three sections: look at object, look at user, look in direction
			//focus on look in direction (up, down, left, right, corners, and forward)
			//First Parameter = up & down (negative = up, postive = down)  <-- pitch
			//Second Parameter = diagonals (positive 10 = upper left, negative 10 = upper right    <--row
			//Third Parameter = left and right (positive = right, negative = left)  <-- yaw

			int speed = 130;
			if (direction == "upperRight")
			{
				_misty.MoveHead(-7, 0, 17, speed, AngularUnit.Degrees, null); //Upper right hand corner
			}
			else if (direction == "lowerRight")
			{
				_misty.MoveHead(7, 0, 17, speed, AngularUnit.Degrees, null); // lower right hand corner
			}
			else if (direction == "upperLeft")
			{
				_misty.MoveHead(-7, 0, -17, speed, AngularUnit.Degrees, null); //upper left hand corner
			}
			else if (direction == "lowerLeft")
			{
				_misty.MoveHead(7, 0, -17, speed, AngularUnit.Degrees, null); //lower left hand corner
			}
			else if (direction == "right")
			{
				_misty.MoveHead(0, 0, 17, speed, AngularUnit.Degrees, null); //look to the right
			}
			else if (direction == "left")
			{
				_misty.MoveHead(0, 0, -17, speed, AngularUnit.Degrees, null); //look to the left
			}
			else if (direction == "down")
			{
				_misty.MoveHead(7, 0, 0, speed, AngularUnit.Degrees, null);  //look down
			}
			else if (direction == "up")
			{
				_misty.MoveHead(-7, 0, 0, speed, AngularUnit.Degrees, null); //look up
			}	
			else if (direction == "center")
            {
				_misty.MoveHead(0, 0, 0, 125, AngularUnit.Position, null);
			}
		}

		public void PointAt(string direction, string arm)
        {
			if(arm =="left")
            {
				if (direction == "straightOut")
				{
					_misty.MoveArms(0, 90, 40, 40, 10, AngularUnit.Position, null); //left arms straight out
				}
				else if (direction == "upwards")
                {
					_misty.MoveArms(-45, 90, 40, 40, 10, AngularUnit.Position, null); //left arm, up
				}
				else if (direction == "downwards")
                {
					_misty.MoveArms(20, 90, 40, 40, 10, AngularUnit.Position, null); //left arm, downwards
				}
				else if (direction == "default")
                {
					_misty.MoveArms(90, 90, 110, 110, 15, AngularUnit.Degrees, null);
				}
			}
			else if (arm == "right")
            {
				if (direction == "straightOut")
                {
					_misty.MoveArms(90, 0, 40, 40, 10, AngularUnit.Position, null); //right arms straight out
				}
				else if (direction == "upwards")
                {
					_misty.MoveArms(90, -45, 0, 40, 10, AngularUnit.Position, null); //right arm up
				}
				else if (direction == "downwards")
                {
					_misty.MoveArms(90, 20, 40, 40, 10, AngularUnit.Position, null); //right arm, downwards
				}
				else if (direction == "default")
				{
					_misty.MoveArms(90, 90, 110, 110, 15, AngularUnit.Degrees, null);
				}
			}
			else if (arm == "both")
            {
				if (direction == "straightOut")
                {
					_misty.MoveArms(0, 0, 40, 40, 10, AngularUnit.Position, null); //both arms straight out
				}
				else if (direction == "downwards")
                {
					_misty.MoveArms(90, 90, 40, 40, 10, AngularUnit.Position, null); //both arm, downwards
				}
				else if (direction == "upwards")
                {
					_misty.MoveArms(-45, -45, 40, 40, 10, AngularUnit.Position, null);
                }
				else if (direction == "default")
				{
					_misty.MoveArms(90, 90, 110, 110, 15, AngularUnit.Degrees, null);
				}
			}
		}

		public void Pause(int milliseconds)
		{
			_misty.Wait(milliseconds);
		}


		public void Reset() //add parameter for position like (sleeping)
        {
			_misty.DisplayImage("e_DefaultContent.jpg", null, false, null);
			_misty.ChangeLED(255, 0, 2, null);
			_misty.MoveHead(0, 0, 0, 125, AngularUnit.Position, null);
			_misty.MoveArms(90, 90, 110, 110, 15, AngularUnit.Degrees, null);
		}

		public void ShakeNo()
		{
			_misty.MoveHead(0, 0, -19, 150, AngularUnit.Degrees, null);
			_misty.Wait(1000);
			_misty.MoveHead(0, 0, 27, 150, AngularUnit.Degrees, null);
			_misty.Wait(1000);
			_misty.MoveHead(0, 0, -17, 150, AngularUnit.Degrees, null);
			_misty.Wait(1000);
			_misty.MoveHead(0, 0, 0, 125, AngularUnit.Position, null);
		}

		public void TiltHead(string direction, string amount)
        {
			if (direction == "left")
            {
				if (amount == "small")
                {
					_misty.MoveHead(0, 8, 0, 130, AngularUnit.Degrees, null);
                }
				else if (amount == "large")
                {
					_misty.MoveHead(0, 25, 0, 130, AngularUnit.Degrees, null);
                }
            }
			else if (direction == "right")
            {
				if (amount == "small")
                {
					_misty.MoveHead(0, -8, 0, 130, AngularUnit.Degrees, null);
                }
				else if (amount == "large")
                {
					_misty.MoveHead(0, -25, 0, 130, AngularUnit.Degrees, null);
                }
            }
        }

		public void SetEyes(string emotion)
        {
			if (emotion == "happy")
            {
				_misty.DisplayImage("e_Admiration.jpg", null, false, null); 
            }
			else if (emotion == "confused")
            {
				_misty.DisplayImage("e_ApprehensionConcerned.jpg", null, false, null);
            }
			else if (emotion == "thinking")
            {
				_misty.DisplayImage("e_Contempt.jpg", null, false, null);
            }
			else if (emotion == "scared")
            {
				_misty.DisplayImage("e_Fear.jpg", null, false, null);
            }
			else if (emotion == "scared")
            {
				_misty.DisplayImage("e_Terror2.jpg", null, false, null);
            }
			else if (emotion == "love")
            {
				_misty.DisplayImage("e_Love.jpg", null, false, null);
            }	
			else if (emotion == "default")
            {
				_misty.DisplayImage("e_DefaultContent.jpg", null, false, null);
			}
			else if (emotion == "looking")
            {
				_misty.DisplayImage("e_ApprehensionConcerned.jpg", null, false, null);
            }
        }

		public void NotDone4()
        {
			List<List<string>> missingPiece2 = new List<List<string>>();

			missingPiece2.Add(new List<string> { "LookInDirection", "down" });
			missingPiece2.Add(new List<string> { "Pause", "2000" });
			missingPiece2.Add(new List<string> { "SayText", "Testing not done Scenario with step 4: gesture" });
			missingPiece2.Add(new List<string> { "Pause", "4000" });
			missingPiece2.Add(new List<string> { "LookInDirection", "center" });
			missingPiece2.Add(new List<string> { "Pause", "2500" });
			missingPiece2.Add(new List<string> { "TiltHead", "left","large"});
			missingPiece2.Add(new List<string> { "SetEyes", "thinking" });
			missingPiece2.Add(new List<string> { "Pause", "2200" });
			missingPiece2.Add(new List<string> { "LookInDirection", "center" });
			missingPiece2.Add(new List<string> { "SetEyes", "default" });
			missingPiece2.Add(new List<string> { "Pause", "1000" });
			missingPiece2.Add(new List<string> { "LookInDirection", "down" });
			missingPiece2.Add(new List<string> { "Pause", "1000" });
			missingPiece2.Add(new List<string> { "SayText", "Rotate that wing tip" });
			missingPiece2.Add(new List<string> { "Pause", "50" });
			missingPiece2.Add(new List<string> { "LookInDirection", "lowerRight" });
            missingPiece2.Add(new List<string> { "PointAt", "downwards", "left" });
			missingPiece2.Add(new List<string> { "Pause", "2200" });
			missingPiece2.Add(new List<string> { "PointAt", "default", "right" });
			missingPiece2.Add(new List<string> { "LookInDirection", "lowerLeft" });
			missingPiece2.Add(new List<string> { "Pause", "20" });
			missingPiece2.Add(new List<string> { "PointAt", "downwards", "right" });
			missingPiece2.Add(new List<string> { "Pause", "50" });
			missingPiece2.Add(new List<string> { "SayText", "to look like it is in the picture" });
			missingPiece2.Add(new List<string> { "Pause", "800" });
			missingPiece2.Add(new List<string> { "PointAt", "default", "right" });
			missingPiece2.Add(new List<string> { "LookInDirection", "center" });


			for (int i = 0; i < missingPiece2.Count(); i++)
			{

				switch (missingPiece2[i][0])
				{
					case "SayText":
						SayText(missingPiece2[i][1]);
						break;

					case "LookInDirection":
						LookInDirection(missingPiece2[i][1]);
						break;

					case "PointAt":
						PointAt(missingPiece2[i][1], missingPiece2[i][2]);
						break;

					case "Pause":
						Pause(Convert.ToInt32(missingPiece2[i][1]));
						break;

					case "TiltHead":
						TiltHead(missingPiece2[i][1], missingPiece2[i][2]);
						break;

					case "SetEyes":
						SetEyes(missingPiece2[i][1]);
						break;

				}
			}

		}

		public void MissingPiece2()
        {
			List<List<string>> myScript = new List<List<string>>();

			myScript.Add(new List<string> { "LookInDirection", "down" });
			myScript.Add(new List<string> { "Pause", "2000" });
			myScript.Add(new List<string> { "SayText", "Testing missing piece scenario with step 2: verbal indirect" });
			myScript.Add(new List<string> { "Pause", "4000" });
			myScript.Add(new List<string> { "LookInDirection", "center" });
			myScript.Add(new List<string> { "Pause", "1100" });
			myScript.Add(new List<string> { "LookInDirection", "upperRight" });
			myScript.Add(new List<string> { "SetEyes", "thinking" });
			myScript.Add(new List<string> { "Pause", "1500" });
			myScript.Add(new List<string> { "TiltHead", "left", "small" });
			myScript.Add(new List<string> { "Pause", "500" });
			myScript.Add(new List<string> { "SetEyes", "default" });
			myScript.Add(new List<string> { "SayText", "You might be onto something." });
			myScript.Add(new List<string> { "Pause", "2000" });
			myScript.Add(new List<string> { "LookInDirection", "down" });

			foreach (List<string> action in myScript)
			{

				switch (action[0])
				{
					case "SayText":
						SayText(action[1]);
						break;

					case "LookInDirection":
						LookInDirection(action[1]);
						break;

					case "PointAt":
						PointAt(action[1], action[2]);
						break;

					case "Pause":
						Pause(Convert.ToInt32(action[1]));
						break;

					case "TiltHead":
						TiltHead(action[1], action[2]);
						break;

					case "SetEyes":
						SetEyes(action[1]);
						break;

					default:
						break;

				}
			}
		}

		//Use case for the positive remark of baking cookies
		public void BakingCookies()
        {
			List<List<string>> myScript = new List<List<string>>();

			myScript.Add(new List<string> { "LookInDirection", "down" });
			myScript.Add(new List<string> { "Pause", "2000" });
			myScript.Add(new List<string> { "SayText", "Testing missing vanilla scenario with step 1: positive remark." });
			myScript.Add(new List<string> { "Pause", "4000" });
			myScript.Add(new List<string> { "LookInDirection", "center" });
			myScript.Add(new List<string> { "SetEyes", "happy" });
			myScript.Add(new List<string> { "SayText", "Looking delicious so far!" });
			myScript.Add(new List<string> { "Pause", "1500" });
			myScript.Add(new List<string> { "SetEyes", "default" });
			myScript.Add(new List<string> { "LookInDirection", "down" });

			foreach (List<string> action in myScript)
			{

				switch (action[0])
				{
					case "SayText":
						SayText(action[1]);
						break;

					case "LookInDirection":
						LookInDirection(action[1]);
						break;

					case "PointAt":
						PointAt(action[1], action[2]);
						break;

					case "Pause":
						Pause(Convert.ToInt32(action[1]));
						break;

					case "TiltHead":
						TiltHead(action[1], action[2]);
						break;

					case "SetEyes":
						SetEyes(action[1]);
						break;

					default:
						break;

				}
			}
		}
		private async void ActionHandler(IUserEvent userEvent)
		{

			/*
			IDictionary<string, object> payloadData = JsonConvert.DeserializeObject<Dictionary<string, object>>(userEvent.Data["Payload"].ToString());
			string text = Convert.ToString(payloadData.FirstOrDefault(x => x.Key == "Text").Value);
			if (!string.IsNullOrWhiteSpace(text))
			{
				await _misty.SpeakAsync(text, true, null);
				await _misty.DisplayTextAsync(text, null);
			}
			jsonScripts(text);
			*/
			jsonScripts(userEvent.Data["Payload"].ToString());
		}

		public class ActionScript
        {
			public string intent { get; set; }
			public string description { get; set; }
			public List<MistyAction> actionList { get; set; }
        }

		public class MistyAction
        {
			public string name { get; set; }
			public List<string> args { get; set; }
        }

		//for further use in the data handler
		public void jsonScripts(string jsonActions)
        {
			/*
			var actionName = script.actionList[0].name;
			*/

			//ActionScript script = new ActionScript();

			var script = JsonConvert.DeserializeObject<ActionScript>(jsonActions);


			//string text = script.intent + script.description;
			//SayText(text);
			
			foreach (var act in script.actionList)
			{
				DisplayText(act.name);
				switch (act.name)
				{
					case "SayText":
						SayText(act.args[0]);
						break;

					case "LookInDirection":
						LookInDirection(act.args[0]);
						break;

					case "PointAt":
						PointAt(act.args[0], act.args[1]);
						break;

					case "Pause":
						Pause(Convert.ToInt32(act.args[0]));
						break;

					case "TiltHead":
						TiltHead(act.args[0], act.args[1]);
						break;

					case "SetEyes":
						SetEyes(act.args[0]);
						break;

					case "DisplayText":
						DisplayText(act.args[0]);
						break;

					default:
						break;

					}
				}
		}


		public void OnStart(object sender, IDictionary<string, object> parameters)
		{
			_misty.ChangeLED(0, 255, 0, null);
			//_misty.DisplayImage("e_love.jpg", null, false, null);
			//_misty.MoveArms(42, 90, 40, 40, 10, AngularUnit.Position, null); //slightly up (could be used for walking animations)
			
			_misty.RegisterUserEvent("ActionScript", ActionHandler, 0, true, null);

			//string jsonActions = "{\"intent\": \"notDone(leftWing, orientation, level 4)\",\"description\": \"Left wing is on incorrectly, level 4 = gesture\",\"actionList\":[{\"name\": \"LookInDirection\",\"args\": [\"center\"]},{\"name\": \"Pause\",\"args\": [\"2500\"]},{\"name\": \"TiltHead\",\"args\": [\"left\",\"large\"]},{\"name\": \"SetEyes\",\"args\": [\"thinking\"]},{\"name\": \"Pause\",\"args\": [\"2200\"]},{\"name\": \"LookInDirection\",\"args\": [\"center\"]},{\"name\": \"SetEyes\",\"args\": [\"default\"]},{\"name\": \"Pause\",\"args\": [\"1000\"]},{\"name\": \"LookInDirection\",\"args\": [\"down\"]},{\"name\": \"Pause\",\"args\": [\"1000\"]},{\"name\": \"SayText\",\"args\": [\"Rotate that wing tip\"]},{\"name\": \"Pause\",\"args\": [\"50\"},{\"name\": \"LookInDirection\",\"args\": [\"lowerRight\"]},{\"name\": \"PointAt\",\"args\": [\"downwards\",\"left\"]},{\"name\": \"Pause\",\"args\": [\"2200\"]},{\"name\": \"PointAt\",\"args\": [\"default\",\"right\"]},{\"name\": \"LookInDirection\",\"args\": [\"lowerLeft\"]},{\"name\": \"Pause\",\"args\": [\"20\"]},{\"name\": \"PointAt\",\"args\": [\"downwards\",\"right\"]},{\"name\": \"Pause\",\"args\": [\"50\"]},{\"name\": \"SayText\",\"args\": [\"to look like it is in the picture\"]},{\"name\": \"Pause\",\"args\": [\"800\"]},{\"name\": \"PointAt\",\"args\": [\"default\",\"right\"]},{\"name\": \"LookInDirection\",\"args\":[\"center\"]}]}";
			//string jsonActions = "{\"intent\": \"notDone(leftWing, orientation, level 4)\",\"description\": \"Left wing is on incorrectly, level 4 = gesture\",\"actionList\":[{\"name\": \"LookInDirection\",\"args\": [\"center\"]},{\"name\": \"Pause\",\"args\": [\"2500\"]},{\"name\": \"TiltHead\",\"args\": [\"left\",\"large\"]},{\"name\": \"SetEyes\",\"args\": [\"thinking\"]},{\"name\": \"Pause\",\"args\": [\"2200\"]},{\"name\": \"LookInDirection\",\"args\": [\"center\"]},{\"name\": \"SetEyes\",\"args\": [\"default\"]},{\"name\": \"Pause\",\"args\": [\"1000\"]},{\"name\": \"LookInDirection\",\"args\": [\"down\"]},{\"name\": \"Pause\",\"args\": [\"1000\"]},{\"name\": \"SayText\",\"args\": [\"Rotate that wing tip\"]},{\"name\": \"Pause\",\"args\": [\"50\"]},{\"name\": \"LookInDirection\",\"args\": [\"lowerRight\"]},{\"name\": \"PointAt\",\"args\": [\"downwards\",\"left\"]},{\"name\": \"Pause\",\"args\": [\"2200\"]},{\"name\": \"PointAt\",\"args\": [\"default\",\"right\"]},{\"name\": \"LookInDirection\",\"args\": [\"lowerLeft\"]},{\"name\": \"Pause\",\"args\": [\"20\"]},{\"name\": \"PointAt\",\"args\": [\"downwards\",\"right\"]},{\"name\": \"Pause\",\"args\": [\"50\"]},{\"name\": \"SayText\",\"args\": [\"to look like it is in the picture\"]},{\"name\": \"Pause\",\"args\": [\"800\"]},{\"name\": \"PointAt\",\"args\": [\"default\",\"right\"]},{\"name\": \"LookInDirection\",\"args\":[\"center\"]}]}";
			string jsonActions = "{\"intent\": \"missingVanilla(level 4)\",\"description\": \"Vanilla is missing from the recipe. Level 4. Gesture\",\"actionList\":[{\"name\": \"LookInDirection\",\"args\": [\"center\"]},{\"name\": \"Pause\",\"args\": [\"2500\"]},{\"name\": \"TiltHead\",\"args\": [\"left\",\"large\"]},{\"name\": \"SetEyes\",\"args\": [\"thinking\"]},{\"name\": \"Pause\",\"args\": [\"2200\"]},{\"name\": \"LookInDirection\",\"args\": [\"center\"]},{\"name\": \"SetEyes\",\"args\": [\"default\"]},{\"name\": \"Pause\",\"args\": [\"1000\"]},{\"name\": \"LookInDirection\",\"args\": [\"down\"]},{\"name\": \"Pause\",\"args\": [\"1000\"]},{\"name\": \"SayText\",\"args\": [\"Don't forget!\"]},{\"name\": \"Pause\",\"args\": [\"59\"]},{\"name\": \"SayText\",\"args\": [\"You still need the vanilla.\"]},{\"name\": \"Pause\",\"args\": [\"50\"]},{\"name\": \"PointAt\",\"args\": [\"straightOut\",\"left\"]},{\"name\": \"Pause\",\"args\": [\"2200\"]},{\"name\": \"PointAt\",\"args\": [\"default\",\"right\"]},{\"name\": \"LookInDirection\",\"args\": [\"lowerLeft\"]},{\"name\": \"Pause\",\"args\": [\"20\"]},{\"name\": \"PointAt\",\"args\": [\"downwards\",\"right\"]},{\"name\": \"Pause\",\"args\": [\"150\"]},{\"name\": \"SayText\",\"args\": [\"It's right over there!\"]},{\"name\": \"Pause\",\"args\": [\"800\"]},{\"name\": \"PointAt\",\"args\": [\"default\",\"right\"]},{\"name\": \"LookInDirection\",\"args\":[\"center\"]}]}";

			//jsonScripts(jsonActions);
			/*
			MissingPiece2();
			Pause(3000);
			Reset();
			Pause(3000);
			NotDone4(); //plays the gesture part of the notDone scenario
			Pause(3000);
			Reset();
			Pause(3000);
			BakingCookies();
			*/
		}

		public void OnPause(object sender, IDictionary<string, object> parameters)
		{
			//In this template, Pause is not implemented by default
			_misty.ChangeLED(255, 0, 2, null);
		}

		public void OnResume(object sender, IDictionary<string, object> parameters)
		{
			//TODO Put your code here and update the summary above
		}
		
		public void OnCancel(object sender, IDictionary<string, object> parameters)
		{
			//TODO Put your code here and update the summary above
			//_misty.Speak("Goodbye", false, null, null);
			//_misty.Speak("See you next time!", false, null, null);
			Reset();
		}

		/// <summary>
		/// This event handler is called when the skill timeouts
		/// You currently have a few seconds to do cleanup and robot resets before the skill is shut down... 
		/// Events will be unregistered for you 
		/// </summary>
		public void OnTimeout(object sender, IDictionary<string, object> parameters)
		{
			//TODO Put your code here and update the summary above
			_misty.ChangeLED(255, 0, 2, null);
		}

		public void OnResponse(IRobotCommandResponse response)
		{
			Debug.WriteLine("Response: " + response.ResponseType.ToString());
		}

		#region IDisposable Support
		private bool _isDisposed = false;
        //private MistyRobotics.Common.Types.RobotArm left;

        private void Dispose(bool disposing)
		{
			if (!_isDisposed)
			{
				if (disposing)
				{
					// TODO: dispose managed state (managed objects).
				}

				// TODO: free unmanaged resources (unmanaged objects) and override a finalizer below.
				// TODO: set large fields to null.

				_isDisposed = true;
			}
		}

		// TODO: override a finalizer only if Dispose(bool disposing) above has code to free unmanaged resources.
		// ~MistySkill() {
		//   // Do not change this code. Put cleanup code in Dispose(bool disposing) above.
		//   Dispose(false);
		// }

		// This code added to correctly implement the disposable pattern.
		public void Dispose()
		{
			// Do not change this code. Put cleanup code in Dispose(bool disposing) above.
			Dispose(true);
			// TODO: uncomment the following line if the finalizer is overridden above.
			// GC.SuppressFinalize(this);
		}
		#endregion
	}
}
