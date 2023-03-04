using System.Reflection;

// Decleare unused variables using types in additional assemblies
// Will force additional assemblies to be loaded
System.Data.DataSet ds;
HttpClient client;

Assembly? myApp = Assembly.GetEntryAssembly();

if (myApp == null) return; // quit the app

// Loop through the assemblies that my app references
foreach (AssemblyName name in myApp.GetReferencedAssemblies())
{
    // Load the assembly so we can read its details
    Assembly a = Assembly.Load(name);

    // Declare a variable to count the number of methods
    int methodCount = 0;

    // Loop through all the types in the assembly
    foreach (TypeInfo t in a.DefinedTypes)
    {
        // Add up the counts of methods
        methodCount += t.GetMethods().Length;
    }

    // Output the Count of types and their methods
    Console.WriteLine(
        "{0:N0} types with {1:N0} methods in {2} assembly.",
        arg0: a.DefinedTypes.Count(),
        arg1: methodCount,
        arg2: name.Name);
}