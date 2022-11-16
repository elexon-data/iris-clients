namespace IrisClient.helpers;

public static class FileDownloadHelpers
{
    public static async Task WriteFile(string path, string filename, string content)
    {
        if (!Directory.Exists(path))
        {
            Directory.CreateDirectory(path);
            Console.WriteLine($"Target directory created: \"{path}\"");
        }

        await File.WriteAllTextAsync(Path.Combine(path, filename), content);
        Console.WriteLine($"Created file {filename}");
    }

    public static string GetDownloadDirectory()
    {
        var downloadDirectory = Directory.GetCurrentDirectory();
        var rootDirectoryPathSuffix = $"{Path.DirectorySeparatorChar}IrisClient"; // = "\IrisClient"
        if (downloadDirectory.EndsWith(rootDirectoryPathSuffix))
        {
            // This is the simple case
            // e.g. running from PowerShell 
            return downloadDirectory;
        }

        var rootDirectoryPathSegment = rootDirectoryPathSuffix + Path.DirectorySeparatorChar; // = "\IrisClient\"
        if (downloadDirectory.Contains(rootDirectoryPathSegment))
        {
            // When running from an IDE the current directory is more like: "iris-clients\dotnet\IrisClient\bin\Debug\net6.0"
            // To make sure data is always saved in the same place, truncate the path to the IrisClient directory
            return downloadDirectory.Split(rootDirectoryPathSegment)[0] + rootDirectoryPathSuffix;
        }

        // Data should always be saved in the same folder. If it cannot be found, the user needs to intervene
        throw new DirectoryNotFoundException("Could not find the \"IrisClient\" directory. Please try running this " +
                                             "program from a location inside the \"IrisClient\" directory.");
    }
}
