# Унікальні ідентифікатори
class IDGenerator:
    _id = 0

    @classmethod
    def generate_id(cls):
        cls._id += 1
        return cls._id

# Клас "Автобус"
class Bus:
    def __init__(self, model, seats):
        if seats <= 0:
            raise ValueError("Seats must be a positive integer.")
        self.id = IDGenerator.generate_id()
        self.model = model
        self.seats = seats
        self.available_seats = list(range(1, seats + 1))

    def book_seat(self):
        if self.available_seats:
            return self.available_seats.pop(0)
        else:
            raise ValueError("No available seats in the bus.")

# Клас "Маршрут"
class Route:
    def __init__(self, route_name, stations, date):
        if len(stations) < 2:
            raise ValueError("A route must have at least two stations.")
        self.id = IDGenerator.generate_id()
        self.route_name = route_name
        self.stations = stations
        self.date = date

# Клас "Клієнт"
class Client:
    def __init__(self, name):
        self.id = IDGenerator.generate_id()
        self.name = name

# Клас "Квиток"
class Ticket:
    def __init__(self, client, bus, route, seat, from_station, to_station):
        self.id = IDGenerator.generate_id()
        self.client = client
        self.bus = bus
        self.route = route
        self.seat = seat
        self.from_station = from_station
        self.to_station = to_station

# Основна логіка компанії
class TransportCompany:
    def __init__(self):
        self.buses = []
        self.routes = []
        self.clients = []
        self.tickets = []

    def add_bus(self, model, seats):
        bus = Bus(model, seats)
        self.buses.append(bus)
        return bus

    def add_route(self, route_name, stations, date):
        route = Route(route_name, stations, date)
        self.routes.append(route)
        return route

    def add_client(self, name):
        client = Client(name)
        self.clients.append(client)
        return client

    def book_ticket(self, client, bus, route, from_station, to_station):
        if from_station not in route.stations or to_station not in route.stations:
            raise ValueError("Invalid stations selected.")

        if route.stations.index(from_station) >= route.stations.index(to_station):
            raise ValueError("Departure station must precede arrival station.")

        seat = bus.book_seat()
        ticket = Ticket(client, bus, route, seat, from_station, to_station)
        self.tickets.append(ticket)
        return ticket
