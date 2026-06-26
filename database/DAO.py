from database.DB_connect import DBConnect
from model.Artist import Artist
from model.Genre import Genre


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllGenre():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "select * from genre"

        cursor.execute(query)

        for row in cursor:
            results.append(Genre(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(genere):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select ar.ArtistId , ar.Name 
                    from artist ar , album al, track t , genre g 
                    where g.GenreId = t.GenreId 
                    and ar.ArtistId = al.ArtistId 
                    and al.AlbumId  = t.AlbumId 
                    and g.Name = %s
                    group by ar.ArtistId """

        cursor.execute(query, (genere,),)

        for row in cursor:
            results.append(Artist(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges(genere):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select a1.artistid as id1 , a2.artistid as id2 
                    from (select distinct ar.ArtistId , ic.CustomerId 
                    from artist ar , album al, track t , genre g , invoiceline il, invoice ic 
                    where g.GenreId = t.GenreId 
                    and ar.ArtistId = al.ArtistId 
                    and al.AlbumId  = t.AlbumId 
                    and g.Name = %s
                    and t.TrackId = il.TrackId 
                    and il.InvoiceId = ic.InvoiceId ) as a1, 
                    (select distinct ar.ArtistId , ic.CustomerId 
                    from artist ar , album al, track t , genre g , invoiceline il, invoice ic 
                    where g.GenreId = t.GenreId 
                    and ar.ArtistId = al.ArtistId 
                    and al.AlbumId  = t.AlbumId 
                    and g.Name = %s
                    and t.TrackId = il.TrackId 
                    and il.InvoiceId = ic.InvoiceId  ) as a2
                    where a1.customerid = a2.customerid and a1.artistid < a2.artistid

                                        """

        cursor.execute(query, (genere, genere), )

        for row in cursor:
            results.append((row["id1"], row["id2"]))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getPopolarita(genere):
        conn = DBConnect.get_connection()

        results = {}

        cursor = conn.cursor(dictionary=True)
        query = """SELECT ar.ArtistId, SUM(il.Quantity) as popolarita 
                    FROM artist ar, album al, track t, genre g, invoiceline il, invoice ic
                    WHERE ar.ArtistId = al.ArtistId 
                    AND al.AlbumId  = t.AlbumId 
                    AND t.GenreId = g.GenreId
                    AND t.TrackId = il.TrackId 
                    AND il.InvoiceId = ic.InvoiceId
                    AND g.Name = %s
                    GROUP BY ar.ArtistId  """

        cursor.execute(query, (genere,)  )

        for row in cursor:
            results[row["ArtistId"]] = row["popolarita"]

        cursor.close()
        conn.close()
        return results
