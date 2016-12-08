using System;
using System.Collections.Generic;
using ArdaLib; // https://github.com/ardaozkal/ArdaLib/releases/
using System.IO;
using System.Net;

namespace PebbleFirmwareDownloader
{
	class MainClass
	{
		static List<string> hardwarevariations = new List<string> {"unknown","ev1","ev2","ev2_3","ev2_4","bigboard","v1_5","v2_0","snowy_evt2","snowy_dvt","snowy_bb","snowy_bb2"};
		static List<string> releasechannels = new List<string> {"nightly","beta","release","release-v2","release-v3"};
		static string link = "http://pebblefw.s3.amazonaws.com/pebble/%1/%2/latest.json";
		public static void Main(string[] args)
		{
			var wc = new WebClient();
			Console.WriteLine("Initialized Pebble Firmware Downloader. By github/ardaozkal");
			Console.WriteLine("Rest in Peace, Pebble.");
			foreach (var hardwarevariation in hardwarevariations)
			{
				foreach (var releasechannel in releasechannels)
				{
					var currentlink = link.Replace("%1",hardwarevariation).Replace("%2",releasechannel);
					try
					{
						Console.WriteLine("Trying to download json: " + currentlink);
						var thejson = wc.DownloadString(currentlink);

						if (!Directory.Exists(hardwarevariation))
						{
							Directory.CreateDirectory(hardwarevariation);
						}

						if (!Directory.Exists(hardwarevariation + "/" + releasechannel))
						{
							Directory.CreateDirectory(hardwarevariation + "/" + releasechannel);
						}

						var dirdiff = hardwarevariation + "/" + releasechannel + "/";

						File.WriteAllText(dirdiff + "latest.json",thejson);

						var FirmwaresList = StringOperations.FindAllBetween(thejson, "\"url\": \"", "\"", true);
						foreach (var firmware in FirmwaresList)
						{
							Console.WriteLine("Downloading: " + firmware);
							var FileName = dirdiff + StringOperations.After(firmware, "/", true, true);
							wc.DownloadFile(firmware, FileName);
						}
					}
					catch
					{
						Console.WriteLine("Error on " + currentlink);
					}
				}
			}
		}
	}
}
