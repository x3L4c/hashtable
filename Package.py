class Package:
    def __init__(self, package_id, address, city, state, zipcode, deadline, weight, note, status, timedelivered):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline = deadline
        self.weight = weight
        self.note = note
        self.status = status
        self.timedelivered = timedelivered

    def __repr__(self):
        return "Package ID: %s\n" \
               "Address: %s\n" \
               "City: %s\n" \
               "State: %s\n" \
               "Zipcode: %s\n" \
               "Weight: %s lbs\n" \
               "Delivery Status: %s\n" \
               "Delivery time: %s" % (self.package_id, self.address, self.city, self.state,
                                                           self.zipcode, self.weight,
                                                           self.status, self.timedelivered)


