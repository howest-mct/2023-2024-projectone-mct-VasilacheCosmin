from .Database import Database


class DataRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.method != 'GET' and request.content_type == 'application/json':
            gegevens = request.get_json()
        else:
            gegevens = request.form.to_dict()
        return gegevens

    @staticmethod
    def read_status_lampen():
        sql = "SELECT * from lampen"
        return Database.get_rows(sql)

    @staticmethod
    def read_status_lamp_by_id(id):
        sql = "SELECT * from lampen WHERE id = %s"
        params = [id]
        return Database.get_one_row(sql, params)

    @staticmethod
    def update_status_lamp(id, status):
        sql = "UPDATE lampen SET status = %s WHERE id = %s"
        params = [status, id]
        return Database.execute_sql(sql, params)

    @staticmethod
    def update_status_alle_lampen(status):
        sql = "UPDATE lampen SET status = %s"
        params = [status]
        return Database.execute_sql(sql, params)

    @staticmethod
    def save_mpu_data(timestamp, accel_x,accel_y, accel_z, ritid):
        sql = "INSERT INTO VersnellingsS (InleesTijd, versnelling_X, versnelling_Y,versnelling_Z, RitID) VALUES (%s, %s, %s, %s, %s)"
        params = (timestamp, accel_x, accel_y,accel_z, ritid)
        Database.execute_sql(sql, params)

    @staticmethod
    def save_ldr_data(timestamp, ldr_value, ritid):
        sql = "INSERT INTO LichtintensiteitS (InleesTijd, Meting , RitID) VALUES (%s, %s , %s)"
        params = (timestamp, ldr_value, ritid)
        Database.execute_sql(sql, params)


    @staticmethod
    def save_session(timestamp):
        sql = """
        INSERT INTO Rit (StartTijd, EindTijd) 
        VALUES (%s, null); 
        """
        params = [timestamp]
        return Database.execute_sql(sql, params)

    @staticmethod
    def end_session(timestamp):
        sql = """UPDATE Rit SET EindTijd = %s WHERE idRit = (SELECT MAX(idRit) FROM Rit);"""
        params = [timestamp]
        return Database.execute_sql(sql, params)
    
    @staticmethod
    def get_ritID():
        sql = "SELECT idRit from Rit group by idRit desc limit 1"
        return Database.get_rows(sql)
    
    @staticmethod
    def read_alles_lichtintensiteit():
        sql = "SELECT * FROM LichtintensiteitS"
        return Database.get_rows(sql)
    
    @staticmethod
    def read_alles_GPS():
        sql = "SELECT * FROM GPSsensor"
        return Database.get_rows(sql)
    
    
    @staticmethod
    def read_alles_lichtintensiteit_byID():
        sql = "SELECT distinct RitID FROM LichtintensiteitS where RitID is not null"
        return Database.get_rows(sql)
    
    @staticmethod
    def read_alles_GPS_byID():
        sql = "SELECT distinct RitID FROM GPSsensor where RitID is not null"
        return Database.get_rows(sql)
    
    @staticmethod
    def read_lichtintensiteit_by_rit_id(id):
        sql = "select * from LichtintensiteitS where RitID = %s"
        params = [id]
        return Database.get_rows(sql,params)
    
    @staticmethod
    def read_gps_by_rit_id(id):
        sql = "select * from GPSsensor where RitID = %s"
        params = [id]
        return Database.get_rows(sql,params)
    
    @staticmethod
    def read_lichtintensiteit_TODAY(startTijd,eindTijd):
        sql = "    SELECT * FROM LichtintensiteitS WHERE InleesTijd >= %s AND InleesTijd <= %s"
        params = [startTijd,eindTijd]
        return Database.get_rows(sql,params)
    

    @staticmethod
    def save_gps_data(timestamp, lat,lon,speed, ritid):
        sql = "INSERT INTO GPSsensor (inleesTijd, Coordinaat_X,Coordinaat_Y,snelheid , RitID) VALUES (%s, %s , %s,%s,%s)"
        params = (timestamp, lat,lon,speed, ritid)
        Database.execute_sql(sql, params)
    

    



