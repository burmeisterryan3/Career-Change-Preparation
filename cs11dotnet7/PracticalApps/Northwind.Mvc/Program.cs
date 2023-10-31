/*
 * SECTION 1 - import namespaces
 */
using System.Net; // HttpVersion
using Microsoft.AspNetCore.Identity; // IdentityUser
using Microsoft.EntityFrameworkCore; // UseSqlServer, UseSqlite (for SQLite)
using Northwind.Mvc.Data; // ApplicationDbContext
// See obj\Debug\net7.0\Northwind.Mvc.GlobalUsings.g.cs for the generated global usings

using Packt.Shared; // AddNorthwindContext extension method
using System.Net.Http.Headers;

/*
 * SECTION 2 - configure the host web server including services
 */
var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
var connectionString = builder.Configuration.GetConnectionString("DefaultConnection") ?? throw new InvalidOperationException("Connection string 'DefaultConnection' not found.");
builder.Services.AddDbContext<ApplicationDbContext>(options => options.UseSqlServer(connectionString)); // or UseSqlite for SQLite
builder.Services.AddDatabaseDeveloperPageExceptionFilter();

builder.Services.AddDefaultIdentity<IdentityUser>(options => options.SignIn.RequireConfirmedAccount = true)
    .AddRoles<IdentityRole>() // enable role management
    .AddEntityFrameworkStores<ApplicationDbContext>();
builder.Services.AddControllersWithViews();

string? sqlServerConnection = builder.Configuration.GetConnectionString("NorthwindConnection");
if (sqlServerConnection is null)
{
    Console.WriteLine("SQL Server database connection string is missing!");
}
else
{
    builder.Services.AddNorthwindContext(sqlServerConnection);
}

// Default is 60 seconds
builder.Services.AddOutputCache(options =>
{
    options.DefaultExpirationTimeSpan = TimeSpan.FromSeconds(20); // default is 60 seconds
    options.AddPolicy("views", p => p.SetVaryByQuery("alertstyle"));
});

builder.Services.AddHttpClient(name: "Northwind.WebApi", configureClient: options =>
{
    options.DefaultRequestVersion = HttpVersion.Version30;
    options.DefaultVersionPolicy = HttpVersionPolicy.RequestVersionExact; // HttpVersionPolicy.RequestVersionOrLower;

    options.BaseAddress = new Uri("https://localhost:5002/");
    options.DefaultRequestHeaders.Accept.Add(
        new MediaTypeWithQualityHeaderValue(mediaType: "application/json", quality: 1.0));
});

builder.Services.AddHttpClient(name: "Minimal.WebApi", configureClient: options =>
{
    options.BaseAddress = new Uri("https://localhost:5003/");
    options.DefaultRequestHeaders.Accept.Add(
        new MediaTypeWithQualityHeaderValue("application/json", 1.0));
});

var app = builder.Build();

/*
 * SECTION 3 - Configure the HTTP request pipeline.
 */
if (app.Environment.IsDevelopment())
{
    app.UseMigrationsEndPoint();
}
else
{
    app.UseExceptionHandler("/Home/Error");
    // The default HSTS value is 30 days. You may want to change this for production scenarios, see https://aka.ms/aspnetcore-hsts.
    app.UseHsts();
}

app.UseHttpsRedirection();
app.UseStaticFiles();

app.UseRouting();

app.UseAuthentication();
app.UseAuthorization();

app.UseOutputCache();

app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Home}/{action=Index}/{id?}")
   .CacheOutput("views");
app.MapRazorPages();

app.MapGet("/notcached", () => DateTime.Now.ToString());
app.MapGet("/cached", () => DateTime.Now.ToString()).CacheOutput();

/*
 * SECTION 4 - Start the host web server listening for HTTP requests
 */
app.Run();
