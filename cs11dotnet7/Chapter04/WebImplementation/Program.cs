WebApplicationBuilder builder = WebApplication.CreateBuilder(args);
builder.Services.AddRazorPages();
WebApplication app = builder.Build();

if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Error");
    app.UseHsts();
}

app.UseHttpsRedirection();
app.UseDefaultFiles(); // index.html, default.html, etc.
app.UseStaticFiles();

app.MapRazorPages();

app.MapGet("/hello", () => "Hello World!");

app.Run();
