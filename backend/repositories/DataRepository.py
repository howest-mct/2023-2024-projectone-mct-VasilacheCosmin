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
    def save_mpu_data(timestamp, accel_x,accel_y, accel_z):
        sql = "INSERT INTO VersnellingsS (InleesTijd, versnelling_X, versnelling_Y,versnelling_Z) VALUES (%s, %s, %s, %s)"
        params = (timestamp, accel_x, accel_y,accel_z)
        Database.execute_sql(sql, params)

    @staticmethod
    def save_ldr_data(timestamp, ldr_value):
        sql = "INSERT INTO LichtintensiteitS (InleesTijd, Meting) VALUES (%s, %s)"
        params = (timestamp, ldr_value)
        Database.execute_sql(sql, params)