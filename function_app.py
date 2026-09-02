import json
import pyodbc
import azure.functions as func

connection_string = (
    "Driver={SQL Server};"
    "Server=tcp:cityuweek8marcelo.database.windows.net,1433;"
    "Database=week8-marcelo;"
    "Uid=marcelo-admin;"
    "Pwd=tfWR3sK1;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)


def get_db_connection():
    return pyodbc.connect(connection_string)


app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@app.route(route="login", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def login(req: func.HttpRequest) -> func.HttpResponse:
    func.HttpResponse("Hello")
    
    username = req.params.get("username")
    password = req.params.get("password")

    if not username or not password:
        return func.HttpResponse(
            json.dumps({"error": "username and password are required"}),
            status_code=400,
            mimetype="application/json",
        )

    try:
        with get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT username
                FROM users
                WHERE username = ? AND password = ?
                """,
                username,
                password,
            )
            user = cursor.fetchone()
    except Exception as exc:
        return func.HttpResponse(
            json.dumps({"error": f"Database error: {str(exc)}"}),
            status_code=500,
            mimetype="application/json",
        )

    if user:
        return func.HttpResponse(
            json.dumps({
                "message": "Login successful",
                "username": user.username,
            }),
            status_code=200,
            mimetype="application/json",
        )

    return func.HttpResponse(
        json.dumps({"message": "Invalid username or password"}),
        status_code=401,
        mimetype="application/json",
    )
