using Microsoft.EntityFrameworkCore; // DbContext
using Microsoft.EntityFrameworkCore.Diagnostics; // RelationalEventId.ComandExeucting


namespace Packt.Shared;
public class Northwind : DbContext
{

    // these properties map to tables in the database
    public DbSet<Category>? Categories { get; set; }
    public DbSet<Product> Products { get; set; }

    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
    {
        string path = Path.Combine(Environment.CurrentDirectory, "NorthwindDb\\Northwind.db");

        string connection = $"Filename={path}";

        ConsoleColor previousColor = ForegroundColor;
        ForegroundColor = ConsoleColor.DarkYellow;
        WriteLine($"Connection: {connection}");
        ForegroundColor = previousColor;

        optionsBuilder.UseSqlite(connection);
        optionsBuilder.LogTo(WriteLine, new[] { RelationalEventId.CommandExecuting }).EnableSensitiveDataLogging();

        optionsBuilder.UseLazyLoadingProxies();
    }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        // Fluent API statements as an alternative to decorating your entity classes with attributes
        modelBuilder.Entity<Category>()
            .Property(category => category.CategoryName)
            .IsRequired()
            .HasMaxLength(15);

        if (Database.ProviderName?.Contains("Sqlite") ?? false)
        {
            // added to "fix" the lack of decimal support in SQLite
            modelBuilder.Entity<Product>()
                .Property(product => product.Cost)
                .HasConversion<double>();
        }

        // global filter to remove discontinued products
        modelBuilder.Entity<Product>()
            .HasQueryFilter(p => !p.Discontinued);
    }
}