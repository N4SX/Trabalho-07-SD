import random
from locust import HttpUser, task, between

class PetClinicUser(HttpUser):
    wait_time = between(1, 3)
    host = "http://localhost:8080"

    @task(4) # 40% de peso
    def list_owners(self):
        self.client.get("/api/customer/owners")

    @task(3) # 30% de peso
    def get_owner_details(self):
        owner_id = random.randint(1, 10)
        self.client.get(f"/api/customer/owners/{owner_id}")

    @task(2) # 20% de peso
    def list_vets(self):
        self.client.get("/api/vet/vets") 

    @task(1) # 10% de peso
    def create_owner(self):
        first_name = random.choice(["Joe", "Jane", "Peter", "Maria", "Chris"])
        last_name = random.choice(["Doe", "Smith", "Jones", "Test"])
        
        new_owner = {
            "firstName": f"{first_name}-{random.randint(1, 1000)}",
            "lastName": last_name,
            "address": "123 Test Street",
            "city": "Testville",
            "telephone": "1234567890"
        }
        
        self.client.post("/api/customer/owners", json=new_owner)