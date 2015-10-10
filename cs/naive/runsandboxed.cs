using System;
using System.Security;
using System.Security.Policy;
using System.Security.Permissions;


class RunSandBoxed
{
    /// Run the code with less permissions than usual
    /// (so it can't read/write to files).
    /// This is a false sense of security... the program can still run unmanaged
    /// code. But shhh don't worry about that.
    static int Main(string[] args)
    {
        String path = args[0];
        PermissionSet ps = new PermissionSet(PermissionState.None);
        AppDomainSetup setup = new AppDomainSetup();
        Evidence ev = new Evidence();
        AppDomain sandbox = AppDomain.CreateDomain("Sandbox",
            ev,
            setup,
            ps);
        sandbox.ExecuteAssembly(path);
        return 0;
    }
}
