from src import create_app

app = create_app()

if __name__ == '__main__':
    # We change the port to 5001 to avoid the Windows "Access Permissions" error on port 5000
    app.run(debug=True, port=5001)