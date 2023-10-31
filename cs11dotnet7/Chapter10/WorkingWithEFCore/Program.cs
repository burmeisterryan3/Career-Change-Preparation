using Packt.Shared;

// Northwind db = new();
// WriteLine($"Provider: {db.Database.ProviderName}");

// WriteLine(); WriteLine();
// QueryingCategories();

// WriteLine(); WriteLine();
// FilteredIncludes();

// WriteLine(); WriteLine();
// QueryingProducts();

// WriteLine(); WriteLine();
// QueryingWithLike();

// WriteLine(); WriteLine();
// GetRandomProduct();

(int affected, int productId) = AddProduct(categoryId: 6, productName: "Bob's Burgers", price: 500M);
if (affected == 1)
{
    WriteLine($"Add product successful with ID: {productId}.");
}
ListProducts(productIdsToHighlight: new int[] { productId });


//(affected, productId) = IncreaseProductPrice(productNameStartsWith: "Bob", amount: 20M);
//if (affected == 1)
//{
//    WriteLine("Increase price success for ID: {resultUpdate.productId}.");
//}
//ListProducts(productIdsToHighlight: new int[] { productId });

//WriteLine("About to delete all products whose name starts with Bob.");
//Write("Press Enter to continue or any other key to exit: ");
//if (ReadKey(intercept: true).Key == ConsoleKey.Enter)
//{
//    int deleted = DeleteProducts(productNameStartsWith: "Bob");
//    WriteLine($"{deleted} product(s) were deleted.");
//}
//else
//{
//    WriteLine("Delete was canceled.");
//}

(affected, int[]? productIds) = IncreaseProductPricesBetter(productNameStartsWith: "Bob", amount: 20M);
if (affected > 0)
{
    WriteLine("Increase product price successful.");
}
ListProducts(productIdsToHighlight: productIds);

WriteLine("About to delete all products whose name starts with Bob.");
Write("Press Enter to continue or any other key to exit: ");
if (ReadKey(intercept: true).Key == ConsoleKey.Enter)
{
    int deleted = DeleteProductsBetter(productNameStartsWith: "Bob");
    WriteLine($"{deleted} product(s) were deleted.");
}
else
{
    WriteLine("Delete was canceled.");
}