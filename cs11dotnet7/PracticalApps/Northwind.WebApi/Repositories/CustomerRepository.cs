using Microsoft.EntityFrameworkCore.ChangeTracking; // EntityEntry<T>
using Packt.Shared; // Customer
using System.Collections.Concurrent; // ConcurrentDictionary

namespace Northwind.WebApi.Repositories;

public class CustomerRepository : ICustomerRepository
{
    // Use a static thread-safe dictonary field to cache the customers
    private static ConcurrentDictionary<string, Customer>? customersCache;

    // Use an instance data context field because it should not be
    // cached due to the data context having internal caching.
    private readonly NorthwindContext db;

    public CustomerRepository(NorthwindContext injectedContext)
    {
        db = injectedContext;

        // Pre-Load customers from database as a normal Dictinary with CustomerId as the key,
        // then convert to a thread-safe ConcurrentDictionary
        customersCache ??= new ConcurrentDictionary<string, Customer>(db.Customers.ToDictionary(c => c.CustomerId));
    }

    public async Task<Customer?> CreateAsync(Customer customer)
    {
        // Normalize CustomerId to uppercase
        customer.CustomerId = customer.CustomerId.ToUpper();

        // Add to database using EF Core
        _ = await db.Customers.AddAsync(customer); // _ would be of type EntityEntry<Customer>
        int affected = await db.SaveChangesAsync();

        if (affected == 1)
        {
            if (customersCache is null) return customer;
            // If the customer is new, add it to cache, else call UpdateCache method.
            return customersCache.AddOrUpdate(customer.CustomerId, customer, UpdateCache);
        }
        else
        {
            return null;
        }
    }

    public Task<IEnumerable<Customer>> RetrieveAllAsync()
    {
        // For performance, get from cache.
        return Task.FromResult(customersCache?.Values.AsEnumerable() ?? Enumerable.Empty<Customer>());
    }

    public Task<Customer?> RetrieveAsync(string id)
    {
        // Normalize customer Id.
        id = id.ToUpper();

        // For performance, get from cache.
        if (customersCache is null) return null!;
        customersCache.TryGetValue(id, out Customer? customer);
        return Task.FromResult(customer);
    }

    private Customer UpdateCache(string id, Customer customer)
    {
        if (customersCache is not null)
        {
            if (customersCache.TryGetValue(id, out Customer? old))
            {
                if (customersCache.TryUpdate(id, customer, old))
                {
                    return customer;
                }
            }
        }
        return null!;
    }

    public async Task<Customer?> UpdateAsync(string id, Customer customer)
    {
        // Normalize customer Id.
        id = id.ToUpper();
        customer.CustomerId = customer.CustomerId.ToUpper();

        //Update in database
        db.Customers.Update(customer);
        int affected = await db.SaveChangesAsync();
        if (affected == 1)
        {
            // update in cache
            return UpdateCache(id, customer);
        }
        return null;
    }

    public async Task<bool?> DeleteAsync(string id)
    {
        // Normalize customer Id.
        id = id.ToUpper();

        // Delete from database
        Customer? customer = await db.Customers.FindAsync(id);
        if (customer is null) return null;
        db.Customers.Remove(customer!);
        int affected = await db.SaveChangesAsync();
        if (affected == 1)
        {
            if (customersCache is null) return null;
            // Delete from cache
            return customersCache.TryRemove(id, out _);
        }
        else
        {
            return null;
        }
    }
}
