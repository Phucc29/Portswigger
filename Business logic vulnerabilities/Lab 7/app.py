from flask import Flask, request, session, redirect, render_template

app = Flask(__name__)
app.secret_key = "secret"

PRODUCTS = {
    "pen": 10,
    "book": 20,
    "jacket": 500
}

USERS = {
    "wiener": {
        "password": "peter",
        "balance": 100
    }
}

# Lưu giỏ hàng trên server
CARTS = {
    "wiener": {}
}

orders = []


@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if USERS.get(username) and USERS[username]["password"] == password:

            session["user"] = username
            session["checked_out"] = False

            CARTS[username] = {}

            return redirect("/shop")

    return render_template("login.html")


@app.route("/shop")
def shop():

    if "user" not in session:
        return redirect("/")

    cart = CARTS[session["user"]]

    total = sum(
        PRODUCTS[item] * qty
        for item, qty in cart.items()
    )

    return render_template(
        "shop.html",
        products=PRODUCTS,
        balance=USERS[session["user"]]["balance"],
        cart=cart,
        total=total
    )


@app.post("/cart/add")
def add():

    cart = CARTS[session["user"]]

    item = request.form["item"]

    cart[item] = cart.get(item, 0) + 1

    return redirect("/shop")


@app.post("/cart/increase")
def increase():

    cart = CARTS[session["user"]]

    item = request.form["item"]

    cart[item] += 1

    return redirect("/shop")


@app.post("/cart/decrease")
def decrease():

    cart = CARTS[session["user"]]

    item = request.form["item"]

    cart[item] -= 1

    if cart[item] <= 0:
        del cart[item]

    return redirect("/shop")


@app.post("/cart/remove")
def remove():

    cart = CARTS[session["user"]]

    item = request.form["item"]

    cart.pop(item, None)

    return redirect("/shop")


@app.post("/cart/checkout")
def checkout():

    user = USERS[session["user"]]
    cart = CARTS[session["user"]]

    total = sum(
        PRODUCTS[item] * qty
        for item, qty in cart.items()
    )

    if total > user["balance"]:
        return "Not enough credit"

    user["balance"] -= total

    # Chỉ đánh dấu đã checkout
    session["checked_out"] = True

    return redirect("/cart/order-confirmation?order-confirmed=true")


@app.get("/cart/order-confirmation")
def confirm():

    if request.args.get("order-confirmed") != "true":
        return "Invalid workflow", 400

    # ==========================
    # LỖ HỔNG NẰM Ở ĐÂY
    #
    # Không hề kiểm tra:
    # session["checked_out"]
    #
    # Chỉ cần gọi endpoint này là tạo đơn.
    # ==========================

    cart = CARTS[session["user"]]

    total = sum(
        PRODUCTS[item] * qty
        for item, qty in cart.items()
    )

    orders.append({
        "user": session["user"],
        "items": cart.copy(),
        "total": total
    })

    CARTS[session["user"]] = {}

    return render_template(
        "order_confirmation.html",
        items=cart,
        total=total,
        products=PRODUCTS
    )


@app.get("/orders")
def view_orders():

    return render_template(
        "orders.html",
        orders=orders,
        products=PRODUCTS
    )


if __name__ == "__main__":
    app.run(debug=True)