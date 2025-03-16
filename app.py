from flask import Flask, render_template, request, redirect, url_for
import os
import razorpay
import subprocess

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Razorpay API Keys (Replace with your own)
RAZORPAY_KEY_ID = "rzp_test_PyySScCyy77rUo"
RAZORPAY_KEY_SECRET = "WhQxBPVGw0qFZMhyRfuOTkP7"

client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        copies = int(request.form["copies"])
        color_option = request.form["color"]
        
        if file:
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(file_path)
            
            # Calculate price (₹5 for color, ₹2 for B/W)
            price_per_copy = 5 if color_option == "color" else 2
            total_price = price_per_copy * copies * 100  # Razorpay uses paise
            
            # Create Razorpay Order
            order = client.order.create({
                "amount": total_price,
                "currency": "INR",
                "payment_capture": "1"
            })

            return render_template("payment.html", file_path=file_path, order_id=order["id"], amount=total_price)
    
    return render_template("index.html")

@app.route("/success", methods=["POST"])
def success():
    file_path = request.form["file_path"]
    copies = int(request.form["copies"])
    color_option = request.form["color"]

    # Trigger Printer
    subprocess.run(["python3", "printer.py", file_path, str(copies), color_option])

    return render_template("success.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
