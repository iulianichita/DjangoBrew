document.addEventListener("DOMContentLoaded", function() {

    let cartActions = document.querySelectorAll(".cart-actions");

    cartActions.forEach(action => {
        let decreaseButton = action.querySelector(".decrease");
        let increaseButton = action.querySelector(".increase");
        let quantityInput = action.querySelector(".quantity");
        let addToCartButton = action.querySelector(".btn_cos_virtual");
        let removeFromCartButton = action.querySelector(".remove-from-cart");
        let menuItem = action.closest('.menu-item');

        let productId = addToCartButton.dataset.id;
        let productName = addToCartButton.dataset.nume;
        let productPrice = addToCartButton.dataset.pret;

        let cart = localStorage.getItem("cos_virtual");
        if (cart) {
            let cartItems = cart.split(",");
            cartItems.forEach(item => {
                let [name, qty, price] = item.split("/"); 
                if (name === productName) {
                    addToCartButton.textContent = "Adăugat în coș";
                    addToCartButton.style.backgroundColor = "#ffaf84";
                    addToCartButton.disabled = true;
                    quantityInput.value = qty; 
                }
            });
        }

        decreaseButton.addEventListener("click", function () {
            let currentValue = parseInt(quantityInput.value, 10) || 0;
            if (currentValue > 0) {
                quantityInput.value = currentValue - 1;
            }
            addToCartButton.textContent = "Adaugă în coș";
            addToCartButton.style.backgroundColor = ""; 
            addToCartButton.disabled = false;
        });

        increaseButton.addEventListener("click", function () {
            let currentValue = parseInt(quantityInput.value, 10) || 0;
            if (currentValue < 10) {
                quantityInput.value = currentValue + 1;
            } else {
                alert("Ne pare rău, stocul maxim este 10.");
            }
            addToCartButton.textContent = "Adaugă în coș";
            addToCartButton.style.backgroundColor = ""; 
            addToCartButton.disabled = false; 
        });

        quantityInput.addEventListener("input", function () {
            let currentValue = parseInt(quantityInput.value, 10) || 0;
            
            if (currentValue > 0 && currentValue <= 10) {
                addToCartButton.textContent = "Adaugă în coș";
                addToCartButton.style.backgroundColor = "";
                addToCartButton.disabled = false; 
            } else {
                addToCartButton.disabled = true;
            }
        });

        addToCartButton.addEventListener("click", function () {
            let quantity = parseInt(quantityInput.value, 10) || 0;

            if (quantity > 0 && quantity <= 10) {
                let cart = localStorage.getItem("cos_virtual");

                if (cart) {
                    let cartItems = cart.split(",");
                    let updated = false;

                    cartItems = cartItems.map(item => {
                        let [name, qty, price] = item.split("/"); 
                        if (name === productName) {
                            updated = true;
                            return `${name}/${quantity}/${productPrice}`; 
                        }
                        return item;
                    });

                    if (!updated) {
                        cartItems.push(`${productName}/${quantity}/${productPrice}`); 
                    }

                    localStorage.setItem("cos_virtual", cartItems.join(","));
                } else {
                    localStorage.setItem("cos_virtual", `${productName}/${quantity}/${productPrice}`);
                }

                addToCartButton.textContent = "Adăugat în coș";
                addToCartButton.style.backgroundColor = "#ffaf84"; 
                addToCartButton.disabled = true; 

                quantityInput.value = quantity;

                console.log("Coșul virtual:", localStorage.getItem("cos_virtual"));
            } else {
                alert("Cantitatea trebuie să fie între 1 și 10.");
            }
        });

        removeFromCartButton.addEventListener("click", function () {
            let cart = localStorage.getItem("cos_virtual");

            if (cart) {
                let cartItems = cart.split(",");
                cartItems = cartItems.filter(item => {
                    let [name, qty, price] = item.split("/");
                    return name !== productName; 
                });

                if (cartItems.length > 0) {
                    localStorage.setItem("cos_virtual", cartItems.join(","));
                } else {
                    localStorage.removeItem("cos_virtual");
                }

                addToCartButton.textContent = "Adaugă în coș";
                addToCartButton.style.backgroundColor = ""; 
                addToCartButton.disabled = false;
                quantityInput.value = 0; 

                console.log("Coșul virtual după ștergere:", localStorage.getItem("cos_virtual"));
            }
        });
    });
});
