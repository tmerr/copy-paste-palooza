using System;
using System.CodeDom;
using System.CodeDom.Compiler;
using System.Collections;
using System.Collections.Generic;
using System.ComponentModel;
using System.Diagnostics;
using System.IO;
using Roslyn.Compilers;
using Roslyn.Compilers.CSharp;

class Program {
    static int Main(string[] args) {
        var provOptions = new Dictionary<string, string>();
        provOptions.Add("CompilerVersion", "v4");
        var provider = CodeDomProvider.CreateProvider("CSharp", provOptions);
        String[] referenceAssemblies = { "System.dll" };
        CompilerParameters cp = new CompilerParameters(referenceAssemblies, "wat.exe", false);
        cp.GenerateExecutable = true;
        CompilerResults cr = provider.CompileAssemblyFromSource(cp, "class X {}");
        foreach (var o in cr.Output) {
            Console.WriteLine(o);
        }

        return 0;
    }
}
