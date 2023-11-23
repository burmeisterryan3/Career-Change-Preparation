using Microsoft.AspNetCore.Mvc; // [Route], [ApiController], [ProducesResponseType], ControllerBase
using Packt.Shared; // Customer
using Northwind.WebApi.Repositories; // ICustomerRepository

namespace Northwind.WebApi.Controllers;

// base address: api/customers
[Route("api/[controller]")]
[ApiController]
public class CustomersController : Controller
{
    private readonly ICustomerRepository repo;

    public CustomersController(ICustomerRepository repo)
    {
        this.repo = repo;
    }

    // GET: api/customers
    // GET: api/customers/?country=[country]
    // this will always return a list of customers (but it might be empty)
    [HttpGet]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(IEnumerable<Customer>))]
    [ProducesDefaultResponseType]
    public async Task<IEnumerable<Customer>> GetCustomers(string? country)
    {
        if (string.IsNullOrWhiteSpace(country))
        {
            return await repo.RetrieveAllAsync();
        }
        else
        {
            return (await repo.RetrieveAllAsync()).Where(customer => customer.Country == country);
        }
    }

    // GET: api/customers/[id]
    [HttpGet("{id}", Name = nameof(GetCustomer))] // named route
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(Customer))]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    [ProducesDefaultResponseType]
    public async Task<IActionResult> GetCustomer(string id)
    {
        Customer? customer = await repo.RetrieveAsync(id);
        if (customer is null)
        {
            return NotFound(); // 404 Resource not found
        }
        else
        {
            return Ok(customer); // 200 OK with customer in body
        }
    }

    // POST: api/customers/[id]
    // BODY: Customer (JSON, XML)
    [HttpPost]
    [ProducesResponseType(StatusCodes.Status201Created, Type = typeof(Customer))]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    [ProducesDefaultResponseType]
    public async Task<IActionResult> Create([FromBody] Customer customer)
    {
        if (customer is null)
        {
            return BadRequest(); // 400 Bad Request
        }

        Customer? addedCustomer = await repo.CreateAsync(customer);
        if (addedCustomer is null)
        {
            return BadRequest("Repository failed to create customer."); // 400 Bad Request
        }
        else
        {
            return CreatedAtRoute( // 201 Created
                routeName: nameof(GetCustomer),
                routeValues: new { id = addedCustomer.CustomerId.ToLower() },
                value: addedCustomer);
        }
    }

    // PUT: api/customers/[id]
    // BODY: Customer (JSON, XML)
    [HttpPut("{id}")]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    [ProducesDefaultResponseType]
    public async Task<IActionResult> Update(string id, [FromBody] Customer customer)
    {
        id = id.ToUpper();
        customer.CustomerId = customer.CustomerId.ToUpper();

        if (customer is null || customer.CustomerId != id)
        {
            return BadRequest(); // 400 Bad Request
        }

        Customer? existing = await repo.RetrieveAsync(id);
        if (existing is null)
        {
            return NotFound(); // 404 Resource not found
        }

        await repo.UpdateAsync(id, customer);
        return new NoContentResult(); // 204 No Content
    }

    // DELETE: api/customers/[id]
    [HttpDelete("{id}")]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> Delete(string id)
    {
        if (id == "bad")
        {
            ProblemDetails problemDetails = new()
            {
                Status = StatusCodes.Status400BadRequest,
                Type = "https://localhost.5001/customers/failed-to-delete",
                Title = $"Customer ID {id} found but failed to delete.",
                Detail = "More details like Company Name, Country, etc.",
                Instance = HttpContext.Request.Path
            };
            return BadRequest(problemDetails); // 400 Bad Request
        }

        Customer? existing = await repo.RetrieveAsync(id);

        if (existing is null)
        {
            return NotFound(); // 404 Resource not found
        }

        bool? deleted = await repo.DeleteAsync(id);
        
        if (deleted.HasValue && deleted.Value)
        {
            return new NoContentResult(); // 204 No Content
        }
        else
        {
            return BadRequest($"Customer {id} was found but failed to delete."); // 400 Bad Request
        }
    }
}
