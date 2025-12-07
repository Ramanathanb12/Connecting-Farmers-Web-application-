<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Buy Product</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f9;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }

        .purchase-container {
            background-color: #fff;
            padding: 30px;
            border-radius: 10px;
            width: 500px;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
            text-align: center;
            position: relative;
        }

        .purchase-container h2 {
            margin-bottom: 20px;
            color: #16a085;
            font-size: 28px;
        }

        .purchase-info {
            margin-bottom: 30px;
            font-size: 18px;
            color: #333;
        }

        .product-info {
            font-weight: bold;
            margin-bottom: 10px;
        }

        .form-field {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border-radius: 5px;
            border: 1px solid #ddd;
        }

        .form-field:focus {
            border-color: #16a085;
            outline: none;
        }

        .total-price {
            margin-top: 20px;
            font-size: 20px;
            color: #e74c3c;
        }

        .payment-method {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border-radius: 5px;
            border: 1px solid #ddd;
            color: #333;
            font-size: 16px;
        }

        .button-container {
            margin-top: 20px;
        }

        .button-container button {
            padding: 12px 24px;
            border: none;
            border-radius: 30px;
            cursor: pointer;
            font-size: 16px;
            width: 48%;
            margin: 5px;
        }

        .submit-btn {
            background-color: #16a085;
            color: white;
        }

        .cancel-btn {
            background-color: #f44336;
            color: white;
        }

        .back-btn {
            position: absolute;
            top: 15px;
            right: 20px;
            font-size: 24px;
            font-weight: bold;
            color: #aaa;
            cursor: pointer;
        }

        .back-btn:hover {
            color: black;
        }

        /* Success message */
        .success-message {
            margin-top: 20px;
            color: #27ae60;
            font-weight: bold;
            display: none;
        }

        /* Available stock info */
        .available-stock {
            color: #555;
            font-size: 16px;
            margin-bottom: 15px;
        }
    </style>
</head>
<body>

<div class="purchase-container">
    <span class="back-btn" onclick="window.history.back()">&times;</span>
    <h2>Purchase Order</h2>
    <div class="purchase-info">
        <div class="product-info" id="productInfo">Loading product info...</div>
        <div class="available-stock" id="availableStock">Checking stock...</div>
    </div>

    <input type="text" id="marketName" class="form-field" placeholder="Enter Market Name" required />
    <input type="number" id="kgQuantity" class="form-field" placeholder="Enter Quantity (kg)" required min="1" />

    <div class="total-price">
        Total Price: ₹<span id="price">0.00</span>
    </div>

    <select id="paymentMethod" class="payment-method">
        <option value="">Select Payment Method</option>
        <option value="cash">Cash</option>
    </select>

    <div class="button-container">
        <button class="submit-btn" onclick="submitOrder()">Submit Order</button>
        <button class="cancel-btn" onclick="window.history.back()">Cancel</button>
    </div>

    <!-- Success message -->
    <div class="success-message" id="successMessage">Order placed successfully!</div>
</div>

<script>
    // Get query parameters from URL
    const urlParams = new URLSearchParams(window.location.search);
    const productId = urlParams.get('product_id');
    const productName = urlParams.get('product_name');
    const pricePerKg = parseFloat(urlParams.get('price_per_kg'));
    const farmerName = urlParams.get('farmer_name');
    const availableQuantity = parseFloat(urlParams.get('available_quantity'));

    // Display product info
    document.getElementById('productInfo').textContent =
        `Product: ${productName} (₹${pricePerKg}/kg) from ${farmerName}`;
    document.getElementById('availableStock').textContent =
        `Available Stock: ${availableQuantity} kg`;

    // Handle price calculation
    document.getElementById('kgQuantity').addEventListener('input', function () {
        const kg = parseFloat(this.value);
        const total = isNaN(kg) ? 0 : kg * pricePerKg;
        document.getElementById('price').textContent = total.toFixed(2);
    });

    // Submit order function
    function submitOrder() {
        const marketName = document.getElementById('marketName').value;
        const kg = parseFloat(document.getElementById('kgQuantity').value);
        const paymentMethod = document.getElementById('paymentMethod').value;
        const totalPrice = kg * pricePerKg;

        if (!marketName || !kg || kg <= 0 || !paymentMethod) {
            alert("Please fill in all fields correctly.");
            return;
        }

        if (kg > availableQuantity) {
            alert(`Only ${availableQuantity} kg available. Please reduce your order quantity.`);
            return;
        }

        // Send data to backend to save the order
        fetch('/place_order', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                product_id: productId,
                market_name: marketName,
                quantity_kg: kg,
                total_price: totalPrice,
                payment_method: paymentMethod,
                farmer_name: farmerName
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // Show success message and hide it after a few seconds
                document.getElementById('successMessage').style.display = 'block';
                setTimeout(() => {
                    document.getElementById('successMessage').style.display = 'none';
                }, 3000);
            } else {
                alert('Order failed: ' + data.message);
            }
        })
        .catch(err => {
            console.error(err);
            alert('Error submitting order');
        });
    }
</script>
</body>
</html>
