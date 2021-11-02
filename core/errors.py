

class NotFoundOnDb(Exception):
    def __str__(self):
        return 'Object not found on database'
