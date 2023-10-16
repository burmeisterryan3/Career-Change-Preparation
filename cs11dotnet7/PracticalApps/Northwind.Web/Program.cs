using Packt.Shared; // AddNorthwindContext extension method
using Microsoft.AspNetCore.Server.Kestrel.Core; // HttpProocols

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddRazorPages();
builder.Services.AddNorthwindContext();
builder.Services.AddRequestDecompression();

builder.WebHost.ConfigureKestrel((context, options) =>
{
    options.ListenAnyIP(5001, listenOptions =>
    {
        listenOptions.Protocols = HttpProtocols.Http1AndHttp2AndHttp3;
        listenOptions.UseHttps(); // HTTP/3 requires TLS
    });
});


var app = builder.Build();

if (!app.Environment.IsDevelopment())
{
    app.UseHsts();
}

app.Use(async (HttpContext context, Func<Task> next) =>
{
    RouteEndpoint? rep = context.GetEndpoint() as RouteEndpoint;

    if (rep is not null)
    {
        WriteLine($"Endpoint name: {rep.DisplayName}");
        WriteLine($"Endpoint route pattern: {rep.RoutePattern.RawText}");
    }

    if (context.Request.Path == "/bonjour")
    {
        // in the case of a match on URL path, this becomes a terminating
        // delegate that returns so does not call the next delegate
        await context.Response.WriteAsync("Bonjour Monde!");
        return;
    }

    // we could modify the request before calling the next delegate
    await next();

    // we could modify the response after calling the next delegate
});

app.UseHttpsRedirection(); // check properties\launchSettings.json for port number
app.UseRequestDecompression();
app.UseDefaultFiles(); // index.html, default.html, and so on
app.UseStaticFiles();

app.MapRazorPages();

app.MapGet("/hello", () => "Hello World!");

app.Run();

WriteLine("This executes after the web server has stopped!");
