from website import create_app


app = create_app()

if __name__ == '__main__':
    #app.run(debug=True) #TODO Remove later
    app.run(host="202.61.200.166", port=5000) #TODO Remove later
    
