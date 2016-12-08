using System;
using ArdaLib; // https://github.com/ardaozkal/ArdaLib/releases/
using System.IO;
using System.Net;

namespace PebbleLangDownloader
{
	class MainClass
	{
		public static void Main(string[] args)
		{
			var wc = new WebClient();
			Console.WriteLine("Initialized Pebble Language Downloader. By github/ardaozkal");
			Console.WriteLine("Rest in Peace, Pebble.");
			try
			{
				var LanguagesFile = wc.DownloadString("http://lp.getpebble.com/v1/languages");
				Console.WriteLine("Successfully downloaded language file. Attempting to write that in a file called \"languages.json\".");
				File.WriteAllText("languages.json", LanguagesFile);
				Console.WriteLine("Successfully wrote down language file. Starting download of language files.");
				var LanguagesList = StringOperations.FindAllBetween(LanguagesFile, "\"file\":\"", "\"", true);
				foreach (var language in LanguagesList)
				{
					Console.WriteLine("Downloading: " + language);
					var FileName =  StringOperations.After(language, "/", true, true);
					wc.DownloadFile(language, FileName);
				}
				Console.WriteLine("Successfully downloaded everything.");
			}
			catch
			{
				Console.WriteLine("Couldn't download language file. Rip pebble servers.");
			}
		}
	}
}
