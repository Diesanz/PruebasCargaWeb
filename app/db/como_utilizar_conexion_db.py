@main.route("/users/")
def user_list():
    users = query_db("SELECT id, name FROM users")
    return render_template("users.html", users=users)

@main.route("/add_user/", methods=["POST"])
def add_user():
    name = request.form["name"]
    query = "INSERT INTO users (name) VALUES (%s)"
    execute_db(query, (name,))
    return f"Usuario {name} agregado exitosamente!"

@main.route("/update_user/<int:id>/<string:new_name>")
def update_user(id, new_name):
    query = "UPDATE users SET name = %s WHERE id = %s"
    execute_db(query, (new_name, id))
    return f"El usuario con ID {id} ha sido actualizado con el nuevo nombre {new_name}"

@main.route("/delete_user/<int:id>")
def delete_user(id):
    query = "DELETE FROM users WHERE id = %s"
    execute_db(query, (id,))
    return f"El usuario con ID {id} ha sido eliminado."