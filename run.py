from app import create_app

#root file that starts the server
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)