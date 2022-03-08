from Utils.run import Run



#myJson.create_coord_json()

app = Run()

app.mytime()

app.start() 


print(str(app.address).split(",")[5])