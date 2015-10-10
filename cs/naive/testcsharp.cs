using System;
using System.CodeDom;
using System.CodeDom.Compiler;
using System.Collections;
using System.Collections.Generic;
using System.ComponentModel;
using System.Diagnostics;
using System.IO;
using System.Security.Policy;
using System.Security;
using System.Security.Permissions;
using System.Text.RegularExpressions;

class Program
{
    /// Return the text output to the console by the sandboxed program
    static String executeSandboxed(String path)
    {
        int runtime_limit_ms = 5000;

        var startInfo = new ProcessStartInfo
        {
            FileName = "runsandboxed.exe",
            Arguments = path,
            RedirectStandardOutput = true,
            UseShellExecute = false,
        };
        var process = Process.Start(startInfo);
        if(!process.WaitForExit(runtime_limit_ms))
        { 
            process.Kill();
            return "";
        }
        return process.StandardOutput.ReadToEnd();
    }

    static int Main(string[] args)
    {
        String sourcetext = args[0];
        String regextext = args[1];

        var provOptions = new Dictionary<string, string>();
        provOptions.Add("CompilerVersion", "v4");
        var provider = CodeDomProvider.CreateProvider("CSharp", provOptions);
        String[] referenceAssemblies = { "System.dll" };
        String fname = "temp.exe";
        CompilerParameters cp = new CompilerParameters(referenceAssemblies, fname, false);
        cp.GenerateExecutable = true;
        CompilerResults cr = provider.CompileAssemblyFromSource(cp, sourcetext);
        if (cr.NativeCompilerReturnValue == 0)
        {
            String stdout = executeSandboxed(fname);
            if (regextext != "")
            {
                Regex regex = new Regex(regextext, RegexOptions.Singleline);
                if (regex.IsMatch(stdout))
                {
                    Console.WriteLine(sourcetext);
                    return 0;
                }
                else
                {
                    return 1;
                }
            }
            return 0;
        }
        else
        {
            Console.WriteLine("failed to compile");
            return 1;
        }
    }
}
