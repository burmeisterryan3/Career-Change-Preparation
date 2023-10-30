using Microsoft.AspNetCore.Mvc.Formatters; // IOutputFormatter, OutputFormatter
using Microsoft.AspNetCore.HttpLogging; // HttpLoggingFields
using Microsoft.AspNetCore.Server.Kestrel.Core; // HttpProtocols
using Swashbuckle.AspNetCore.SwaggerUI; // SubmitMethod

using Packt.Shared; // AddNorthwindContext extension method
using Northwind.WebApi; // SecurityHeaders
using Northwind.WebApi.Repositories; // ICustomerRepository, CustomerRepository


var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.AddNorthwindContext();
builder.Services.AddControllers(options =>
{
    WriteLine("Default output formatters:");
    foreach (IOutputFormatter formatter in options.OutputFormatters)
    {
        if (formatter is not OutputFormatter mediaFormatter)
        {
            WriteLine($"  {formatter.GetType().Name}");
        }
        else // OutputFormatter class has SupportedMediaTypes
        {
            WriteLine("  {0}, Media Types: {1}",
                arg0: mediaFormatter.GetType().Name,
                arg1: string.Join(", ", mediaFormatter.SupportedMediaTypes) ?? "None");
        }
    }
})
.AddXmlDataContractSerializerFormatters()
.AddXmlSerializerFormatters();

// Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

builder.Services.AddScoped<ICustomerRepository, CustomerRepository>();

builder.Services.AddHttpLogging(options =>
{
    options.LoggingFields = HttpLoggingFields.All;
    options.RequestBodyLogLimit = 4096; // default is 32 KB
    options.ResponseBodyLogLimit = 4096; // default is 32 KB
});

builder.Services.AddHealthChecks()
    .AddDbContextCheck<NorthwindContext>()
    // execute SELECT 1 using the specified context string
    .AddSqlServer("Data Source=(localdb)\\mssqllocaldb;Initial Catalog=Northwind;Integrated Security=true;"); // do not keep connection string in production code

builder.WebHost.ConfigureKestrel((context, options) =>
{
    options.ListenAnyIP(5002, listenOptions =>
    {
        listenOptions.Protocols = HttpProtocols.Http1AndHttp2AndHttp3;
        listenOptions.UseHttps(); // HTTP/3 requires secure connections, i.e., HTTPS
    });
});

var app = builder.Build();

// Configure the HTTP request pipeline.
app.UseHttpLogging();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI(options =>
    {
        options.SwaggerEndpoint("/swagger/v1/swagger.json", "Northwind Service API Version 1");
        options.SupportedSubmitMethods(new[] { SubmitMethod.Get, SubmitMethod.Post, SubmitMethod.Put, SubmitMethod.Delete });
    });
}

app.UseHttpsRedirection();

app.UseAuthorization();

app.UseHealthChecks(path: "/health");

app.UseMiddleware<SecurityHeaders>();

app.MapControllers();

app.Run();
