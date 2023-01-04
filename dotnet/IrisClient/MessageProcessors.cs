using System.Text.Json;
using System.Text.Json.Nodes;
using System.Text.RegularExpressions;
using Azure.Messaging.ServiceBus;
using IrisClient.helpers;

namespace IrisClient;

public class MessageProcessors
{
    private readonly string _relativeDownloadDirectory;

    public MessageProcessors(string relativeDownloadDirectory)
    {
        _relativeDownloadDirectory = relativeDownloadDirectory;
    }

    public async Task DownloadHandler(ProcessMessageEventArgs args)
    {
        var body = args.Message.Body.ToString();

        // Regex.Unescape removes the unwanted backslash characters that escape the speech marks around properties
        // Trim removes the unwanted speech marks at beginning and end of the body string
        var rawJson = Regex.Unescape(body).Trim('"');
        var node = JsonNode.Parse(rawJson);
        var jsonString = node!.ToJsonString(new JsonSerializerOptions { WriteIndented = true });

        var baseDownloadDirectory = FileDownloadHelpers.GetDownloadDirectory();

        var dataset = args.Message.Subject ?? "unknown";
        
        var path = Path.Combine(baseDownloadDirectory, _relativeDownloadDirectory, dataset);
        var time = DateTime.Now.ToString("yyyy-MM-ddTHH-mm-ss_fff");
        var filename = $"{dataset}_{time}.json";
        try
        {
            await FileDownloadHelpers.WriteFile(path, filename, jsonString);
            await args.CompleteMessageAsync(args.Message);
        }
        catch (Exception e)
        {
            Console.Error.WriteLine($"Unable to create file \"{filename}\":\n{e}");
        }
    }

    public static Task ErrorHandler(ProcessErrorEventArgs args)
    {
        Console.WriteLine(args.Exception.ToString());
        return Task.CompletedTask;
    }
}
