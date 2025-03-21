document.addEventListener("DOMContentLoaded", function() {
    let cartContainer = document.querySelector("#cart-items");
    let totalContainer = document.querySelector("#cart-total");
    let sortBySelect = document.querySelector("#sort-by");

    let cart = localStorage.getItem("cos_virtual");
    let total = 0;

    if (cart) {
        let cartItems = cart.split(",");
        let products = [];

        cartItems.forEach(item => {
            let [name, qty, price] = item.split("/");
            let totalPrice = parseFloat(price) * parseInt(qty, 10);

            products.push({
                name: name,
                qty: parseInt(qty, 10),
                price: parseFloat(price),
                totalPrice: totalPrice
            });

            total += totalPrice;
        });

        function displayCartItems(items) {
            cartContainer.innerHTML = "";
            items.forEach(product => {
                let cartItemHTML = `
                    <div class="cart-item">
                        <p>${product.qty} x ${product.name} (LEI ${product.price}) </p> <p> LEI ${product.totalPrice.toFixed(2)}</p>
                    </div>
                `;
                cartContainer.innerHTML += cartItemHTML;
            });

            totalContainer.innerHTML = `Total: LEI ${total.toFixed(2)}`;
        }

        displayCartItems(products);

        sortBySelect.addEventListener("change", function() {
            let sortBy = this.value;

            if (sortBy === "name-asc") {
                products.sort((a, b) => a.name.localeCompare(b.name));
            } else if (sortBy === "name-desc") {
                products.sort((a, b) => b.name.localeCompare(a.name)); 
            } else if (sortBy === "price-asc") {
                products.sort((a, b) => a.price - b.price); 
            } else if (sortBy === "price-desc") {
                products.sort((a, b) => b.price - a.price); 
            }

            displayCartItems(products);
        });
    } else {
        cartContainer.innerHTML = "<p>Coșul este gol.</p>";
        totalContainer.innerHTML = "Total: LEI 0.00";
    }


    
    
});
